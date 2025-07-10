# debugging/migrations/migrate_add_plugins.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from sqlalchemy import create_engine, text
from app.core.config import settings

def migrate_add_plugins():
    """Migración para añadir campo plugins_activos a la tabla usuarios"""
    
    # Crear conexión a la base de datos
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            print("🔧 Iniciando migración: Añadir campo plugins_activos...")
            
            # Verificar si la columna ya existe
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'usuarios' 
                AND column_name = 'plugins_activos'
            """)
            
            result = conn.execute(check_query)
            column_exists = result.fetchone() is not None
            
            if column_exists:
                print("✅ La columna plugins_activos ya existe")
                return
            
            # Añadir la columna plugins_activos
            add_column_query = text("""
                ALTER TABLE usuarios 
                ADD COLUMN plugins_activos TEXT[] DEFAULT '{}'
            """)
            
            conn.execute(add_column_query)
            conn.commit()
            
            print("✅ Columna plugins_activos añadida exitosamente")
            
            # Verificar que la columna se creó correctamente
            verify_query = text("""
                SELECT column_name, data_type, column_default
                FROM information_schema.columns 
                WHERE table_name = 'usuarios' 
                AND column_name = 'plugins_activos'
            """)
            
            result = conn.execute(verify_query)
            column_info = result.fetchone()
            
            if column_info:
                print(f"✅ Verificación exitosa:")
                print(f"   - Columna: {column_info[0]}")
                print(f"   - Tipo: {column_info[1]}")
                print(f"   - Default: {column_info[2]}")
            else:
                print("❌ Error: La columna no se creó correctamente")
                
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        raise
    finally:
        engine.dispose()

if __name__ == "__main__":
    migrate_add_plugins() 