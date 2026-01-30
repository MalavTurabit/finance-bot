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
    llm = get_llm()
    chain = INTENT_PROMPT | llm
    result = chain.invoke({"input": text})
    return result.content.strip().lower()
