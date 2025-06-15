from organizational_management.infrastructure.repositories import HotelRepository

class OrganizationalManagementService:
    def __init__(self):
        self.hotel_repository = HotelRepository()

    def get_hotel_by_owner_id(self, owner_id: int):
        """
        Retrieves a hotel by its owner's ID.
        
        :param owner_id: The ID of the owner to retrieve the hotel for.
        :return: A Hotel entity associated with the owner.
        """
        return self.hotel_repository.get_hotel_by_owner_id(owner_id)