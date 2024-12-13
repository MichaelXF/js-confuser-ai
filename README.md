# JS-Confuser AI Backend

This projects powers the AI chat services for [JS-Confuser.com](https://js-confuser.com)!

- Powered by Google's Gemini AI:
- - Gemini 2.0 Flash: `gemini-2.0-flash-exp`
- - Text Embeddings: `models/text-embedding-004`

- [Google's Gemini API is FREE for up to 1,500 requests per day!](https://ai.google.dev/pricing#1_5flash)

- **[>> Get your API Key here! <<](https://aistudio.google.com/apikey)**

> [!TIP]
> The Gemini API “free tier” is offered through the API service with lower rate limits for testing purposes. Google AI Studio usage is completely free in all available countries.
>
> _Rate Limits_
>
> - 15 RPM (requests per minute)
> - 1 million TPM (tokens per minute)
> - 1,500 RPD (requests per day)

## Internals

- [Phidata](https://www.phidata.com/) AI agent for creating a RAG (Retrieval-Augmented Generation) chatbot
- FastAPI WebSocket for smoothly streaming generated responses back to client
- Knowledge database, storing the JS-Confuser Doc's MD files
- PostgreSQL + PGVector for storing embeddings

## Requirements

Requires Python >= 3.8
Requires PostgreSQL >= 16, with PGVector installed

- [Install PostgreSQL here](https://www.postgresql.org/download/)
- [Install PGVector here](https://github.com/pgvector/pgvector?tab=readme-ov-file#installation)

## Install Packages

- This projects uses Python's virtual environment system. You are recommended to simply 'activate' the virtual environment; and then install packages like so:

```bash
source venv/bin/activate

pip install -r requirements.txt
```

## Packages

| Package               | Purpose                                                |
| --------------------- | ------------------------------------------------------ |
| `fastapi`             | ASGI Web Server                                        |
| `pydantic`            | Data validation                                        |
| `phidata`             | AI Agent Model                                         |
| `google-generativeai` | Gemini Model APIs                                      |
| `openai`, `ollama`    | _(Optional)_ Model APIs for choosing a different model |

## First-Time Initialization

**Create your knowledge base**
Drop any `.txt`, `.md` files into the `knowledge_base` folder. This will be the data your AI agent can query on. In JS-Confuser's case, I simply exported the entire Docs as individual markdown files.

**Index the knowledge base**
You must index your knowledge base by running the server with the `--index` flag. This will recreate the embeddings for your knowledge.

## Configure .env File

You will need to supply your `GEMINI_API_KEY` if you plan to use Gemini's API.

```
.env
MODE=development

DATABASE_URL=postgresql+asyncpg://username:password@localhost:5433/ai_db

# Recommend model choice
GEMINI_API_KEY=

# If you want to use Ollama
# OLLAMA_HOST="http://127.0.0.1:11434"
# OLLAMA_MODEL=llama3.2
# OLLAMA_MODEL_DIMENSIONS=3072
# OLLAMA_MODEL_NUM_CTX=1536

# If you want to use OpenAI's GPT 4o
# OPENAI_API_KEY=

# If you want to use Claude
# ANTHROPIC_API_KEY=
# VOYAGE_API_KEY=
```

## Development Server

Run the development server in watch mode using:

```
fastapi dev src/main.py
```

## Production Server

**Update the .env file**

```
MODE=production
```

This simply prepares the server for production, such as disabling the CORS middleware that was added in for development purposes only.

**Launch server with [Uvicorn](https://www.uvicorn.org/)**

```
uvicorn src/main:app --host 0.0.0.0 --port 80
```

## Change Model

You may switch model providers by editing the file `src/agent/main.py`. Simply swap out providers by commenting/uncommenting out the imports:

```python
from agent.gem_model import model, model_embedder
# from agent.ollama_model import model, model_embedder
# from agent.openai_model import model, model_embedder
```

## Project Structure

- `knowledge_base`
- - _Files for your AI knowledge base:_
- - `MyDoc1.md`
- - `MyDoc2.md`

- `src`
- - `main.py` _App launch_
- - `agent/` _Phidata Agent creation_
- - `routes/` _FastAPI routes_
- - `env/` _Load environment variables_
- - `models/` _Pydantic models (none for now)_
- - `dependencies/` _FastAPI dependencies (none for now)_
- - `db/` _DB loading (unused for now)_

- `venv` _Python virtual enviroment_
- `requirements.txt` Package list

## License

MIT License
