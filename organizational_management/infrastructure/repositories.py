from sqlacademy import select
from shared.infrastructure.database import db

from organizational_management.infrastructure.models import Hotel as HotelModel
from organizational_management.domain.entities import Hotel
from organizational_management.application.external.services import HotelExternalService

class HotelRepository:
    def get_hotel_by_owner_id(self, owner_id: int) -> Hotel:
        """
        Retrieves a hotel by its owner's ID.
        
        :param owner_id: The ID of the owner to retrieve the hotel for.
        :return: A Hotel entity associated with the owner.
        """

        service = HotelExternalService()
        hotel = service.get_hotel_by_owner_id(owner_id)

        return hotel