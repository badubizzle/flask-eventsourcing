from flask_marshmallow import Marshmallow
import flask_marshmallow

ma = Marshmallow()

class UserSchema(ma.Schema):
    class Meta:
        fields = ("username", "uuid")


class BankAccountSchema(ma.Schema):
    class Meta:
        fields = ("uuid", 'balance')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

bank_account_schema = BankAccountSchema()
bank_accounts_schema = BankAccountSchema(many=True)