from graph.workflow import build_graph

graph = build_graph()

state = graph.invoke(
    {
        "input": "Should I buy a new laptop?",
        "price": 1200,
        "budget": 2000,
        "expenses": [],
    }
)

print("\nFINAL STATE:\n")
print(state)
print("\nAI RESPONSE:\n")
print(state["response"])
