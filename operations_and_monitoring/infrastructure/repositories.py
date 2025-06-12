from sqlalchemy import select
from shared.infrastructure.database import db

from operations_and_monitoring.infrastructure.models import Thermostat as ThermostatModel, SmokeSensor as SmokeSensorModel
from operations_and_monitoring.domain.entities import Thermostat, SmokeSensor

class MonitoringRepository:    
    def get_thermostats(self) -> list[Thermostat]:
        """
        Retrieves thermostats associated with a specific hotel.
        
        :param hotel_id: The ID of the hotel to retrieve thermostats for.
        :return: A list of Thermostat entities associated with the hotel.
        """
        
        result = db.session.execute(select(ThermostatModel)).scalars().all()
        
        return [Thermostat(device_id=device.device_id, ip_address=device.ip_address, mac_address=device.mac_address, state=device.state, temperature=device.temperature, last_update=device.last_update) for device in result]
    
    def get_smoke_sensors(self) -> list[SmokeSensor]:
        """
        Retrieves smoke sensors associated with a specific hotel.
        
        :param hotel_id: The ID of the hotel to retrieve smoke sensors for.
        :return: A list of SmokeSensor entities associated with the hotel.
        """
        
        result = db.session.execute(select(SmokeSensorModel)).scalars().all()
        
        return [SmokeSensor(device_id=device.device_id, ip_address=device.ip_address, mac_address=device.mac_address, state=device.state, last_analogic_value=device.last_analogic_value, last_alert_time=device.last_alert_time) for device in result]