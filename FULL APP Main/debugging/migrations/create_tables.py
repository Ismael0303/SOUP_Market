# backend/create_tables.py
import os
import sys

    # Add the parent directory to the Python path to allow importing 'app'
    # This is necessary because this script is outside the 'app' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

    # Import necessary components
from app.database import engine
from app.models import Base

def create_tables():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("All tables created successfully!")

    