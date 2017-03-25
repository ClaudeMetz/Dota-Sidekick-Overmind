from .base import Base


# Class representing a hero talent
class Talent(Base):
    def __init__(self):
        super(Talent, self).__init__()
        self.hero = None
        self.level = None
        self.left_talent = None
        self.right_talent = None

    def __str__(self):
        return self.left_talent + "|" + self.right_talent

    # Returns name and value of all fields required by the database
    def get_required(self):
        required = super(Talent, self).get_required()
        required.update({"hero": self.hero, "level": self.level, "left_talent": self.left_talent,
                         "right_talent": self.right_talent})
        return required
