from phi.model.openai import OpenAIChat
from os import getenv
from phi.embedder.openai import OpenAIEmbedder


model = OpenAIChat(id="gpt-4o", api_key=getenv("OPENAI_API_KEY"))
model_embedder = OpenAIEmbedder(
    model="text-embedding-3-large", api_key=getenv("OPENAI_API_KEY")
)
