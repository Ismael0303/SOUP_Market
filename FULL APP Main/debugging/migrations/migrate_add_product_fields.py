# backend/migrate_add_product_fields.py

from sqlalchemy import text
from app.database import engine

def migrate_add_product_fields():
    """Add new fields to the productos table."""
    with engine.connect() as connection:
        try:
            # Add precio_venta field
            connection.execute(text("""
                ALTER TABLE productos 
                ADD COLUMN IF NOT EXISTS precio_venta FLOAT
            """))
            print("Added precio_venta field")
            
            # Add margen_ganancia_sugerido field
            connection.execute(text("""
                ALTER TABLE productos 
                ADD COLUMN IF NOT EXISTS margen_ganancia_sugerido FLOAT
            """))
            print("Added margen_ganancia_sugerido field")
            
            # Commit the changes
            connection.commit()
            print("Migration completed successfully!")
            
        except Exception as e:
            print(f"Error during migration: {e}")
            connection.rollback()
            raise

if __name__ == "__main__":
    migrate_add_product_fields() 