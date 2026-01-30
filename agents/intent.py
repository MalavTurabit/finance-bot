from langchain_core.prompts import ChatPromptTemplate
from graph.llm import get_llm


INTENT_PROMPT =ChatPromptTemplate.from_template("""
Classify the user intent into one of:

budget
spending
purchase
coach

User message:
{input}

Respond with ONLY the label.
""")


def classify_intent(text: str) -> str:
    t = text.lower()

    if any(x in t for x in ["buy", "purchase", "order"]):
        return "purchase"

    if any(x in t for x in ["budget", "how much left", "remaining"]):
        return "budget"

    if any(x in t for x in ["spent", "spending", "expenses"]):
        return "spending"

    return "general"