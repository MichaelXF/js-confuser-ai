import sys
from os import getenv
from phi.agent import Agent
from phi.knowledge.text import TextKnowledgeBase
from phi.vectordb.pgvector import PgVector

from agent.gem_model import model, model_embedder

# from agent.ollama_model import model, model_embedder
# from agent.openai_model import model, model_embedder


vector_db = PgVector(
    table_name="chat_documents",
    db_url=getenv("DATABASE_URL"),
    embedder=model_embedder,
)

knowledge_base = TextKnowledgeBase(
    path="./knowledge_base",
    vector_db=vector_db,
    num_documents=5,
)

# Use the --index flag to recreate the embeddings
if len(sys.argv) > 1 and sys.argv[1] == "--index":
    print("Indexing knowledge base...")

    # Load the knowledge base: Comment out after first run
    knowledge_base.load(recreate=True, upsert=True)

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
    description="You are an AI assistant for JS-Confuser",
    instructions=[
        "Always include links for sources for where you found the information, typically https://js-confuser.com/."
        "Query the knowledge base for further information, you should query at least once.",
        "Do not perform code deobfuscation, the AI is not designed for this.",
        "You can not execute code, or access external/outside resources.",
    ],
)

# Test out the agent when running the file directly
if __name__ == "__main__":
    while True:
        message = input("> ")
        if message == "exit":
            break

        agent.print_response(message, stream=True)
