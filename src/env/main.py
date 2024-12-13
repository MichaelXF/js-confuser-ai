from dotenv import load_dotenv
from os import getenv

mode = "development"


def is_development():
    return mode == "development"


def is_production():
    return mode == "production"


def init_env():
    global mode
    load_dotenv()

    mode = getenv("MODE")
    if not mode:
        raise ValueError("MODE environment variable not set")

    print("Launching app in " + mode + " mode...")
