#!/usr/bin/env python3
"""
Script para verificar la estructura de la tabla productos y corregir problemas
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'soup_app_db',
    'user': 'soupuser',
    'password': 'soup123'
}

def check_productos_structure():
    """Verificar la estructura de la tabla productos"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("🔍 VERIFICANDO ESTRUCTURA DE TABLA PRODUCTOS")
        print("=" * 50)
        
        # Verificar estructura de la tabla
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'productos' 
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        print("📋 Estructura actual de la tabla productos:")
        for col in columns:
            print(f"  - {col['column_name']}: {col['data_type']} (nullable: {col['is_nullable']}, default: {col['column_default']})")
        
        # Verificar si fecha_actualizacion tiene valor por defecto
        fecha_actualizacion_col = next((col for col in columns if col['column_name'] == 'fecha_actualizacion'), None)
        
        if fecha_actualizacion_col:
            print(f"\n📅 fecha_actualizacion:")
            print(f"  - Tipo: {fecha_actualizacion_col['data_type']}")
            print(f"  - Nullable: {fecha_actualizacion_col['is_nullable']}")
            print(f"  - Default: {fecha_actualizacion_col['column_default']}")
            
            if fecha_actualizacion_col['is_nullable'] == 'NO' and fecha_actualizacion_col['column_default'] is None:
                print("❌ PROBLEMA: fecha_actualizacion es NOT NULL pero no tiene valor por defecto")
                return False
            else:
                print("✅ fecha_actualizacion está configurada correctamente")
                return True
        else:
            print("❌ ERROR: No se encontró la columna fecha_actualizacion")
            return False
            
    except Exception as e:
        print(f"❌ Error al verificar estructura: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def fix_fecha_actualizacion():
    """Corregir el problema de fecha_actualizacion"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("\n🔧 CORRIGIENDO fecha_actualizacion")
        print("=" * 40)
        
        # Agregar valor por defecto a fecha_actualizacion
        cursor.execute("""
            ALTER TABLE productos 
            ALTER COLUMN fecha_actualizacion SET DEFAULT CURRENT_TIMESTAMP
        """)
        
        # Actualizar registros existentes que tengan fecha_actualizacion NULL
        cursor.execute("""
            UPDATE productos 
            SET fecha_actualizacion = CURRENT_TIMESTAMP 
            WHERE fecha_actualizacion IS NULL
        """)
        
        updated_rows = cursor.rowcount
        print(f"✅ Actualizados {updated_rows} registros con fecha_actualizacion NULL")
        
        conn.commit()
        print("✅ Corrección aplicada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al corregir fecha_actualizacion: {e}")
        if 'conn' in locals():
            conn.rollback()
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def test_product_creation():
    """Probar la creación de un producto después de la corrección"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("\n🧪 PROBANDO CREACIÓN DE PRODUCTO")
        print("=" * 40)
        
        # Insertar un producto de prueba
        cursor.execute("""
            INSERT INTO productos (
                nombre, descripcion, precio, tipo_producto, negocio_id, propietario_id,
                stock_terminado, precio_venta, margen_ganancia_sugerido,
                rating_promedio, reviews_count
            ) VALUES (
                'Test Product Fix', 'Producto de prueba para verificar corrección',
                10.0, 'PHYSICAL_GOOD', 
                (SELECT id FROM negocios LIMIT 1),
                (SELECT id FROM usuarios LIMIT 1),
                100.0, 15.0, 50.0, 0.0, 0
            ) RETURNING id, fecha_creacion, fecha_actualizacion
        """)
        
        result = cursor.fetchone()
        if result:
            print(f"✅ Producto creado exitosamente:")
            print(f"  - ID: {result[0]}")
            print(f"  - fecha_creacion: {result[1]}")
            print(f"  - fecha_actualizacion: {result[2]}")
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"❌ Error al probar creación: {e}")
        if 'conn' in locals():
            conn.rollback()
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def main():
    """Función principal"""
    print("🔧 SCRIPT DE CORRECCIÓN DE TABLA PRODUCTOS")
    print("=" * 50)
    
    # Verificar estructura
    if not check_productos_structure():
        print("\n🔧 Aplicando corrección...")
        if fix_fecha_actualizacion():
            print("\n✅ Verificando corrección...")
            if check_productos_structure():
                print("\n🧪 Probando creación de producto...")
                test_product_creation()
            else:
                print("❌ La corrección no funcionó correctamente")
        else:
            print("❌ No se pudo aplicar la corrección")
    else:
        print("\n✅ La tabla productos está correctamente configurada")
        print("\n🧪 Probando creación de producto...")
        test_product_creation()

if __name__ == "__main__":
    main() 