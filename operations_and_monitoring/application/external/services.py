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

