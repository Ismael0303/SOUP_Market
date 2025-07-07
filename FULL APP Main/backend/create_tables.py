# backend/create_tables.py
import os
import sys

    # Add the parent directory to the Python path to allow importing 'app'
    # This is necessary because this script is outside the 'app' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

    # Import necessary components
from app.database import Base, engine
import app.models # Import all models so Base.metadata knows about them

print("Attempting to create database tables...")
print(f"SQLAlchemy Engine URL for script: {engine.url}")
try:
        # Drop all tables first (useful for clean slate during development)
        # Be CAREFUL with this in production!
        # Base.metadata.drop_all(bind=engine)
        # print("Existing tables dropped (if any).")

        # Create all tables defined in Base.metadata
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully by script.")
except Exception as e:
        print(f"Error creating tables: {e}")
        # Print the full traceback for more details
        import traceback
        traceback.print_exc()

    