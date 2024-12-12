from routes.chat_routes import router as chat_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from env.main import is_development


def init_api() -> FastAPI:
    app = FastAPI()

    # React CORS enable for development purposes
    if is_development():
        # Allow CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "*"
            ],  # Replace "*" with a list of allowed origins for stricter security
            allow_credentials=True,
            allow_methods=[
                "*"
            ],  # Replace "*" with a list of allowed methods, e.g., ["GET", "POST"]
            allow_headers=[
                "*"
            ],  # Replace "*" with a list of allowed headers, e.g., ["Authorization", "Content-Type"]
        )

    app.include_router(chat_router)
    return app
