# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# SQLAlchemy database URL from settings
DATABASE_URL = settings.DATABASE_URL

# Create the SQLAlchemy engine
# 'echo=True' logs all SQL statements, useful for debugging
engine = create_engine(DATABASE_URL, echo=True)

# Create a SessionLocal class for database sessions
# 'autocommit=False' means changes won't be committed automatically
# 'autoflush=False' means changes won't be flushed to DB automatically on query
# 'bind=engine' links sessions to our engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our declarative models.
# This Base is essential; all our SQLAlchemy models (like Usuario, Negocio, etc.)
# will inherit from this Base. When they inherit, they automatically register
# their metadata with Base.metadata.
Base = declarative_base()

# Dependency to get a database session (used in FastAPI routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
