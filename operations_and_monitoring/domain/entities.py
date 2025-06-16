from iam.domain.entities import Device

class Thermostat(Device):
    def __init__(self, id: int, device_id: str, api_key: str, ip_address: str, mac_address: str, temperature: float, last_update: str, state: str = None):
        super().__init__(device_id, api_key)
        self.id = id
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.temperature = temperature
        self.last_update = last_update
        self.state = state if state else "active"

    def to_json(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "api_key": self.api_key,
            "ip_address": self.ip_address,
            "mac_address": self.mac_address,
            "temperature": self.temperature,
            "last_update": self.last_update,
            "state": self.state
        }

class SmokeSensor(Device):
    def __init__(self, id: int, device_id: str, api_key: str, ip_address: str, mac_address: str, last_analogic_value: float, last_alert_time: str = None, state: str = None):
        super().__init__(device_id, api_key)
        self.id = id
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.last_analogic_value = last_analogic_value
        self.last_alert_time = last_alert_time
        self.state = state if state else "active"

    def to_json(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "api_key": self.api_key,
            "ip_address": self.ip_address,
            "mac_address": self.mac_address,
            "last_analogic_value": self.last_analogic_value,
            "last_alert_time": self.last_alert_time
        }

class Booking:
    def __init__(self, id: int, payment_customer_id: int, room_id: int, description: str, start_date: str, final_date: str, price_room: float, night_count:int, amount: float, state: str, preference_id: int = None):
        self.id = id
        self.payment_customer_id = payment_customer_id
        self.room_id = room_id
        self.description = description
        self.start_date = start_date
        self.final_date = final_date
        self.price_room = price_room
        self.night_count = night_count
        self.amount = amount
        self.state = state
        self.preference_id = preference_id

    def to_dict(self):
        return {
            "id": self.id,
            "payment_customer_id": self.payment_customer_id,
            "room_id": self.room_id,
            "description": self.description,
            "start_date": self.start_date,
            "final_date": self.final_date,
            "price_room": self.price_room,
            "night_count": self.night_count,
            "amount": self.amount,
            "state": self.state,
            "preference_id": self.preference_id
        }

class Room:
    def __init__(self, id: int, type_room_id: int, hotel_id: int, state: str):
        self.id = id
        self.type_room_id = type_room_id
        self.hotel_id = hotel_id
        self.state = state

    def to_dict(self):
        return {
            "id": self.id,
            "type_room_id": self.type_room_id,
            "hotel_id": self.hotel_id,
            "state": self.state
        }