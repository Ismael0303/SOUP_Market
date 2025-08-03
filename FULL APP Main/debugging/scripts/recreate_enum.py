#!/usr/bin/env python3
"""
Script para recrear el enum producttype en la base de datos
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'soup_app_db',
    'user': 'soupuser',
    'password': 'souppass'
}

def recreate_producttype_enum():
    """Recrear el enum producttype en la base de datos"""
    
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("Conectado a la base de datos.")
        
        # 1. Verificar valores actuales del enum
        cursor.execute("""
            SELECT enumlabel 
            FROM pg_enum 
            WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'producttype') 
            ORDER BY enumsortorder;
        """)
        
        current_values = [row[0] for row in cursor.fetchall()]
        print(f"Valores actuales del enum: {current_values}")
        
        # 2. Verificar productos existentes
        cursor.execute("SELECT id, nombre, tipo_producto FROM productos;")
        products = cursor.fetchall()
        print(f"Productos existentes: {len(products)}")
        for product in products:
            print(f"  - {product[1]}: {product[2]}")
        
        # 3. Crear un nuevo enum con los valores correctos
        print("\nRecreando el enum producttype...")
        
        # Primero, crear un nuevo tipo temporal
        cursor.execute("""
            CREATE TYPE producttype_new AS ENUM (
                'PHYSICAL_GOOD',
                'SERVICE_BY_HOUR', 
                'SERVICE_BY_PROJECT',
                'DIGITAL_GOOD'
            );
        """)
        
        # 4. Actualizar la columna para usar el nuevo tipo
        cursor.execute("""
            ALTER TABLE productos 
            ALTER COLUMN tipo_producto TYPE producttype_new 
            USING tipo_producto::text::producttype_new;
        """)
        
        # 5. Eliminar el tipo viejo y renombrar el nuevo
        cursor.execute("DROP TYPE producttype;")
        cursor.execute("ALTER TYPE producttype_new RENAME TO producttype;")
        
        print("Enum producttype recreado exitosamente!")
        
        # 6. Verificar el resultado
        cursor.execute("""
            SELECT enumlabel 
            FROM pg_enum 
            WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'producttype') 
            ORDER BY enumsortorder;
        """)
        
        new_values = [row[0] for row in cursor.fetchall()]
        print(f"Nuevos valores del enum: {new_values}")
        
        cursor.close()
        conn.close()
        
        print("\n¡Enum recreado exitosamente! Reinicia el servidor para aplicar los cambios.")
        
    except Exception as e:
        print(f"Error: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    recreate_producttype_enum() 