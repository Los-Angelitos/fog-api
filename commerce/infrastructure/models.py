from sqlalchemy import Table, Column, String, Integer, Float
from shared.infrastructure.database import db

class PaymentCustomer:
    __table__ = Table(
        'payment_customers',
        db.meta,
        Column('id', Integer, primary_key=True),
        Column('guest_id', String(50), nullable=False),
        Column('final_amount', String(200), nullable=False),
    )

class PaymentOwner:
    __table__ = Table(
        'payment_owners',
        db.meta,
        Column('id', Integer, primary_key=True),
        Column('owner_id', String(50), nullable=False),
        Column('description', String(200), nullable=False),
        Column('final_amount', Float, nullable=False),
    )

class Subscription:
    __table__ = Table(
        'subscriptions',
        db.meta,
        Column('id', Integer, primary_key=True),
        Column('name', String(200), nullable=False),
        Column('content', String(500), nullable=False),
        Column('price', Float, nullable=False),
        Column('status', String(50), nullable=False)
    )

class ContractOwner:
    __table__ = Table(
        'contract_owners',
        db.meta,
        Column('id', Integer, primary_key=True),
        Column('owner_id', String(50), nullable=False),
        Column('start_date', String(50), nullable=False),
        Column('final_date', String(50), nullable=False),
        Column('subscription_id', String(50), nullable=False),
        Column('status', String(50), nullable=False)
    )