from flask import Blueprint, request, jsonify

from inventory.application.services import SupplyService
from inventory.application.services import SupplyRequestService
from inventory.application.services import RfidCodeService


supply_api = Blueprint('supply_api', __name__)
supply_request_api = Blueprint('supply_request_api', __name__)
rfid_api = Blueprint('rfid_api', __name__)

rfid_service = RfidCodeService()
supply_service = SupplyService()
supply_request_service = SupplyRequestService()

# Supply endpoints
@supply_api.route('/api/v1/supply/create-supply', methods=['POST'])
def create_supply():
    """Create a new supply
    ---
    tags:
      - Supply
    summary: Create a new supply
    description: Creates a new supply in the system with the provided information
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: supply
        description: Supply object that needs to be created
        required: true
        schema:
          type: object
          required:
            - provider_id
            - hotel_id
            - name
            - price
            - stock
            - state
          properties:
            provider_id:
              type: integer
              description: ID of the provider
            hotel_id:
              type: integer
              description: ID of the hotel
            name:
              type: string
              description: Name of the supply
            price:
              type: number
              description: Price of the supply
            stock:
              type: integer
              description: Stock quantity
            state:
              type: string
              enum: [available, unavailable, discontinued]
              description: State of the supply
    responses:
      201:
        description: Supply created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: ID of the created supply
            provider_id:
              type: integer
              description: ID of the provider
            hotel_id:
              type: integer
              description: ID of the hotel
            name:
              type: string
              description: Name of the supply
            price:
              type: number
              description: Price of the supply
            stock:
              type: integer
              description: Stock quantity
            state:
              type: string
              description: State of the supply
      400:
        description: Invalid input data
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    try:
        data = request.json
        supply = supply_service.add_supply(data)
        return jsonify(supply.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@supply_api.route('/api/v1/supply/get-all-supplies', methods=['GET'])
def get_all_supplies():
    """Get all supplies in the system
    ---
    tags:
      - Supply
    summary: Retrieve all supplies
    description: Returns a list of all supplies in the system
    produces:
      - application/json
    responses:
      200:
        description: List of supplies retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID of the supply
              provider_id:
                type: integer
                description: ID of the provider
              hotel_id:
                type: integer
                description: ID of the hotel
              name:
                type: string
                description: Name of the supply
              price:
                type: number
                description: Price of the supply
              stock:
                type: integer
                description: Stock quantity
              state:
                type: string
                description: State of the supply
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    try:
        supplies = supply_service.get_all_supplies()
        return jsonify([supply.to_dict() for supply in supplies]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@supply_api.route('/api/v1/supply/<int:supply_id>', methods=['GET'])
def get_supply_by_id(supply_id):
    """Get a specific supply by ID
    ---
    tags:
      - Supply
    summary: Retrieve a supply by ID
    description: Returns a specific supply based on the provided ID
    produces:
      - application/json
    parameters:
      - in: path
        name: supply_id
        type: integer
        required: true
        description: ID of the supply to retrieve
    responses:
      200:
        description: Supply retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: ID of the supply
            provider_id:
              type: integer
              description: ID of the provider
            hotel_id:
              type: integer
              description: ID of the hotel
            name:
              type: string
              description: Name of the supply
            price:
              type: number
              description: Price of the supply
            stock:
              type: integer
              description: Stock quantity
            state:
              type: string
              description: State of the supply
      404:
        description: Supply not found
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    try:
        supply = supply_service.get_supply_by_id(supply_id)
        if supply is None:
            return jsonify({"error": "Supply not found"}), 404
        return jsonify(supply.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Supply Request endpoints
@supply_request_api.route('/api/v1/supply/create-supply-request', methods=['POST'])
def create_supply_request():
    """Create a new supply request
    ---
    tags:
      - Supply Request
    summary: Create a new supply request
    description: Creates a new supply request in the system
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: supply_request
        description: Supply request object that needs to be created
        required: true
        schema:
          type: object
          required:
            - payment_owner_id
            - supply_id
            - count
            - amount
          properties:
            payment_owner_id:
              type: integer
              description: ID of the payment owner
            supply_id:
              type: integer
              description: ID of the supply being requested
            count:
              type: integer
              description: Quantity of supplies requested
            amount:
              type: number
              description: Total amount for the request
    responses:
      201:
        description: Supply request created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: ID of the created supply request
            payment_owner_id:
              type: integer
              description: ID of the payment owner
            supply_id:
              type: integer
              description: ID of the supply
            count:
              type: integer
              description: Quantity requested
            amount:
              type: number
              description: Total amount
      400:
        description: Invalid input data
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    try:
        data = request.json
        supply_request = supply_request_service.add_supply_request(data)
        return jsonify(supply_request.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@supply_request_api.route('/api/v1/supply/supply-request/<int:request_id>', methods=['GET'])
def get_supply_request_by_id(request_id):
    """Get a specific supply request by ID
    ---
    tags:
      - Supply Request
    summary: Retrieve a supply request by ID
    description: Returns a specific supply request based on the provided ID
    produces:
      - application/json
    parameters:
      - in: path
        name: request_id
        type: integer
        required: true
        description: ID of the supply request to retrieve
    responses:
      200:
        description: Supply request retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: ID of the supply request
            payment_owner_id:
              type: integer
              description: ID of the payment owner
            supply_id:
              type: integer
              description: ID of the supply
            count:
              type: integer
              description: Quantity requested
            amount:
              type: number
              description: Total amount
      404:
        description: Supply request not found
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    try:
        supply_request = supply_request_service.get_supply_request_by_id(request_id)
        if supply_request is None:
            return jsonify({"error": "Supply request not found"}), 404
        return jsonify(supply_request.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rfid_api.route('/api/v1/rfid/validate-access', methods=['POST'])
def validate_rfid_access():
    """Validate RFID access to a room
    ---
    tags:
      - RFID
    summary: Validate RFID access
    description: Validates if an RFID UID has access to a specific room
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: rfid_validation
        description: RFID validation request from IoT device
        required: true
        schema:
          type: object
          required:
            - rfid_uid
            - room_id
          properties:
            rfid_uid:
              type: string
              description: RFID UID in hexadecimal format
            room_id:
              type: string
              description: Room identifier
    responses:
      200:
        description: Access validation result
        schema:
          type: object
          properties:
            access_granted:
              type: boolean
              description: Whether access is granted or not
      400:
        description: Invalid request data
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        rfid_uid = data.get('rfid_uid')
        room_id = data.get('room_id')
        
        if not rfid_uid or not room_id:
            return jsonify({"error": "Missing required fields: rfid_uid and room_id"}), 400
        
        # Validate access
        access_granted = rfid_service.validate_rfid_access(rfid_uid, room_id)
        
        return jsonify({"access_granted": access_granted}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rfid_api.route('/api/v1/rfid/create', methods=['POST'])
def create_rfid_code():
    """Create a new RFID code
    ---
    tags:
      - RFID
    summary: Create a new RFID code
    description: Creates a new RFID code in the system
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: rfid_code
        description: RFID code object that needs to be created
        required: true
        schema:
          type: object
          required:
            - room_id
            - guest_id
            - booking_id
            - uuid
          properties:
            room_id:
              type: string
              description: Room identifier
            guest_id:
              type: integer
              description: ID of the guest
            booking_id:
              type: integer
              description: ID of the booking
            uuid:
              type: string
              description: RFID UUID in hexadecimal format
    responses:
      201:
        description: RFID code created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: ID of the created RFID code
            room_id:
              type: string
              description: Room identifier
            guest_id:
              type: integer
              description: ID of the guest
            booking_id:
              type: integer
              description: ID of the booking
            uuid:
              type: string
              description: RFID UUID
      400:
        description: Invalid input data
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    try:
        data = request.json
        rfid_code = rfid_service.add_rfid_code(data)
        return jsonify(rfid_code.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rfid_api.route('/api/v1/rfid/<string:uuid>', methods=['GET'])
def get_rfid_code_by_uuid(uuid):
    """Get RFID code by UUID
    ---
    tags:
      - RFID
    summary: Retrieve RFID code by UUID
    description: Returns a specific RFID code based on the provided UUID
    produces:
      - application/json
    parameters:
      - in: path
        name: uuid
        type: string
        required: true
        description: UUID of the RFID code to retrieve
    responses:
      200:
        description: RFID code retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: ID of the RFID code
            room_id:
              type: string
              description: Room identifier
            guest_id:
              type: integer
              description: ID of the guest
            booking_id:
              type: integer
              description: ID of the booking
            uuid:
              type: string
              description: RFID UUID
      404:
        description: RFID code not found
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    try:
        rfid_code = rfid_service.get_rfid_code_by_uuid(uuid)
        if rfid_code is None:
            return jsonify({"error": "RFID code not found"}), 404
        return jsonify(rfid_code.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500