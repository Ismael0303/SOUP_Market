#!/usr/bin/env python3
"""
Script para verificar y reparar la integridad de la base de datos del sistema POS
Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import psycopg2
from psycopg2 import sql
import os

# Configuración de conexión (ajusta según tus credenciales reales)
DB_NAME = 'soup_app_db'
DB_USER = 'soupuser'
DB_PASSWORD = 'souppass'
DB_HOST = 'localhost'
DB_PORT = '5432'

def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def check_and_fix_products_table(cur, conn):
    print("\n🔍 Verificando tabla productos...")
    # Verificar existencia de campo stock_terminado
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'productos' AND column_name = 'stock_terminado';
    """)
    if not cur.fetchone():
        print("❌ Campo 'stock_terminado' no existe. Añadiendo...")
        cur.execute("ALTER TABLE productos ADD COLUMN stock_terminado FLOAT DEFAULT 0.0;")
        conn.commit()
        print("✅ Campo 'stock_terminado' añadido.")
    else:
        print("✅ Campo 'stock_terminado' existe.")

    # Verificar valores nulos en campos obligatorios
    cur.execute("SELECT COUNT(*) FROM productos WHERE nombre IS NULL OR precio IS NULL OR tipo_producto IS NULL OR negocio_id IS NULL OR propietario_id IS NULL;")
    n_invalid = cur.fetchone()[0]
    if n_invalid > 0:
        print(f"⚠️ Hay {n_invalid} productos con campos obligatorios nulos. Eliminando...")
        cur.execute("DELETE FROM productos WHERE nombre IS NULL OR precio IS NULL OR tipo_producto IS NULL OR negocio_id IS NULL OR propietario_id IS NULL;")
        conn.commit()
        print("✅ Productos inválidos eliminados.")
    else:
        print("✅ Todos los productos tienen campos obligatorios completos.")

    # Verificar stock_terminado nulo
    cur.execute("SELECT COUNT(*) FROM productos WHERE stock_terminado IS NULL;")
    n_null_stock = cur.fetchone()[0]
    if n_null_stock > 0:
        print(f"⚠️ Hay {n_null_stock} productos con stock_terminado nulo. Corrigiendo a 0...")
        cur.execute("UPDATE productos SET stock_terminado = 0 WHERE stock_terminado IS NULL;")
        conn.commit()
        print("✅ stock_terminado corregido a 0 donde era nulo.")
    else:
        print("✅ Todos los productos tienen stock_terminado definido.")

    # Verificar relaciones con negocio y propietario
    cur.execute("""
        DELETE FROM productos
        WHERE negocio_id NOT IN (SELECT id FROM negocios)
           OR propietario_id NOT IN (SELECT id FROM usuarios);
    """)
    conn.commit()
    print("✅ Productos huérfanos eliminados (sin negocio o propietario válido).")

def check_and_fix_insumos_table(cur, conn):
    print("\n🔍 Verificando tabla insumos...")
    # Verificar valores nulos en campos obligatorios
    cur.execute("SELECT COUNT(*) FROM insumos WHERE nombre IS NULL OR cantidad_disponible IS NULL OR unidad_medida_compra IS NULL OR costo_unitario_compra IS NULL OR usuario_id IS NULL;")
    n_invalid = cur.fetchone()[0]
    if n_invalid > 0:
        print(f"⚠️ Hay {n_invalid} insumos con campos obligatorios nulos. Eliminando...")
        cur.execute("DELETE FROM insumos WHERE nombre IS NULL OR cantidad_disponible IS NULL OR unidad_medida_compra IS NULL OR costo_unitario_compra IS NULL OR usuario_id IS NULL;")
        conn.commit()
        print("✅ Insumos inválidos eliminados.")
    else:
        print("✅ Todos los insumos tienen campos obligatorios completos.")

    # Verificar relaciones con usuario
    cur.execute("""
        DELETE FROM insumos
        WHERE usuario_id NOT IN (SELECT id FROM usuarios);
    """)
    conn.commit()
    print("✅ Insumos huérfanos eliminados (sin usuario válido).")

def check_and_fix_negocios_table(cur, conn):
    print("\n🔍 Verificando tabla negocios...")
    # Verificar valores nulos en campos obligatorios
    cur.execute("SELECT COUNT(*) FROM negocios WHERE nombre IS NULL OR propietario_id IS NULL OR tipo_negocio IS NULL;")
    n_invalid = cur.fetchone()[0]
    if n_invalid > 0:
        print(f"⚠️ Hay {n_invalid} negocios con campos obligatorios nulos. Eliminando...")
        cur.execute("DELETE FROM negocios WHERE nombre IS NULL OR propietario_id IS NULL OR tipo_negocio IS NULL;")
        conn.commit()
        print("✅ Negocios inválidos eliminados.")
    else:
        print("✅ Todos los negocios tienen campos obligatorios completos.")

    # Verificar relaciones con usuario
    cur.execute("""
        DELETE FROM negocios
        WHERE propietario_id NOT IN (SELECT id FROM usuarios);
    """)
    conn.commit()
    print("✅ Negocios huérfanos eliminados (sin propietario válido).")

def main():
    print("🛠️ VERIFICACIÓN Y REPARACIÓN DE INTEGRIDAD DE BASE DE DATOS POS")
    print("=" * 60)
    try:
        conn = connect_db()
        cur = conn.cursor()
        check_and_fix_products_table(cur, conn)
        check_and_fix_insumos_table(cur, conn)
        check_and_fix_negocios_table(cur, conn)
        cur.close()
        conn.close()
        print("\n🎉 Integridad de la base de datos verificada y reparada.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 