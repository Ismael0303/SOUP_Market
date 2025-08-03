#!/usr/bin/env python3
"""
Script simple para corregir fecha_actualizacion en productos
"""

import psycopg2
import os

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'soup_app_db',
    'user': 'soupuser',
    'password': 'soup123',
    'client_encoding': 'utf8'
}

def fix_fecha_actualizacion():
    """Corregir el problema de fecha_actualizacion"""
    try:
        print("🔧 Corrigiendo fecha_actualizacion en tabla productos...")
        
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Agregar valor por defecto a fecha_actualizacion
        cursor.execute("ALTER TABLE productos ALTER COLUMN fecha_actualizacion SET DEFAULT CURRENT_TIMESTAMP")
        print("✅ Valor por defecto agregado a fecha_actualizacion")
        
        # Actualizar registros existentes que tengan fecha_actualizacion NULL
        cursor.execute("UPDATE productos SET fecha_actualizacion = CURRENT_TIMESTAMP WHERE fecha_actualizacion IS NULL")
        
        updated_rows = cursor.rowcount
        print(f"✅ Actualizados {updated_rows} registros con fecha_actualizacion NULL")
        
        conn.commit()
        print("✅ Corrección aplicada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'conn' in locals():
            conn.rollback()
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    fix_fecha_actualizacion() 