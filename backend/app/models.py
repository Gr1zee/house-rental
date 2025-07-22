from sqlalchemy import Column, Integer, String, Float
from .db import Base

class House(Base):
    __tablename__ = "houses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    price = Column(Float)
    location = Column(String(100))
    image_url = Column(String(200), default="https://cdn-edge.kwork.ru/files/portfolio/t3/27/107f0270391347973cce1728c87cbb49c40266dd-1723240605.jpg")