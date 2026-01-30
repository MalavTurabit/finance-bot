from sqlalchemy.orm import Session
from typing import Tuple

from db import models
from graph.workflow import build_graph


def extract_price_from_url(url: str) -> float:
    """
    Placeholder price extractor.
    Later replace with scraper.
    """
    return 100.0


def get_monthly_spending(db: Session, user_id: int) -> float:
    expenses = db.query(models.Expense).filter(models.Expense.user_id == user_id).all()
    return sum(e.amount for e in expenses)


def evaluate_purchase(
    db: Session,
    user_id: int,
    product_url: str,
) -> Tuple[str, float]:

    price = extract_price_from_url(product_url)

    spending = get_monthly_spending(db, user_id)

    # Temporary hard-coded monthly budget
    monthly_budget = 2000.0

    remaining = monthly_budget - spending

    graph = build_graph()

    result = graph.invoke(
        {
            "input": "purchase evaluation",
            "price": price,
            "budget": remaining,
            "expenses": spending,
        }
    )

    return result["response"], price
