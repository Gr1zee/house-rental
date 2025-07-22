from pydantic import BaseModel

class HouseBase(BaseModel):
    title: str
    price: int

class HouseCreate(HouseBase):
    pass

class House(HouseBase):
    id: int
    class Config:
        from_attributes = True