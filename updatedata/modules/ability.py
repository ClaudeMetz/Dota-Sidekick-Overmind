from ..database.session_scope import Base

from sqlalchemy import Column, Integer, Text, ForeignKey


# SQLAlchemy declarative class representing an ability
class Ability(Base):
    __tablename__ = "abilities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hero = Column(Text, ForeignKey("heroes.name"), nullable=False)
    name = Column(Text, nullable=False)
    dname = Column(Text, nullable=False)
    spot = Column(Integer, nullable=False)
    hotkey = Column(Text)
    behavior = Column(Text)
    affects = Column(Text)
    damage_type = Column(Text)
    pierces_SI = Column(Text)
    description = Column(Text)
    aghs_description = Column(Text)
    notes = Column(Text)
    stats = Column(Text)
    cooldown = Column(Text)
    manacost = Column(Text)
    lore = Column(Text)
    image = Column(Text)
    patch = Column(Text, nullable=False)
    revision = Column(Integer, nullable=False)
