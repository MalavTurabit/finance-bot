from graph.llm import get_llm


def coach_agent(state: dict) -> dict:
    llm = get_llm()

    prompt = f"""
You are a Financial Coach.

User data:
{state}

Give motivational financial advice.
"""

    response = llm.invoke(prompt)

    return {"response": response.content}
