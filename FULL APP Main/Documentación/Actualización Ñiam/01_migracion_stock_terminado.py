#!/usr/bin/env python3
"""
Script de Migración: Añadir campo stock_terminado a tabla productos
Capítulo Ñiam - SOUP Emprendimientos

Este script añade el campo stock_terminado a la tabla productos para implementar
el sistema de inventario de productos terminados para el punto de venta.

Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import psycopg2
import sys
import os
from datetime import datetime

def get_db_config():
    """Obtiene la configuración de la base de datos"""
    print("Configuracion de base de datos:")
    print("Presiona Enter para usar valores por defecto")
    
    host = input("Host (default: localhost): ").strip() or "localhost"
    port = input("Puerto (default: 5432): ").strip() or "5432"
    database = input("Base de datos (default: soup_app_db): ").strip() or "soup_app_db"
    user = input("Usuario (default: soupuser): ").strip() or "soupuser"
    password = input("Contraseña: ").strip()
    
    return {
        'host': host,
        'port': int(port),
        'database': database,
        'user': user,
        'password': password
    }

def conectar_db():
    """Establece conexión con la base de datos PostgreSQL"""
    try:
        # Intentar diferentes configuraciones
        configs_to_try = [
            # Configuración con contraseña
            get_db_config(),
            # Configuración sin contraseña (para desarrollo local)
            {
                'host': 'localhost',
                'port': 5432,
                'database': 'soup_app_db',
                'user': 'soupuser',
                'password': ''
            },
            # Configuración alternativa
            {
                'host': 'localhost',
                'port': 5432,
                'database': 'soup_app_db',
                'user': 'postgres',
                'password': ''
            }
        ]
        
        for i, config in enumerate(configs_to_try):
            try:
                print(f"Intentando conexion {i+1}...")
                conn = psycopg2.connect(**config)
                print("Conexion a la base de datos establecida")
                return conn
            except psycopg2.Error as e:
                print(f"Intento {i+1} fallo: {e}")
                if i == len(configs_to_try) - 1:
                    print("Todos los intentos de conexion fallaron")
                    print("Por favor, verifica:")
                    print("1. Que PostgreSQL esté corriendo")
                    print("2. Que la base de datos 'soup_app_db' exista")
                    print("3. Que el usuario tenga permisos")
                    print("4. Que la contraseña sea correcta")
                    sys.exit(1)
                continue
                
    except Exception as e:
        print(f"Error inesperado al conectar: {e}")
        sys.exit(1)

def verificar_campo_existe(conn, campo):
    """Verifica si el campo ya existe en la tabla productos"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'productos' 
            AND column_name = %s
        """, (campo,))
        
        existe = cursor.fetchone() is not None
        cursor.close()
        return existe
    except psycopg2.Error as e:
        print(f"Error al verificar campo {campo}: {e}")
        return False

def añadir_campo_stock_terminado(conn):
    """Añade el campo stock_terminado a la tabla productos"""
    try:
        cursor = conn.cursor()
        
        # Verificar si el campo ya existe
        if verificar_campo_existe(conn, 'stock_terminado'):
            print("El campo 'stock_terminado' ya existe en la tabla productos")
            cursor.close()
            return True
        
        # Añadir el campo stock_terminado
        cursor.execute("""
            ALTER TABLE productos 
            ADD COLUMN stock_terminado FLOAT DEFAULT 0.0
        """)
        
        # Añadir comentario al campo
        try:
            cursor.execute("""
                COMMENT ON COLUMN productos.stock_terminado IS 
                'Cantidad de productos terminados disponibles para venta'
            """)
        except:
            print("No se pudo añadir comentario al campo (no crítico)")
        
        conn.commit()
        cursor.close()
        print("Campo 'stock_terminado' anadido exitosamente a la tabla productos")
        return True
        
    except psycopg2.Error as e:
        print(f"Error al anadir campo stock_terminado: {e}")
        conn.rollback()
        return False

def actualizar_stock_terminado_existente(conn):
    """Actualiza el stock_terminado de productos existentes basado en insumos disponibles"""
    try:
        cursor = conn.cursor()
        
        # Verificar si existe la tabla producto_insumo
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'producto_insumo'
            )
        """)
        
        tabla_existe = cursor.fetchone()[0]
        
        if not tabla_existe:
            print("Tabla 'producto_insumo' no existe. Saltando actualizacion de stock...")
            cursor.close()
            return True
        
        # Obtener productos que tienen insumos asociados
        cursor.execute("""
            SELECT DISTINCT p.id, p.nombre
            FROM productos p
            INNER JOIN producto_insumo pi ON p.id = pi.producto_id
            WHERE p.stock_terminado IS NULL OR p.stock_terminado = 0
        """)
        
        productos = cursor.fetchall()
        print(f"Encontrados {len(productos)} productos para actualizar stock")
        
        for producto_id, nombre in productos:
            # Calcular stock disponible basado en insumos
            cursor.execute("""
                SELECT 
                    i.cantidad_disponible,
                    pi.cantidad_necesaria,
                    i.unidad_medida_compra
                FROM producto_insumo pi
                INNER JOIN insumos i ON pi.insumo_id = i.id
                WHERE pi.producto_id = %s
            """, (producto_id,))
            
            insumos = cursor.fetchall()
            
            if insumos:
                # Calcular el stock mínimo disponible
                stock_disponible = float('inf')
                for cantidad_disponible, cantidad_necesaria, unidad in insumos:
                    if cantidad_necesaria > 0:
                        stock_posible = cantidad_disponible / cantidad_necesaria
                        stock_disponible = min(stock_disponible, stock_posible)
                
                # Si no es infinito, actualizar el stock
                if stock_disponible != float('inf'):
                    cursor.execute("""
                        UPDATE productos 
                        SET stock_terminado = %s 
                        WHERE id = %s
                    """, (stock_disponible, producto_id))
                    
                    print(f"  {nombre}: {stock_disponible:.2f} unidades disponibles")
        
        conn.commit()
        cursor.close()
        print("Stock terminado actualizado para productos existentes")
        return True
        
    except psycopg2.Error as e:
        print(f"Error al actualizar stock terminado: {e}")
        conn.rollback()
        return False

def verificar_migracion(conn):
    """Verifica que la migración se haya realizado correctamente"""
    try:
        cursor = conn.cursor()
        
        # Verificar que el campo existe
        if not verificar_campo_existe(conn, 'stock_terminado'):
            print("El campo 'stock_terminado' no existe")
            return False
        
        # Verificar que hay productos con stock
        cursor.execute("""
            SELECT COUNT(*) 
            FROM productos 
            WHERE stock_terminado > 0
        """)
        
        productos_con_stock = cursor.fetchone()[0]
        print(f"Productos con stock terminado: {productos_con_stock}")
        
        # Mostrar algunos ejemplos
        cursor.execute("""
            SELECT nombre, stock_terminado 
            FROM productos 
            WHERE stock_terminado > 0 
            LIMIT 5
        """)
        
        ejemplos = cursor.fetchall()
        if ejemplos:
            print("Ejemplos de productos con stock:")
            for nombre, stock in ejemplos:
                print(f"  - {nombre}: {stock:.2f} unidades")
        
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        print(f"Error al verificar migracion: {e}")
        return False

def main():
    """Función principal del script"""
    print("Iniciando migracion: Anadir campo stock_terminado")
    print("=" * 60)
    
    # Conectar a la base de datos
    conn = conectar_db()
    
    try:
        # Paso 1: Añadir campo stock_terminado
        print("\nPaso 1: Anadiendo campo stock_terminado...")
        if not añadir_campo_stock_terminado(conn):
            print("Fallo al anadir campo stock_terminado")
            return
        
        # Paso 2: Actualizar stock de productos existentes
        print("\nPaso 2: Actualizando stock de productos existentes...")
        if not actualizar_stock_terminado_existente(conn):
            print("Fallo al actualizar stock existente")
            return
        
        # Paso 3: Verificar migración
        print("\nPaso 3: Verificando migracion...")
        if not verificar_migracion(conn):
            print("Fallo la verificacion de migracion")
            return
        
        print("\n" + "=" * 60)
        print("Migracion completada exitosamente")
        print("Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("Campo 'stock_terminado' listo para el sistema POS")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("Conexion a la base de datos cerrada")

if __name__ == "__main__":
    main() 