from langchain_groq import ChatGroq


def get_llm() -> ChatGroq:
    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.2,
    )
