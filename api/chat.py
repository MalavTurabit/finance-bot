from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db import models
from graph.workflow import build_graph

router = APIRouter()


@router.post("/")
def chat(user_id: int, message: str, db: Session = Depends(get_db)):
    # Save user message
    user_msg = models.ConversationMemory(
        user_id=user_id,
        role="user",
        content=message,
    )
    db.add(user_msg)
    db.commit()

    graph = build_graph()

    result = graph.invoke(
        {
            "input": message,
        }
    )

    reply = result["response"]

    # Save assistant message
    bot_msg = models.ConversationMemory(
        user_id=user_id,
        role="assistant",
        content=reply,
    )
    db.add(bot_msg)
    db.commit()

    return {"reply": reply}
