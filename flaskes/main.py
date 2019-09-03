from .app import create_app
from .models import db
from flask_migrate import Migrate
from flask import g
from .blueprint.account.views import bp as accounts_view, init_app as init_account_view, init_jwt
from .es.app import app as ev_app

from flask_jwt_extended import JWTManager

from flask_restplus import Api

import os
basedir = os.path.abspath(os.path.dirname(__file__))    
print(basedir)

config = {}

config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db', 'data.sqlite')

# create app instance
app = create_app(config_override=config)

# setup db
db.init_app(app)

# setup migration
migrate = Migrate(app, db)

api = Api(app)

# setup blueprint
init_account_view(app)

jwt = JWTManager(app)



@app.route("/")
def index():

    return "<p>Hello World!</p>"

if __name__ == '__main__':
    port = app.config['PORT'] or 5000
    app.run(port=port)
