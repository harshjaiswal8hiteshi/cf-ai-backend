import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

APP_BACKEND_URL = os.getenv("APP_BACKEND_URL", "http://localhost:8000")
AI_BACKEND_PORT = int(os.getenv("AI_BACKEND_PORT", 8001))

POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")