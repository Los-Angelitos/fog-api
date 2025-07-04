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

    def get_rfid(self):
        """
        Retrieves RFID devices associated with a specific hotel.

        :return: A list of RFID devices associated with the hotel.
        """

        return self.monitoring_repository.get_rfid()
    
    def add_thermostat(self, data):
        """
        Adds a new thermostat to the system.
        
        :param data: The data for the new thermostat.
        :return: The added thermostat entity.
        """

        if not data or 'device_id' not in data or 'api_key' not in data:
            raise ValueError("Invalid data for thermostat. 'device_id', 'api_key' are required.")
        
        return self.monitoring_repository.add_thermostat(data)
    
    def add_smoke_sensor(self, data):
        """
        Adds a new smoke sensor to the system.
        
        :param data: The data for the new smoke sensor.
        :return: The added smoke sensor entity.
        """

        if not data or 'api_key' not in data or 'device_id' not in data:
            raise ValueError("Invalid data for smoke sensor. 'device_id', 'api_key' are required.")
        
        return self.monitoring_repository.add_smoke_sensor(data)

    def validation_service(self, data):
        """
        Validates if there's an existing device with the provided room_id and u_id.
        :param data: The data containing room_id and u_id for validation.
        :return: True if the device exists, False otherwise.
        """

        if not data or 'room_id' not in data or 'u_id' not in data:
            raise ValueError("Invalid data for validation. 'room_id' and 'u_id' are required.")

        return self.monitoring_repository.validation_service(data)

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
    
    def check_in(self, booking_id):
        """
        Checks in a booking by ID.
        
        :param booking_id: The ID of the booking to check in.
        :return: The updated booking entity after check-in.
        """
        
        return self.booking_repository.check_in(booking_id)
    
    def check_out(self, booking_id):
        """
        Checks out a booking by ID.
        
        :param booking_id: The ID of the booking to check out.
        :return: The updated booking entity after check-out.
        """
        
        return self.booking_repository.check_out(booking_id)