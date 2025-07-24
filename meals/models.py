from sqlalchemy import Column, Integer, String, Date, ForeignKey
from ..database import Base

class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    calories = Column(Integer)
    eaten_at = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))
