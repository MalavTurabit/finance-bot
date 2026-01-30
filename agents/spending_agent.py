from graph.llm import get_llm


def spending_agent(state: dict) -> dict:
    llm = get_llm()

    prompt = f"""
You are a Spending Analysis Agent.

Expenses:
{state.get("expenses")}

Summarize spending patterns.
"""

    response = llm.invoke(prompt)

    return {"response": response.content}
