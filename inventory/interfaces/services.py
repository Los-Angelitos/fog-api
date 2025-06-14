from flask import Blueprint, request, jsonify

from inventory.application.services import SupplyService
from inventory.application.services import SupplyRequestService

supply_api = Blueprint('supply_api', __name__)
supply_request_api = Blueprint('supply_request_api', __name__)

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
              format: float
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
              format: float
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
                format: float
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
              format: float
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

@supply_api.route('/api/v1/supply/test', methods=['GET'])
def test_supply():
    """Test endpoint to verify Supply API is working
    ---
    tags:
      - Supply
    summary: Test Supply API
    description: Test endpoint to verify that the Supply API is working correctly
    produces:
      - application/json
    responses:
      200:
        description: API is working correctly
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message
            available_endpoints:
              type: array
              items:
                type: string
              description: List of available endpoints
    """
    return jsonify({
        "message": "Supply API is working!",
        "available_endpoints": [
            "POST /api/v1/supply/create-supply - Create a new supply",
            "GET /api/v1/supply/get-all-supplies - Get all supplies",
            "GET /api/v1/supply/{id} - Get supply by ID"
        ]
    }), 200

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
              format: float
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
              format: float
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
              format: float
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

@supply_request_api.route('/api/v1/supply/supply-request/test', methods=['GET'])
def test_supply_request():
    """Test endpoint to verify Supply Request API is working
    ---
    tags:
      - Supply Request
    summary: Test Supply Request API
    description: Test endpoint to verify that the Supply Request API is working correctly
    produces:
      - application/json
    responses:
      200:
        description: API is working correctly
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message
            available_endpoints:
              type: array
              items:
                type: string
              description: List of available endpoints
    """
    return jsonify({
        "message": "Supply Request API is working!",
        "available_endpoints": [
            "POST /api/v1/supply/supply-request - Create a new supply request",
            "GET /api/v1/supply/supply-request/{id} - Get supply request by ID"
        ]
    }), 200