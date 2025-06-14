from flasgger import swag_from
from flask import Blueprint, request, jsonify
from commerce.application.services import CommerceApplicationService

commerce = Blueprint('commerce', __name__)
commerce_service = CommerceApplicationService()

# Payment Customer Endpoints
@commerce.route('/api/v1/payment-customer', methods=['POST'])
@swag_from({
    'tags': ['Payment Customers']
})
def create_payment_customer():
    data = request.json
    try:
        guest_id = data['guest_id']
        final_amount = data['final_amount']

        payment_customer = commerce_service.create_payment_customer(
            guest_id, final_amount,
            request.headers.get('X-API-Key')
        )

        return jsonify({
            "id": payment_customer.id,
            "guest_id": payment_customer.guest_id,
            "final_amount": float(payment_customer.final_amount)
        }), 201

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@commerce.route('/api/v1/payment-customer', methods=['GET'])
@swag_from({
    'tags': ['Payment Customers']
})
def get_all_payment_customers():
    try:
        payment_customers = commerce_service.get_all_payment_customers()
        return jsonify([{
            "id": pc.id,
            "guest_id": pc.guest_id,
            "final_amount": float(pc.final_amount)
        } for pc in payment_customers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@commerce.route('/api/v1/payment-customer/<string:payment_customer_id>', methods=['GET'])
@swag_from({
    'tags': ['Payment Customers']
})
def get_payment_customer_by_id(payment_customer_id):
    try:
        payment_customer = commerce_service.get_payment_customer_by_id(payment_customer_id)
        return jsonify({
            "id": payment_customer.id,
            "guest_id": payment_customer.guest_id,
            "final_amount": float(payment_customer.final_amount)
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@commerce.route('/api/v1/payment-customer/<string:payment_customer_id>', methods=['PUT'])
@swag_from({
    'tags': ['Payment Customers']
})
def update_payment_customer(payment_customer_id):
    data = request.json
    try:
        final_amount = data['final_amount']

        payment_customer = commerce_service.update_payment_customer(
            payment_customer_id, final_amount,
            request.headers.get('X-API-Key')
        )

        return jsonify({
            "id": payment_customer.id,
            "guest_id": payment_customer.guest_id,
            "final_amount": float(payment_customer.final_amount)
        }), 200

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@commerce.route('/api/v1/payment-customer/by-customer/<string:customer_id>', methods=['GET'])
@swag_from({
    'tags': ['Payment Customers']
})
def get_payment_customer_by_customer_id(customer_id):
    try:
        payment_customer = commerce_service.get_payment_customer_by_customer_id(customer_id)
        return jsonify({
            "id": payment_customer.id,
            "guest_id": payment_customer.guest_id,
            "final_amount": float(payment_customer.final_amount)
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# Payment Owner Endpoints
@commerce.route('/api/v1/payment-owner', methods=['POST'])
@swag_from({
    'tags': ['Payment Owners']
})
def create_payment_owner():
    data = request.json
    try:
        owner_id = data['owner_id']
        description = data['description']
        final_amount = data['final_amount']

        payment_owner = commerce_service.create_payment_owner(
            owner_id, description, final_amount,
            request.headers.get('X-API-Key')
        )

        return jsonify({
            "id": payment_owner.id,
            "owner_id": payment_owner.owner_id,
            "description": payment_owner.description,
            "final_amount": float(payment_owner.final_amount)
        }), 201

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@commerce.route('/api/v1/payment-owner', methods=['GET'])
@swag_from({
    'tags': ['Payment Owners']
})
def get_all_payment_owners():
    try:
        payment_owners = commerce_service.get_all_payment_owners()
        return jsonify([{
            "id": po.id,
            "owner_id": po.owner_id,
            "description": po.description,
            "final_amount": float(po.final_amount)
        } for po in payment_owners]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@commerce.route('/api/v1/payment-owner/<string:payment_owner_id>', methods=['GET'])
@swag_from({
    'tags': ['Payment Owners']
})
def get_payment_owner_by_id(payment_owner_id):
    try:
        payment_owner = commerce_service.get_payment_owner_by_id(payment_owner_id)
        return jsonify({
            "id": payment_owner.id,
            "owner_id": payment_owner.owner_id,
            "description": payment_owner.description,
            "final_amount": float(payment_owner.final_amount)
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@commerce.route('/api/v1/payment-owner/<string:payment_owner_id>', methods=['PUT'])
@swag_from({
    'tags': ['Payment Owners']
})
def update_payment_owner(payment_owner_id):
    data = request.json
    try:
        description = data['description']
        final_amount = data['final_amount']

        payment_owner = commerce_service.update_payment_owner(
            payment_owner_id, description, final_amount,
            request.headers.get('X-API-Key')
        )

        return jsonify({
            "id": payment_owner.id,
            "owner_id": payment_owner.owner_id,
            "description": payment_owner.description,
            "final_amount": float(payment_owner.final_amount)
        }), 200

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@commerce.route('/api/v1/payment-owner/by-owner/<string:owner_id>', methods=['GET'])
@swag_from({
    'tags': ['Payment Owners']
})
def get_payment_owner_by_owner_id(owner_id):
    try:
        payment_owner = commerce_service.get_payment_owner_by_owner_id(owner_id)
        return jsonify({
            "id": payment_owner.id,
            "owner_id": payment_owner.owner_id,
            "description": payment_owner.description,
            "final_amount": float(payment_owner.final_amount)
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# Subscription Endpoints
@commerce.route('/api/v1/subscription', methods=['POST'])
@swag_from({
    'tags': ['Subscriptions']
})
def create_subscription():
    data = request.json
    try:
        name = data['name']
        content = data['content']
        price = data['price']
        status = data['status']

        subscription = commerce_service.create_subscription(
            name, content, price, status,
            request.headers.get('X-API-Key')
        )

        return jsonify({
            "id": subscription.id,
            "name": subscription.name,
            "content": subscription.content,
            "price": float(subscription.price),
            "status": subscription.status
        }), 201

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400



# Contract Owner Endpoints
@commerce.route('/api/v1/contract-owner', methods=['POST'])
@swag_from({
    'tags': ['Contract Owners']
})
def create_contract_owner():
    data = request.json
    try:
        owner_id = data['owner_id']
        start_date = data['start_date']
        final_date = data['final_date']
        subscription_id = data['subscription_id']
        status = data['status']

        contract_owner = commerce_service.create_contract_owner(
            owner_id, start_date, final_date, subscription_id, status,
            request.headers.get('X-API-Key')
        )

        return jsonify({
            "id": contract_owner.id,
            "owner_id": contract_owner.owner_id,
            "start_date": contract_owner.start_date,
            "final_date": contract_owner.final_date,
            "subscription_id": contract_owner.subscription_id,
            "status": contract_owner.status
        }), 201

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400