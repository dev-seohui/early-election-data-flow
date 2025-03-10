import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 🔹 네이버 API 정보
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# 🔹 PostgreSQL 연결 정보
DB_HOST = os.getenv("DB_HOST", "postgres_container")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_USER = os.getenv("DB_USER", "myuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword")
