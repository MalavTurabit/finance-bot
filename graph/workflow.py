from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from agents.intent import classify_intent
from agents.budget_agent import budget_agent
from agents.spending_agent import spending_agent
from agents.purchase_agent import purchase_agent
from agents.coach_agent import coach_agent


class GraphState(TypedDict):
    input: str
    price: Optional[float]
    budget: Optional[float]
    expenses: Optional[list]
    response: Optional[str]


def router(state: GraphState) -> str:
    intent = classify_intent(state["input"])
    return intent


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("budget", budget_agent)
    graph.add_node("spending", spending_agent)
    graph.add_node("purchase", purchase_agent)
    graph.add_node("coach", coach_agent)

    graph.set_conditional_entry_point(
        router,
        {
            "budget": "budget",
            "spending": "spending",
            "purchase": "purchase",
            "coach": "coach",
        },
    )

    graph.add_edge("budget", END)
    graph.add_edge("spending", END)
    graph.add_edge("purchase", END)
    graph.add_edge("coach", END)

    return graph.compile()
