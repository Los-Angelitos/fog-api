from sqlalchemy import select
from shared.infrastructure.database import db

from operations_and_monitoring.infrastructure.models import Thermostat as ThermostatModel, SmokeSensor as SmokeSensorModel
from operations_and_monitoring.domain.entities import Thermostat, SmokeSensor

from operations_and_monitoring.domain.entities import Booking
from operations_and_monitoring.infrastructure.models import Booking as BookingModel

from operations_and_monitoring.application.external.services import BookingExternalService

from typing import Optional
import datetime

class MonitoringRepository:    
    def get_thermostats(self) -> list[Thermostat]:
        """
        Retrieves thermostats associated with a specific hotel.
        
        :param hotel_id: The ID of the hotel to retrieve thermostats for.
        :return: A list of Thermostat entities associated with the hotel.
        """
        try:
            result = db.session.execute(ThermostatModel.__table__.select()).scalars().all()
            print(f"Found {len(result)} thermostats.")

            return [Thermostat(device_id=device.device_id, ip_address=device.ip_address, mac_address=device.mac_address, state=device.state, temperature=device.temperature, last_update=device.last_update) for device in result]
        except Exception as e:
            print(f"Error retrieving thermostats: {e}")
            return []
    
    def get_smoke_sensors(self) -> list[SmokeSensor]:
        """
        Retrieves smoke sensors associated with a specific hotel.
        
        :param hotel_id: The ID of the hotel to retrieve smoke sensors for.
        :return: A list of SmokeSensor entities associated with the hotel.
        """
        
        result = db.session.execute(SmokeSensorModel.__table__.select()).scalars().all()
        print(f"Found {len(result)} smoke sensors.")
        
        return [SmokeSensor(device_id=device.device_id, ip_address=device.ip_address, mac_address=device.mac_address, state=device.state, last_analogic_value=device.last_analogic_value, last_alert_time=device.last_alert_time) for device in result]
    
    def add_thermostat(self, data: dict) -> Optional[Thermostat]:
        """
        Adds a new thermostat to the system.
        
        :param data: The data for the new thermostat.
        :return: The added Thermostat entity.
        """
        
        try:

            thermostat = ThermostatModel(
                ip_address=data['ip_address'],
                mac_address=data['mac_address'],
                temperature=data.get('temperature', 20.0),  # Default temperature
                last_update=datetime.datetime.now(),
                state=data.get('state', 'active')  # Default state
            )
            
            session = db.session
            session.add(thermostat)
            session.commit()
            print(f"Thermostat added with ID: {thermostat.id}")
            
            return Thermostat(
                id=thermostat.id,ip_address=thermostat.ip_address, mac_address=thermostat.mac_address, state=thermostat.state, temperature=thermostat.temperature, last_update=thermostat.last_update)

        except Exception as e:
            print(f"Error add_thermostat: {e}")
            db.session.rollback()
            return None
    
    def add_smoke_sensor(self, data: dict) -> SmokeSensor:
        """
        Adds a new smoke sensor to the system.
        
        :param data: The data for the new smoke sensor.
        :return: The added SmokeSensor entity.
        """
        
        smoke_sensor = SmokeSensorModel(
            ip_address=data['ip_address'],
            mac_address=data['mac_address'],
            last_analogic_value=data.get('last_analogic_value', 0.0),  # Default value
            last_alert_time=data.get('last_alert_time', None)
        )
        
        db.session.add(smoke_sensor)
        db.session.commit()
        
        return SmokeSensor( ip_address=smoke_sensor.ip_address, mac_address=smoke_sensor.mac_address, state=smoke_sensor.state, last_analogic_value=smoke_sensor.last_analogic_value, last_alert_time=smoke_sensor.last_alert_time)
    
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
    
    def check_in(self, booking_id: str) -> bool:
        """
        Checks in a customer for a booking.
        
        :param booking_id: The ID of the booking to check in.
        :return: True if the check-in was successful, False otherwise.

        When a booking is checked in, the fog layer will save the record in the local database.
        """

        # Update the booking state in the external service
        try:
            BookingExternalService.update_booking_state(booking_id, 'checked_in')
        except Exception as e:
            print(f"Error updating booking state for {booking_id}: {e}")
           
        try:
            booking = BookingExternalService.get_booking_by_id(booking_id)
            if not booking:
                return False
            booking = BookingModel(
                id=booking.id,
                payment_customer_id=booking.payment_customer_id,
                room_id=booking.room_id,
                description=booking.description,
                start_date=booking.start_date,
                final_date=booking.final_date,
                price_room=booking.price_room,
                night_count=booking.night_count,
                amount=booking.amount,
                state='checked_in',  # Update state to checked_in
                preference_id=booking.preference_id
            )

            db.session.add(booking)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error checking in booking {booking_id}: {e}")
            return False
        
    def check_out(self, booking_id: str) -> bool:
        """
        Checks out a customer for a booking.
        
        :param booking_id: The ID of the booking to check out.
        :return: True if the check-out was successful, False otherwise.
        """
        
        # Update the booking state in the external service
        try:
            BookingExternalService.update_booking_state(booking_id, 'checked_out')
        except Exception as e:
            print(f"Error updating booking state for {booking_id}: {e}")
        
        try:
            # removing from the local database
            
            query = select(BookingModel).where(BookingModel.id == booking_id)
            booking = db.session.execute(query).scalar_one_or_none()
            if not booking:
                return False
            
            db.session.delete(booking)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error checking out booking {booking_id}: {e}")
            return False
        
        