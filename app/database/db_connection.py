import os
from sqlalchemy import create_engine

def get_db_engine():
    user = os.getenv('DB_USER', 'user')
    password = os.getenv('DB_PASSWORD', 'password')
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    database = os.getenv('DB_NAME', 'your_database')
    return create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
