from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from db import models


def rolling_average(db: Session, user_id: int, days: int = 30) -> float:
    since = datetime.utcnow() - timedelta(days=days)

    expenses = (
        db.query(models.Expense)
        .filter(models.Expense.user_id == user_id)
        .filter(models.Expense.created_at >= since)
        .all()
    )

    if not expenses:
        return 0.0

    total = sum(e.amount for e in expenses)
    return total / days


def emergency_check(db: Session, user_id: int, monthly_budget: float = 2000) -> bool:
    avg = rolling_average(db, user_id)
    projected = avg * 30

    return projected > monthly_budget * 0.9
