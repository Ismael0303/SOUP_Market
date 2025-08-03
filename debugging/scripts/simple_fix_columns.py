#!/usr/bin/env python3
"""
Script simple para añadir columna faltante
"""

import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "soup_app_db",
    "user": "soupuser",
    "password": "soup123"
}

def add_missing_column():
    """Añadir columna margen_ganancia_real"""
    print("Fixing missing column: margen_ganancia_real")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Add the missing column
        cursor.execute("""
            ALTER TABLE productos 
            ADD COLUMN margen_ganancia_real DOUBLE PRECISION
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Column margen_ganancia_real added successfully")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    add_missing_column() 