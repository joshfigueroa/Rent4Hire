from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Rental(Base):
    __tablename__ = "rentals"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    category = Column(String(255))
    quantity = Column(Integer)
    price = Column(Float)
    value = Column(Float)
    description = Column(String(255))
    image = Column(String(255))
    location = Column(String(255))
    def __repr__(self):
        return f"User(id={self.id!r})"
