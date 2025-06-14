from shared.infrastructure.database import db
from sqlalchemy import Table, Column, String

class Device:
    __table__ = Table(
        'devices',
        db.meta,
        Column('device_id',String, primary_key=True),
        Column('api_key', String(500), nullable=False)
    )