from commerce.infrastructure.models import PaymentCustomer as PaymentCustomerModel, PaymentOwner as PaymentOwnerModel, Subscription as SubscriptionModel, ContractOwner as ContractOwnerModel
from commerce.domain.entities import PaymentCustomer, PaymentOwner, Subscription, ContractOwner

class PaymentCustomerRepository:
    def save(self, payment_customer):
        record = PaymentCustomerModel.create(
            guest_id=payment_customer.guest_id,
            final_amount=payment_customer.final_amount
        )
        return PaymentCustomer(
            payment_customer.guest_id,
            payment_customer.final_amount,
            record.id
        )

    def find_by_id(self, payment_customer_id):
        try:
            record = PaymentCustomerModel.get(PaymentCustomerModel.id == payment_customer_id)
            return PaymentCustomer(
                record.guest_id,
                float(record.final_amount),
                record.id
            )
        except PaymentCustomerModel.DoesNotExist:
            return None

class PaymentOwnerRepository:
    def save(self, payment_owner):
        record = PaymentOwnerModel.create(
            owner_id=payment_owner.owner_id,
            description=payment_owner.description,
            final_amount=payment_owner.final_amount
        )
        return PaymentOwner(
            payment_owner.owner_id,
            payment_owner.description,
            payment_owner.final_amount,
            record.id
        )

    def find_by_id(self, payment_owner_id):
        try:
            record = PaymentOwnerModel.get(PaymentOwnerModel.id == payment_owner_id)
            return PaymentOwner(
                record.owner_id,
                record.description,
                float(record.final_amount),
                record.id
            )
        except PaymentOwnerModel.DoesNotExist:
            return None

class SubscriptionRepository:
    def save(self, subscription):
        record = SubscriptionModel.create(
            name=subscription.name,
            content=subscription.content,
            price=subscription.price,
            status=subscription.status
        )
        return Subscription(
            subscription.name,
            subscription.content,
            subscription.price,
            subscription.status,
            record.id
        )

    def find_by_id(self, subscription_id):
        try:
            record = SubscriptionModel.get(SubscriptionModel.id == subscription_id)
            return Subscription(
                record.name,
                record.content,
                float(record.price),
                record.status,
                record.id
            )
        except SubscriptionModel.DoesNotExist:
            return None

class ContractOwnerRepository:
    def save(self, contract_owner):
        record = ContractOwnerModel.create(
            owner_id=contract_owner.owner_id,
            start_date=contract_owner.start_date,
            final_date=contract_owner.final_date,
            subscription_id=contract_owner.subscription_id,
            status=contract_owner.status
        )
        return ContractOwner(
            contract_owner.owner_id,
            contract_owner.start_date,
            contract_owner.final_date,
            contract_owner.subscription_id,
            contract_owner.status,
            record.id
        )

    def find_by_id(self, contract_owner_id):
        try:
            record = ContractOwnerModel.get(ContractOwnerModel.id == contract_owner_id)
            return ContractOwner(
                record.owner_id,
                record.start_date,
                record.final_date,
                record.subscription_id,
                record.status,
                record.id
            )
        except ContractOwnerModel.DoesNotExist:
            return None