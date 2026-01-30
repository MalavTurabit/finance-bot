from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db import models, schemas

router = APIRouter()


@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
