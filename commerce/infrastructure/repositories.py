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
    def add_payment_customer(self, payment_customer):
        session = db.session
        record = PaymentCustomerModel(
            guest_id=payment_customer.guest_id,
            final_amount=payment_customer.final_amount
        )
        session.add(record)
        session.commit()
        return PaymentCustomer(record.guest_id, record.final_amount, record.id)

    def find_all(self):
        session = db.session
        records = session.query(PaymentCustomerModel).all()
        return [PaymentCustomer(r.guest_id, float(r.final_amount), r.id) for r in records]

    def find_by_id(self, payment_customer_id):
        session = db.session
        try:
            r = session.query(PaymentCustomerModel).filter_by(id=payment_customer_id).one()
            return PaymentCustomer(r.guest_id, float(r.final_amount), r.id)
        except NoResultFound:
            return None

    def update_payment_customer(self, payment_customer):
        session = db.session
        try:
            record = session.query(PaymentCustomerModel).filter_by(id=payment_customer.id).one()
            record.guest_id = payment_customer.guest_id
            record.final_amount = payment_customer.final_amount
            session.commit()
            return PaymentCustomer(record.guest_id, float(record.final_amount), record.id)
        except NoResultFound:
            return None

    def get_payment_customer_by_customer_id(self, customer_id):
        session = db.session
        try:
            record = session.query(PaymentCustomerModel).filter_by(guest_id=customer_id).one()
            return PaymentCustomer(record.guest_id, float(record.final_amount), record.id)
        except NoResultFound:
            return None

class PaymentOwnerRepository:
    def add_payment_owner(self, payment_owner):
        session = db.session
        record = PaymentOwnerModel(
            owner_id=payment_owner.owner_id,
            description=payment_owner.description,
            final_amount=payment_owner.final_amount
        )
        session.add(record)
        session.commit()
        return PaymentOwner(record.owner_id, record.description, record.final_amount, record.id)

    def find_all(self):
        session = db.session
        records = session.query(PaymentOwnerModel).all()
        return [PaymentOwner(r.owner_id, r.description, float(r.final_amount), r.id) for r in records]

    def find_by_id(self, payment_owner_id):
        session = db.session
        try:
            r = session.query(PaymentOwnerModel).filter_by(id=payment_owner_id).one()
            return PaymentOwner(r.owner_id, r.description, float(r.final_amount), r.id)
        except NoResultFound:
            return None

    def update_payment_owner(self, payment_owner):
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

    def get_payment_owner_by_owner_id(self, owner_id):
        session = db.session
        try:
            record = session.query(PaymentOwnerModel).filter_by(owner_id=owner_id).one()
            return PaymentOwner(record.owner_id, record.description, float(record.final_amount), record.id)
        except NoResultFound:
            return None

class SubscriptionRepository:
    def add_subscription(self, subscription):
        session = db.session
        record = SubscriptionModel(
            name=subscription.name,
            content=subscription.content,
            price=subscription.price,
            status=subscription.status
        )
        session.add(record)
        session.commit()
        return Subscription(record.name, record.content, record.price, record.status, record.id)

    def find_all(self):
        session = db.session
        records = session.query(SubscriptionModel).all()
        return [Subscription(r.name, r.content, float(r.price), r.status, r.id) for r in records]

    def find_by_id(self, subscription_id):
        session = db.session
        try:
            r = session.query(SubscriptionModel).filter_by(id=subscription_id).one()
            return Subscription(r.name, r.content, float(r.price), r.status, r.id)
        except NoResultFound:
            return None

    def update_subscription(self, subscription):
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

    def get_subscription_by_name(self, name):
        session = db.session
        try:
            record = session.query(SubscriptionModel).filter_by(name=name).one()
            return Subscription(record.name, record.content, float(record.price), record.status, record.id)
        except NoResultFound:
            return None

    def get_subscription_by_status(self, status):
        session = db.session
        records = session.query(SubscriptionModel).filter_by(status=status).all()
        return [Subscription(r.name, r.content, float(r.price), r.status, r.id) for r in records]

class ContractOwnerRepository:
    def add_contract_owner(self, contract_owner):
        session = db.session
        record = ContractOwnerModel(
            owner_id=contract_owner.owner_id,
            start_date=contract_owner.start_date,
            final_date=contract_owner.final_date,
            subscription_id=contract_owner.subscription_id,
            status=contract_owner.status
        )
        session.add(record)
        session.commit()
        return ContractOwner(record.owner_id, record.start_date, record.final_date, record.subscription_id, record.status, record.id)

    def find_all(self):
        session = db.session
        records = session.query(ContractOwnerModel).all()
        return [ContractOwner(r.owner_id, r.start_date, r.final_date, r.subscription_id, r.status, r.id) for r in records]

    def find_by_id(self, contract_owner_id):
        session = db.session
        try:
            r = session.query(ContractOwnerModel).filter_by(id=contract_owner_id).one()
            return ContractOwner(r.owner_id, r.start_date, r.final_date, r.subscription_id, r.status, r.id)
        except NoResultFound:
            return None

    def update_contract_owner(self, contract_owner):
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

    def get_contract_owner_by_owner_id(self, owner_id):
        session = db.session
        try:
            record = session.query(ContractOwnerModel).filter_by(owner_id=owner_id).one()
            return ContractOwner(record.owner_id, record.start_date, record.final_date, record.subscription_id, record.status, record.id)
        except NoResultFound:
            return None

    def get_contract_owner_by_subscription_id(self, subscription_id):
        session = db.session
        try:
            record = session.query(ContractOwnerModel).filter_by(subscription_id=subscription_id).one()
            return ContractOwner(record.owner_id, record.start_date, record.final_date, record.subscription_id, record.status, record.id)
        except NoResultFound:
            return None
