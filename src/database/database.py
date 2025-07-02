"""Database setup using SQLAlchemy"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.settings import DatabaseConfig

engine = create_engine(DatabaseConfig.get_connection_url())
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
