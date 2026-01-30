from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db.database import get_db
from db import models
from graph.workflow import build_graph
from tool.forecasting import emergency_check
from agents.intent import classify_intent
from tool.purchase_tool import evaluate_purchase

router = APIRouter()


class ChatRequest(BaseModel):
    user_id: int
    message: str


def try_parse_number(text: str):
    import re
    m = re.search(r"(\d+(\.\d+)?)", text)
    return float(m.group(1)) if m else None


@router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    user_id = request.user_id
    message = request.message.strip()

    user = db.query(models.User).filter(models.User.id == user_id).first()

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        user = models.User(id=user_id)
        db.add(user)
        db.commit()
        db.refresh(user)

    # Save user message
    db.add(models.ConversationMemory(user_id=user_id, role="user", content=message))
    db.commit()

    # -----------------
    # ONBOARDING FLOW
    # -----------------

    if user.onboarding_step == 0:
        income = try_parse_number(message)
        if income:
            user.monthly_income = income
            user.onboarding_step = 1
            db.commit()
            reply = "Got it. What is your monthly budget?"
        else:
            reply = "Welcome! Please tell me your monthly income."

    elif user.onboarding_step == 1:
        budget = try_parse_number(message)
        if budget:
            user.monthly_budget = budget
            user.onboarding_step = 2
            db.commit()
            reply = "Thanks. Do you have a monthly savings goal?"
        else:
            reply = "Please enter your monthly budget."

    elif user.onboarding_step == 2:
        goal = try_parse_number(message)
        if goal:
            user.savings_goal = goal
        user.onboarding_step = 3
        db.commit()
        reply = "Perfect. You're all set! You can now ask me anything about your finances."

    # -----------------
    # NORMAL CHAT FLOW
    # -----------------

    else:
        intent = classify_intent(message)

        if intent == "purchase":
            reply, _ = evaluate_purchase(db, user_id, message)

        elif intent == "budget":
            spent = sum(e.amount for e in user.expenses)
            remaining = (user.monthly_budget or 0) - spent

            reply = (
                f"Your monthly budget is ${user.monthly_budget:.0f}.\n"
                f"You’ve spent ${spent:.0f} so far.\n"
                f"You have ${remaining:.0f} remaining."
            )

        else:
            graph = build_graph()
            result = graph.invoke({"input": message})
            reply = result.get("response", "")


        if emergency_check(db, user_id, user.monthly_budget or 2000):
            reply += "\n\n⚠️ Warning: you're close to exceeding your monthly budget."

    # Save assistant reply
    db.add(models.ConversationMemory(user_id=user_id, role="assistant", content=reply))
    db.commit()

    return {"reply": reply}
