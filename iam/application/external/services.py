from typing import List

from iam.domain.entities import Device


class ExternalOperationAndMonitoringService:
    def __init__(self):
        pass

    def fetch_all_devices_by_room_id(room_id:int) -> List[Device]:
        # Here call the external service
        return []