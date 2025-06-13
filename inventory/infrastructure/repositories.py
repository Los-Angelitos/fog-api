from sqlalchemy import select
from shared.infrastructure.database import db

from inventory.infrastructure.models import Supply as SupplyModel, SupplyRequest as SupplyRequestModel
from inventory.domain.entities import Supply, SupplyRequest

class SupplyRepository:
    def get_supplies(self, hotel_id: int) -> list[Supply]:
        """
        Retrieves supplies associated with a specific hotel.
        
        :param hotel_id: The ID of the hotel to retrieve supplies for.
        :return: A list of Supply entities associated with the hotel.
        """
        
        result = db.session.execute(select(SupplyModel).where(SupplyModel.hotel_id == hotel_id)).scalars().all()
        
        return [Supply(id=supply.id, provider_id=supply.provider_id, hotel_id=supply.hotel_id, name=supply.name, price=supply.price, stock=supply.stock, state=supply.state) for supply in result]
    
    def add_supply(self, data: dict) -> Supply:
        """
        Adds a new supply to the system.
        
        :param data: The data for the new supply.
        :return: The added Supply entity.
        """
        
        # Insert into database using raw SQL
        result = db.session.execute(
            SupplyModel.__table__.insert().values(
                provider_id=data['provider_id'],
                hotel_id=data['hotel_id'],
                name=data['name'],
                price=data['price'],
                stock=data['stock'],
                state=data['state']
            )
        )
        
        db.session.commit()
        
        # Get the inserted ID
        supply_id = result.lastrowid
        
        return Supply(
            id=supply_id,
            provider_id=data['provider_id'],
            hotel_id=data['hotel_id'],
            name=data['name'],
            price=data['price'],
            stock=data['stock'],
            state=data['state']
        )

class SupplyRequestRepository:
    def get_supply_requests(self) -> list[SupplyRequest]:
        """
        Retrieves all supply requests.
        
        :return: A list of SupplyRequest entities.
        """
        
        result = db.session.execute(select(SupplyRequestModel)).scalars().all()
        
        return [SupplyRequest(id=request.id, payment_owner_id=request.payment_owner_id, supply_id=request.supply_id, count=request.count, amount=request.amount) for request in result]
    
    def add_supply_request(self, data: dict) -> SupplyRequest:
        """
        Adds a new supply request to the system.
        
        :param data: The data for the new supply request.
        :return: The added SupplyRequest entity.
        """
        
        # Insert into database using raw SQL
        result = db.session.execute(
            SupplyRequestModel.__table__.insert().values(
                payment_owner_id=data['payment_owner_id'],
                supply_id=data['supply_id'],
                count=data['count'],
                amount=data['amount']
            )
        )
        
        db.session.commit()
        
        # Get the inserted ID
        request_id = result.lastrowid
        
        return SupplyRequest(
            id=request_id,
            payment_owner_id=data['payment_owner_id'],
            supply_id=data['supply_id'],
            count=data['count'],
            amount=data['amount']
        )