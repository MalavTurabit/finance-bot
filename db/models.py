from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)

    monthly_income = Column(Float, nullable=True)
    monthly_budget = Column(Float, nullable=True)
    savings_goal = Column(Float, nullable=True)

    onboarding_step = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    expenses = relationship("Expense", back_populates="user")
    income = relationship("Income", back_populates="user")



class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="income")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String)
    amount = Column(Float)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="expenses")


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String)
    target_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class ConversationMemory(Base):
    __tablename__ = "conversation_memory"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    role = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class PurchaseRequest(Base):
    __tablename__ = "purchase_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_url = Column(Text)
    price = Column(Float)
    recommendation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    message = Column(Text)
    level = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
