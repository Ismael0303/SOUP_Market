#!/usr/bin/env python3
"""
Script para corregir la columna fecha_actualizacion en la tabla usuarios.
Agrega un valor por defecto para evitar errores de NOT NULL.
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
    
    print("🔧 Corrigiendo columna fecha_actualizacion...")
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Verificar el estado actual de fecha_actualizacion
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'usuarios' 
            AND column_name = 'fecha_actualizacion';
        """))
        
        row = result.fetchone()
        if row:
            print(f"📋 Estado actual: {row[0]} | {row[1]} | Nullable: {row[2]} | Default: {row[3]}")
            
            if row[3] is None:
                print("⚠️  Columna fecha_actualizacion no tiene valor por defecto")
                
                # Agregar valor por defecto
                print("🔄 Agregando valor por defecto...")
                db.execute(text("""
                    ALTER TABLE usuarios 
                    ALTER COLUMN fecha_actualizacion 
                    SET DEFAULT now();
                """))
                db.commit()
                print("✅ Valor por defecto agregado exitosamente")
                
                # Verificar el cambio
                result = db.execute(text("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'usuarios' 
                    AND column_name = 'fecha_actualizacion';
                """))
                
                row = result.fetchone()
                print(f"📋 Estado final: {row[0]} | {row[1]} | Nullable: {row[2]} | Default: {row[3]}")
            else:
                print("✅ Columna fecha_actualizacion ya tiene valor por defecto")
        
        print("\n✅ Corrección completada!")
        
    except Exception as e:
        print(f"❌ Error corrigiendo fecha_actualizacion: {e}")
        db.rollback()
    finally:
        db.close()
        
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1) 