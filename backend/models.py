# Models used with SQLAlchemy

from uuid import UUID
from sqlalchemy import DATETIME, Text, Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from database import Base

# Add user table with public facing UUID, internal int ID4
# TODO Add relationships between tables

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    date_created = Column(DATETIME, default=datetime.utcnow, index=True)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    street = Column(String(255), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"))
    availability = Column(DATETIME, nullable=False) #????????
    
    items = relationship("Item", backref="owner")
    orders = relationship("Order_Item", backref="renter")
    reviews = relationship("Review", backref="user") #modified backrf
    

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    availability = Column(DATETIME, nullable=False) #???????????
    description = Column(Text, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    #item_location_id = Column(Integer)#, ForeignKey("locations.id"), index=True) #Not sure if this is needed
    price = Column(Float(5), nullable=False, index=True) #Same thig here
    
    item_reviews = relationship("Review", backref="item") #its the item being reviewed
    orders = relationship("Order_Item", backref="item")


class Order_Item(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    date_placed = Column(DATETIME, default=datetime.utcnow, nullable=False) #Not sure if im defaulting these dates right
    renter_id = Column(Integer, ForeignKey("users.id"), index=True)
    pickup_date = Column(DATETIME, nullable=False)
    dropoff_date = Column(DATETIME, nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), index=True) 
    
    transaction = relationship("Transaction", backref="order", uselist=False) #one-to-one rel
    

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(255), nullable=False)
    state = Column(String(2), nullable=False)
    zip = Column(String(5), nullable=False)
    country = Column(String(255), nullable=False) 
    
    users = relationship("User", backref="location")   
    
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(255), index=True)
    
    items = relationship("Item", backref="category")   

    
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    reviewer = Column(Integer, ForeignKey("users.id"), index=True)
    reviewed_item = Column(Integer, ForeignKey("items.id"), index=True) 
    title = Column(String(255), index=True)
    descritpion = Column(Text, index=True)
    
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    processor_id = Column(Integer, nullable=False) #WHAT IS THIS DO we need another table?
    processor = Column(String(255), nullable=False) 
    #amount = Column(Float(5), nullable=False)   #Not sure how Float works so put 5 in to test / This comes in through order_id then item_is then price, does that work??
    card_type = Column(String(255), nullable=False) #Does this need another table with all card types to choose from?
    card_last4 = Column(String(4), nullable=False) #Whats this? Shouldt this be card number? Or not because its just the record?
    card_exp_month = Column(String(2), nullable=False) 
    card_exp_year = Column(String(4), nullable=False) 
    created_at = Column(DATETIME, default=datetime.utcnow, nullable=False)

    records = relationship("Record", backref="transactions") #not sure if this rel is right
    
class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))

