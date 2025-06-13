from inventory.infrastructure.repositories import SupplyRepository
from inventory.infrastructure.repositories import SupplyRequestRepository

class SupplyService:
    def __init__(self):
        self.supply_repository = SupplyRepository()

    def get_supplies(self, hotel_id):
        """
        Retrieves supplies associated with a specific hotel.
        
        :param hotel_id: The ID of the hotel to retrieve supplies for.
        :return: A list of supplies associated with the hotel.
        """
        
        return self.supply_repository.get_supplies(hotel_id)
    
    def add_supply(self, data):
        """
        Adds a new supply to the system.
        
        :param data: The data for the new supply.
        :return: The added supply entity.
        """

        if not data or 'provider_id' not in data or 'hotel_id' not in data or 'name' not in data or 'price' not in data or 'stock' not in data or 'state' not in data:
            raise ValueError("Invalid data for supply. 'provider_id', 'hotel_id', 'name', 'price', 'stock', and 'state' are required.")
        
        return self.supply_repository.add_supply(data)

class SupplyRequestService:
    def __init__(self):
        self.supply_request_repository = SupplyRequestRepository()

    def get_supply_requests(self):
        """
        Retrieves all supply requests.
        
        :return: A list of supply requests.
        """
        
        return self.supply_request_repository.get_supply_requests()
    
    def add_supply_request(self, data):
        """
        Adds a new supply request to the system.
        
        :param data: The data for the new supply request.
        :return: The added supply request entity.
        """

        if not data or 'payment_owner_id' not in data or 'supply_id' not in data or 'count' not in data or 'amount' not in data:
            raise ValueError("Invalid data for supply request. 'payment_owner_id', 'supply_id', 'count', and 'amount' are required.")
        
        return self.supply_request_repository.add_supply_request(data)