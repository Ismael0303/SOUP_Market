#!/usr/bin/env python3
"""
Script de migración para añadir la columna tipo_negocio a la tabla negocios.
Este script debe ejecutarse una sola vez para actualizar la base de datos existente.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

# Añadir el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

def migrate_add_tipo_negocio():
    """Añade la columna tipo_negocio a la tabla negocios"""
    
    # Crear conexión a la base de datos
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Verificar si la columna ya existe
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'negocios' 
                AND column_name = 'tipo_negocio'
            """)
            
            result = conn.execute(check_query)
            column_exists = result.fetchone() is not None
            
            if column_exists:
                print("✅ La columna 'tipo_negocio' ya existe en la tabla 'negocios'")
                return
            
            # Añadir la columna tipo_negocio
            print("🔄 Añadiendo columna 'tipo_negocio' a la tabla 'negocios'...")
            
            # Primero, crear el tipo enum si no existe
            create_enum_query = text("""
                DO $$ 
                BEGIN 
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'businesstype') THEN
                        CREATE TYPE businesstype AS ENUM ('productos', 'servicios', 'ambos');
                    END IF;
                END $$;
            """)
            
            conn.execute(create_enum_query)
            conn.commit()
            
            # Añadir la columna con valor por defecto
            alter_query = text("""
                ALTER TABLE negocios 
                ADD COLUMN tipo_negocio businesstype NOT NULL DEFAULT 'productos'
            """)
            
            conn.execute(alter_query)
            conn.commit()
            
            print("✅ Columna 'tipo_negocio' añadida exitosamente a la tabla 'negocios'")
            print("   - Tipo: businesstype (ENUM: 'productos', 'servicios', 'ambos')")
            print("   - Valor por defecto: 'productos'")
            
    except ProgrammingError as e:
        print(f"❌ Error al ejecutar la migración: {e}")
        print("   Asegúrate de que tienes permisos para modificar la base de datos")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Iniciando migración para añadir columna tipo_negocio...")
    print(f"📊 Base de datos: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Local'}")
    print()
    
    success = migrate_add_tipo_negocio()
    
    if success:
        print()
        print("🎉 Migración completada exitosamente!")
        print("   La aplicación ahora debería funcionar correctamente.")
    else:
        print()
        print("💥 La migración falló. Revisa los errores arriba.")
        sys.exit(1) 