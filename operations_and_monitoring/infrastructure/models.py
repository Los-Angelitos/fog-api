from shared.infrastructure.database import db
from sqlalchemy import Table, Column, String, Float, DateTime, Integer

class Thermostat(db.Base):
    __tablename__ = 'thermostats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(100), nullable=False, unique=True)
    api_key = Column(String(100), nullable=False)
    ip_address = Column(String(100), nullable=False)
    mac_address = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    temperature = Column(Float, nullable=False)
    last_update = Column(DateTime, nullable=False)

class SmokeSensor(db.Base):
    __tablename__ = 'smoke_sensors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(100), nullable=False, unique=True)
    api_key = Column(String(100), nullable=False)
    ip_address = Column(String(100), nullable=False)
    mac_address = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    last_analogic_value = Column(Float, nullable=False)
    last_alert_time = Column(DateTime, nullable=True)

class Booking(db.Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_customer_id = Column(Integer, nullable=False)
    room_id = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
    start_date = Column(DateTime, nullable=False)
    final_date = Column(DateTime, nullable=False)
    price_room = Column(Float, nullable=False)
    night_count = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    state = Column(String(50), nullable=False)
    preference_id = Column(Integer, nullable=True)

class Room(db.Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_room_id = Column(Integer, nullable=False)
    hotel_id = Column(Integer, nullable=False)
    state = Column(String(50), nullable=False)
