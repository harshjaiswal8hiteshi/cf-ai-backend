from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis
import psycopg2
import requests
from config import APP_BACKEND_URL, POSTGRES_URL, REDIS_URL

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check Postgres connection
def check_db():
    print(POSTGRES_URL)
    try:
        conn = psycopg2.connect(POSTGRES_URL)
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, name TEXT);")
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Postgres Error:", e)
        return False

# Check Redis connection
def check_redis():
    try:
        r = redis.Redis.from_url(REDIS_URL)
        r.ping()
        return True
    except Exception as e:
        print("Redis Error:", e)
        return False

@app.get("/")
def ai_status():
    # Check backend connectivity
    try:
        response = requests.get(f"{APP_BACKEND_URL}/connect", timeout=2)
        res = response.json()
        backend_to_ai_connection = res.get("backend_to_ai_connection", False)
    except Exception as e:
        print("Backend Connection Error:", e)
        backend_to_ai_connection = False

    return {
        "app": "ai_backend",
        "status": "running",
        "backend_to_ai_connection": backend_to_ai_connection,
        "db_connected": check_db(),
        "redis_connected": check_redis()
    }

@app.get("/connect")
def connect():
    # Return True so backend can confirm connectivity
    return {"ai_to_backend_connection": True}


@app.get("/health")
def health_check():
    return {"status": "ok"}