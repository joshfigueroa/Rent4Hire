# Models used for Pydantic

from datetime import datetime
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: int
    is_active: bool
    date_created: datetime
    first_name: str
    last_name: str
    email: str
    street: str
    location_id: int
    availability: datetime


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []
    
    class Config:
        orm_mode = True