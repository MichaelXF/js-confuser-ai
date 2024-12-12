from phi.model.ollama import Ollama
from phi.embedder.ollama import OllamaEmbedder
from os import getenv

host = getenv("OLLAMA_HOST")
model_id = getenv("OLLAMA_MODEL")
model_dimensions = getenv("OLLAMA_MODEL_DIMENSIONS")
model_num_ctx = getenv("OLLAMA_MODEL_NUM_CTX")

if not host or not model_id or not model_dimensions or not model_num_ctx:
    raise ValueError(
        "OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_MODEL_DIMENSIONS, and OLLAMA_MODEL_NUM_CTX must be set in .env"
    )

# Example Context Values for qwen2.5-coder:32b
#
# DEFAULT_NUM_CTX=32768 # Consumes 36GB of VRAM
# DEFAULT_NUM_CTX=24576 # Consumes 32GB of VRAM
# DEFAULT_NUM_CTX=12288 # Consumes 26GB of VRAM
# DEFAULT_NUM_CTX=6144 # Consumes 24GB of VRAM
model = Ollama(id=model_id, host=host, options={"num_ctx": int(model_num_ctx)})

model_embedder = OllamaEmbedder(
    model=model_id,
    host=host,
    dimensions=int(model_dimensions),
)
