from eventsourcing.domain.model.aggregate import AggregateRoot
from eventsourcing.domain.model.decorators import attribute
from eventsourcing.domain.model.events import DomainEvent

from eventsourcing.domain.model.events import subscribe

import datetime


class EventLogger(object):

    @classmethod
    def log(cls, event, data):
        print(f"Applying event {event.__class__.__name__} with data {data}")


class BankAccountEntity(AggregateRoot):

    def log_event(self, event, data):
        EventLogger.log(event, data)

    def __init__(self, user_uuid, **kwargs):
        super(BankAccountEntity, self).__init__(**kwargs)
        self._user_uuid = user_uuid
        self._deposits = []
        self._balance = 0

    @property
    def account_number(self):
        return self.id

    @attribute
    def user_uuid(self):
        "Event source entity attribute"

    @attribute
    def balance(self):
        "Event source entity attribute"

    @property
    def deposits(self):
        return tuple(self._deposits)

    @property
    def total_deposits(self):
        total = 0
        for deposit in self._deposits:
            total = total + deposit.amount

        return total

    def make_deposit(self, amount):
        # validate deposit and trigger event

        import inspect
        fn_name = inspect.stack()[0][3]
        account_uuid = self.id
        deposit = BankAccountEntity.Deposit(account_uuid, amount)
        self.__trigger_event__(BankAccountEntity.MoneyDeposited, deposit=deposit)

    class Deposit(object):
        def __init__(self, account_uuid, amount):
            self.amount = amount
            self.account_uuid = account_uuid
            self.timestamp = datetime.datetime.now()
        
    class MoneyDeposited(AggregateRoot.Event):
        """
        Event triggered for when user deposits money
        """

        def mutate(self, bank_account):
            super(BankAccountEntity.MoneyDeposited, self).mutate(bank_account)
            # apply deposit to bank account
            bank_account._deposits.append(self.deposit)
            bank_account._balance += self.deposit.amount
