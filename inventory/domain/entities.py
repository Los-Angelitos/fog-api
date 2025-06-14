class Supply:
    def __init__(self, id: int, provider_id: int, hotel_id: int, name: str, price: float, stock: int, state: str):
        self.id = id
        self.provider_id = provider_id
        self.hotel_id = hotel_id
        self.name = name
        self.price = price
        self.stock = stock
        self.state = state
    
    def to_dict(self):
        return {
            "id": self.id,
            "provider_id": self.provider_id,
            "hotel_id": self.hotel_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "state": self.state
        }

class SupplyRequest:
    def __init__(self, id: int, payment_owner_id: int, supply_id: int, count: int, amount: float):
        self.id = id
        self.payment_owner_id = payment_owner_id
        self.supply_id = supply_id
        self.count = count
        self.amount = amount
    
    def to_dict(self):
        return {
            "id": self.id,
            "payment_owner_id": self.payment_owner_id,
            "supply_id": self.supply_id,
            "count": self.count,
            "amount": self.amount
        }