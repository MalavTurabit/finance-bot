from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from db import models, schemas

router = APIRouter()


@router.post("/", response_model=schemas.ExpenseResponse)
def add_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.get("/{user_id}", response_model=List[schemas.ExpenseResponse])
def get_expenses(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Expense).filter(models.Expense.user_id == user_id).all()
