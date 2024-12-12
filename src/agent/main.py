from phi.agent import Agent
from phi.knowledge.text import TextKnowledgeBase
from phi.vectordb.pgvector import PgVector


from agent.gem_model import model, model_embedder

# from agent.ollama_model import model, model_embedder
# from agent.openai_model import model, model_embedder


vector_db = PgVector(
    table_name="chat_documents",
    db_url="postgresql+psycopg://username:password@localhost:5433/ai_db",
    embedder=model_embedder,
)

knowledge_base = TextKnowledgeBase(
    path="./knowledge_base",
    vector_db=vector_db,
    num_documents=5,
)


# Load the knowledge base: Comment out after first run
# knowledge_base.load(recreate=True, upsert=True)

agent = Agent(
    name="JS-Confuser AI",
    model=model,
    knowledge=knowledge_base,
    # Add a tool to read chat history.
    read_chat_history=False,  # Causes error?
    show_tool_calls=True,
    markdown=True,
    prevent_hallucinations=True,
    debug_mode=False,
    stream=True,
    instructions=[
        "Always include links for sources for where you found the information, typically https://js-confuser.com/."
    ],
)

# Test out the agent when running the file directly
if __name__ == "__main__":
    while True:
        message = input("> ")
        if message == "exit":
            break

        agent.print_response(message, stream=True)
