from organizational_management.domain.entities import Hotel
from shared.infrastructure.external_services import ExternalService

class HotelExternalService:
    @staticmethod
    def get_hotel_by_owner_id(owner_id: int) -> Hotel:
        """
        Retrieves a hotel by its owner's ID.
        
        :param owner_id: The ID of the owner to retrieve the hotel for.
        :return: A Hotel entity associated with the owner.
        """
        try:
            # consume the external service to get hotel data
            service = ExternalService()
            response = service.get(f"hotels/get-hotel-by-owner-id?owner_id={owner_id}")
            
            hotel_data = response.json()
            if not hotel_data:
                return None
            
            return Hotel(
                id=hotel_data['id'],
                owner_id=hotel_data['owner_id'],
                name=hotel_data['name'],
                description=hotel_data['description'],
                email=hotel_data['email'],
                address=hotel_data['address'],
                phone=hotel_data['phone']
            )
        except Exception as e:
            print(f"Error retrieving hotel by owner ID {owner_id}: {e}")
            return None