from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class House(Base):
    __tablename__ = "houses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    price = Column(Integer)
    rooms = Column(Integer)
    area = Column(Float)
    location = Column(String)
    has_garage = Column(Boolean, default=False)
    has_garden = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    contact_phone = Column(String)
    images = Column(Text)  # JSON строку с путями к изображениям
    
    # Relationship
    bookings = relationship("Booking", back_populates="house")