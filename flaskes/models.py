
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(db.String(), primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    accounts = db.relationship('BankAccount', backref='accounts')
    
    # def __repr__(self):
    #     return "<User %>" % self.username

class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'
    uuid = db.Column(db.String(), primary_key=True)
    balance = db.Column(db.Integer(), default=0)
    status = db.Column(db.Integer(), default=1)    
    owner_id = db.Column(db.String(), db.ForeignKey('users.uuid'))
    owner = db.relationship('User', backref='owner')
    deposits = db.relationship('AccountDeposit', backref='deposits')

    # def __repr__(self):
    #     return "<BankAccount %s >" % self.uuid


class AccountDeposit(db.Model):
    __tablename__ = 'deposits'
    uuid = db.Column(db.String(), primary_key=True)
    account_id = db.Column(db.String(), db.ForeignKey('bank_accounts.uuid'))
    account = db.relationship('BankAccount', backref='account')
    amount = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
