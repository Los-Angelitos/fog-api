class Hotel:
    def __init__(self, id: int, owner_id: int, name: str = None, description: str = None, email: str = None, address: str = None, phone: str = None):
        self.id = id
        self.owner_id = owner_id
        self.name = name
        self.description = description
        self.email = email
        self.address = address
        self.phone = phone
        