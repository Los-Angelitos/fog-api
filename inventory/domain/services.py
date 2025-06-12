from decimal import Decimal
from inventory.domain.entities import Supply, SupplyRequest


class SupplyService:
    def __init__(self):
        pass

    @staticmethod
    def create_supply(provider_id: str, name: str, price: float, stock: int, state: str) -> Supply:
        try:
            price = float(price)
            stock = int(stock)
            
            if price < 0:
                raise ValueError("Price must be non-negative")
            if stock < 0:
                raise ValueError("Stock must be non-negative")
            if not name.strip():
                raise ValueError("Name cannot be empty")
            if state not in ["available", "unavailable", "discontinued"]:
                raise ValueError("State must be 'available', 'unavailable', or 'discontinued'")
                
        except (ValueError, TypeError) as e:
            if "invalid literal" in str(e):
                raise ValueError("Invalid price or stock format")
            raise e

        return Supply(provider_id, name.strip(), price, stock, state)


class SupplyRequestService:
    def __init__(self):
        pass

    @staticmethod
    def create_supply_request(payment_owner_id: str, supply_id: int, count: int, amount: float) -> SupplyRequest:
        try:
            supply_id = int(supply_id)
            count = int(count)
            amount = float(amount)
            
            if count <= 0:
                raise ValueError("Count must be greater than 0")
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
                
        except (ValueError, TypeError) as e:
            if "invalid literal" in str(e):
                raise ValueError("Invalid supply_id, count, or amount format")
            raise e

        return SupplyRequest(payment_owner_id, supply_id, count, amount)