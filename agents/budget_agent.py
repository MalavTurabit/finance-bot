from graph.llm import get_llm


def budget_agent(state: dict) -> dict:
    llm = get_llm()

    prompt = f"""
You are a Budget Agent.

User income: {state.get("income")}
Expenses: {state.get("expenses")}

Give budgeting advice.
"""

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }
