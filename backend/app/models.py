from sqlalchemy import Column, Integer, String
from .db import Base

class House(Base):
    __tablename__ = "houses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Integer)