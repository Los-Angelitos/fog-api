class Supply:
    def __init__(self, provider_id, name, price, stock, state, id=None):
        self.id = id
        self.provider_id = provider_id
        self.name = name
        self.price = price
        self.stock = stock
        self.state = state


class SupplyRequest:
    def __init__(self, payment_owner_id, supply_id, count, amount, id=None):
        self.id = id
        self.payment_owner_id = payment_owner_id
        self.supply_id = supply_id
        self.count = count
        self.amount = amount