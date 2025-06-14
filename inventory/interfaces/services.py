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
    """Create a new supply"""
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
    """Get all supplies in the system"""
    try:
        supplies = supply_service.get_all_supplies()
        return jsonify([supply.to_dict() for supply in supplies]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@supply_api.route('/api/v1/supply/<int:supply_id>', methods=['GET'])
def get_supply_by_id(supply_id):
    """Get a specific supply by ID"""
    try:
        supply = supply_service.get_supply_by_id(supply_id)
        if supply is None:
            return jsonify({"error": "Supply not found"}), 404
        return jsonify(supply.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@supply_api.route('/api/v1/supply/test', methods=['GET'])
def test_supply():
    """Test endpoint to verify API is working"""
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
    """Create a new supply request"""
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
    """Get a specific supply request by ID"""
    try:
        supply_request = supply_request_service.get_supply_request_by_id(request_id)
        if supply_request is None:
            return jsonify({"error": "Supply request not found"}), 404
        return jsonify(supply_request.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@supply_request_api.route('/api/v1/supply/supply-request/test', methods=['GET'])
def test_supply_request():
    """Test endpoint to verify API is working"""
    return jsonify({
        "message": "Supply Request API is working!",
        "available_endpoints": [
            "POST /api/v1/supply/supply-request - Create a new supply request",
            "GET /api/v1/supply/supply-request/{id} - Get supply request by ID"
        ]
    }), 200