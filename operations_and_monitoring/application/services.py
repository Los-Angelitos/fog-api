from operations_and_monitoring.infrastructure.repositories import MonitoringRepository

class MonitoringService:
    def __init__(self):
        self.monitoring_repository = MonitoringRepository()

    def get_thermostats(self):
        """
        Retrieves devices associated with a specific hotel.
        
        :return: A list of devices associated with the hotel.
        """
        
        return self.monitoring_repository.get_thermostats()
    
    def get_smoke_sensors(self):
        """
        Retrieves smoke sensors associated with a specific hotel.
        
        :return: A list of smoke sensors associated with the hotel.
        """
        
        return self.monitoring_repository.get_smoke_sensors()
    
    def add_thermostat(self, data):
        """
        Adds a new thermostat to the system.
        
        :param data: The data for the new thermostat.
        :return: The added thermostat entity.
        """

        if not data or 'device_id' not in data or 'ip_address' not in data or 'mac_address' not in data:
            raise ValueError("Invalid data for thermostat. 'device_id', 'ip_address', and 'mac_address' are required.")
        
        return self.monitoring_repository.add_thermostat(data)