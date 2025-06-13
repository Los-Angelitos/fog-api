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

    def create_payment_customer(self, guest_id: str, final_amount: float):
        payment_customer = self.payment_customer_service.create_payment_customer(
            guest_id, final_amount)
        return self.payment_customer_repository.save(payment_customer)

    def create_payment_owner(self, owner_id: str, description: str, final_amount: float):
        payment_owner = self.payment_owner_service.create_payment_owner(
            owner_id, description, final_amount)
        return self.payment_owner_repository.save(payment_owner)

    def create_subscription(self, name: str, content: str, price: float, status: str):
        subscription = self.subscription_service.create_subscription(
            name, content, price, status)
        return self.subscription_repository.save(subscription)

    def create_contract_owner(self, owner_id: str, start_date: str, final_date: str, subscription_id: str, status: str):
        # Validate subscription exists
        subscription = self.subscription_repository.find_by_id(subscription_id)
        if not subscription:
            raise ValueError("Subscription not found")

        contract_owner = self.contract_owner_service.create_contract_owner(
            owner_id, start_date, final_date, subscription_id, status)
        return self.contract_owner_repository.save(contract_owner)