from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)  # Создаем таблицы

app = FastAPI()

# Зависимость для сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/houses/", response_model=schemas.House)
def create_house(house: schemas.HouseCreate, db: Session = Depends(get_db)):
    db_house = models.House(**house.model_dump())
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house

@app.get("/houses/", response_model=list[schemas.House])
def read_houses(db: Session = Depends(get_db)):
    return db.query(models.House).all()