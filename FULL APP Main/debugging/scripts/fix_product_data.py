#!/usr/bin/env python3
"""
Script para corregir los datos de productos en la base de datos
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

def fix_product_data():
    """Corregir los datos de productos en la base de datos"""
    
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("=== CORRIGIENDO DATOS DE PRODUCTOS ===\n")
        
        # 1. Verificar datos actuales
        cursor.execute("SELECT id, nombre, precio, negocio_id FROM productos;")
        products = cursor.fetchall()
        print("Datos actuales de productos:")
        for product in products:
            print(f"  - {product[1]}: precio={product[2]}, negocio_id={product[3]}")
        
        # 2. Obtener un negocio_id válido
        cursor.execute("SELECT id FROM negocios LIMIT 1;")
        business_result = cursor.fetchone()
        if business_result:
            business_id = business_result[0]
            print(f"\nUsando negocio_id: {business_id}")
        else:
            print("❌ No hay negocios en la base de datos")
            return
        
        # 3. Actualizar productos
        print("\nActualizando productos...")
        
        # Actualizar precios y negocio_id
        cursor.execute("""
            UPDATE productos 
            SET precio = 10.0, negocio_id = %s 
            WHERE precio = 0.0 OR negocio_id IS NULL;
        """, (business_id,))
        
        updated_count = cursor.rowcount
        print(f"Productos actualizados: {updated_count}")
        
        # 4. Verificar datos después de la actualización
        cursor.execute("SELECT id, nombre, precio, negocio_id FROM productos;")
        products_after = cursor.fetchall()
        print("\nDatos después de la actualización:")
        for product in products_after:
            print(f"  - {product[1]}: precio={product[2]}, negocio_id={product[3]}")
        
        cursor.close()
        conn.close()
        
        print(f"\n✅ Datos de productos corregidos exitosamente!")
        
    except Exception as e:
        print(f"Error: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    fix_product_data() 