from .extendedbase import ExtendedBase
from ..database import verification


# Class representing a hero
class Hero(ExtendedBase):
    def __init__(self):
        super(Hero, self).__init__()
        self.type = None
        self.roles = None
        self.prim_atr = None
        self.str_base = None
        self.str_growth = None
        self.agi_base = None
        self.agi_growth = None
        self.int_base = None
        self.int_growth = None
        self.dmg_min = None
        self.dmg_max = None
        self.armor = None
        self.movement_speed = None
        self.sight_range = None
        self.attack_range = None
        self.attack_time = None
        self.attack_point = None
        self.missile_speed = None

        self.abilities = []
        self.talents = []

    # Returns name and value of all fields required by the database
    def get_required(self):
        required = super(Hero, self).get_required()
        required.update({"type": self.type, "roles": self.roles, "prim_atr": self.prim_atr, "str_base": self.str_base,
                         "str_growth": self.str_growth, "agi_base": self.agi_base, "agi_growth": self.agi_growth,
                         "int_base": self.int_base, "int_growth": self.int_growth, "dmg_min": self.dmg_min,
                         "dmg_max": self.dmg_max, "armor": self.armor, "movement_speed": self.movement_speed,
                         "sight_range": self.sight_range, "attack_time": self.attack_time,
                         "attack_point": self.attack_point})
        return required

    # Appends an ability or talent to this class after verifying compatibility
    def append(self, appendage):
        verification.check_compatibility(self, appendage)
