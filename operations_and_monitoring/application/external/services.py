from operations_and_monitoring.domain.entities import Booking
from shared.infrastructure.external_services import ExternalService

class BookingExternalService:

    @staticmethod
    def get_booking_by_customer_id(customer_id: str) -> Booking:
        """
        Retrieves a booking by customer ID.
        
        :param customer_id: The ID of the customer to retrieve the booking for.
        :return: The booking associated with the customer ID.
        """

        try:
            # consume the external service to get booking data

            service = ExternalService()
            response = service.get(f"bookings/get-booking-by-customer-id?customer_id={customer_id}")

            booking_data = response.json()
            if not booking_data:
                return None
            return Booking(
                booking_id=booking_data['booking_id'],
                customer_id=booking_data['customer_id'],
                hotel_id=booking_data['hotel_id'],
                room_number=booking_data['room_number'],
                check_in_date=booking_data['check_in_date'],
                check_out_date=booking_data['check_out_date']
            )
        except Exception as e:
            print(f"Error retrieving booking by customer ID {customer_id}: {e}")
            return None

    @staticmethod
    def get_booking_by_id(booking_id: str) -> Booking:
        """
        Retrieves a booking by booking ID.
        
        :param booking_id: The ID of the booking to retrieve.
        :return: The booking associated with the booking ID.
        """

        try:
            # consume the external service to get booking data

            service = ExternalService()
            response = service.get(f"bookings/get-booking-by-id?id={booking_id}")

            booking_data = response.json()
            if not booking_data:
                return None
            return Booking(
                id=booking_data['id'],
                payment_customer_id=booking_data['payment_customer_id'],
                room_id=booking_data['room_id'],
                description=booking_data['description'],
                start_date=booking_data['start_date'],
                final_date=booking_data['final_date'],
                price_room=booking_data['price_room'],
                night_count=booking_data['night_count'],
                amount=booking_data['amount'],
                state=booking_data['state'],
                preference_id=booking_data.get('preference_id', None)
            )
        except Exception as e:
            print(f"Error retrieving booking by ID {booking_id}: {e}")
            return None

    @staticmethod
    def update_booking_state(booking_id: str, state: str) -> bool:
        """
        Updates the state of a booking.
        
        :param booking_id: The ID of the booking to update.
        :param state: The new state to set for the booking.
        :return: True if the update was successful, False otherwise.
        """

        try:
            # consume the external service to update booking state

            service = ExternalService()
            response = service.put(f"bookings/update-booking-state", data={"id": booking_id, "state": state})

            return response.status_code == 200
        except Exception as e:
            print(f"Error updating booking state for {booking_id}: {e}")
            return False
        
    @staticmethod
    def get_bookings(hotel_id: str) -> list:
        """
        Retrieves bookings associated with a specific hotel.
        
        :param hotel_id: The ID of the hotel to retrieve bookings for.
        :return: A list of bookings associated with the hotel.
        """

        try:
            # consume the external service to get bookings data

            service = ExternalService()
            response = service.get(f"bookings/get-all-bookings?hotel_id={hotel_id}")

            bookings_data = response.json()
            return [Booking(
                id=booking['id'],
                payment_customer_id=booking['payment_customer_id'],
                room_id=booking['room_id'],
                description=booking['description'],
                start_date=booking['start_date'],
                final_date=booking['final_date'],
                price_room=booking['price_room'],
                night_count=booking['night_count'],
                amount=booking['amount'],
                state=booking['state'],
                preference_id=booking.get('preference_id', None)
            ) for booking in bookings_data]
        except Exception as e:
            print(f"Error retrieving bookings for hotel {hotel_id}: {e}")
            return []