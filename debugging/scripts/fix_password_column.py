#!/usr/bin/env python3
"""
Script para corregir la estructura de la tabla usuarios.
Elimina la columna password_hash duplicada y mantiene solo hashed_password.
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
    
    print("🔧 Corrigiendo estructura de la tabla usuarios...")
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Verificar si existe la columna password_hash
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'usuarios' 
            AND column_name = 'password_hash';
        """))
        
        if result.fetchone():
            print("⚠️  Encontrada columna password_hash duplicada")
            
            # Verificar si hay datos en password_hash que necesiten migrarse
            result = db.execute(text("""
                SELECT COUNT(*) as count 
                FROM usuarios 
                WHERE password_hash IS NOT NULL;
            """))
            
            count = result.fetchone()[0]
            print(f"📊 Registros con password_hash: {count}")
            
            if count > 0:
                # Migrar datos de password_hash a hashed_password
                print("🔄 Migrando datos de password_hash a hashed_password...")
                db.execute(text("""
                    UPDATE usuarios 
                    SET hashed_password = password_hash 
                    WHERE password_hash IS NOT NULL 
                    AND hashed_password IS NULL;
                """))
                db.commit()
                print("✅ Datos migrados exitosamente")
            
            # Eliminar la columna password_hash
            print("🗑️  Eliminando columna password_hash...")
            db.execute(text("ALTER TABLE usuarios DROP COLUMN password_hash;"))
            db.commit()
            print("✅ Columna password_hash eliminada")
            
        else:
            print("✅ No se encontró columna password_hash duplicada")
        
        # Verificar estructura final
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'usuarios' 
            AND column_name IN ('hashed_password', 'password_hash')
            ORDER BY column_name;
        """))
        
        print("\n📋 Estado final de columnas de contraseña:")
        for row in result:
            print(f"Columna: {row[0]:<15} | Tipo: {row[1]:<15} | Nullable: {row[2]}")
        
        print("\n✅ Estructura de tabla corregida exitosamente!")
        
    except Exception as e:
        print(f"❌ Error corrigiendo estructura: {e}")
        db.rollback()
    finally:
        db.close()
        
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1) 