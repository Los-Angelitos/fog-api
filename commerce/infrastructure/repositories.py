from typing import Optional

from commerce.infrastructure.models import (
    PaymentCustomer as PaymentCustomerModel,
    PaymentOwner as PaymentOwnerModel,
    Subscription as SubscriptionModel,
    ContractOwner as ContractOwnerModel
)
from commerce.domain.entities import PaymentCustomer, PaymentOwner, Subscription, ContractOwner
from shared.infrastructure.database import db
from sqlalchemy.exc import NoResultFound

class PaymentCustomerRepository:
    def add_payment_customer(self, guest_id: str, final_amount: str) -> Optional[PaymentCustomer]:
        session = db.session
        try:
            payment_customer = PaymentCustomerModel(
                guest_id=guest_id,
                final_amount=final_amount
            )
            session.add(payment_customer)
            session.commit()
            return PaymentCustomer(payment_customer.id, payment_customer.guest_id, payment_customer.final_amount)
        except Exception as e:
            print(f"Error adding payment customer: {e}")
            session.rollback()
            return None

    def find_all(self) -> list[PaymentCustomer]:
        try:
            session = db.session
            result = session.query(PaymentCustomerModel).all()
            return [PaymentCustomer(id=r.id, guest_id=r.guest_id, final_amount=r.final_amount) for r in result]
        except Exception as e:
            print(f"Error fetching payment customers: {e}")
            return []

    def find_by_id(self, payment_customer_id: str) -> Optional[PaymentCustomer]:
        session = db.session
        try:
            record = session.query(PaymentCustomerModel).filter_by(id=payment_customer_id).one()
            return PaymentCustomer(record.id, record.guest_id, float(record.final_amount))
        except NoResultFound:
            return None

    def update_payment_customer(self, payment_customer: PaymentCustomer) -> Optional[PaymentCustomer]:
        session = db.session
        try:
            record = session.query(PaymentCustomerModel).filter_by(id=payment_customer.id).one()
            record.guest_id = payment_customer.guest_id
            record.final_amount = payment_customer.final_amount
            session.commit()
            return PaymentCustomer(record.id, record.guest_id, float(record.final_amount))
        except NoResultFound:
            return None

    def get_payment_customer_by_customer_id(self, guest_id: str) -> Optional[PaymentCustomer]:
        session = db.session
        try:
            record = session.query(PaymentCustomerModel).filter_by(guest_id=guest_id).one()
            return PaymentCustomer(record.id, record.guest_id, float(record.final_amount))
        except NoResultFound:
            return None


class PaymentOwnerRepository:
    def add_payment_owner(self, owner_id: str, description: str, final_amount: str) -> Optional[PaymentOwner]:
        session = db.session
        try:
            payment_owner = PaymentOwnerModel(
                owner_id=owner_id,
                description=description,
                final_amount=final_amount
            )
            session.add(payment_owner)
            session.commit()
            return PaymentOwner(payment_owner.owner_id, payment_owner.description, float(payment_owner.final_amount), payment_owner.id)
        except Exception as e:
            print(f"Error adding payment owner: {e}")
            session.rollback()
            return None

    def find_all(self) -> list[PaymentOwner]:
        session = db.session
        try:
            records = session.query(PaymentOwnerModel).all()
            return [PaymentOwner(r.owner_id, r.description, float(r.final_amount), r.id) for r in records]
        except Exception as e:
            print(f"Error fetching payment owners: {e}")
            return []

    def find_by_id(self, payment_owner_id: str) -> Optional[PaymentOwner]:
        session = db.session
        try:
            record = session.query(PaymentOwnerModel).filter_by(id=payment_owner_id).one()
            return PaymentOwner(record.owner_id, record.description, float(record.final_amount), record.id)
        except NoResultFound:
            return None

    def update_payment_owner(self, payment_owner: PaymentOwner) -> Optional[PaymentOwner]:
        session = db.session
        try:
            record = session.query(PaymentOwnerModel).filter_by(id=payment_owner.id).one()
            record.owner_id = payment_owner.owner_id
            record.description = payment_owner.description
            record.final_amount = payment_owner.final_amount
            session.commit()
            return PaymentOwner(record.owner_id, record.description, float(record.final_amount), record.id)
        except NoResultFound:
            return None

    def get_payment_owner_by_owner_id(self, owner_id: str) -> Optional[PaymentOwner]:
        session = db.session
        try:
            record = session.query(PaymentOwnerModel).filter_by(owner_id=owner_id).one()
            return PaymentOwner(record.owner_id, record.description, float(record.final_amount), record.id)
        except NoResultFound:
            return None


class SubscriptionRepository:
    def add_subscription(self, name: str, content: str, price: float, status: str) -> Optional[Subscription]:
        session = db.session
        try:
            subscription = SubscriptionModel(
                name=name,
                content=content,
                price=price,
                status=status
            )
            session.add(subscription)
            session.commit()
            return Subscription(subscription.name, subscription.content, float(subscription.price), subscription.status, subscription.id)
        except Exception as e:
            print(f"Error adding subscription: {e}")
            session.rollback()
            return None

    def find_all(self) -> list[Subscription]:
        session = db.session
        try:
            records = session.query(SubscriptionModel).all()
            return [Subscription(r.name, r.content, float(r.price), r.status, r.id) for r in records]
        except Exception as e:
            print(f"Error fetching subscriptions: {e}")
            return []

    def find_by_id(self, subscription_id: str) -> Optional[Subscription]:
        session = db.session
        try:
            record = session.query(SubscriptionModel).filter_by(id=subscription_id).one()
            return Subscription(record.name, record.content, float(record.price), record.status, record.id)
        except NoResultFound:
            return None

    def update_subscription(self, subscription: Subscription) -> Optional[Subscription]:
        session = db.session
        try:
            record = session.query(SubscriptionModel).filter_by(id=subscription.id).one()
            record.name = subscription.name
            record.content = subscription.content
            record.price = subscription.price
            record.status = subscription.status
            session.commit()
            return Subscription(record.name, record.content, float(record.price), record.status, record.id)
        except NoResultFound:
            return None

    def get_subscription_by_name(self, name: str) -> list[Subscription]:
        session = db.session
        try:
            records = session.query(SubscriptionModel).filter_by(name=name).all()
            return [Subscription(r.name, r.content, float(r.price), r.status, r.id) for r in records]
        except NoResultFound:
            return []

    def get_subscription_by_status(self, status: str) -> list[Subscription]:
        session = db.session
        try:
            records = session.query(SubscriptionModel).filter_by(status=status).all()
            return [Subscription(r.name, r.content, float(r.price), r.status, r.id) for r in records]
        except NoResultFound:
            return []


class ContractOwnerRepository:
    def add_contract_owner(self, owner_id: str, start_date: str, final_date: str, subscription_id: str, status: str) -> Optional[ContractOwner]:
        session = db.session
        try:
            contract_owner = ContractOwnerModel(
                owner_id=owner_id,
                start_date=start_date,
                final_date=final_date,
                subscription_id=subscription_id,
                status=status
            )
            session.add(contract_owner)
            session.commit()
            return ContractOwner(contract_owner.owner_id, contract_owner.start_date, contract_owner.final_date, contract_owner.subscription_id, contract_owner.status, contract_owner.id)
        except Exception as e:
            print(f"Error adding contract owner: {e}")
            session.rollback()
            return None

    def find_all(self) -> list[ContractOwner]:
        session = db.session
        try:
            records = session.query(ContractOwnerModel).all()
            return [ContractOwner(r.owner_id, r.start_date, r.final_date, r.subscription_id, r.status, r.id) for r in records]
        except Exception as e:
            print(f"Error fetching contract owners: {e}")
            return []

    def find_by_id(self, contract_owner_id: str) -> Optional[ContractOwner]:
        session = db.session
        try:
            record = session.query(ContractOwnerModel).filter_by(id=contract_owner_id).one()
            return ContractOwner(record.owner_id, record.start_date, record.final_date, record.subscription_id, record.status, record.id)
        except NoResultFound:
            return None

    def update_contract_owner(self, contract_owner: ContractOwner) -> Optional[ContractOwner]:
        session = db.session
        try:
            record = session.query(ContractOwnerModel).filter_by(id=contract_owner.id).one()
            record.owner_id = contract_owner.owner_id
            record.start_date = contract_owner.start_date
            record.final_date = contract_owner.final_date
            record.subscription_id = contract_owner.subscription_id
            record.status = contract_owner.status
            session.commit()
            return ContractOwner(record.owner_id, record.start_date, record.final_date, record.subscription_id, record.status, record.id)
        except NoResultFound:
            return None

    def get_contract_owner_by_owner_id(self, owner_id: str) -> list[ContractOwner]:
        session = db.session
        try:
            records = session.query(ContractOwnerModel).filter_by(owner_id=owner_id).all()
            return [ContractOwner(r.owner_id, r.start_date, r.final_date, r.subscription_id, r.status, r.id) for r in records]
        except NoResultFound:
            return []

    def get_contract_owner_by_subscription_id(self, subscription_id: str) -> list[ContractOwner]:
        session = db.session
        try:
            records = session.query(ContractOwnerModel).filter_by(subscription_id=subscription_id).all()
            return [ContractOwner(r.owner_id, r.start_date, r.final_date, r.subscription_id, r.status, r.id) for r in records]
        except NoResultFound:
            return []
