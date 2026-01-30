from fastapi import FastAPI

from db.database import Base, engine
from api.users import router as users_router
from api.expenses import router as expenses_router
from api.purchase import router as purchase_router
from api.chat import router as chat_router



Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Personal Finance Assistant")
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(expenses_router, prefix="/expenses", tags=["expenses"])
app.include_router(purchase_router, prefix="/purchase", tags=["purchase"])


@app.get("/")
def health_check():
    return {"status": "ok"}
