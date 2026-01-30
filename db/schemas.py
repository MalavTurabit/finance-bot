from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    name: str


class UserResponse(UserCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    user_id: int
    category: str
    amount: float
    description: str


class ExpenseResponse(ExpenseCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PurchaseRequestCreate(BaseModel):
    user_id: int
    product_url: str


class PurchaseRequestResponse(BaseModel):
    id: int
    recommendation: str
    price: float
    created_at: datetime

    class Config:
        from_attributes = True
