import os

from eventsourcing.application.notificationlog import NotificationLogReader
from eventsourcing.domain.model.aggregate import AggregateRoot
from eventsourcing.utils.random import encode_random_bytes
from eventsourcing.application.sqlalchemy import SQLAlchemyApplication
from eventsourcing.exceptions import ConcurrencyError
from eventsourcing.utils.topic import get_topic
from eventsourcing.domain.model.decorators import subscribe_to

from .account_domain import BankAccountEntity
from uuid import uuid4
import uuid
from eventsourcing.domain.model.events import subscribe, DomainEvent
from flaskes.models import BankAccount as BankAccountModel, User as UserModel, db, AccountDeposit

cipher_key = '3c185ca5-b1a1-42fa-bd45-04df5da1023c'

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'evs.db')
os.environ['CIPHER_KEY'] = cipher_key
os.environ['DB_URI'] = 'sqlite:///' + db_path

app = SQLAlchemyApplication(persist_event_type=BankAccountEntity.Event)

received_events = []


def pull_notifications():
    global app
    notifications = NotificationLogReader(app.notification_log)
    for notification in notifications:
        # print(notification)
        pass

@subscribe_to(BankAccountEntity.Created)
def on_account_created_event(event):

    e = event
    account_id = str(e.originator_id)
    # print(f"On Create account event {e}")
    # create account
    user = UserModel.query.filter_by(uuid=str(e.user_uuid)).first()
    account = BankAccountModel(uuid=account_id, status=1)
    if user is not None:
        account.owner = user

    db.session.add(account)
    db.session.commit()
    received_events.append(e)
    pull_notifications()


@subscribe_to(BankAccountEntity.MoneyDeposited)
def on_money_deposited_event(event):

    e: BankAccountEntity.MoneyDeposited = event
    # print(dir(e))
    deposit_id = str(uuid4())
    # print(f"Handling event: {e}")
    account = BankAccountModel.query.filter_by(uuid=str(e.deposit.account_uuid)).first()

    # create deposit
    if account:
        deposit = AccountDeposit(uuid=deposit_id, timestamp=e.deposit.timestamp, amount=e.deposit.amount)
        deposit.account = account
        account.balance = account.balance + deposit.amount
        db.session.add(account)
        db.session.add(deposit)
        db.session.commit()
        return True, deposit
    else:
        return False, "Account not found."

    received_events.append(e)
    pull_notifications()


# subscribe(handler=on_create_account, predicate=lambda e: isinstance(e, AggregateRoot.Created))

# subscribe(handler=on_account_created_event,
#           predicate=lambda e: e[0].__event_topic__ == get_topic(BankAccountEntity.Created))
#
# subscribe(handler=on_money_deposited_event,
#           predicate=lambda e: e[0].__event_topic__ == get_topic(BankAccountEntity.MoneyDeposited))
