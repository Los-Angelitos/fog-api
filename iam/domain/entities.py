class Device:
    def __init__(self, device_id: str, ip_address: str, mac_address: str):
        self.device_id = device_id
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.state = "active"

    def __repr__(self):
        return f"Device(device_id={self.device_id}, ip_address={self.ip_address}, mac_address={self.mac_address})"