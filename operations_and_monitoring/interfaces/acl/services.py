from operations_and_monitoring.domain.entities import Thermostat, SmokeSensor
from operations_and_monitoring.infrastructure.repositories import MonitoringRepository
from iam.domain.entities import Device

class MonitoringFacade:
    def __init__(self):
        self.repository = MonitoringRepository()

    def get_devices_by_room_id(self, room_id: str) -> list[Device]:
        if room_id == None or room_id == "":
            raise Exception("room_id parameter is necessary")

        thermostats = self.repository.get_thermostats()
        smoke_sensors = self.repository.get_smoke_sensors()
        rfid_devices = self.repository.get_rfid()

        devices = thermostats + smoke_sensors + rfid_devices
        
        return [device for device in devices if device.room_id == room_id]