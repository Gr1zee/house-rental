from pydantic import BaseModel, validator
from typing import Optional
from datetime import date, datetime

class BookingBase(BaseModel):
    house_id: int
    guest_name: str
    guest_email: str
    guest_phone: str
    check_in_date: date
    check_out_date: date
    notes: Optional[str] = None
    
    @validator('check_out_date')
    def check_out_date_must_be_after_check_in(cls, v, values):
        if 'check_in_date' in values and v <= values['check_in_date']:
            raise ValueError('check_out_date must be after check_in_date')
        return v

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None

class Booking(BookingBase):
    id: int
    total_price: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class BookingWithHouse(Booking):
    house_title: str
    house_location: str 