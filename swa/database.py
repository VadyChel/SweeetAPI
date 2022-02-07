from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from swa.core.config import Config

SQLALCHEMY_DATABASE_URL = f"postgresql://{Config.DB_USER}:{Config.DB_PASS}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=100)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()