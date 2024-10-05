import os

from dotenv import load_dotenv

"""
Переменные окружения загружаются из .env
"""
load_dotenv()

_pg_user = os.environ.get('POSTGRES_USER')
_pg_pass = os.environ.get('POSTGRES_PASSWORD')
_pg_host = os.environ.get('POSTGRES_HOST')
_pg_db = os.environ.get('POSTGRES_DB')
_pg_port = os.environ.get("POSTGRES_PORT")

db_engine_url = f"postgresql+psycopg://{_pg_user}:{_pg_pass}@{_pg_host}:{_pg_port}/{_pg_db}"