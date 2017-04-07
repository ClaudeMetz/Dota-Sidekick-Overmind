from ..database.session_scope import Base

from sqlalchemy import Column, Integer, Float, Text
from sqlalchemy.orm import relationship


# SQLAlchemy declarative class representing a hero
class Hero(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    dname = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    roles = Column(Text, nullable=False)
    prim_atr = Column(Text, nullable=False)
    str_base = Column(Integer, nullable=False)
    str_growth = Column(Float, nullable=False)
    agi_base = Column(Integer, nullable=False)
    agi_growth = Column(Float, nullable=False)
    int_base = Column(Integer, nullable=False)
    int_growth = Column(Float, nullable=False)
    dmg_min = Column(Integer, nullable=False)
    dmg_max = Column(Integer, nullable=False)
    armor = Column(Float, nullable=False)
    movement_speed = Column(Integer, nullable=False)
    sight_range = Column(Text, nullable=False)
    attack_range = Column(Integer)
    attack_time = Column(Float, nullable=False)
    attack_point = Column(Float, nullable=False)
    missile_speed = Column(Integer)
    lore = Column(Text)
    image = Column(Text)
    patch = Column(Text, nullable=False)
    revision = Column(Integer, nullable=False)

    abilities = relationship("Ability")
    talents = relationship("Talent")
