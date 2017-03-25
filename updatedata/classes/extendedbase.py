from .base import Base


# Extends the base with a few fields common to items, heroes and abilities
class ExtendedBase(Base):
    def __init__(self):
        super(ExtendedBase, self).__init__()
        self.name = None
        self.dname = None
        self.lore = None
        self.image = None

    def __str__(self):
        return self.name + "|" + self.dname

    # Returns name and value of all fields required by the database
    def get_required(self):
        required = super(ExtendedBase, self).get_required()
        required.update({"name": self.name, "dname": self.dname})
        return required
