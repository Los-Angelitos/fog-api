from shared.infrastructure.database import db
from sqlalchemy import Table, Column, String, Integer, Float

class Supply:
    __table__ = Table(
        'supplies',
        db.meta,
        Column('id', Integer, primary_key=True),
        Column('provider_id', Integer, nullable=False),
        Column('hotel_id', Integer, nullable=False),
        Column('name', String(200), nullable=False),
        Column('price', Float, nullable=False),
        Column('stock', Integer, nullable=False),
        Column('state', String(50), nullable=False)
    )

class SupplyRequest:
    __table__ = Table(
        'supply_requests',
        db.meta,
        Column('id', Integer, primary_key=True),
        Column('payment_owner_id', Integer, nullable=False),
        Column('supply_id', Integer, nullable=False),
        Column('count', Integer, nullable=False),
        Column('amount', Float, nullable=False)
    )

class Rfid(db.Base):
    __tablename__ = 'rfid_devices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(String(100), nullable=False)
    api_key = Column(String(100), nullable=False)
    u_id = Column(String(100), nullable=False)