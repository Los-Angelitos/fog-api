from iam.domain.entities import Device

class Thermostat(Device):
    def __init__(self, device_id: str, ip_address: str, mac_address: str, temperature: float, last_update: str, state: str = None):
        super().__init__(device_id, ip_address, mac_address)
        self.temperature = temperature
        self.last_update = last_update
        self.state = state if state else "active"

class SmokeSensor(Device):
    def __init__(self, device_id: str, ip_address: str, mac_address: str, last_analogic_value: float, last_alert_time: str = None):
        super().__init__(device_id, ip_address, mac_address)
        self.last_analogic_value = last_analogic_value
        self.last_alert_time = last_alert_time
