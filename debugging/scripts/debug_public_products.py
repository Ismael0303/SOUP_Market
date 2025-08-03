#!/usr/bin/env python3
"""
Script para diagnosticar el problema del endpoint público de productos
Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import requests
import json
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración
API_BASE_URL = "http://localhost:8000"
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "soup_app_db",
    "user": "soupuser",
    "password": "soup123"
}

def check_database_products():
    """Verificar productos en la base de datos directamente"""
    print("🗄️ VERIFICANDO PRODUCTOS EN BASE DE DATOS")
    print("=" * 50)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Verificar estructura de la tabla productos
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'productos' 
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        
        print("📋 Estructura de tabla productos:")
        for col in columns:
            print(f"  - {col['column_name']}: {col['data_type']} (nullable: {col['is_nullable']})")
        
        # Verificar productos existentes
        cursor.execute("SELECT COUNT(*) as total FROM productos")
        total_products = cursor.fetchone()['total']
        print(f"\n📊 Total de productos: {total_products}")
        
        if total_products > 0:
            cursor.execute("""
                SELECT id, nombre, stock_terminado, propietario_id, negocio_id, 
                       precio, tipo_producto, fecha_creacion
                FROM productos 
                LIMIT 3
            """)
            products = cursor.fetchall()
            
            print("\n📦 Primeros 3 productos:")
            for product in products:
                print(f"  - ID: {product['id']}")
                print(f"    Nombre: {product['nombre']}")
                print(f"    Stock: {product['stock_terminado']}")
                print(f"    Propietario: {product['propietario_id']}")
                print(f"    Negocio: {product['negocio_id']}")
                print(f"    Precio: {product['precio']}")
                print(f"    Tipo: {product['tipo_producto']}")
                print(f"    Fecha: {product['fecha_creacion']}")
                print()
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def test_public_products_endpoint():
    """Probar el endpoint público de productos"""
    print("\n🌐 TESTING ENDPOINT PÚBLICO DE PRODUCTOS")
    print("=" * 50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/public/products")
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Endpoint funcionando. Productos obtenidos: {len(products)}")
            return True
        else:
            print("❌ Endpoint falló")
            return False
            
    except Exception as e:
        print(f"❌ Error en endpoint: {e}")
        return False

def test_products_crud_direct():
    """Probar CRUD de productos directamente"""
    print("\n🔧 TESTING CRUD DE PRODUCTOS DIRECTO")
    print("=" * 50)
    
    try:
        # Primero obtener un token
        login_data = {
            "username": "test_auth@example.com",
            "password": "testpass123"
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        response = requests.post(f"{API_BASE_URL}/users/login", data=login_data, headers=headers)
        if response.status_code != 200:
            print("❌ No se pudo obtener token")
            return False
            
        token = response.json()["access_token"]
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Probar obtener productos del usuario
        response = requests.get(f"{API_BASE_URL}/products/", headers=auth_headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ CRUD de productos funcionando")
            return True
        else:
            print("❌ CRUD de productos falló")
            return False
            
    except Exception as e:
        print(f"❌ Error en CRUD: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 DIAGNÓSTICO ENDPOINT PÚBLICO DE PRODUCTOS")
    print("=" * 60)
    
    # Verificar base de datos
    db_ok = check_database_products()
    
    # Probar endpoint público
    endpoint_ok = test_public_products_endpoint()
    
    # Probar CRUD directo
    crud_ok = test_products_crud_direct()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE DIAGNÓSTICO")
    print("=" * 60)
    print(f"Base de Datos: {'✅ OK' if db_ok else '❌ FALLÓ'}")
    print(f"Endpoint Público: {'✅ OK' if endpoint_ok else '❌ FALLÓ'}")
    print(f"CRUD Directo: {'✅ OK' if crud_ok else '❌ FALLÓ'}")

if __name__ == "__main__":
    main() 