from shared.infrastructure.database import db
from sqlalchemy import Column, String, Integer

class Hotel(db.Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, nullable=False)
    name = Column(String(100), nullable=True)
    description = Column(String(255), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    
    