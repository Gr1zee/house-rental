from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from datetime import date

from app.db.session import get_db
from app.schemas.booking import Booking, BookingCreate, BookingUpdate, BookingWithHouse
from app.db.models.booking import Booking as BookingModel
from app.db.models.house import House

router = APIRouter()

@router.post("/bookings/", response_model=Booking)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    # Проверяем, что дом существует
    house = db.query(House).filter(House.id == booking.house_id).first()
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    
    # Проверяем, что дом активен
    if not house.is_active:
        raise HTTPException(status_code=400, detail="House is not available for booking")
    
    # Проверяем доступность дат
    conflicting_bookings = db.query(BookingModel).filter(
        and_(
            BookingModel.house_id == booking.house_id,
            BookingModel.status.in_(["pending", "confirmed"]),
            and_(
                BookingModel.check_in_date < booking.check_out_date,
                BookingModel.check_out_date > booking.check_in_date
            )
        )
    ).first()
    
    if conflicting_bookings:
        raise HTTPException(status_code=400, detail="House is not available for these dates")
    
    # Вычисляем общую стоимость
    days = (booking.check_out_date - booking.check_in_date).days
    total_price = house.price * days
    
    # Создаем бронирование
    db_booking = BookingModel(
        **booking.dict(),
        total_price=total_price
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.get("/bookings/", response_model=List[BookingWithHouse])
def read_bookings(
    skip: int = 0, 
    limit: int = 100, 
    house_id: int = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(BookingModel)
    
    if house_id:
        query = query.filter(BookingModel.house_id == house_id)
    
    if status:
        query = query.filter(BookingModel.status == status)
    
    bookings = query.offset(skip).limit(limit).all()
    
    # Добавляем информацию о доме
    result = []
    for booking in bookings:
        house = db.query(House).filter(House.id == booking.house_id).first()
        booking_dict = {
            **booking.__dict__,
            "house_title": house.title if house else "Unknown",
            "house_location": house.location if house else "Unknown"
        }
        result.append(BookingWithHouse(**booking_dict))
    
    return result

@router.get("/bookings/{booking_id}", response_model=BookingWithHouse)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    house = db.query(House).filter(House.id == booking.house_id).first()
    booking_dict = {
        **booking.__dict__,
        "house_title": house.title if house else "Unknown",
        "house_location": house.location if house else "Unknown"
    }
    return BookingWithHouse(**booking_dict)

@router.put("/bookings/{booking_id}", response_model=Booking)
def update_booking(booking_id: int, booking_update: BookingUpdate, db: Session = Depends(get_db)):
    booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    for field, value in booking_update.dict(exclude_unset=True).items():
        setattr(booking, field, value)
    
    db.commit()
    db.refresh(booking)
    return booking

@router.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}

@router.get("/houses/{house_id}/availability")
def check_house_availability(
    house_id: int,
    check_in_date: date,
    check_out_date: date,
    db: Session = Depends(get_db)
):
    # Проверяем, что дом существует
    house = db.query(House).filter(House.id == house_id).first()
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    
    # Проверяем доступность
    conflicting_bookings = db.query(BookingModel).filter(
        and_(
            BookingModel.house_id == house_id,
            BookingModel.status.in_(["pending", "confirmed"]),
            and_(
                BookingModel.check_in_date < check_out_date,
                BookingModel.check_out_date > check_in_date
            )
        )
    ).first()
    
    is_available = conflicting_bookings is None
    days = (check_out_date - check_in_date).days
    total_price = house.price * days if is_available else 0
    
    return {
        "house_id": house_id,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "is_available": is_available,
        "total_price": total_price,
        "price_per_day": house.price
    } 