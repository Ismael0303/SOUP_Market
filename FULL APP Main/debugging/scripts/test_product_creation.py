#!/usr/bin/env python3
"""
Script para probar la creación de producto manualmente
"""

import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_product_creation():
    """Probar creación de producto paso a paso"""
    print("🧪 TESTING CREACIÓN DE PRODUCTO")
    print("=" * 40)
    
    # 1. Login
    login_data = {
        "username": "test_auth@example.com",
        "password": "testpass123"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    response = requests.post(f"{API_BASE_URL}/users/login", data=login_data, headers=headers)
    if response.status_code != 200:
        print(f"❌ Login falló: {response.status_code}")
        print(f"Response: {response.text}")
        return
    
    token = response.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login exitoso")
    
    # 2. Crear negocio
    business_data = {
        "nombre": "Test Business",
        "descripcion": "Business for testing",
        "tipo_negocio": "PRODUCTOS"
    }
    
    response = requests.post(f"{API_BASE_URL}/businesses/", json=business_data, headers=auth_headers)
    if response.status_code != 201:
        print(f"❌ Creación de negocio falló: {response.status_code}")
        print(f"Response: {response.text}")
        return
    
    business = response.json()
    business_id = business["id"]
    print(f"✅ Negocio creado: {business['nombre']} (ID: {business_id})")
    
    # 3. Crear producto con todos los campos requeridos
    product_data = {
        "nombre": "Test Product",
        "descripcion": "Product for testing",
        "precio": 10.0,
        "tipo_producto": "PHYSICAL_GOOD",
        "negocio_id": business_id,
        "precio_venta": 15.0,
        "margen_ganancia_sugerido": 50.0,
        "stock_terminado": 100.0
    }
    
    print(f"📦 Intentando crear producto con datos:")
    print(json.dumps(product_data, indent=2))
    
    response = requests.post(f"{API_BASE_URL}/products/", json=product_data, headers=auth_headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        product = response.json()
        print(f"✅ Producto creado exitosamente: {product['nombre']}")
        print(f"Producto ID: {product['id']}")
        print(f"COGS: {product.get('cogs')}")
        print(f"Precio sugerido: {product.get('precio_sugerido')}")
        print(f"Margen real: {product.get('margen_ganancia_real')}")
    else:
        print(f"❌ Creación de producto falló")
        try:
            error_detail = response.json()
            print(f"Error detail: {json.dumps(error_detail, indent=2)}")
        except:
            print(f"Error text: {response.text}")

if __name__ == "__main__":
    test_product_creation() 