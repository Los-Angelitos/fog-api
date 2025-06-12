from inventory.domain.services import SupplyService, SupplyRequestService
from inventory.infrastructure.repositories import SupplyRepository, SupplyRequestRepository
##from iam.application.services import AuthApplicationService


class InventoryApplicationService:
    def __init__(self):
        self.supply_repository = SupplyRepository()
        self.supply_request_repository = SupplyRequestRepository()
        self.supply_service = SupplyService()
        self.supply_request_service = SupplyRequestService()
       ## self.iam_service = AuthApplicationService()

    def create_supply(self, provider_id: str, name: str, price: float, stock: int, state: str, api_key: str):
        # Validate API key
        if not self.iam_service.get_device_by_id_and_api_key(provider_id, api_key):
            raise ValueError("Provider not found or Invalid API key")

        # Create supply
        supply = self.supply_service.create_supply(provider_id, name, price, stock, state)
        return self.supply_repository.save(supply)

    def create_supply_request(self, payment_owner_id: str, supply_id: int, count: int, amount: float, api_key: str):
        # Validate API key
        if not self.iam_service.get_device_by_id_and_api_key(payment_owner_id, api_key):
            raise ValueError("Payment owner not found or Invalid API key")

        # Verify supply exists
        supply = self.supply_repository.find_by_id(supply_id)
        if not supply:
            raise ValueError("Supply not found")

        # Verify stock availability
        if supply.stock < count:
            raise ValueError("Insufficient stock available")

        # Create supply request
        supply_request = self.supply_request_service.create_supply_request(
            payment_owner_id, supply_id, count, amount
        )
        return self.supply_request_repository.save(supply_request)