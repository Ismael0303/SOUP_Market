#!/usr/bin/env python3
"""
Script genérico para debugging de base de datos
Autor: Asistente AI
Fecha: 7 de Julio de 2025
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import os

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'soup_app_db',
    'user': 'soupuser',
    'password': 'souppass'
}

def connect_db():
    """Conectar a la base de datos"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except Exception as e:
        print(f"❌ Error conectando a BD: {e}")
        return None

def check_table_exists(conn, table_name):
    """Verificar si una tabla existe"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = %s
        );
    """, (table_name,))
    exists = cursor.fetchone()[0]
    cursor.close()
    return exists

def check_enum_values(conn, table_name, column_name):
    """Verificar valores únicos en una columna enum"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT DISTINCT {column_name} FROM {table_name};")
    values = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return values

def check_invalid_data(conn, table_name, conditions):
    """Verificar datos inválidos según condiciones"""
    cursor = conn.cursor()
    where_clause = " AND ".join(conditions)
    query = f"SELECT COUNT(*) FROM {table_name} WHERE {where_clause};"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    cursor.close()
    return count

def debug_database():
    """Función principal de debugging"""
    print("🔍 DEBUGGING DE BASE DE DATOS")
    print("=" * 50)
    
    conn = connect_db()
    if not conn:
        return
    
    try:
        # 1. Verificar tablas principales
        tables = ['usuarios', 'negocios', 'productos', 'insumos']
        print("\n📋 VERIFICACIÓN DE TABLAS:")
        for table in tables:
            exists = check_table_exists(conn, table)
            status = "✅" if exists else "❌"
            print(f"{status} Tabla '{table}': {'Existe' if exists else 'No existe'}")
        
        # 2. Verificar enums
        print("\n🔤 VERIFICACIÓN DE ENUMS:")
        
        # Negocios
        if check_table_exists(conn, 'negocios'):
            business_types = check_enum_values(conn, 'negocios', 'tipo_negocio')
            print(f"📊 Tipos de negocio: {business_types}")
        
        # Productos
        if check_table_exists(conn, 'productos'):
            product_types = check_enum_values(conn, 'productos', 'tipo_producto')
            print(f"📦 Tipos de producto: {product_types}")
        
        # 3. Verificar datos inválidos
        print("\n⚠️ VERIFICACIÓN DE DATOS INVÁLIDOS:")
        
        if check_table_exists(conn, 'productos'):
            invalid_products = check_invalid_data(conn, 'productos', [
                'precio = 0.0 OR precio IS NULL',
                'negocio_id IS NULL'
            ])
            print(f"📦 Productos con datos inválidos: {invalid_products}")
        
        if check_table_exists(conn, 'usuarios'):
            users_no_password = check_invalid_data(conn, 'usuarios', [
                'hashed_password IS NULL OR hashed_password = \'\''
            ])
            print(f"👤 Usuarios sin contraseña: {users_no_password}")
        
        # 4. Estadísticas generales
        print("\n📊 ESTADÍSTICAS GENERALES:")
        cursor = conn.cursor()
        
        for table in tables:
            if check_table_exists(conn, table):
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                print(f"📈 {table.capitalize()}: {count} registros")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error durante debugging: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    debug_database() 