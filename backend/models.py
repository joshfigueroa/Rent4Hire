from uuid import UUID
from sqlalchemy import DATETIME, VARCHAR, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

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
    created_at = Column(DATETIME, index=True)
    email = Column(String(255), unique=True, index=True)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)
    availability = Column(DATETIME, nullable=False)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    item_type = Column(String(255), ForeignKey("item.id"), index=True)
    availability = Column(DATETIME, nullable=False)
    description = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    item_location_id = Column(Integer, ForeignKey("location.id"))
    category = Column(String(50), index=True)


class Order_Item(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DATETIME, nullable=False)
    renter_id = Column(Integer, ForeignKey("user.id"), index=True)
    pickup_date = Column(DATETIME, nullable=False)
    dropoff_date = Column(DATETIME, nullable=False)
    to_street = Column(String(255), index=True)
    to_city = Column(String(255), index=True)
    to_state = Column(String(2), nullable=False)
    to_zip = Column(String(5), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), index=True) 

class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(2), nullable=False)
    zip = Column(String(5), nullable=False)
    country = Column(String(255), nullable=False)    
    
