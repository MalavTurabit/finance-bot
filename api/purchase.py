from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db import models, schemas

router = APIRouter()


@router.post("/", response_model=schemas.PurchaseRequestResponse)
def evaluate_purchase(request: schemas.PurchaseRequestCreate, db: Session = Depends(get_db)):
    # Placeholder logic (real logic comes STEP 5)
    fake_price = 100.0
    recommendation = "WAIT"

    record = models.PurchaseRequest(
        user_id=request.user_id,
        product_url=request.product_url,
        price=fake_price,
        recommendation=recommendation,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record
