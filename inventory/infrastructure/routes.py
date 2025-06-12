from flask import Blueprint, request, jsonify

from inventory.application.services import InventoryApplicationService
#from iam.interfaces.services import authenticate_request

inventory_api = Blueprint('inventory_api', __name__)

inventory_service = InventoryApplicationService()


@inventory_api.route('/api/v1/supply/create-supply', methods=['POST'])
def create_supply():
   # auth_result = authenticate_request()
   # if auth_result:
    #    return auth_result
    
    data = request.json
    try:
        provider_id = data['provider_id']
        name = data['name']
        price = data['price']
        stock = data['stock']
        state = data['state']
        
        supply = inventory_service.create_supply(
            provider_id, name, price, stock, state,
            request.headers.get('X-API-Key')
        )
        
        return jsonify({
            "id": supply.id,
            "provider_id": supply.provider_id,
            "name": supply.name,
            "price": float(supply.price),
            "stock": supply.stock,
            "state": supply.state
        }), 201
        
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@inventory_api.route('/api/v1/supply-request', methods=['POST'])
def create_supply_request():
   # auth_result = authenticate_request()
   # if auth_result:
        #return auth_result
    
    data = request.json
    try:
        payment_owner_id = data['payment_owner_id']
        supply_id = data['supply_id']
        count = data['count']
        amount = data['amount']
        
        supply_request = inventory_service.create_supply_request(
            payment_owner_id, supply_id, count, amount,
            request.headers.get('X-API-Key')
        )
        
        return jsonify({
            "id": supply_request.id,
            "payment_owner_id": supply_request.payment_owner_id,
            "supply_id": supply_request.supply_id,
            "count": supply_request.count,
            "amount": float(supply_request.amount)
        }), 201
        
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400