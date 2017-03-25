from .extendedbase import ExtendedBase


# Class representing an item
class Item(ExtendedBase):
    def __init__(self):
        super(Item, self).__init__()
        self.recipe = None
        self.quality = None
        self.price = None
        self.description = None
        self.notes = None
        self.stats = None
        self.cooldown = None
        self.manacost = None
        self.components = None
        self.component_in = None
        self.shop_info = None

    # Returns name and value of all fields required by the database
    def get_required(self):
        required = super(Item, self).get_required()
        required.update({"recipe": self.recipe, "quality": self.quality})
        return required
