from operations_and_monitoring.infrastructure.repositories import MonitoringRepository
from operations_and_monitoring.infrastructure.repositories import BookingRepository

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
    
    def add_smoke_sensor(self, data):
        """
        Adds a new smoke sensor to the system.
        
        :param data: The data for the new smoke sensor.
        :return: The added smoke sensor entity.
        """

        if not data or 'device_id' not in data or 'ip_address' not in data or 'mac_address' not in data:
            raise ValueError("Invalid data for smoke sensor. 'device_id', 'ip_address', and 'mac_address' are required.")
        
        return self.monitoring_repository.add_smoke_sensor(data)

class BookingService:
    def __init__(self):
        self.booking_repository = BookingRepository()

    def get_booking_by_customer_id(self, customer_id):
        """
        Retrieves a booking by customer ID.
        
        :param customer_id: The ID of the customer to retrieve the booking for.
        :return: The booking associated with the customer ID.
        """
        
        return self.booking_repository.get_booking_by_customer_id(customer_id)

    def get_bookings(self, hotel_id):
        """
        Retrieves bookings associated with a specific hotel.
        
        :param hotel_id: The ID of the hotel to retrieve bookings for.
        :return: A list of bookings associated with the hotel.
        """
        
        return self.booking_repository.get_bookings(hotel_id)
    
    def add_booking(self, data):
        """
        Adds a new booking to the system.
        
        :param data: The data for the new booking.
        :return: The added booking entity.
        """

        if not data or 'payment_customer_id' not in data or 'room_id' not in data or 'description' not in data or 'start_date' not in data or 'final_date' not in data or 'price_room' not in data or 'night_count' not in data or 'amount' not in data:
            raise ValueError("Invalid data for booking. Required fields are: 'payment_customer_id', 'room_id', 'description', 'start_date', 'final_date', 'price_room', 'night_count', and 'amount'.")
        
        return self.booking_repository.add_booking(data)