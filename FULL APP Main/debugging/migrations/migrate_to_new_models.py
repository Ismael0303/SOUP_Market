# backend/migrate_to_new_models.py

from sqlalchemy import text
from app.database import engine

def migrate_to_new_models():
    """Migrate database to new model structure."""
    with engine.connect() as connection:
        try:
            # Add new fields to productos table
            connection.execute(text("""
                ALTER TABLE productos 
                ADD COLUMN IF NOT EXISTS precio FLOAT NOT NULL DEFAULT 0.0
            """))
            print("Added precio field to productos")
            
            connection.execute(text("""
                ALTER TABLE productos 
                ADD COLUMN IF NOT EXISTS precio_venta FLOAT
            """))
            print("Added precio_venta field to productos")
            
            connection.execute(text("""
                ALTER TABLE productos 
                ADD COLUMN IF NOT EXISTS margen_ganancia_sugerido FLOAT
            """))
            print("Added margen_ganancia_sugerido field to productos")
            
            connection.execute(text("""
                ALTER TABLE productos 
                ADD COLUMN IF NOT EXISTS cogs FLOAT
            """))
            print("Added cogs field to productos")
            
            connection.execute(text("""
                ALTER TABLE productos 
                ADD COLUMN IF NOT EXISTS precio_sugerido FLOAT
            """))
            print("Added precio_sugerido field to productos")
            
            # Rename usuario_id to propietario_id in productos table
            connection.execute(text("""
                ALTER TABLE productos 
                ADD COLUMN IF NOT EXISTS propietario_id UUID
            """))
            print("Added propietario_id field to productos")
            
            # Copy data from usuario_id to propietario_id if propietario_id is null
            connection.execute(text("""
                UPDATE productos 
                SET propietario_id = usuario_id 
                WHERE propietario_id IS NULL AND usuario_id IS NOT NULL
            """))
            print("Copied data from usuario_id to propietario_id")
            
            # Add new fields to negocios table
            connection.execute(text("""
                ALTER TABLE negocios 
                ADD COLUMN IF NOT EXISTS propietario_id UUID
            """))
            print("Added propietario_id field to negocios")
            
            # Copy data from usuario_id to propietario_id in negocios if propietario_id is null
            connection.execute(text("""
                UPDATE negocios 
                SET propietario_id = usuario_id 
                WHERE propietario_id IS NULL AND usuario_id IS NOT NULL
            """))
            print("Copied data from usuario_id to propietario_id in negocios")
            
            # Add new fields to usuarios table
            connection.execute(text("""
                ALTER TABLE usuarios 
                ADD COLUMN IF NOT EXISTS hashed_password VARCHAR
            """))
            print("Added hashed_password field to usuarios")
            
            connection.execute(text("""
                ALTER TABLE usuarios 
                ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE
            """))
            print("Added is_active field to usuarios")
            
            connection.execute(text("""
                ALTER TABLE usuarios 
                ADD COLUMN IF NOT EXISTS curriculum_vitae TEXT
            """))
            print("Added curriculum_vitae field to usuarios")
            
            # Add new fields to publicidades table
            connection.execute(text("""
                ALTER TABLE publicidades 
                ADD COLUMN IF NOT EXISTS nombre VARCHAR NOT NULL DEFAULT 'Publicidad'
            """))
            print("Added nombre field to publicidades")
            
            connection.execute(text("""
                ALTER TABLE publicidades 
                ADD COLUMN IF NOT EXISTS item_publicitado_tipo VARCHAR NOT NULL DEFAULT 'producto'
            """))
            print("Added item_publicitado_tipo field to publicidades")
            
            # Add fecha_asociacion to producto_insumo table
            connection.execute(text("""
                ALTER TABLE producto_insumo 
                ADD COLUMN IF NOT EXISTS fecha_asociacion TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            """))
            print("Added fecha_asociacion field to producto_insumo")
            
            # Commit the changes
            connection.commit()
            print("Migration completed successfully!")
            
        except Exception as e:
            print(f"Error during migration: {e}")
            connection.rollback()
            raise

if __name__ == "__main__":
    migrate_to_new_models() 