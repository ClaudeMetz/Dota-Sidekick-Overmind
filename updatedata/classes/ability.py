from .extendedbase import ExtendedBase


# Class representing an Ability
class Ability(ExtendedBase):
    def __init__(self):
        super(Ability, self).__init__()
        self.hero = None
        self.spot = None
        self.hotkey = None
        self.behavior = None
        self.affects = None
        self.damage_type = None
        self.pierces_SI = None
        self.description = None
        self.aghs_description = None
        self.notes = None
        self.stats = None
        self.cooldown = None
        self.manacost = None

    # Returns name and value of all fields required by the database
    def get_required(self):
        required = super(Ability, self).get_required()
        required.update({"hero": self.hero, "spot": self.spot})
        return required
