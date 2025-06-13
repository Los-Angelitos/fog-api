from commerce.domain.entities import PaymentOwner, PaymentCustomer, Subscription, ContractOwner

class PaymentCustomerService:
    def __init__(self):
        pass

    @staticmethod
    def create_payment_customer(guest_id: str, final_amount: float) -> PaymentCustomer:
        try:
            final_amount = float(final_amount)

            if final_amount < 0:
                raise ValueError("Final amount must be non-negative")

        except (ValueError, TypeError) as e:
            if "invalid literal" in str(e):
                raise ValueError("Invalid format")
            raise e

        return PaymentCustomer(guest_id, final_amount)

class PaymentOwnerService:
    def __init__(self):
        pass

    @staticmethod
    def create_payment_owner(owner_id: str, description: str, final_amount: float) -> PaymentOwner:
        try:
            final_amount = float(final_amount)

            if final_amount < 0:
                raise ValueError("Final amount must be non-negative")
            if not description.strip():
                raise ValueError("Description cannot be empty")

        except (ValueError, TypeError) as e:
            if "invalid literal" in str(e):
                raise ValueError("Invalid format")
            raise e

        return PaymentOwner(owner_id, description.strip(), final_amount)

class SuscriptionService:
    def __init__(self):
        pass

    @staticmethod
    def create_subscription(name: str, content: str, price: float, status: str) -> Subscription:
        try:
            price = float(price)

            if price < 0:
                raise ValueError("Price must be non-negative")
            if not name.strip():
                raise ValueError("Name cannot be empty")
            if not content.strip():
                raise ValueError("Content cannot be empty")
            if status not in ["active", "inactive"]:
                raise ValueError("Status must be 'active' or 'inactive'")

        except (ValueError, TypeError) as e:
            if "invalid literal" in str(e):
                raise ValueError("Invalid format")
            raise e

        return Subscription(name.strip(), content.strip(), price, status)

class ContractOwnerService:
    def __init__(self):
        pass

    @staticmethod
    def create_contract_owner(owner_id: str, start_date: str, final_date: str, subscription_id: str, status: str) -> ContractOwner:
        try:
            if not start_date.strip() or not final_date.strip():
                raise ValueError("Start date and final date cannot be empty")
            if status not in ["active", "inactive"]:
                raise ValueError("Status must be 'active' or 'inactive'")

        except (ValueError, TypeError) as e:
            if "invalid literal" in str(e):
                raise ValueError("Invalid format")
            raise e

        return ContractOwner(owner_id, start_date.strip(), final_date.strip(), subscription_id, status)