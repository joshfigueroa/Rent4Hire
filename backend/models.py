from pydantic import BaseModel

class Rental(BaseModel):
    id: int
    name: str
    category: str
    quantity: int
    price: float
    value: float
    description: str
    image: str
    location: str