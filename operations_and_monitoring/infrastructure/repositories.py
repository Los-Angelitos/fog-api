from sqlalchemy import select
from shared.infrastructure.database import db

from operations_and_monitoring.infrastructure.models import Thermostat as ThermostatModel, SmokeSensor as SmokeSensorModel
from operations_and_monitoring.domain.entities import Thermostat, SmokeSensor

from operations_and_monitoring.domain.entities import Booking
from operations_and_monitoring.infrastructure.models import Booking as BookingModel

from operations_and_monitoring.application.external.services import BookingExternalService

from typing import Optional

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
    
    def add_thermostat(self, data: dict) -> Thermostat:
        """
        Adds a new thermostat to the system.
        
        :param data: The data for the new thermostat.
        :return: The added Thermostat entity.
        """
        
        thermostat = ThermostatModel(
            device_id=data['device_id'],
            ip_address=data['ip_address'],
            mac_address=data['mac_address'],
            temperature=data.get('temperature', 20.0),  # Default temperature
            last_update=data.get('last_update', db.func.now())
        )
        
        db.session.add(thermostat)
        db.session.commit()
        
        return Thermostat(device_id=thermostat.device_id, ip_address=thermostat.ip_address, mac_address=thermostat.mac_address, state=thermostat.state, temperature=thermostat.temperature, last_update=thermostat.last_update)
    
    def add_smoke_sensor(self, data: dict) -> SmokeSensor:
        """
        Adds a new smoke sensor to the system.
        
        :param data: The data for the new smoke sensor.
        :return: The added SmokeSensor entity.
        """
        
        smoke_sensor = SmokeSensorModel(
            device_id=data['device_id'],
            ip_address=data['ip_address'],
            mac_address=data['mac_address'],
            last_analogic_value=data.get('last_analogic_value', 0.0),  # Default value
            last_alert_time=data.get('last_alert_time', None)
        )
        
        db.session.add(smoke_sensor)
        db.session.commit()
        
        return SmokeSensor(device_id=smoke_sensor.device_id, ip_address=smoke_sensor.ip_address, mac_address=smoke_sensor.mac_address, state=smoke_sensor.state, last_analogic_value=smoke_sensor.last_analogic_value, last_alert_time=smoke_sensor.last_alert_time)
    
class BookingRepository:
    def get_booking_by_customer_id(self, customer_id: str) -> Optional[Booking]:
        """
        Retrieves a booking by customer ID.
        
        :param customer_id: The ID of the customer to retrieve the booking for.
        :return: The booking associated with the customer ID, or None if not found.
        """
        
        service = BookingExternalService()
        booking = service.get_booking_by_customer_id(customer_id)
        
        return booking


    def get_bookings(self, hotel_id: str) -> list:
        """
        Retrieves bookings associated with a specific hotel.
        
        :param hotel_id: The ID of the hotel to retrieve bookings for.
        :return: A list of bookings associated with the hotel.
        """
        
        result = db.session.execute(select(BookingModel).where(BookingModel.hotel_id == hotel_id)).scalars().all()
        
        return [Booking(id=booking.id, payment_customer_id=booking.payment_customer_id, room_id=booking.room_id, description=booking.description, start_date=booking.start_date, final_date=booking.final_date, price_room=booking.price_room, night_count=booking.night_count, amount=booking.amount, state=booking.state, preference_id=booking.preference_id) for booking in result]
    
    def add_booking(self, data: dict) -> Booking:
        """
        Adds a new booking to the system.
        
        :param data: The data for the new booking.
        :return: The added Booking entity.
        """
        
        booking = BookingModel(
            id=data['id'],
            payment_customer_id=data['payment_customer_id'],
            room_id=data['room_id'],
            description=data.get('description', ''),
            start_date=data['start_date'],
            final_date=data['final_date'],
            price_room=data['price_room'],
            night_count=data['night_count'],
            amount=data['amount'],
            state=data['state'],
            preference_id=data.get('preference_id', None)
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return Booking(id=booking.id, payment_customer_id=booking.payment_customer_id, room_id=booking.room_id, description=booking.description, start_date=booking.start_date, final_date=booking.final_date, price_room=booking.price_room, night_count=booking.night_count, amount=booking.amount, state=booking.state, preference_id=booking.preference_id)