from flask import Blueprint, request, jsonify

from operations_and_monitoring.application.services import MonitoringService
from operations_and_monitoring.application.services import BookingService

monitoring_api = Blueprint('monitoring_api', __name__)
operations_api = Blueprint('operations_api', __name__)

monitoring_service = MonitoringService()
operations_service = BookingService()

"""
Endpoint to retrieve all devices (thermostats and smoke sensors) associated with a hotel.
"""
@monitoring_api.route('/monitoring/devices', methods=['GET'])
def get_devices():
    try:
        thermostats = monitoring_service.get_thermostats()
        smoke_sensors = monitoring_service.get_smoke_sensors()

        devices = {
            "thermostats": [thermostat.to_dict() for thermostat in thermostats],
            "smoke_sensors": [smoke_sensor.to_dict() for smoke_sensor in smoke_sensors]
        }
        return jsonify(devices), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""
Endpoint to retrieve all thermostats associated with a hotel.
"""
@monitoring_api.route('/monitoring/devices/thermostats', methods=['POST'])
def add_thermostat():
    try:
        data = request.json
        thermostat = monitoring_service.add_thermostat(data)
        return jsonify(thermostat.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""
Endpoint to retrieve all smoke sensors associated with a hotel.
"""
@monitoring_api.route('/monitoring/devices/smoke_sensors', methods=['POST'])
def add_smoke_sensor():
    try:
        data = request.json
        smoke_sensor = monitoring_service.add_smoke_sensor(data)
        return jsonify(smoke_sensor.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""
Endpoint to retrieve a booking by customer ID.
"""
@operations_api.route('/operations/booking/<string:customer_id>', methods=['GET'])
def get_booking_by_customer_id(customer_id):
    try:
        booking = operations_service.get_booking_by_customer_id(customer_id)
        if booking:
            return jsonify(booking.to_dict()), 200
        else:
            return jsonify({"error": "Booking not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""
Endpont to retrieve all bookings for a hotel.
"""
@operations_api.route('/operations/bookings/<string:hotel_id>', methods=['GET'])
def get_bookings(hotel_id):
    try:
        bookings = operations_service.get_bookings(hotel_id)
        return jsonify([booking.to_dict() for booking in bookings]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""
Endpoint to check-in a customer for a booking.
"""
@operations_api.route('/operations/booking/check-in/<string:booking_id>', methods=['POST'])
def check_in_booking(booking_id):
    try:
        result = operations_service.check_in_booking(booking_id)
        if result:
            return jsonify({"message": "Check-in successful"}), 200
        else:
            return jsonify({"error": "Check-in failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""
Endpoint to check-out a customer for a booking.
"""
@operations_api.route('/operations/booking/check-out/<string:booking_id>', methods=['POST'])
def check_out_booking(booking_id):
    try:
        result = operations_service.check_out_booking(booking_id)
        if result:
            return jsonify({"message": "Check-out successful"}), 200
        else:
            return jsonify({"error": "Check-out failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
