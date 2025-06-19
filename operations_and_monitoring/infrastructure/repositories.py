from sqlalchemy import select
from shared.infrastructure.database import db

from operations_and_monitoring.infrastructure.models import Thermostat as ThermostatModel, SmokeSensor as SmokeSensorModel
from inventory.infrastructure.models import Rfid as RfidModel
from operations_and_monitoring.domain.entities import Thermostat, SmokeSensor
from inventory.domain.entities import Rfid

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
            session = db.session
            result = session.query(ThermostatModel).all()
            print(f"Found {len(result)} thermostats.")

            return [Thermostat(id=device.id, device_id=device.device_id,
                               api_key=device.api_key,ip_address=device.ip_address,
                               mac_address=device.mac_address,
                               state=device.state, temperature=device.temperature,
                               last_update=device.last_update,
                               room_id=device.room_id) for device in result]
        except Exception as e:
            print(f"Error retrieving thermostats: {e}")
            return []

    def get_rfid(self) -> list[Rfid]:
        """
        Retrieves RFID devices associated with a specific hotel.
        """
        try:
            session = db.session
            print("[Repository] Getting RFID devices from DB...")
            result = session.query(RfidModel).all()
            print(f"[Repository] Raw result from DB: {result}")
            print(f"[Repository] Found {len(result)} RFID devices.")

            rfids = []
            for device in result:
                print("[Repository] Mapping device to entity:")
                print(f"  - ID: {device.id}")
                print(f"  - device_id: {getattr(device, 'device_id', 'MISSING')}")
                print(f"  - room_id: {device.room_id}")
                print(f"  - api_key: {device.api_key}")
                print(f"  - u_id: {device.u_id}")

                try:
                    rfid_entity = Rfid(
                        id=device.id,
                        room_id=device.room_id,
                        device_id=device.device_id,
                        api_key=device.api_key,
                        u_id=device.u_id,
                    )
                    rfids.append(rfid_entity)
                except Exception as inner_e:
                    print(f"[Repository] Error mapping RFID entity: {inner_e}")

            print(f"[Repository] Total mapped RFID entities: {len(rfids)}")
            return rfids

        except Exception as e:
            print(f"[Repository] Error retrieving RFID devices: {e}")
            return []

    def save_thermostat(self, item: dict, ):
        session = db.session
        try:
            # Buscar si ya existe un termostato con ese device_id
            existing = session.query(ThermostatModel).filter_by(device_id=item["id"]).first()

            if existing:
                print(f"[Repository] Thermostat with ID {item['id']} already exists. Skipping.")
                return

            # Crear uno nuevo si no existe
            new_thermostat = ThermostatModel(
                device_id=item["id"],
                api_key=item.get("api_key", ""),
                ip_address=item.get("ipAddress", ""),
                mac_address=item.get("macAddress", ""),
                state=item.get("state", "OFF"),
                last_update=item.get("lastUpdate", datetime.datetime.now()),
                temperature=item.get("temperature", "0"),
                room_id=item.get("roomId"),
            )

            session.add(new_thermostat)
            session.commit()
            print(f"[Repository] Thermostat {item['id']} inserted successfully.")

        except Exception as e:
            session.rollback()
            print(f"[Repository] Error inserting thermostat: {e}")


    def get_smoke_sensors(self) -> list[SmokeSensor]:
        """
        Retrieves smoke sensors associated with a specific hotel.
        
        :param hotel_id: The ID of the hotel to retrieve smoke sensors for.
        :return: A list of SmokeSensor entities associated with the hotel.
        """
        try:
            session = db.session
            result = session.query(SmokeSensorModel).all()
            print(f"Found {len(result)} smoke sensors.")
        
            return [SmokeSensor(id=device.id, device_id=device.device_id, api_key=device.api_key, ip_address=device.ip_address, mac_address=device.mac_address, state=device.state, last_analogic_value=device.last_analogic_value,room_id=device.room_id, last_alert_time=device.last_alert_time) for device in result]
        except Exception as e:
            print(f"Error retrieving smoke sensors: {e}")
            return []

    def save_rfid(self, item: dict):
        try:
            session = db.session

            existing = session.query(RfidModel).filter_by(device_id=item["id"]).first()
            if existing:
                print(f"[Repository] RFID with ID {item['id']} already exists. Skipping.")
                return

            new_rfid = RfidModel(
                device_id=item["id"],  # <- aquí usamos el campo lógico
                room_id=item.get("roomId"),
                api_key=item.get("apiKey", ""),
                u_id=item.get("uId", ""),
            )

            session.add(new_rfid)
            session.commit()
            print(f"[Repository] RFID device {item['id']} inserted successfully.")

        except Exception as e:
            print(f"[Repository] Error inserting RFID device: {e}")

    def add_thermostat(self, data: dict) -> Optional[Thermostat]:
        """
        Adds a new thermostat to the system.
        
        :param data: The data for the new thermostat.
        :return: The added Thermostat entity.
        """
        
        session = db.session
        try:
            thermostat = ThermostatModel(
                device_id=data['device_id'],
                api_key=data['api_key'],
                ip_address=data['ip_address'],
                mac_address=data['mac_address'],
                temperature=data.get('temperature', 20.0),  # Default temperature
                last_update=datetime.datetime.now(),
                state=data.get('state', 'active'),  # Default state
                room_id=data['room_id']
            )
            
            session.add(thermostat)
            session.commit()
            print(f"Thermostat added with ID: {thermostat.id}")
            
            return Thermostat(
                id=thermostat.id, device_id=thermostat.device_id, api_key=thermostat.api_key, ip_address=thermostat.ip_address, mac_address=thermostat.mac_address, state=thermostat.state, temperature=thermostat.temperature, last_update=thermostat.last_update, room_id=thermostat.room_id)

        except Exception as e:
            print(f"Error add_thermostat: {e}")
            session.rollback()
            return None
    
    def add_smoke_sensor(self, data: dict) -> SmokeSensor:
        """
        Adds a new smoke sensor to the system.
        
        :param data: The data for the new smoke sensor.
        :return: The added SmokeSensor entity.
        """

        session = db.session
        try:     
            smoke_sensor = SmokeSensorModel(
                device_id=data['device_id'],
                api_key=data['api_key'],
                ip_address=data['ip_address'],
                mac_address=data['mac_address'],
                last_analogic_value=data.get('last_analogic_value', 0.0),  # Default value
                last_alert_time=data.get('last_alert_time', datetime.datetime.now()),  # Default to now
                state=data.get('state', 'active'),  # Default state
                room_id=data['room_id']
            )
            
            session.add(smoke_sensor)
            session.commit()
            print(f"Smoke sensor added with ID: {smoke_sensor.id}")
            
            return SmokeSensor(id=smoke_sensor.id, device_id=smoke_sensor.device_id, api_key=smoke_sensor.api_key, ip_address=smoke_sensor.ip_address, mac_address=smoke_sensor.mac_address, state=smoke_sensor.state,last_analogic_value=smoke_sensor.last_analogic_value, room_id=smoke_sensor.room_id, last_alert_time=smoke_sensor.last_alert_time)
        except Exception as e:
            print(f"Error add_smoke_sensor: {e}")
            session.rollback()
            return None

    def validation_service(self, data: dict) -> bool:
        """
        Validates if there's an existing rfid device with the provided room_id and u_id.
        :param data: The data containing room_id and u_id to validate.
        :return: True if the device exists, False otherwise.
        """
        if not data or 'room_id' not in data or 'u_id' not in data:
            raise ValueError("Invalid data for validation. 'room_id' and 'u_id' are required.")

        room_id = data['room_id']
        u_id = data['u_id']

        try:
            session = db.session
            query = select(RfidModel).where(RfidModel.room_id == room_id, RfidModel.u_id == u_id)
            device = session.execute(query).scalar_one_or_none()
            return device is not None
        except Exception as e:
            print(f"Error validating service: {e}")
            return False

    
class BookingRepository:
    def get_booking_by_customer_id(self, customer_id: str) -> Optional[Booking]:
        """
        Retrieves a booking by customer ID.
        
        :param customer_id: The ID of the customer to retrieve the booking for.
        :return: The booking associated with the customer ID, or None if not found.
        """

        try:
            booking = BookingExternalService.get_booking_by_customer_id(customer_id)
            
            return booking
        except Exception as e:
            print(f"Error retrieving booking by customer ID {customer_id}: {e}")
            return None


    def get_bookings(self, hotel_id: str) -> list:
        """
        Retrieves bookings associated with a specific hotel.
        
        :param hotel_id: The ID of the hotel to retrieve bookings for.
        :return: A list of bookings associated with the hotel.
        """
        try:
            bookings = BookingExternalService.get_bookings(hotel_id)
            return bookings
        except Exception as e:
            print(f"Error retrieving bookings for hotel {hotel_id}: {e}")
            return []
    
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

        session = db.session
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

            session.add(booking)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
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
        
        session = db.session

        try:
            # removing from the local database
            
            query = select(BookingModel).where(BookingModel.id == booking_id)
            booking = db.session.execute(query).scalar_one_or_none()
            if not booking:
                return False
            
            session.delete(booking)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error checking out booking {booking_id}: {e}")
            return False
        
        