import os

from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "/")
DISABLED_PLUGINS = os.getenv("DISABLED_PLUGINS", "").strip().split(",")
