from sqlalchemy.orm import Session
from . import models, schemas

def get_houses(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.House).offset(skip).limit(limit).all()

def create_house(db: Session, house: schemas.HouseCreate):
    db_house = models.House(**house.model_dump())
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house