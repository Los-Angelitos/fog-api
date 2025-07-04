from flask import Blueprint, request, jsonify
from flasgger import swag_from

from inventory.domain.entities import Rfid
from operations_and_monitoring.application.services import MonitoringService
from operations_and_monitoring.application.services import BookingService
from operations_and_monitoring.domain.entities import Thermostat
from operations_and_monitoring.infrastructure.repositories import MonitoringRepository
from operations_and_monitoring.interfaces.acl.services import MonitoringFacade
import requests
from shared.infrastructure.hotelconfig import   BACKEND_URL, HOTEL_ID

monitoring_api = Blueprint('monitoring', __name__)
operations_api = Blueprint('operations', __name__)

monitoring_service = MonitoringService()
operations_service = BookingService()
monitoring_facade = MonitoringFacade()



"""
Endpoint to retrieve all devices (thermostats, smoke sensors adn rfid readers) associated with a hotel.
"""
@monitoring_api.route('/monitoring/devices', methods=['GET'])
@swag_from({
    'tags': ['Monitoring']
})
def get_devices():
    """
    Retrieves all devices (thermostats, smoke sensors and rfid readers) associated with a hotel.
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
        rfid_devices = monitoring_service.get_rfid()

        devices = {
            "thermostats": [thermostat.to_json() for thermostat in thermostats],
            "smoke_sensors": [smoke_sensor.to_json() for smoke_sensor in smoke_sensors],
            "rfid_devices": [rfid.to_json() for rfid in rfid_devices]
        }

        return jsonify(devices), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@monitoring_api.route('/monitoring/devices/validation', methods=['POST'])
@swag_from({
    'tags': ['Monitoring']
})
def validation_service():
    """
    Validates if there's an existing device with the provided room_id and u_id.
    ---
    parameters:
      - in: body
        name: validation_data
        description: Data to validate device existence
        required: true
        schema:
          type: object
          properties:
            room_id:
              type: integer
              description: The ID of the room
            u_id:
              type: string
              description: The unique ID of the device
    responses:
      200:
        description: Validation successful
      400:
        description: Bad request
      500:
        description: Internal server error
    """

    try:
        data = request.json
        print(data)
        room_id = data.get('room_id')
        u_id = data.get('u_id')
        if not room_id or not u_id:
            return jsonify({"error": "room_id and u_id are required"}), 400
        exists = monitoring_service.validation_service(data)
        if exists:
            return jsonify({"access": True}), 200
        else:
            return jsonify({"access": False}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
"""
Endpoint to retrieve all thermostats associated with a hotel.
"""
@monitoring_api.route('/monitoring/devices/thermostats', methods=['GET'])
@swag_from({
    'tags': ['Monitoring'],
    'responses': {
        200: {'description': 'Thermostats retrieved successfully'},
        500: {'description': 'Internal server error'}
    }
})
def get_thermostats():
    """
    Retrieves all thermostats associated with a hotel.
    """
    try:
        thermostats = monitoring_service.get_thermostats()
        return jsonify([t.to_json() for t in thermostats]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@monitoring_api.route('/monitoring/devices/smoke-sensors', methods=['GET'])
@swag_from({
    'tags': ['Monitoring'],
    'responses': {
        200: {'description': 'Smoke sensors retrieved successfully'},
        500: {'description': 'Internal server error'}
    }
})
def get_smoke_sensors():
    """
    Retrieves all smoke sensors associated with a hotel.
    """
    try:
        smoke_sensors = monitoring_service.get_smoke_sensors()
        return jsonify([s.to_json() for s in smoke_sensors]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@monitoring_api.route('/monitoring/devices/rfid', methods=['GET'])
@swag_from({
    'tags': ['Monitoring'],
    'responses': {
        200: {'description': 'RFID devices retrieved successfully'},
        500: {'description': 'Internal server error'}
    }
})
def get_rfid_devices():
    """
    Retrieves all RFID devices associated with a hotel.
    """
    try:
        rfid_devices = monitoring_service.get_rfid()
        return jsonify([r.to_json() for r in rfid_devices]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
            room_id:
              type: integer
              default: 1
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
            room_id:
              type: integer
              default: 1
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

@swag_from({
    'tags': ['Monitoring'],
})
@monitoring_api.route('/monitoring/devices/thermostats/<int:room_id>', methods=['GET'])
@swag_from({
    'tags': ['Monitoring']
})
def get_thermostats_by_room_id(room_id):
    """
    Retrieves thermostats by room ID.
    ---
    parameters:
      - in: path
        name: room_id
        type: integer
        required: true
        description: The ID of the room
    responses:
      200:
        description: Thermostats retrieved successfully
      400:
        description: Missing room_id parameter
      500:
        description: Internal server error
    """
    try:
        if not room_id:
            return jsonify({"error": "room_id is required"}), 400

        # Usa el service correctamente instanciado
        thermostats = monitoring_facade.get_thermostats_by_room_id(room_id)

        return jsonify([thermostat.to_json() for thermostat in thermostats]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@swag_from({
    'tags': ['Monitoring'],
})
@monitoring_api.route('/monitoring/devices/rfid-readers/<int:room_id>', methods=['GET'])
def get_rfid_by_room_id(room_id):
    """
        Retrieves RFID readers by room ID.
        ---
        parameters:
          - in: path
            name: room_id
            type: int
            required: true
            description: The ID of the room
        responses:
          200:
            description: RFID readers retrieved successfully
          400:
            description: Missing room_id parameter
          500:
            description: Internal server error
    """
    if room_id == None or room_id == "":
        raise Exception("room_id parameter is necessary")

    print("[Route] LLAMANDO A monitoring_facade.get_rfid_by_room_id...")
    rfid_devices = monitoring_facade.get_rfid_by_room_id(room_id)
    print(f"[Route] Recibido {len(rfid_devices)} dispositivos.")

    # TODO si es que esta vacio, le pide al backend
    # y guarda en la base de datos
    # Pero como lo haria si el backend requiere json token
    # si no, devuelve los dispositivos que ya tiene

    return [rfid_device.to_json() for rfid_device in rfid_devices]


@swag_from({
    'tags': ['Notifications'],
})
@operations_api.route('/notifications', methods=['POST'])
def send_smoke_sensor_notification():
    """
    Sends a notification when a smoke sensor detects smoke.
    ---
    parameters:
      - in: body
        name: notification_data
        description: Data for the notification
        required: true
        schema:
          type: object
          properties:
            device_id:
              type: string
              description: The ID of the smoke sensor device
            current_value:
              type: string
              description: The current analog value from the smoke sensor
            room_id:
              type: integer
              description: The ID of the room where the smoke sensor is located
    responses:
      200:
        description: Notification sent successfully
      400:
        description: Invalid request, device_id and current_value are required
      500:
        description: Internal server error
    """

    token = monitoring_facade._get_auth_token()
    if not token:
        raise Exception("Authentication with backend failed")

    data = request.json
    device_id = data.get('device_id')
    current_value = data.get('current_value')
    room_id = data.get('room_id')
    if not device_id or not current_value or not room_id:
        return jsonify({"error": "Invalid request, device_id, current_value and room_id are required"}), 400

    back_url = f"{BACKEND_URL}/notifications"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    owner_id = monitoring_facade.get_owner_id_by_hotel_id(HOTEL_ID)
    payload = {
        "title": "SMOKE SENSOR ALERT",
        "content": "Alerta de humo detectado por el sensor con ID: " + device_id +
                   " en la habitación con ID: " + str(room_id) +
                   ". Alcanzó el valor: " + str(current_value),
        "senderType": "System",
        "senderId": 0,
        "receiverId": owner_id,
        "hotelId": HOTEL_ID
    }

    print(f"[OperationsAndMonitoringService] Enviando solicitud POST a {back_url} con payload:")
    print(payload)

    try:
        response = requests.post(back_url, json=payload, headers=headers)

        print(f"[OperationsAndMonitoringService] Código de respuesta del API: {response.status_code}")

        if response.status_code != 200 and response.status_code != 201:
            print("[OperationsAndMonitoringService] ❌ Error en la respuesta del API.")
            return {"access": False}

        back_result = response.json()
        print(f"[OperationsAndMonitoringService] Respuesta del API: {back_result}")

        access_granted = back_result.get("access", False)

        return {"access": access_granted}

    except Exception as e:
        print(f"[OperationsAndMonitoringService] 🛑 Excepción durante la solicitud al API: {e}")
        return {"access": False}