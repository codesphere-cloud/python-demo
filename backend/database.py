import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL from environment variable, with fallback for local development
DATABASE_URL = os.getenv(
    "DB_CONNECTION_STRING",
    "postgresql://postgres:postgres@localhost:5432/demo"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DataPoint(Base):
    """Model for storing randomly generated data points."""
    __tablename__ = "data_points"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String, index=True)  # Groups points from the same request
    value_a = Column(Float, nullable=False)
    value_b = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
