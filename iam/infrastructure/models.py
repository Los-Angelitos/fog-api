from shared.infrastructure.database import db
from sqlalchemy import Table, Column, String

class Device:
    __table__ = Table(
        'devices',
        db.meta,
        Column('device_id', String, primary_key=True),
        Column('ip_address', String(100), nullable=False),
        Column('mac_address', String(50), nullable=False),
        Column('state', String(50), nullable=False),
    )