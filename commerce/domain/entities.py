class PaymentCustomer:
    def __init__(self, guest_id, final_amount, id=None):
        self.id = id
        self.guest_id = guest_id
        self.final_amount = final_amount

class PaymentOwner:
    def __init__(self, owner_id, description, final_amount, id=None):
        self.id = id
        self.owner_id = owner_id
        self.description = description
        self.final_amount = final_amount

class Subscription:
    def __init__(self, name, content, price, status, id=None):
        self.id = id
        self.name = name
        self.content = content
        self.price = price
        self.status = status

class ContractOwner:
    def __init__(self, owner_id, start_date, final_date, subscription_id, status, id=None):
        self.id = id
        self.owner_id = owner_id
        self.start_date = start_date
        self.final_date = final_date
        self.subscription_id = subscription_id
        self.status = status