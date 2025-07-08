#!/usr/bin/env python3
"""
Script para verificar el estado actual del enum producttype
"""

import psycopg2

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'soup_app_db',
    'user': 'soupuser',
    'password': 'souppass'
}

def check_enum_status():
    """Verificar el estado actual del enum producttype"""
    
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("=== VERIFICACIÓN DEL ENUM PRODUCTTYPE ===\n")
        
        # 1. Verificar valores actuales del enum
        cursor.execute("""
            SELECT enumlabel 
            FROM pg_enum 
            WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'producttype') 
            ORDER BY enumsortorder;
        """)
        
        enum_values = [row[0] for row in cursor.fetchall()]
        print(f"Valores del enum producttype: {enum_values}")
        
        # 2. Verificar productos existentes
        cursor.execute("SELECT id, nombre, tipo_producto FROM productos;")
        products = cursor.fetchall()
        print(f"\nProductos existentes ({len(products)}):")
        for product in products:
            print(f"  - {product[1]}: {product[2]}")
        
        # 3. Verificar si hay productos con valores inválidos
        print(f"\nVerificando productos con valores inválidos...")
        for product in products:
            if product[2] not in enum_values:
                print(f"  ❌ {product[1]}: {product[2]} (INVÁLIDO)")
            else:
                print(f"  ✅ {product[1]}: {product[2]} (VÁLIDO)")
        
        cursor.close()
        conn.close()
        
        print(f"\n=== RESUMEN ===")
        print(f"Enum values: {enum_values}")
        print(f"Products count: {len(products)}")
        
        # Verificar si todos los productos tienen valores válidos
        invalid_products = [p for p in products if p[2] not in enum_values]
        if invalid_products:
            print(f"❌ Hay {len(invalid_products)} productos con valores inválidos")
        else:
            print("✅ Todos los productos tienen valores válidos")
        
    except Exception as e:
        print(f"Error: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_enum_status() 