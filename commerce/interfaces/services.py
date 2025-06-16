from flasgger import swag_from
from flask import Blueprint, request, jsonify
from commerce.application.services import CommerceApplicationService

commerce = Blueprint('commerce_api', __name__)
commerce_service = CommerceApplicationService()

# Payment Customer Endpoints
@commerce.route('/api/v1/payment-customer', methods=['POST'])
@swag_from({
    'tags': ['Payment Customers']
})
def create_payment_customer():
    """
    Creates a new payment customer with the provided guest ID and final amount.
    ---
    parameters:
      - in: body
        name: payment_customer
        description: Payment customer data
        required: true
        schema:
          type: object
          properties:
            guest_id:
              type: string
              description: The ID of the guest.
              example: "guest123"
            final_amount:
              type: number
              format: float
              description: The final amount for the payment.
              example: 149.99
    responses:
      201:
        description: Payment customer created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the payment customer.
              example: "cust123"
            guest_id:
              type: string
              description: The ID of the guest.
              example: "guest123"
            final_amount:
              type: number
              format: float
              description: The final amount for the payment.
              example: 149.99
      400:
        description: Bad request, missing required fields or invalid data
      404:
        description: Not found, if the guest does not exist
    """
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
    """
    Retrieves all payment customers.
    ---
    responses:
      200:
        description: A list of payment customers
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                description: The ID of the payment customer.
              guest_id:
                type: string
                description: The ID of the guest.
              final_amount:
                type: number
                format: float
                description: The final amount for the payment.
      500:
        description: Internal server error
    """
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
    """
    Retrieves a payment customer by ID.
    ---
    parameters:
      - in: path
        name: payment_customer_id
        type: string
        required: true
        description: The ID of the payment customer.
    responses:
      200:
        description: Payment customer retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the payment customer.
            guest_id:
              type: string
              description: The ID of the guest.
            final_amount:
              type: number
              format: float
              description: The final amount for the payment.
      404:
        description: Payment customer not found
    """
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
    """
    Updates a payment customer by ID.
    ---
    parameters:
      - in: path
        name: payment_customer_id
        type: string
        required: true
        description: The ID of the payment customer.
      - in: body
        name: payment_customer
        description: Payment customer data to update
        required: true
        schema:
          type: object
          properties:
            final_amount:
              type: number
              format: float
              description: The final amount for the payment.
    responses:
      200:
        description: Payment customer updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the payment customer.
            guest_id:
              type: string
              description: The ID of the guest.
            final_amount:
              type: number
              format: float
              description: The final amount for the payment.
      400:
        description: Bad request, missing required fields or invalid data
      404:
        description: Payment customer not found
    """
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
    """
    Retrieves a payment customer by customer ID.
    ---
    parameters:
      - in: path
        name: customer_id
        type: string
        required: true
        description: The ID of the customer.
    responses:
      200:
        description: Payment customer retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the payment customer.
            guest_id:
              type: string
              description: The ID of the guest.
            final_amount:
              type: number
              format: float
              description: The final amount for the payment.
      404:
        description: Payment customer not found
    """
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
    """
    Creates a new payment owner with the provided owner ID, description, and final amount.
    ---
    parameters:
      - in: body
        name: payment_owner
        description: Payment owner data
        required: true
        schema:
          type: object
          properties:
            owner_id:
              type: string
              description: The ID of the owner.
            description:
              type: string
              description: Description of the payment.
            final_amount:
              type: number
              format: float
              description: The final amount for the payment.
    responses:
      201:
        description: Payment owner created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the payment owner.
            owner_id:
              type: string
              description: The ID of the owner.
            description:
              type: string
              description: Description of the payment.
            final_amount:
              type: number
              format: float
              description: The final amount for the payment.
      400:
        description: Bad request, missing required fields or invalid data
      404:
        description: Not found, if the owner does not exist
    """
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
    """
    Retrieves all payment owners.
    ---
    responses:
      200:
        description: A list of payment owners
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                description: The ID of the payment owner.
              owner_id:
                type: string
                description: The ID of the owner.
              description:
                type: string
                description: Description of the payment.
              final_amount:
                type: number
                format: float
                description: The final amount for the payment.
      500:
        description: Internal server error
    """
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
    """
    Retrieves a payment owner by ID.
    ---
    parameters:
      - in: path
        name: payment_owner_id
        required: true
        type: string
        description: The ID of the payment owner.
    responses:
      200:
        description: Payment owner retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the payment owner.
            owner_id:
              type: string
              description: The ID of the owner.
            description:
              type: string
              description: Description of the payment.
            final_amount:
              type: number
              format: float
              description: The final amount for the payment.
      404:
        description: Payment owner not found
    """
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
    """
    Updates a payment owner by ID.
    ---
    parameters:
      - in: path
        name: payment_owner_id
        type: string
        required: true
        description: The ID of the payment owner.
      - in: body
        name: payment_owner
        description: Payment owner data to update
        required: true
        schema:
          type: object
          properties:
            description:
              type: string
              description: Description of the payment.
            final_amount:
              type: number
              format: float
              description: The final amount for the payment.
    responses:
      200:
        description: Payment owner updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the payment owner.
            owner_id:
              type: string
              description: The ID of the owner.
            description:
              type: string
              description: Description of the payment.
            final_amount:
              type: number
              format: float
              description: The final amount for the payment.
      400:
        description: Bad request, missing required fields or invalid data
      404:
        description: Payment owner not found
    """
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
    """
    Retrieves a payment owner by owner ID.
    ---
    parameters:
      - in: path
        name: owner_id
        type: string
        required: true
        description: The ID of the owner.
    responses:
      200:
        description: Payment owner retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the payment owner.
            owner_id:
              type: string
              description: The ID of the owner.
            description:
              type: string
              description: Description of the payment.
            final_amount:
              type: number
              format: float
              description: The final amount for the payment.
      404:
        description: Payment owner not found
    """
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
    """
    Creates a new subscription with the provided name, content, price, and status.
    ---
    parameters:
      - in: body
        name: subscription
        description: Subscription data
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the subscription.
            content:
              type: string
              description: The content of the subscription.
            price:
              type: number
              format: float
              description: The price of the subscription.
            status:
              type: string
              description: The status of the subscription.
    responses:
      201:
        description: Subscription created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the subscription.
            name:
              type: string
              description: The name of the subscription.
            content:
              type: string
              description: The content of the subscription.
            price:
              type: number
              format: float
              description: The price of the subscription.
            status:
              type: string
              description: The status of the subscription.
      400:
        description: Bad request, missing required fields or invalid data
    """
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

@commerce.route('/api/v1/subscription', methods=['GET'])
@swag_from({
    'tags': ['Subscriptions']
})
def get_all_subscriptions():
    """
    Retrieves all subscriptions.
    ---
    responses:
      200:
        description: A list of subscriptions
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                description: The ID of the subscription.
              name:
                type: string
                description: The name of the subscription.
              content:
                type: string
                description: The content of the subscription.
              price:
                type: number
                format: float
                description: The price of the subscription.
              status:
                type: string
                description: The status of the subscription.
      500:
        description: Internal server error
    """
    try:
        subscriptions = commerce_service.get_all_subscriptions()
        return jsonify([{
            "id": sub.id,
            "name": sub.name,
            "content": sub.content,
            "price": float(sub.price),
            "status": sub.status
        } for sub in subscriptions]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@commerce.route('/api/v1/subscription/<string:subscription_id>', methods=['GET'])
@swag_from({
    'tags': ['Subscriptions']
})
def get_subscription_by_id(subscription_id):
    """
    Retrieves a subscription by ID.
    ---
    parameters:
      - in: path
        name: subscription_id
        required: true
        type: string
        description: The ID of the subscription.
    responses:
      200:
        description: Subscription retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the subscription.
            name:
              type: string
              description: The name of the subscription.
            content:
              type: string
              description: The content of the subscription.
            price:
              type: number
              format: float
              description: The price of the subscription.
            status:
              type: string
              description: The status of the subscription.
      404:
        description: Subscription not found
    """
    try:
        subscription = commerce_service.get_subscription_by_id(subscription_id)
        return jsonify({
            "id": subscription.id,
            "name": subscription.name,
            "content": subscription.content,
            "price": float(subscription.price),
            "status": subscription.status
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@commerce.route('/api/v1/subscription/<string:subscription_id>', methods=['PUT'])
@swag_from({
    'tags': ['Subscriptions']
})
def update_subscription(subscription_id):
    """
    Updates a subscription by ID.
    ---
    parameters:
      - in: path
        name: subscription_id
        required: true
        type: string
        description: The ID of the subscription.
      - in: body
        name: subscription
        required: true
        description: Subscription data to update
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the subscription.
            content:
              type: string
              description: The content of the subscription.
            price:
              type: number
              format: float
              description: The price of the subscription.
            status:
              type: string
              description: The status of the subscription.
    responses:
      200:
        description: Subscription updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the subscription.
            name:
              type: string
              description: The name of the subscription.
            content:
              type: string
              description: The content of the subscription.
            price:
              type: number
              format: float
              description: The price of the subscription.
            status:
              type: string
              description: The status of the subscription.
      400:
        description: Bad request, missing required fields or invalid data
      404:
        description: Subscription not found
    """
    data = request.json
    try:
        name = data['name']
        content = data['content']
        price = data['price']
        status = data['status']

        subscription = commerce_service.update_subscription(
            subscription_id, name, content, price, status,
            request.headers.get('X-API-Key')
        )

        return jsonify({
            "id": subscription.id,
            "name": subscription.name,
            "content": subscription.content,
            "price": float(subscription.price),
            "status": subscription.status
        }), 200

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@commerce.route('/api/v1/subscription/by-name/<string:name>', methods=['GET'])
@swag_from({
    'tags': ['Subscriptions']
})
def get_subscription_by_name(name):
    """
    Retrieves a subscription by name.
    ---
    parameters:
      - in: path
        name: name
        required: true
        type: string
        description: The name of the subscription.
    responses:
      200:
        description: Subscription retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the subscription.
            name:
              type: string
              description: The name of the subscription.
            content:
              type: string
              description: The content of the subscription.
            price:
              type: number
              format: float
              description: The price of the subscription.
            status:
              type: string
              description: The status of the subscription.
      404:
        description: Subscription not found
    """
    try:
        subscription = commerce_service.get_subscription_by_name(name)
        return jsonify({
            "id": subscription.id,
            "name": subscription.name,
            "content": subscription.content,
            "price": float(subscription.price),
            "status": subscription.status
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@commerce.route('/api/v1/subscription/by-status/<string:status>', methods=['GET'])
@swag_from({
    'tags': ['Subscriptions']
})
def get_subscription_by_status(status):
    """
    Retrieves subscriptions by status.
    ---
    parameters:
      - in: path
        name: status
        required: true
        type: string
        description: The status of the subscriptions.
    responses:
      200:
        description: Subscriptions retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                description: The ID of the subscription.
              name:
                type: string
                description: The name of the subscription.
              content:
                type: string
                description: The content of the subscription.
              price:
                type: number
                format: float
                description: The price of the subscription.
              status:
                type: string
                description: The status of the subscription.
      404:
        description: Subscriptions not found for the given status
    """
    try:
        subscriptions = commerce_service.get_subscription_by_status(status)
        return jsonify([{
            "id": sub.id,
            "name": sub.name,
            "content": sub.content,
            "price": float(sub.price),
            "status": sub.status
        } for sub in subscriptions]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# Contract Owner Endpoints
@commerce.route('/api/v1/contract-owner', methods=['POST'])
@swag_from({
    'tags': ['Contract Owners']
})
def create_contract_owner():
    """
    Creates a new contract owner with the provided owner ID, start date, final date, subscription ID, and status.
    ---
    parameters:
      - in: body
        name: contract_owner
        description: Contract owner data
        required: true
        schema:
          type: object
          properties:
            owner_id:
              type: string
              description: The ID of the owner.
            start_date:
              type: string
              format: date
              description: The start date of the contract.
            final_date:
              type: string
              format: date
              description: The final date of the contract.
            subscription_id:
              type: string
              description: The ID of the subscription.
            status:
              type: string
              description: The status of the contract.
    responses:
      201:
        description: Contract owner created successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the contract owner.
            owner_id:
              type: string
              description: The ID of the owner.
            start_date:
              type: string
              format: date
              description: The start date of the contract.
            final_date:
              type: string
              format: date
              description: The final date of the contract.
            subscription_id:
              type: string
              description: The ID of the subscription.
            status:
              type: string
              description: The status of the contract.
      400:
        description: Bad request, missing required fields or invalid data
    """
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

@commerce.route('/api/v1/contract-owner', methods=['GET'])
@swag_from({
    'tags': ['Contract Owners']
})
def get_all_contract_owners():
    """
    Retrieves all contract owners.
    ---
    responses:
      200:
        description: A list of contract owners
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                description: The ID of the contract owner.
              owner_id:
                type: string
                description: The ID of the owner.
              start_date:
                type: string
                format: date
                description: The start date of the contract.
              final_date:
                type: string
                format: date
                description: The final date of the contract.
              subscription_id:
                type: string
                description: The ID of the subscription.
              status:
                type: string
                description: The status of the contract.
      500:
        description: Internal server error
    """
    try:
        contract_owners = commerce_service.get_all_contract_owners()
        return jsonify([{
            "id": co.id,
            "owner_id": co.owner_id,
            "start_date": co.start_date,
            "final_date": co.final_date,
            "subscription_id": co.subscription_id,
            "status": co.status
        } for co in contract_owners]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@commerce.route('/api/v1/contract-owner/<string:contract_owner_id>', methods=['GET'])
@swag_from({
    'tags': ['Contract Owners']
})
def get_contract_owner_by_id(contract_owner_id):
    """
    Retrieves a contract owner by ID.
    ---
    parameters:
      - name: contract_owner_id
        in: path
        required: true
        type: string
        description: The ID of the contract owner.
    responses:
      200:
        description: Contract owner retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the contract owner.
            owner_id:
              type: string
              description: The ID of the owner.
            start_date:
              type: string
              format: date
              description: The start date of the contract.
            final_date:
              type: string
              format: date
              description: The final date of the contract.
            subscription_id:
              type: string
              description: The ID of the subscription.
            status:
              type: string
              description: The status of the contract.
      404:
        description: Contract owner not found
    """
    try:
        contract_owner = commerce_service.get_contract_owner_by_id(contract_owner_id)
        return jsonify({
            "id": contract_owner.id,
            "owner_id": contract_owner.owner_id,
            "start_date": contract_owner.start_date,
            "final_date": contract_owner.final_date,
            "subscription_id": contract_owner.subscription_id,
            "status": contract_owner.status
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@commerce.route('/api/v1/contract-owner/<string:contract_owner_id>', methods=['PUT'])
@swag_from({
    'tags': ['Contract Owners']
})
def update_contract_owner(contract_owner_id):
    """
    Updates a contract owner by ID.
    ---
    parameters:
      - name: contract_owner_id
        in: path
        required: true
        type: string
        description: The ID of the contract owner.
      - name: body
        in: body
        required: true
        description: Contract owner data to update
        schema:
          type: object
          required:
            - start_date
            - final_date
            - subscription_id
            - status
          properties:
            start_date:
              type: string
              format: date
              description: The start date of the contract.
            final_date:
              type: string
              format: date
              description: The final date of the contract.
            subscription_id:
              type: string
              description: The ID of the subscription.
            status:
              type: string
              description: The status of the contract.
    responses:
      200:
        description: Contract owner updated successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the contract owner.
            owner_id:
              type: string
              description: The ID of the owner.
            start_date:
              type: string
              format: date
              description: The start date of the contract.
            final_date:
              type: string
              format: date
              description: The final date of the contract.
            subscription_id:
              type: string
              description: The ID of the subscription.
            status:
              type: string
              description: The status of the contract.
      400:
        description: Bad request, missing required fields or invalid data
      404:
        description: Contract owner not found
    """
    data = request.json
    try:
        start_date = data['start_date']
        final_date = data['final_date']
        subscription_id = data['subscription_id']
        status = data['status']

        contract_owner = commerce_service.update_contract_owner(
            contract_owner_id, start_date, final_date, subscription_id, status,
            request.headers.get('X-API-Key')
        )

        return jsonify({
            "id": contract_owner.id,
            "owner_id": contract_owner.owner_id,
            "start_date": contract_owner.start_date,
            "final_date": contract_owner.final_date,
            "subscription_id": contract_owner.subscription_id,
            "status": contract_owner.status
        }), 200

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@commerce.route('/api/v1/contract-owner/by-owner/<string:owner_id>', methods=['GET'])
@swag_from({
    'tags': ['Contract Owners']
})
def get_contract_owner_by_owner_id(owner_id):
    """
    Retrieves a contract owner by owner ID.
    ---
    parameters:
      - name: owner_id
        in: path
        required: true
        type: string
        description: The ID of the owner.
    responses:
      200:
        description: Contract owner retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the contract owner.
            owner_id:
              type: string
              description: The ID of the owner.
            start_date:
              type: string
              format: date
              description: The start date of the contract.
            final_date:
              type: string
              format: date
              description: The final date of the contract.
            subscription_id:
              type: string
              description: The ID of the subscription.
            status:
              type: string
              description: The status of the contract.
      404:
        description: Contract owner not found
    """
    try:
        contract_owner = commerce_service.get_contract_owner_by_owner_id(owner_id)
        return jsonify({
            "id": contract_owner.id,
            "owner_id": contract_owner.owner_id,
            "start_date": contract_owner.start_date,
            "final_date": contract_owner.final_date,
            "subscription_id": contract_owner.subscription_id,
            "status": contract_owner.status
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@commerce.route('/api/v1/contract-owner/by-subscription/<string:subscription_id>', methods=['GET'])
@swag_from({
    'tags': ['Contract Owners']
})
def get_contract_owner_by_subscription_id(subscription_id):
    """
    Retrieves a contract owner by subscription ID.
    ---
    parameters:
      - name: subscription_id
        in: path
        required: true
        type: string
        description: The ID of the subscription.
    responses:
      200:
        description: Contract owner retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the contract owner.
            owner_id:
              type: string
              description: The ID of the owner.
            start_date:
              type: string
              format: date
              description: The start date of the contract.
            final_date:
              type: string
              format: date
              description: The final date of the contract.
            subscription_id:
              type: string
              description: The ID of the subscription.
            status:
              type: string
              description: The status of the contract.
      404:
        description: Contract owner not found
    """
    try:
        contract_owner = commerce_service.get_contract_owner_by_subscription_id(subscription_id)
        return jsonify({
            "id": contract_owner.id,
            "owner_id": contract_owner.owner_id,
            "start_date": contract_owner.start_date,
            "final_date": contract_owner.final_date,
            "subscription_id": contract_owner.subscription_id,
            "status": contract_owner.status
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
