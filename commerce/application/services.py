from commerce.domain.services import PaymentCustomerService, PaymentOwnerService, SuscriptionService, ContractOwnerService
from commerce.infrastructure.repositories import PaymentCustomerRepository, PaymentOwnerRepository, SubscriptionRepository, ContractOwnerRepository

class CommerceApplicationService:
    def __init__(self):
        # Initialize services
        self.payment_customer_service = PaymentCustomerService()
        self.payment_owner_service = PaymentOwnerService()
        self.subscription_service = SuscriptionService()
        self.contract_owner_service = ContractOwnerService()
        # Initialize repositories
        self.payment_customer_repository = PaymentCustomerRepository()
        self.payment_owner_repository = PaymentOwnerRepository()
        self.subscription_repository = SubscriptionRepository()
        self.contract_owner_repository = ContractOwnerRepository()

    # Payment Customer Methods
    def create_payment_customer(self, guest_id: str, final_amount: float, api_key: str):
        # Validate API key
        if not self.iam_service.get_device_by_id_and_api_key(guest_id, api_key):
            raise ValueError("Provider not found or Invalid API key")

        payment_customer = self.payment_customer_service.create_payment_customer(
            guest_id, final_amount)
        return self.payment_customer_repository.add_payment_customer(payment_customer)

    def get_all_payment_customers(self):
        return self.payment_customer_repository.find_all()

    def get_payment_customer_by_id(self, customer_id: str):
        payment_customer = self.payment_customer_repository.find_by_id(customer_id)
        if not payment_customer:
            raise ValueError("Payment customer not found")
        return payment_customer

    def update_payment_customer(self, customer_id: str, final_amount: float, api_key: str):
        # Validate API key
        if not self.iam_service.get_device_by_id_and_api_key(customer_id, api_key):
            raise ValueError("Provider not found or Invalid API key")

        payment_customer = self.payment_customer_repository.find_by_id(customer_id)
        if not payment_customer:
            raise ValueError("Payment customer not found")

        payment_customer.final_amount = final_amount
        return self.payment_customer_repository.update_payment_customer(payment_customer)

    def get_payment_customer_by_customer_id(self, guest_id: str):
        payment_customer = self.payment_customer_repository.get_payment_customer_by_customer_id(guest_id)
        if not payment_customer:
            raise ValueError("Payment customer not found")
        return payment_customer

    # Payment Owner Methods
    def create_payment_owner(self, owner_id: str, description: str, final_amount: float, api_key: str):
        # Validate API key
        if not self.iam_service.get_device_by_id_and_api_key(owner_id, api_key):
            raise ValueError("Provider not found or Invalid API key")

        payment_owner = self.payment_owner_service.create_payment_owner(
            owner_id, description, final_amount)
        return self.payment_owner_repository.add_payment_owner(payment_owner)

    def get_all_payment_owners(self):
        return self.payment_owner_repository.find_all()

    def get_payment_owner_by_id(self, owner_id: str):
        payment_owner = self.payment_owner_repository.find_by_id(owner_id)
        if not payment_owner:
            raise ValueError("Payment owner not found")
        return payment_owner

    def update_payment_owner(self, owner_id: str, description: str, final_amount: float, api_key: str):
        # Validate API key
        if not self.iam_service.get_device_by_id_and_api_key(owner_id, api_key):
            raise ValueError("Provider not found or Invalid API key")

        payment_owner = self.payment_owner_repository.find_by_id(owner_id)
        if not payment_owner:
            raise ValueError("Payment owner not found")

        payment_owner.description = description
        payment_owner.final_amount = final_amount
        return self.payment_owner_repository.update_payment_owner(payment_owner)

    def get_payment_owner_by_owner_id(self, owner_id: str):
        payment_owner = self.payment_owner_repository.get_payment_owner_by_owner_id(owner_id)
        if not payment_owner:
            raise ValueError("Payment owner not found")
        return payment_owner


    # Subscription Methods
    def create_subscription(self, name: str, content: str, price: float, status: str, api_key: str):
        # Validate API key
        if not self.iam_service.get_device_by_id_and_api_key(api_key):
            raise ValueError("Provider not found or Invalid API key")

        subscription = self.subscription_service.create_subscription(
            name, content, price, status)
        return self.subscription_repository.add_subscription(subscription)

    def get_all_subscriptions(self):
        return self.subscription_repository.find_all()

    def get_subscription_by_id(self, subscription_id: str):
        subscription = self.subscription_repository.find_by_id(subscription_id)
        if not subscription:
            raise ValueError("Subscription not found")
        return subscription

    def update_subscription(self, subscription_id: str, name: str, content: str, price: float, status: str, api_key: str):
        # Validate API key
        if not self.iam_service.get_device_by_id_and_api_key(subscription_id, api_key):
            raise ValueError("Provider not found or Invalid API key")

        subscription = self.subscription_repository.find_by_id(subscription_id)
        if not subscription:
            raise ValueError("Subscription not found")

        subscription.name = name
        subscription.content = content
        subscription.price = price
        subscription.status = status
        return self.subscription_repository.update_subscription(subscription)

    def get_subscription_by_name(self, name: str):
        subscription = self.subscription_repository.get_subscription_by_name(name)
        if not subscription:
            raise ValueError("Subscription not found")
        return subscription

    def get_subscription_by_status(self, status: str):
        subscriptions = self.subscription_repository.get_subscription_by_status(status)
        if not subscriptions:
            raise ValueError("No subscriptions found with the given status")
        return subscriptions


    # Contract Owner Methods
    def create_contract_owner(self, owner_id: str, start_date: str, final_date: str,
                              subscription_id: str, status: str, api_key: str):
        # Validate API key
        if not self.iam_service.get_device_by_id_and_api_key(owner_id, subscription_id, api_key):
            raise ValueError("Provider not found or Invalid API key")

        # Validate subscription exists
        subscription = self.subscription_repository.find_by_id(subscription_id)
        if not subscription:
            raise ValueError("Subscription not found")

        contract_owner = self.contract_owner_service.create_contract_owner(
            owner_id, start_date, final_date, subscription_id, status)
        return self.contract_owner_repository.add_contract_owner(contract_owner)

    def get_all_contract_owners(self):
        return self.contract_owner_repository.find_all()

    def get_contract_owner_by_id(self, contract_id: str):
        contract_owner = self.contract_owner_repository.find_by_id(contract_id)
        if not contract_owner:
            raise ValueError("Contract owner not found")
        return contract_owner

    def update_contract_owner(self, contract_id: str, start_date: str, final_date: str,
                                subscription_id: str, status: str, api_key: str):
            # Validate API key
            if not self.iam_service.get_device_by_id_and_api_key(contract_id, api_key):
                raise ValueError("Provider not found or Invalid API key")

            contract_owner = self.contract_owner_repository.find_by_id(contract_id)
            if not contract_owner:
                raise ValueError("Contract owner not found")

            # Validate subscription exists
            subscription = self.subscription_repository.find_by_id(subscription_id)
            if not subscription:
                raise ValueError("Subscription not found")

            contract_owner.start_date = start_date
            contract_owner.final_date = final_date
            contract_owner.subscription_id = subscription_id
            contract_owner.status = status
            return self.contract_owner_repository.update_contract_owner(contract_owner)

    def get_contract_owner_by_owner_id(self, owner_id: str):
        contract_owner = self.contract_owner_repository.get_contract_owner_by_owner_id(owner_id)
        if not contract_owner:
            raise ValueError("Contract owner not found")
        return contract_owner

    def get_contract_owner_by_subscription_id(self, subscription_id: str):
        contract_owner = self.contract_owner_repository.get_contract_owner_by_subscription_id(subscription_id)
        if not contract_owner:
            raise ValueError("Contract owner not found")
        return contract_owner