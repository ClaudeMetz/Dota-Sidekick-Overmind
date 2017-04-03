from ..database.session_scope import Base

from sqlalchemy import Column, Integer, Text, ForeignKey


# SQLAlchemy declarative class representing a talent
class Talent(Base):
    __tablename__ = "talents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hero = Column(Text, ForeignKey("heroes.name"), nullable=False)
    level = Column(Integer, nullable=False)
    left_talent = Column(Text, nullable=False)
    right_talent = Column(Text, nullable=False)
    patch = Column(Text, nullable=False)
    revision = Column(Integer, nullable=False)
