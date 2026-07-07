import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
# SQLite path for local development
SQLITE_DB_PATH = "polla_mundial.db"
