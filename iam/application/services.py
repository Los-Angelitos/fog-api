from typing import Optional

from iam.application.external.services import ExternalOperationAndMonitoringService
from iam.domain.entities import Device
from iam.domain.services import AuthService
from iam.infrastructure.repositories import DeviceRepository


class AuthApplicationService:
    def __init__(self):
        self.device_repository = DeviceRepository()
        self.auth_service = AuthService()
        self.external_operation_and_monitoring_service = ExternalOperationAndMonitoringService()

    def authenticate(self, device_id: str, api_key: str) -> bool:
        device: Optional[Device] = self.device_repository.find_by_id_and_api_key(device_id, api_key)
        return self.auth_service.authenticate(device)

    def create_device(self, data:dict) -> Device:
        if not data or 'device_id' not in data:
            raise ValueError("Device id is required")
        response = self.device_repository.create_device(data)
        return response

    def get_device_by_id_and_api_key(self, device_id: str, api_key: str) -> Optional[Device]:
        return self.device_repository.find_by_id_and_api_key(device_id, api_key)
    
    def get_all_devices_by_room_id(self, room_id:int):
        return self.external_operation_and_monitoring_service.fetch_all_devices_by_room_id(room_id)