from peewee import Model, AutoField, CharField, DecimalField, IntegerField
from shared.infrastructure.database import db


class Supply(Model):
    id = AutoField()
    provider_id = CharField()
    name = CharField()
    price = DecimalField(max_digits=10, decimal_places=2)
    stock = IntegerField()
    state = CharField()

    class Meta:
        database = db
        table_name = 'supplies'


class SupplyRequest(Model):
    id = AutoField()
    payment_owner_id = CharField()
    supply_id = IntegerField()
    count = IntegerField()
    amount = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        database = db
        table_name = 'supply_requests'