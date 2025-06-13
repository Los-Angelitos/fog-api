from shared.infrastructure.database import db
from iam.infrastructure.models import Device
from sqlalchemy import Table, Column, String, Float, DateTime

class Thermostat(Device):
    __table__ = Table(
        'thermostats',
        db.meta,
        Column('temperature', Float, nullable=False),
        Column('last_update', DateTime, nullable=False),
    )

class SmokeSensor(Device):
    __table__ = Table(
        'smoke_sensors',
        db.meta,
        Column('last_analogic_value', Float, nullable=False),
        Column('last_alert_time', DateTime, nullable=True),
    )

class Booking:
    __table__ = Table(
        'bookings',
        db.meta,
        Column('id', String, primary_key=True),
        Column('payment_customer_id', String, nullable=False),
        Column('room_id', String, nullable=False),
        Column('description', String, nullable=True),
        Column('start_date', DateTime, nullable=False),
        Column('final_date', DateTime, nullable=False),
        Column('price_room', Float, nullable=False),
        Column('night_count', Float, nullable=False),
        Column('amount', Float, nullable=False),
        Column('state', String, nullable=False),
        Column('preference_id', String, nullable=True)
    )

class Room:
    __table__ = Table(
        'rooms',
        db.meta,
        Column('id', String, primary_key=True),
        Column('type_room_id', String, nullable=False),
        Column('hotel_id', String, nullable=False),
        Column('state', String, nullable=False)
    )