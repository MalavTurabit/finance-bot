from graph.llm import get_llm


def coach_agent(state: dict) -> dict:
    llm = get_llm()

    prompt = f"""
You are a professional financial coach.

User context:
{state}

Include:
- encouragement
- one actionable tip
- short forecast insight

Keep concise.
"""

    response = llm.invoke(prompt)

    return {"response": response.content}
