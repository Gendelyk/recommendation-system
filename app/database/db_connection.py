from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_engine():

    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(DATABASE_URL)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def init_db(engine):
    Base.metadata.create_all(engine)
