from sqlalchemy.orm import Session
from typing import Tuple
import re
from db import models
from graph.workflow import build_graph


def extract_price_from_text(text: str) -> float:
    match = re.search(r"(\d+(\.\d+)?)", text)
    if match:
        return float(match.group(1))
    return 0.0


def get_monthly_spending(db: Session, user_id: int) -> float:
    expenses = db.query(models.Expense).filter(models.Expense.user_id == user_id).all()
    return sum(e.amount for e in expenses)


def evaluate_purchase(db: Session, user_id: int, message: str):

    price = extract_price_from_text(message)

    spending = get_monthly_spending(db, user_id)

    monthly_budget = 2000.0
    remaining = monthly_budget - spending

    graph = build_graph()

    result = graph.invoke(
        {
            "input": message,
            "price": price,
            "budget": remaining,
            "expenses": spending,
        }
    )

    return result["response"], price

