from phi.model.google import Gemini
from phi.embedder.google import GeminiEmbedder
from os import getenv

model = Gemini(id="gemini-2.0-flash-exp", api_key=getenv("GEMINI_API_KEY"))

model_embedder = GeminiEmbedder(
    model="models/text-embedding-004", api_key=getenv("GEMINI_API_KEY"), dimensions=768
)
