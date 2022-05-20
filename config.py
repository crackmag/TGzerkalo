from os import environ
from dotenv import load_dotenv
from utils import parse_string

load_dotenv()


CHANNELS_MAPPING = parse_string(environ.get('CHANNELS_MAPPING', ''))
# Для фильтра по каналам-источникам
SOURCE_CHANNELS = list(CHANNELS_MAPPING.keys())


API_ID = environ.get("API_ID")
API_HASH = environ.get("API_HASH")
SESSION_STRING = environ.get("SESSION_STRING")
SOURCE_CHANNEL = environ.get("SOURCE_CHANNEL")
TARGET_CHANNEL = environ.get("TARGET_CHANNEL")

DATABASE_URL = environ.get("DATABASE_URL")
PG_USER = environ.get("PG_USER")
PG_PASSWORD = environ.get("PG_PASSWORD")
DATABASE = environ.get("DATABASE")
DB_HOST = environ.get("DB_HOST")
DB_PORT = environ.get("DB_PORT")

