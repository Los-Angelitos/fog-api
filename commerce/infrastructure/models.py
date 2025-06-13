from peewee import Model, AutoField, CharField, DecimalField, DateField
from shared.infrastructure.database import db

class PaymentCustomer(Model):
    id = AutoField()
    guest_id = CharField()
    final_amount = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        database = db
        table_name = 'payment_customers'

class PaymentOwner(Model):
    id = AutoField()
    owner_id = CharField()
    description = CharField()
    final_amount = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        database = db
        table_name = 'payment_owners'

class Subscription(Model):
    id = AutoField()
    name = CharField()
    content = CharField()
    price = DecimalField(max_digits=10, decimal_places=2)
    status = CharField()

    class Meta:
        database = db
        table_name = 'subscriptions'

class ContractOwner(Model):
    id = AutoField()
    owner_id = CharField()
    start_date = DateField()
    final_date = DateField()
    subscription_id = CharField()
    status = CharField()

    class Meta:
        database = db
        table_name = 'contract_owners'