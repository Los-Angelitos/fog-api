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