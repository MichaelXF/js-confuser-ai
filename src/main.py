from env.main import init_env

print("Initializing environment...")
init_env()

from routes.main import init_api
from db.main import init_db

print("Initializing database...")
init_db()

print("Initializing API...")
app = init_api()
