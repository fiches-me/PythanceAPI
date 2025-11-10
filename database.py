from sqlmodel import create_engine, Session
from models import SQLModel
import os

# Create engine
engine = create_engine(os.environ["DATABASE_LINK"])

def create_db_and_tables():
    """Create all tables defined in models."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get a database session."""
    return Session(engine)
