from ..database.session_scope import Base

from sqlalchemy import Column, Integer, Float, Text


# SQLAlchemy declarative class representing an item
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    dname = Column(Text, nullable=False)
    recipe = Column(Integer)
    quality = Column(Text, nullable=False)
    price = Column(Integer)
    description = Column(Text)
    notes = Column(Text)
    stats = Column(Text)
    cooldown = Column(Float)
    manacost = Column(Integer)
    components = Column(Text)
    component_in = Column(Text)
    shop_info = Column(Text)
    lore = Column(Text)
    image = Column(Text)
    patch = Column(Text, nullable=False)
    revision = Column(Integer, nullable=False)
