from pydantic import BaseModel

class HouseBase(BaseModel):
    title: str
    price: float
    location: str

class HouseCreate(HouseBase):
    pass

class House(HouseBase):
    id: int
    image_url: str | None = None

    class Config:
        from_attributes = True