from flask import Blueprint, request, jsonify

from inventory.application.services import SupplyService
from inventory.application.services import SupplyRequestService

supply_api = Blueprint('supply_api', __name__)
supply_request_api = Blueprint('supply_request_api', __name__)

supply_service = SupplyService()
supply_request_service = SupplyRequestService()

@supply_api.route('/api/v1/supply/create-supply', methods=['POST'])
def create_supply():
    try:
        data = request.json
        supply = supply_service.add_supply(data)
        return jsonify(supply.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@supply_api.route('/api/v1/supply/test', methods=['GET'])
def test_supply():
    return jsonify({"message": "Supply API is working!", "endpoints": [
        "POST /api/v1/supply/create-supply - Create a new supply",
        "POST /api/v1/supply/create-supply-request - Create a new supply request"
    ]}), 200

@supply_request_api.route('/api/v1/supply/create-supply-request', methods=['POST'])
def create_supply_request():
    try:
        data = request.json
        supply_request = supply_request_service.add_supply_request(data)
        return jsonify(supply_request.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500