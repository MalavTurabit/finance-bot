from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db import models, schemas
from tool.purchase_tool import evaluate_purchase

router = APIRouter()


@router.post("/", response_model=schemas.PurchaseRequestResponse)
def evaluate_purchase_endpoint(
    request: schemas.PurchaseRequestCreate,
    db: Session = Depends(get_db),
):
    recommendation, price = evaluate_purchase(
        db=db,
        user_id=request.user_id,
        product_url=request.product_url,
    )

    record = models.PurchaseRequest(
        user_id=request.user_id,
        product_url=request.product_url,
        price=price,
        recommendation=recommendation,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record
