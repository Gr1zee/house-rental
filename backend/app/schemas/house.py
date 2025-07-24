from pydantic import BaseModel
from typing import Optional, List

class HouseBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: int
    rooms: int
    area: float
    location: str

class HouseCreate(HouseBase):
    contact_phone: str
    has_garage: bool = False
    has_garden: bool = False

class House(HouseBase):
    id: int
    is_active: bool
    images: Optional[List[str]] = None
    
    class Config:
        from_attributes = True