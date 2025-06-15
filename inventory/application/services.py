from inventory.infrastructure.repositories import SupplyRepository
from inventory.infrastructure.repositories import SupplyRequestRepository
from inventory.infrastructure.repositories import RfidCodeRepository


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
    
    def get_all_supplies(self):
        """
        Retrieves all supplies in the system.
        
        :return: A list of all supplies.
        """
        
        return self.supply_repository.get_all_supplies()
    
    def get_supply_by_id(self, supply_id):
        """
        Retrieves a specific supply by its ID.
        
        :param supply_id: The ID of the supply to retrieve.
        :return: The supply entity or None if not found.
        """
        
        return self.supply_repository.get_supply_by_id(supply_id)
    
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
    
    def get_supply_request_by_id(self, request_id):
        """
        Retrieves a specific supply request by its ID.
        
        :param request_id: The ID of the supply request to retrieve.
        :return: The supply request entity or None if not found.
        """
        
        return self.supply_request_repository.get_supply_request_by_id(request_id)
    
    def add_supply_request(self, data):
        """
        Adds a new supply request to the system.
        
        :param data: The data for the new supply request.
        :return: The added supply request entity.
        """

        if not data or 'payment_owner_id' not in data or 'supply_id' not in data or 'count' not in data or 'amount' not in data:
            raise ValueError("Invalid data for supply request. 'payment_owner_id', 'supply_id', 'count', and 'amount' are required.")
        
        return self.supply_request_repository.add_supply_request(data)
    
class RfidCodeService:
    def __init__(self):
        self.rfid_repository = RfidCodeRepository()
    
    def validate_rfid_access(self, rfid_uid: str, room_id: str) -> bool:
        """
        Validates RFID access for a specific room.
        
        :param rfid_uid: The RFID UID to validate
        :param room_id: The room ID to validate access for
        :return: True if access is valid, False otherwise
        """
        if not rfid_uid or not room_id:
            return False
        
        # Normalize the RFID UID (remove spaces, convert to uppercase)
        normalized_uid = rfid_uid.replace(" ", "").upper()
        
        return self.rfid_repository.validate_rfid_access(normalized_uid, room_id)
    
    def get_rfid_code_by_uuid(self, uuid: str):
        """
        Retrieves an RFID code by its UUID.
        
        :param uuid: The UUID of the RFID code to retrieve
        :return: The RFID code entity or None if not found
        """
        if not uuid:
            return None
        
        normalized_uuid = uuid.replace(" ", "").upper()
        return self.rfid_repository.get_rfid_code_by_uuid(normalized_uuid)
    
    def add_rfid_code(self, data):
        """
        Adds a new RFID code to the system.
        
        :param data: The data for the new RFID code
        :return: The added RFID code entity
        """
        if not data or 'room_id' not in data or 'guest_id' not in data or 'booking_id' not in data or 'uuid' not in data:
            raise ValueError("Invalid data for RFID code. 'room_id', 'guest_id', 'booking_id', and 'uuid' are required.")
        
        # Normalize the UUID
        data['uuid'] = data['uuid'].replace(" ", "").upper()
        
        return self.rfid_repository.add_rfid_code(data)