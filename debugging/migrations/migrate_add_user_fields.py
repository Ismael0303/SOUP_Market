#!/usr/bin/env python3
"""
Migración para agregar nuevos campos al modelo Usuario
- plugins_activos
- rol
- negocio_asignado_id
- fecha_contratacion
- salario
- horario_trabajo
- permisos_especiales
"""

import os
from sqlalchemy import create_engine, text

def migrate_add_user_fields():
    """Agrega los nuevos campos al modelo Usuario"""
    # Obtener la URL de la base de datos desde la variable de entorno
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("La variable de entorno DATABASE_URL no está definida. Por favor, expórtala antes de ejecutar la migración.")
    engine = create_engine(db_url)
    print("🔄 Iniciando migración para agregar campos al modelo Usuario...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'usuarios' 
                AND column_name IN ('plugins_activos', 'rol', 'negocio_asignado_id', 'fecha_contratacion', 'salario', 'horario_trabajo', 'permisos_especiales')
            """))
            existing_columns = [row[0] for row in result.fetchall()]
            print(f"📋 Columnas existentes: {existing_columns}")
            if 'plugins_activos' not in existing_columns:
                print("➕ Agregando columna plugins_activos...")
                conn.execute(text("ALTER TABLE usuarios ADD COLUMN plugins_activos TEXT[] DEFAULT '{}'"))
                print("✅ Columna plugins_activos agregada")
            if 'rol' not in existing_columns:
                print("➕ Agregando columna rol...")
                conn.execute(text("ALTER TABLE usuarios ADD COLUMN rol VARCHAR(50)"))
                print("✅ Columna rol agregada")
            if 'negocio_asignado_id' not in existing_columns:
                print("➕ Agregando columna negocio_asignado_id...")
                conn.execute(text("ALTER TABLE usuarios ADD COLUMN negocio_asignado_id UUID REFERENCES negocios(id)"))
                print("✅ Columna negocio_asignado_id agregada")
            if 'fecha_contratacion' not in existing_columns:
                print("➕ Agregando columna fecha_contratacion...")
                conn.execute(text("ALTER TABLE usuarios ADD COLUMN fecha_contratacion DATE"))
                print("✅ Columna fecha_contratacion agregada")
            if 'salario' not in existing_columns:
                print("➕ Agregando columna salario...")
                conn.execute(text("ALTER TABLE usuarios ADD COLUMN salario DECIMAL(10,2)"))
                print("✅ Columna salario agregada")
            if 'horario_trabajo' not in existing_columns:
                print("➕ Agregando columna horario_trabajo...")
                conn.execute(text("ALTER TABLE usuarios ADD COLUMN horario_trabajo VARCHAR(100)"))
                print("✅ Columna horario_trabajo agregada")
            if 'permisos_especiales' not in existing_columns:
                print("➕ Agregando columna permisos_especiales...")
                conn.execute(text("ALTER TABLE usuarios ADD COLUMN permisos_especiales TEXT[] DEFAULT '{}'"))
                print("✅ Columna permisos_especiales agregada")
            conn.commit()
            print("🎉 Migración completada exitosamente!")
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'usuarios' 
                ORDER BY ordinal_position
            """))
            all_columns = [row[0] for row in result.fetchall()]
            print(f"📋 Todas las columnas de usuarios: {all_columns}")
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        raise

if __name__ == "__main__":
    migrate_add_user_fields() 