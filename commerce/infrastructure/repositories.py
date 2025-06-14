from commerce.infrastructure.models import PaymentCustomer as PaymentCustomerModel, PaymentOwner as PaymentOwnerModel, Subscription as SubscriptionModel, ContractOwner as ContractOwnerModel
from commerce.domain.entities import PaymentCustomer, PaymentOwner, Subscription, ContractOwner

class PaymentCustomerRepository:
    def add_payment_customer(self, payment_customer):
        record = PaymentCustomerModel.create(
            guest_id=payment_customer.guest_id,
            final_amount=payment_customer.final_amount
        )
        return PaymentCustomer(
            payment_customer.guest_id,
            payment_customer.final_amount,
            record.id
        )

    def find_all(self):
        records = PaymentCustomerModel.select()
        return [
            PaymentCustomer(
                record.guest_id,
                float(record.final_amount),
                record.id
            ) for record in records
        ]

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

    def update_payment_customer(self, payment_customer):
        try:
            record = PaymentCustomerModel.get(PaymentCustomerModel.id == payment_customer.id)
            record.guest_id = payment_customer.guest_id
            record.final_amount = payment_customer.final_amount
            record.save()
            return PaymentCustomer(
                record.guest_id,
                float(record.final_amount),
                record.id
            )
        except PaymentCustomerModel.DoesNotExist:
            return None

    def get_payment_customer_by_customer_id(self, customer_id):
        try:
            record = PaymentCustomerModel.get(PaymentCustomerModel.guest_id == customer_id)
            return PaymentCustomer(
                record.guest_id,
                float(record.final_amount),
                record.id
            )
        except PaymentCustomerModel.DoesNotExist:
            return None

class PaymentOwnerRepository:
    def add_payment_owner(self, payment_owner):
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

    def find_all(self):
        records = PaymentOwnerModel.select()
        return [
            PaymentOwner(
                record.owner_id,
                record.description,
                float(record.final_amount),
                record.id
            ) for record in records
        ]

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

    def update_payment_owner(self, payment_owner):
        try:
            record = PaymentOwnerModel.get(PaymentOwnerModel.id == payment_owner.id)
            record.owner_id = payment_owner.owner_id
            record.description = payment_owner.description
            record.final_amount = payment_owner.final_amount
            record.save()
            return PaymentOwner(
                record.owner_id,
                record.description,
                float(record.final_amount),
                record.id
            )
        except PaymentOwnerModel.DoesNotExist:
            return None

    def get_payment_owner_by_owner_id(self, owner_id):
        try:
            record = PaymentOwnerModel.get(PaymentOwnerModel.owner_id == owner_id)
            return PaymentOwner(
                record.owner_id,
                record.description,
                float(record.final_amount),
                record.id
            )
        except PaymentOwnerModel.DoesNotExist:
            return None

class SubscriptionRepository:
    def add_subscription(self, subscription):
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

    def find_all(self):
        records = SubscriptionModel.select()
        return [
            Subscription(
                record.name,
                record.content,
                float(record.price),
                record.status,
                record.id
            ) for record in records
        ]

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

    def update_subscription(self, subscription):
        try:
            record = SubscriptionModel.get(SubscriptionModel.id == subscription.id)
            record.name = subscription.name
            record.content = subscription.content
            record.price = subscription.price
            record.status = subscription.status
            record.save()
            return Subscription(
                record.name,
                record.content,
                float(record.price),
                record.status,
                record.id
            )
        except SubscriptionModel.DoesNotExist:
            return None

    def get_subscription_by_name(self, name):
        try:
            record = SubscriptionModel.get(SubscriptionModel.name == name)
            return Subscription(
                record.name,
                record.content,
                float(record.price),
                record.status,
                record.id
            )
        except SubscriptionModel.DoesNotExist:
            return None

    def get_subscription_by_status(self, status):
        records = SubscriptionModel.select().where(SubscriptionModel.status == status)
        return [
            Subscription(
                record.name,
                record.content,
                float(record.price),
                record.status,
                record.id
            ) for record in records
        ]

class ContractOwnerRepository:
    def add_contract_owner(self, contract_owner):
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

    def find_all(self):
        records = ContractOwnerModel.select()
        return [
            ContractOwner(
                record.owner_id,
                record.start_date,
                record.final_date,
                record.subscription_id,
                record.status,
                record.id
            ) for record in records
        ]

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

    def update_contract_owner(self, contract_owner):
        try:
            record = ContractOwnerModel.get(ContractOwnerModel.id == contract_owner.id)
            record.owner_id = contract_owner.owner_id
            record.start_date = contract_owner.start_date
            record.final_date = contract_owner.final_date
            record.subscription_id = contract_owner.subscription_id
            record.status = contract_owner.status
            record.save()
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

    def get_contract_owner_by_owner_id(self, owner_id):
        try:
            record = ContractOwnerModel.get(ContractOwnerModel.owner_id == owner_id)
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

    def get_contract_owner_by_subscription_id(self, subscription_id):
        try:
            record = ContractOwnerModel.get(ContractOwnerModel.subscription_id == subscription_id)
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