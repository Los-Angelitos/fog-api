from flasgger import swag_from
from flask import Blueprint, request, jsonify
from commerce.application.services import CommerceApplicationService

commerce = Blueprint('commerce', __name__)
commerce_service = CommerceApplicationService()

@commerce.route('/api/v1/payment-customers', methods=['POST'])
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

@commerce.route('/api/v1/payment-owners', methods=['POST'])
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

@commerce.route('/api/v1/subscriptions', methods=['POST'])
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

@commerce.route('/api/v1/contract-owners', methods=['POST'])
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