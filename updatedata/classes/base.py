from ..database import verification


# Base class for items, heroes, abilities and talents
class Base:
    def __init__(self):
        self.patch = None
        self.revision = None

    # Returns name and value of all fields required by the database
    def get_required(self):
        return {"patch": self.patch, "revision": self.revision}

    # Checks if all required fields are filled in
    def check_required_fields(self):
        verification.check_completeness(self)
