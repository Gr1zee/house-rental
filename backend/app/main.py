from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .db import SessionLocal, engine

# Создаём таблицы в БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Настройка CORS (разрешаем запросы с фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене замените на домен фронтенда
    allow_methods=["*"],
    allow_headers=["*"],
)

# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинт для получения списка домов
@app.get("/houses", response_model=list[schemas.House])
def read_houses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    houses = crud.get_houses(db, skip=skip, limit=limit)
    return houses

# Эндпоинт для добавления дома (пример)
@app.post("/houses", response_model=schemas.House)
def add_house(house: schemas.HouseCreate, db: Session = Depends(get_db)):
    return crud.create_house(db, house=house)