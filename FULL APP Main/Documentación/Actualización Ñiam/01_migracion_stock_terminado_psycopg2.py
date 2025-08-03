#!/usr/bin/env python3
"""
Script de Migración Directo: Añadir campo stock_terminado a productos
Capítulo Ñiam - SOUP Emprendimientos

Este script usa psycopg2 y las credenciales del archivo utilidades de SOUP.txt
para añadir el campo stock_terminado a la tabla productos y asignar un valor por defecto.

Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import psycopg2
from psycopg2 import sql
from datetime import datetime

# Credenciales extraídas de utilidades de SOUP.txt
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'soup_app_db',
    'user': 'soupuser',
    'password': 'souppass'
}

def conectar_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Conexión a la base de datos establecida")
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        exit(1)

def campo_existe(conn, tabla, campo):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 1 FROM information_schema.columns
                WHERE table_name=%s AND column_name=%s
            """, (tabla, campo))
            return cur.fetchone() is not None
    except Exception as e:
        print(f"Error al verificar existencia de campo: {e}")
        return False

def añadir_campo_stock_terminado(conn):
    if campo_existe(conn, 'productos', 'stock_terminado'):
        print("El campo 'stock_terminado' ya existe en la tabla productos")
        return True
    try:
        with conn.cursor() as cur:
            cur.execute("""
                ALTER TABLE productos
                ADD COLUMN stock_terminado FLOAT DEFAULT 0.0
            """)
            try:
                cur.execute("""
                    COMMENT ON COLUMN productos.stock_terminado IS
                    'Cantidad de productos terminados disponibles para venta'
                """)
            except:
                print("No se pudo añadir comentario al campo (no crítico)")
        conn.commit()
        print("Campo 'stock_terminado' añadido exitosamente")
        return True
    except Exception as e:
        print(f"Error al añadir campo: {e}")
        conn.rollback()
        return False

def asignar_stock_por_defecto(conn, valor_defecto=50):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE productos SET stock_terminado = %s
            """, (valor_defecto,))
        conn.commit()
        print(f"Stock por defecto ({valor_defecto}) asignado a todos los productos")
        return True
    except Exception as e:
        print(f"Error al asignar stock por defecto: {e}")
        conn.rollback()
        return False

def mostrar_ejemplos(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT nombre, stock_terminado FROM productos LIMIT 5
            """)
            rows = cur.fetchall()
            print("Ejemplos de productos con stock_terminado:")
            for nombre, stock in rows:
                print(f"  - {nombre}: {stock}")
    except Exception as e:
        print(f"Error al mostrar ejemplos: {e}")

def main():
    print("Iniciando migración directa de stock_terminado")
    print("="*60)
    conn = conectar_db()
    try:
        print("\nPaso 1: Añadiendo campo stock_terminado...")
        if not añadir_campo_stock_terminado(conn):
            print("Fallo al añadir campo stock_terminado")
            return
        print("\nPaso 2: Asignando stock por defecto a todos los productos...")
        if not asignar_stock_por_defecto(conn, valor_defecto=50):
            print("Fallo al asignar stock por defecto")
            return
        print("\nPaso 3: Mostrando ejemplos...")
        mostrar_ejemplos(conn)
        print("\nMigración completada exitosamente")
        print("Fecha:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    finally:
        conn.close()
        print("Conexión cerrada")

if __name__ == "__main__":
    main() 