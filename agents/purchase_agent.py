from graph.llm import get_llm


def purchase_agent(state: dict) -> dict:
    llm = get_llm()

    prompt = f"""
You are a Purchase Decision Agent.

Price: {state.get("price")}
Monthly budget: {state.get("budget")}

Respond BUY / WAIT / AVOID with explanation.
"""

    response = llm.invoke(prompt)

    return {"response": response.content}
