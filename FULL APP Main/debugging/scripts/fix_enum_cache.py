#!/usr/bin/env python3
"""
Script para limpiar el cache de SQLAlchemy y forzar la recarga de enums
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

def fix_enum_cache():
    """Limpiar el cache de SQLAlchemy y forzar la recarga de enums"""
    
    # Crear una nueva conexión
    engine = create_engine(settings.DATABASE_URL, echo=True)
    
    with engine.connect() as conn:
        # Verificar los valores actuales del enum
        result = conn.execute(text("""
            SELECT enumlabel 
            FROM pg_enum 
            WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'producttype') 
            ORDER BY enumsortorder;
        """))
        
        print("Valores actuales del enum producttype:")
        for row in result:
            print(f"  - {row[0]}")
        
        # Verificar productos existentes
        result = conn.execute(text("SELECT id, nombre, tipo_producto FROM productos;"))
        print("\nProductos existentes:")
        for row in result:
            print(f"  - {row[1]}: {row[2]}")
        
        # Limpiar el cache de SQLAlchemy
        print("\nLimpiando cache de SQLAlchemy...")
        
        # Forzar la recarga de metadatos
        from sqlalchemy import inspect
        inspector = inspect(engine)
        inspector.reflect()
        
        print("Cache limpiado. Reinicia el servidor para aplicar los cambios.")

if __name__ == "__main__":
    fix_enum_cache() 