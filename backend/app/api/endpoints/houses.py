from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.db.session import get_db
from backend.app.schemas.house import House, HouseCreate
from backend.app.db.models.house import House

router = APIRouter()

@router.get("/houses/")
def read_houses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(House).filter(House.is_active == True).offset(skip).limit(limit).all()

@router.post("/houses/")
def create_house(house: HouseCreate, db: Session = Depends(get_db)):
    db_house = House(**house.dict())
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house

@router.get("/houses/{house_id}")
def read_house(house_id: int, db: Session = Depends(get_db)):
    house = db.query(House).filter(House.id == house_id).first()
    if house is None:
        raise HTTPException(status_code=404, detail="House not found")
    return house