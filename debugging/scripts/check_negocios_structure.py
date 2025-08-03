#!/usr/bin/env python3
"""
Script para verificar la estructura de la tabla negocios.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))
os.chdir(backend_path)

try:
    from app.database import get_db, engine
    from sqlalchemy import text
    
    print("🔍 Verificando estructura de la tabla negocios...")
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Verificar estructura de la tabla negocios
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'negocios'
            ORDER BY ordinal_position;
        """))
        
        print("\n📋 Estructura de la tabla 'negocios':")
        print("=" * 60)
        for row in result:
            print(f"Columna: {row[0]:<25} | Tipo: {row[1]:<20} | Nullable: {row[2]:<5} | Default: {row[3]}")
        
        # Verificar datos existentes
        result = db.execute(text("""
            SELECT id, nombre, propietario_id, tipo_negocio
            FROM negocios
            ORDER BY nombre;
        """))
        
        print("\n🏢 Negocios existentes:")
        print("=" * 60)
        for row in result:
            print(f"ID: {row[0]}")
            print(f"Nombre: {row[1]}")
            print(f"Propietario ID: {row[2]}")
            print(f"Tipo: {row[3]}")
            print("-" * 30)
        
        print(f"\n✅ Verificación completada!")
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
    finally:
        db.close()
        
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1) 