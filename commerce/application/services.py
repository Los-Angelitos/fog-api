from commerce.infrastructure.repositories import PaymentCustomerRepository, PaymentOwnerRepository, SubscriptionRepository, ContractOwnerRepository

class CommerceApplicationService:
    def __init__(self):
        # Initialize repositories
        self.payment_customer_repository = PaymentCustomerRepository()
        self.payment_owner_repository = PaymentOwnerRepository()
        self.subscription_repository = SubscriptionRepository()
        self.contract_owner_repository = ContractOwnerRepository()

    # Payment Customer Methods
    def create_payment_customer(self, data):
        if not data or 'guest_id' not in data or 'final_amount' not in data:
            raise ValueError("Invalid data for payment customer. 'guest_id' and 'final_amount' are required.")

        return self.payment_customer_repository.add_payment_customer(data)

    def get_all_payment_customers(self):
        return self.payment_customer_repository.find_all()

    def get_payment_customer_by_id(self, payment_customer_id):
        payment_customer = self.payment_customer_repository.find_by_id(payment_customer_id)
        if not payment_customer:
            raise ValueError("Payment customer not found")
        return payment_customer

    def update_payment_customer(self, data):
        if not data or 'id' not in data or 'gues_id' not in data or 'final_amount' not in data:
            raise ValueError("Invalid data for payment customer. 'id', 'guest_id' and 'final_amount' are required.")

        payment_customer = self.payment_customer_repository.find_by_id(data['id'])
        if not payment_customer:
            raise ValueError("Payment customer not found")
        payment_customer.guest_id = data['guest_id']
        payment_customer.final_amount = data['final_amount']
        return self.payment_customer_repository.update_payment_customer(payment_customer)

    def get_payment_customer_by_customer_id(self, customer_id):
        payment_customer = self.payment_customer_repository.get_payment_customer_by_customer_id(customer_id)
        if not payment_customer:
            raise ValueError("Payment customer not found")
        return payment_customer


    # Payment Owner Methods
    def create_payment_owner(self, data):
        if not data or 'owner_id' not in data or 'description' not in data or 'final_amount' not in data:
            raise ValueError("Invalid data for payment owner. 'owner_id', 'description', and 'final_amount' are required.")

        return self.payment_owner_repository.add_payment_owner(data)

    def get_all_payment_owners(self):
        return self.payment_owner_repository.find_all()

    def get_payment_owner_by_id(self, payment_owner_id):
        payment_owner = self.payment_owner_repository.find_by_id(payment_owner_id)
        if not payment_owner:
            raise ValueError("Payment owner not found")
        return payment_owner

    def update_payment_owner(self, data):
        if not data or 'id' not in data or 'owner_id' not in data or 'description' not in data or 'final_amount' not in data:
            raise ValueError("Invalid data for payment owner. 'id', 'owner_id', 'description', and 'final_amount' are required.")

        payment_owner = self.payment_owner_repository.find_by_id(data['id'])
        if not payment_owner:
            raise ValueError("Payment owner not found")
        payment_owner.owner_id = data['owner_id']
        payment_owner.description = data['description']
        payment_owner.final_amount = data['final_amount']
        return self.payment_owner_repository.update_payment_owner(payment_owner)

    def get_payment_owner_by_owner_id(self, owner_id):
        payment_owner = self.payment_owner_repository.get_payment_owner_by_owner_id(owner_id)
        if not payment_owner:
            raise ValueError("Payment owner not found")
        return payment_owner


    # Subscription Methods
    def create_subscription(self, data):
        if not data or 'name' not in data or 'content' not in data or 'price' not in data or 'status' not in data:
            raise ValueError("Invalid data for subscription. 'name', 'content', 'price', and 'status' are required.")

        return self.subscription_repository.add_subscription(data)

    def get_all_subscriptions(self):
        return self.subscription_repository.find_all()

    def get_subscription_by_id(self, subscription_id):
        subscription = self.subscription_repository.find_by_id(subscription_id)
        if not subscription:
            raise ValueError("Subscription not found")
        return subscription

    def update_subscription(self, data):
        if not data or 'id' not in data or 'name' not in data or 'content' not in data or 'price' not in data or 'status' not in data:
            raise ValueError("Invalid data for subscription. 'id', 'name', 'content', 'price', and 'status' are required.")

        subscription = self.subscription_repository.find_by_id(data['id'])
        if not subscription:
            raise ValueError("Subscription not found")
        subscription.name = data['name']
        subscription.content = data['content']
        subscription.price = data['price']
        subscription.status = data['status']
        return self.subscription_repository.update_subscription(subscription)

    def get_subscription_by_name(self, name):
        subscription = self.subscription_repository.get_subscription_by_name(name)
        if not subscription:
            raise ValueError("Subscription not found")
        return subscription

    def get_subscription_by_status(self, status):
        subscription = self.subscription_repository.get_subscription_by_status(status)
        if not subscription:
            raise ValueError("Subscription not found")
        return subscription


    # Contract Owner Methods
    def create_contract_owner(self, data):
        if not data or 'owner_id' not in data or 'start_date' not in data or 'final_date' not in data or 'subscription_id' not in data or 'status' not in data:
            raise ValueError("Invalid data for contract owner. 'owner_id', 'start_date', 'final_date', 'subscription_id', and 'status' are required.")

        # Validate subscription exists
        subscription = self.subscription_repository.find_by_id(data['subscription_id'])
        if not subscription:
            raise ValueError("Subscription not found")

        return self.contract_owner_repository.add_contract_owner(data)

    def get_all_contract_owners(self):
        return self.contract_owner_repository.find_all()

    def get_contract_owner_by_id(self, contract_id):
        contract_owner = self.contract_owner_repository.find_by_id(contract_id)
        if not contract_owner:
            raise ValueError("Contract owner not found")
        return contract_owner

    def update_contract_owner(self, data):
        if not data or 'id' not in data or 'owner_id' not in data or 'start_date' not in data or 'final_date' not in data or 'subscription_id' not in data or 'status' not in data:
            raise ValueError("Invalid data for contract owner. 'id', 'owner_id', 'start_date', 'final_date', 'subscription_id', and 'status' are required.")

        contract_owner = self.contract_owner_repository.find_by_id(data['id'])
        if not contract_owner:
            raise ValueError("Contract owner not found")
        contract_owner.owner_id = data['owner_id']
        contract_owner.start_date = data['start_date']
        contract_owner.final_date = data['final_date']
        contract_owner.subscription_id = data['subscription_id']
        contract_owner.status = data['status']
        return self.contract_owner_repository.update_contract_owner(contract_owner)

    def get_contract_owner_by_owner_id(self, owner_id):
        contract_owner = self.contract_owner_repository.get_contract_owner_by_owner_id(owner_id)
        if not contract_owner:
            raise ValueError("Contract owner not found")
        return contract_owner

    def get_contract_owner_by_subscription_id(self, subscription_id):
        contract_owner = self.contract_owner_repository.get_contract_owner_by_subscription_id(subscription_id)
        if not contract_owner:
            raise ValueError("Contract owner not found")
        return contract_owner