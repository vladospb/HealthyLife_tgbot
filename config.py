from dotenv import load_dotenv
from os import getenv

load_dotenv()
BOT_API_TOKEN = getenv("BOT_API_TOKEN")
GISMETEO_TOKEN = getenv("GISMETEO_TOKEN")