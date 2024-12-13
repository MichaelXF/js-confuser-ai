# 1. Add version assertion
import sys

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

# 2. Load .env file
from env.main import init_env, is_production

print("Initializing environment...")
init_env()

# 3. Initialize the database and API
from routes.main import init_api
from db.main import init_db

print("Initializing database...")
# init_db()

print("Initializing API...")
app = init_api()


# 4. Run the API
if is_production() and __name__ == "__main__":
    import uvicorn

    print("Listening on port 3000")
    uvicorn.run(app, host="127.0.0.1", port=3000, log_level="info")
