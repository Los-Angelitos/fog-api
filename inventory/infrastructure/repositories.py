from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from shared.infrastructure.database import db

from inventory.infrastructure.models import Supply as SupplyModel, SupplyRequest as SupplyRequestModel
from inventory.domain.entities import Supply, SupplyRequest
from inventory.infrastructure.models import RfidCode as RfidCodeModel
from inventory.domain.entities import RfidCode

class SupplyRepository:
    def get_supplies(self, hotel_id: int) -> list[Supply]:
        """
        Retrieves supplies associated with a specific hotel.
        
        :param hotel_id: The ID of the hotel to retrieve supplies for.
        :return: A list of Supply entities associated with the hotel.
        """
        
        result = db.session.execute(select(SupplyModel.__table__).where(SupplyModel.__table__.c.hotel_id == hotel_id)).fetchall()
        
        return [Supply(id=supply.id, provider_id=supply.provider_id, hotel_id=supply.hotel_id, name=supply.name, price=supply.price, stock=supply.stock, state=supply.state) for supply in result]
    
    def get_all_supplies(self) -> list[Supply]:
        """
        Retrieves all supplies in the system.
        
        :return: A list of all Supply entities.
        """
        
        result = db.session.execute(select(SupplyModel.__table__)).fetchall()
        
        return [Supply(id=supply.id, provider_id=supply.provider_id, hotel_id=supply.hotel_id, name=supply.name, price=supply.price, stock=supply.stock, state=supply.state) for supply in result]
    
    def get_supply_by_id(self, supply_id: int) -> Supply:
        """
        Retrieves a specific supply by its ID.
        
        :param supply_id: The ID of the supply to retrieve.
        :return: The Supply entity or None if not found.
        """
        
        result = db.session.execute(select(SupplyModel.__table__).where(SupplyModel.__table__.c.id == supply_id)).fetchone()
        
        if result is None:
            return None
            
        return Supply(id=result.id, provider_id=result.provider_id, hotel_id=result.hotel_id, name=result.name, price=result.price, stock=result.stock, state=result.state)
    
    def add_supply(self, data: dict) -> Supply:
        """
        Adds a new supply to the system.
        
        :param data: The data for the new supply.
        :return: The added Supply entity.
        """
        
        session = db.session
        try:
            # Insert into database using raw SQL
            result = session.execute(
                SupplyModel.__table__.insert().values(
                    provider_id=data['provider_id'],
                    hotel_id=data['hotel_id'],
                    name=data['name'],
                    price=data['price'],
                    stock=data['stock'],
                    state=data['state']
                )
            )
            
            # Obtener el ID insertado
            supply_id = result.lastrowid
            
            # Hacer commit explícito
            session.commit()
            
            print(f"Supply inserted with ID: {supply_id}")  # Debug log
            
            return Supply(
                id=supply_id,
                provider_id=data['provider_id'],
                hotel_id=data['hotel_id'],
                name=data['name'],
                price=data['price'],
                stock=data['stock'],
                state=data['state']
            )
            
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Database error: {str(e)}")  # Debug log
            raise e
        except Exception as e:
            session.rollback()
            print(f"Unexpected error: {str(e)}")  # Debug log
            raise e

class SupplyRequestRepository:
    def get_supply_requests(self) -> list[SupplyRequest]:
        """
        Retrieves all supply requests.
        
        :return: A list of SupplyRequest entities.
        """
        
        result = db.session.execute(select(SupplyRequestModel.__table__)).fetchall()
        
        return [SupplyRequest(id=request.id, payment_owner_id=request.payment_owner_id, supply_id=request.supply_id, count=request.count, amount=request.amount) for request in result]
    
    def get_supply_request_by_id(self, request_id: int) -> SupplyRequest:
        """
        Retrieves a specific supply request by its ID.
        
        :param request_id: The ID of the supply request to retrieve.
        :return: The SupplyRequest entity or None if not found.
        """
        
        result = db.session.execute(select(SupplyRequestModel.__table__).where(SupplyRequestModel.__table__.c.id == request_id)).fetchone()
        
        if result is None:
            return None
            
        return SupplyRequest(id=result.id, payment_owner_id=result.payment_owner_id, supply_id=result.supply_id, count=result.count, amount=result.amount)
    
    def add_supply_request(self, data: dict) -> SupplyRequest:
        """
        Adds a new supply request to the system.
        
        :param data: The data for the new supply request.
        :return: The added SupplyRequest entity.
        """
        
        session = db.session
        try:
            # Insert into database using raw SQL
            result = session.execute(
                SupplyRequestModel.__table__.insert().values(
                    payment_owner_id=data['payment_owner_id'],
                    supply_id=data['supply_id'],
                    count=data['count'],
                    amount=data['amount']
                )
            )
            
            # Obtener el ID insertado
            request_id = result.lastrowid
            
            # Hacer commit explícito
            session.commit()
            
            print(f"Supply request inserted with ID: {request_id}")  # Debug log
            
            return SupplyRequest(
                id=request_id,
                payment_owner_id=data['payment_owner_id'],
                supply_id=data['supply_id'],
                count=data['count'],
                amount=data['amount']
            )
            
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Database error: {str(e)}")  # Debug log
            raise e
        except Exception as e:
            session.rollback()
            print(f"Unexpected error: {str(e)}")  # Debug log
            raise e
        

class RfidCodeRepository:
    def validate_rfid_access(self, rfid_uid: str, room_id: str) -> bool:
        """
        Validates if the RFID UID and room ID combination is valid for access.
        
        :param rfid_uid: The RFID UID to validate
        :param room_id: The room ID to validate access for
        :return: True if access is valid, False otherwise
        """
        try:
            result = db.session.execute(
                select(RfidCodeModel.__table__).where(
                    RfidCodeModel.__table__.c.uuid == rfid_uid,
                    RfidCodeModel.__table__.c.room_id == room_id
                )
            ).fetchone()
            
            return result is not None
            
        except SQLAlchemyError as e:
            print(f"Database error during RFID validation: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error during RFID validation: {str(e)}")
            return False
    
    def get_rfid_code_by_uuid(self, uuid: str) -> RfidCode:
        """
        Retrieves an RFID code by its UUID.
        
        :param uuid: The UUID of the RFID code to retrieve
        :return: The RfidCode entity or None if not found
        """
        result = db.session.execute(
            select(RfidCodeModel.__table__).where(RfidCodeModel.__table__.c.uuid == uuid)
        ).fetchone()
        
        if result is None:
            return None
            
        return RfidCode(
            id=result.id,
            room_id=result.room_id,
            guest_id=result.guest_id,
            booking_id=result.booking_id,
            uuid=result.uuid
        )
    
    def add_rfid_code(self, data: dict) -> RfidCode:
        """
        Adds a new RFID code to the system.
        
        :param data: The data for the new RFID code
        :return: The added RfidCode entity
        """
        session = db.session
        try:
            result = session.execute(
                RfidCodeModel.__table__.insert().values(
                    room_id=data['room_id'],
                    guest_id=data['guest_id'],
                    booking_id=data['booking_id'],
                    uuid=data['uuid']
                )
            )
            
            rfid_id = result.lastrowid
            session.commit()
            
            print(f"RFID code inserted with ID: {rfid_id}")
            
            return RfidCode(
                id=rfid_id,
                room_id=data['room_id'],
                guest_id=data['guest_id'],
                booking_id=data['booking_id'],
                uuid=data['uuid']
            )
            
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Database error: {str(e)}")
            raise e
        except Exception as e:
            session.rollback()
            print(f"Unexpected error: {str(e)}")
            raise e