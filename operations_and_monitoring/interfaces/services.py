from flask import Blueprint, request, jsonify
from flasgger import swag_from

from operations_and_monitoring.application.services import MonitoringService
from operations_and_monitoring.application.services import BookingService

monitoring_api = Blueprint('monitoring', __name__)
operations_api = Blueprint('operations', __name__)

monitoring_service = MonitoringService()
operations_service = BookingService()

"""
Endpoint to retrieve all devices (thermostats and smoke sensors) associated with a hotel.
"""
@monitoring_api.route('/monitoring/devices', methods=['GET'])
@swag_from({
    'tags': ['Monitoring']
})
def get_devices():
    """
    Retrieves all devices (thermostats and smoke sensors) associated with a hotel.
    ---
    responses:
      200:
        description: Devices retrieved successfully
      500:
        description: Internal server error
    """

    try:
        thermostats = monitoring_service.get_thermostats()
        smoke_sensors = monitoring_service.get_smoke_sensors()

        devices = {
            "thermostats": [thermostat.to_json() for thermostat in thermostats],
            "smoke_sensors": [smoke_sensor.to_json() for smoke_sensor in smoke_sensors]
        }

        return jsonify(devices), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""
Endpoint to retrieve all thermostats associated with a hotel.
"""
@monitoring_api.route('/monitoring/devices/thermostats', methods=['POST'])
@swag_from({
    'tags': ['Monitoring'],
})
def add_thermostat():
    """
    Adds a new thermostat to the system.
    ---
    parameters:
      - in: body
        name: thermostat
        description: Thermostat data
        required: true
        schema:
          type: object
          properties:
            device_id:
              type: string
            api_key:
              type: string
            ip_address:
              type: string
            mac_address:
              type: string
            temperature:
              type: number
              default: 20.0
    responses:
      201:
        description: Thermostat added successfully
      500:
        description: Internal server error
    """
    try:
        data = request.json
        thermostat = monitoring_service.add_thermostat(data)
        if not thermostat:
            raise Exception("Error creating the thermostat, possibly device_id is duplicated")
        return jsonify(thermostat.to_json()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""
Endpoint to retrieve all smoke sensors associated with a hotel.
"""
@swag_from({
    'tags': ['Monitoring'],
})
@monitoring_api.route('/monitoring/devices/smoke_sensors', methods=['POST'])
def add_smoke_sensor():
    """
    Adds a new smoke sensor to the system.
    ---
    parameters:
      - in: body
        name: smoke_sensor
        description: Smoke sensor data
        required: true
        schema:
          type: object
          properties:
            device_id:
              type: string
            api_key:
              type: string
            ip_address:
              type: string
            mac_address:
              type: string
            last_analogic_value:
              type: number
              default: 0.0
    responses:
      201:
        description: Smoke sensor added successfully
      500:
        description: Internal server error
    """
    try:
        data = request.json
        smoke_sensor = monitoring_service.add_smoke_sensor(data)
        if not smoke_sensor:
            raise Exception("Error creating the smoke sensor, possibly device_id is duplicated")
        return jsonify(smoke_sensor.to_json()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""
Endpoint to retrieve a booking by customer ID.
"""
@operations_api.route('/operations/booking/<string:customer_id>', methods=['GET'])
@swag_from({
    'tags': ['Operations'],
})
def get_booking_by_customer_id(customer_id):
    """
    Retrieves a booking by customer ID.
    ---
    parameters:
      - in: path
        name: customer_id
        type: string
        required: true
    responses:
      200:
        description: Booking retrieved successfully
      404:
        description: Booking not found
      500:
        description: Internal server error
    """
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
@swag_from({
    'tags': ['Operations'],
})
@operations_api.route('/operations/bookings/<string:hotel_id>', methods=['GET'])
def get_bookings(hotel_id):
    """
    Retrieves all bookings for a specific hotel.
    ---
    parameters:
      - in: path
        name: hotel_id
        type: string
        required: true
    responses:
      200:
        description: Bookings retrieved successfully
      500:
        description: Internal server error
    """

    try:
        bookings = operations_service.get_bookings(hotel_id)
        return jsonify([booking.to_dict() for booking in bookings]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""
Endpoint to check-in a customer for a booking.
"""
@operations_api.route('/operations/booking/check-in/<string:booking_id>', methods=['POST'])
@swag_from({
    'tags': ['Operations'],
})
def check_in_booking(booking_id):
    """
    Checks in a customer for a booking.
    ---
    parameters:
      - in: path
        name: booking_id
        type: string
        required: true
    responses:
        200:
            description: Check-in successful
        400:
            description: Check-in failed
        500:
            description: Internal server error
    """
    try:
        result = operations_service.check_in(booking_id)
        if result:
            return jsonify({"message": "Check-in successful"}), 200
        else:
            return jsonify({"error": "Check-in failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""
Endpoint to check-out a customer for a booking.
"""
@swag_from({
    'tags': ['Operations'],
})  
@operations_api.route('/operations/booking/check-out/<string:booking_id>', methods=['POST'])
def check_out_booking(booking_id):
    """
    Checks out a customer for a booking.
    ---
    parameters:
      - in: path
        name: booking_id
        type: string
        required: true
    responses:
        200:
            description: Check-out successful
        400:
            description: Check-out failed
        500:
            description: Internal server error
    """
    
    try:
        result = operations_service.check_out(booking_id)
        if result:
            return jsonify({"message": "Check-out successful"}), 200
        else:
            return jsonify({"error": "Check-out failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
