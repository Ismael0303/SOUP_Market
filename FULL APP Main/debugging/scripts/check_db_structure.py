#!/usr/bin/env python3
"""
Script para verificar la estructura de la base de datos.
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
    
    print("🔍 Verificando estructura de la base de datos...")
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Verificar estructura de la tabla usuarios
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'usuarios'
            ORDER BY ordinal_position;
        """))
        
        print("\n📋 Estructura de la tabla 'usuarios':")
        print("=" * 60)
        for row in result:
            print(f"Columna: {row[0]:<20} | Tipo: {row[1]:<15} | Nullable: {row[2]:<5} | Default: {row[3]}")
        
        # Verificar si existe la columna password_hash o hashed_password
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'usuarios' 
            AND column_name IN ('password_hash', 'hashed_password');
        """))
        
        password_columns = [row[0] for row in result]
        print(f"\n🔑 Columnas de contraseña encontradas: {password_columns}")
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
    finally:
        db.close()
        
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1) 