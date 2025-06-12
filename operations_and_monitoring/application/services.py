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