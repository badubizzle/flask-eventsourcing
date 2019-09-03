import uuid

from flask import (
    current_app,
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import json
from flaskes.models import db, User, BankAccount
from .serializer import ma, user_schema, users_schema, bank_account_schema, bank_accounts_schema
from flask import request
from flask import g
from flaskes.es.account_domain import BankAccountEntity as BankAccountEntity

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from functools import wraps
from eventsourcing.utils.topic import get_topic

bp = Blueprint('api', __name__, url_prefix='/api')


def match_current_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        current_user = get_jwt_identity()
        if kwargs['username'] != current_user:
            return send_json({'error': 'Unauthorized access1'}, 400)
        return f(*args, **kwargs)
   
    return wrap

def match_account_user(f):
    @wraps(f)    
    def wrap(*args, **kwargs):        
        current_user = get_jwt_identity()    
        account_uuid = kwargs['account_id']                
        account = BankAccount.query.filter_by(uuid=account_uuid).first()

        if not account:            
            return send_json({'error': 'Unauthorized access'}, 400)
        if account.owner.username != current_user:
            return send_json({'error': 'Unauthorized access'}, 400)

        kwargs['account'] = account    
        return f(*args, **kwargs)
   
    return wrap

def authenticate(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user

def identity(payload):
    username = payload['identity']
    return User.query.filter_by(username=username).first()


def init_jwt(app):
    jwt = JWT(app, authenticate, identity)
    return  jwt

def init_app(app):
    app.register_blueprint(bp)
    # app.register_blueprint(bp)
    ma.init_app(app)


def send_json(data, status_code=200):
    if isinstance(data, dict):
        data = json.dumps(data)
    return data, status_code, {'Content-Type': 'application/json'}


@bp.route("/refresh-token/", methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return send_json({'token': new_token}, 200)



@bp.route("/users/<username>/")
@jwt_required
@match_current_user
def user_details(username):
    if request.method == 'GET':                                    
        user = User.query.filter_by(username=username).first()
        if user:
            return send_json(user_schema.dumps(user))
        else:
            return send_json(json.dumps({'error': 'User not found'}), 404)

# @bp.route("/users/<username>/", methods=['POST'])
# def create_user(username):
#     if request.method == 'POST':
#         user_uuid = str(uuid.uuid4())
#         user = User(username=username, uuid=user_uuid)
#         user_exists = User.query.filter_by(username=username).first()
#         user_claims = {'access_type': 1}
#         access_token = create_access_token(user.username, user_claims=user_claims),
#         refresh_token = create_refresh_token(user.username, user_claims=user_claims),
#         if not user_exists:
#             db.session.add(user)
#             db.session.commit()
#             return send_json({'user': user_schema.dump(user), 'token': access_token, 'refresh': refresh_token})
#         else:
#             return send_json({'error': 'Username already exists.'}, 200)


@bp.route("/users/", methods=('POST',))
def users():    
    if request.method == 'POST':
        
        if not 'username' in request.form:
            return send_json({'error': 'Bad request'}, 400)
        else:
            username = request.form['username']
            user_uuid = str(uuid.uuid4())
            user = User(username=username, uuid=user_uuid)
            user_exists = User.query.filter_by(username=username).first()
            user_claims = {'access_type': 1}
            access_token = create_access_token(user.username, user_claims=user_claims),
            refresh_token = create_refresh_token(user.username, user_claims=user_claims),
            if not user_exists:
                db.session.add(user)
                db.session.commit()
                return send_json({'user': user_schema.dump(user), 'token': access_token, 'refresh': refresh_token})
            else:
                return send_json({'error': 'Username already exists.'}, 200)        


@bp.route("/users/<username>/accounts/", methods=['POST', 'GET'])
@jwt_required
@match_current_user
def user_accounts(username):
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        if user:
            from flaskes.es.app import app as es_app
            event = BankAccountEntity.__create__(user_uuid=user.uuid)
            event.__save__()
            return 'OK', 201
        else:
            return 'ERROR', 400
    elif request.method == 'GET':
        if user:
            accounts = BankAccount.query.filter_by(owner_id=user.uuid).all()
            return send_json({'accounts': bank_accounts_schema.dump(accounts)}, 200)

@bp.route("/users/<username>/accounts/<account_id>/", methods=['GET'])
@jwt_required
@match_current_user
@match_account_user
def user_account_details(username, account_id, account=None):
    user = User.query.filter_by(username=username).first()    
    accoun = account or BankAccount.query.filter_by(uuid=account_id).first()

    if request.method == 'GET':
        if user and account:
            from flaskes.es.app import app as es_app
            events = es_app.event_store.get_domain_events(account.uuid)
            deposits = []
            for ev in events:
                # print(ev)
                if ev.__event_topic__ == get_topic(BankAccountEntity.MoneyDeposited):
                    # print(ev)
                    pass

                # if events[ev].topic() == 
                #     print(ev.deposit.amount)
                
                # print(ev)

            return send_json(bank_account_schema.dump(account), 200)
    
    return send_json({'error':'Not allowed'})


@bp.route("/users/<username>/accounts/<account_id>/deposits/", methods=['POST'])
@jwt_required
@match_current_user
@match_account_user
def deposit(username, account_id, account=None):

    if not 'amount' in request.form:
        return send_json({'error': 'Bad request'}, 400)
    amount = int(request.form['amount'])
    if amount <=0:
        return send_json({'error': 'Bad request'}, 400)

    account =  account or BankAccount.query.filter_by(uuid=account_id).first()
    if account:
        from flaskes.es.app import app as es_app
        account_entity = es_app.repository.get_entity(account_id)
        if account_entity:
            account_entity.make_deposit(amount)
            account_entity.__save__()
            return 'OK', 201

    return 'ERROR', 400
