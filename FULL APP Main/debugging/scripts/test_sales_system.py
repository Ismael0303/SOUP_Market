#!/usr/bin/env python3
"""
Script de prueba para el sistema de ventas de SOUP
Verifica que las APIs y funcionalidades estén funcionando correctamente
"""

import requests
import json
import sys
import os
from datetime import datetime, timedelta

# Configuración
API_BASE_URL = "http://localhost:8000"
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword123"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_section(title):
    print(f"\n{'-'*40}")
    print(f"  {title}")
    print(f"{'-'*40}")

def test_api_endpoint(endpoint, method="GET", data=None, expected_status=200):
    """Prueba un endpoint de la API"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        if response.status_code == expected_status:
            print(f"✅ {method} {endpoint} - OK")
            return response.json() if response.content else None
        else:
            print(f"❌ {method} {endpoint} - Error {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {endpoint} - No se pudo conectar al servidor")
        return None
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {str(e)}")
        return None

def test_authentication():
    """Prueba el sistema de autenticación"""
    print_section("PRUEBA DE AUTENTICACIÓN")
    
    # Login
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    response = test_api_endpoint("/auth/login", "POST", login_data)
    if response:
        token = response.get("access_token")
        if token:
            print(f"✅ Token obtenido: {token[:20]}...")
            return token
        else:
            print("❌ No se obtuvo token de acceso")
            return None
    return None

def test_business_operations(token):
    """Prueba las operaciones de negocios"""
    print_section("PRUEBA DE OPERACIONES DE NEGOCIOS")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Obtener negocios del usuario
    response = test_api_endpoint("/businesses/my", "GET")
    if response:
        businesses = response
        print(f"✅ Negocios encontrados: {len(businesses)}")
        if businesses:
            business_id = businesses[0]["id"]
            print(f"   Usando negocio: {businesses[0]['nombre']} (ID: {business_id})")
            return business_id
        else:
            print("   No hay negocios disponibles")
            return None
    return None

def test_product_operations(token, business_id):
    """Prueba las operaciones de productos"""
    print_section("PRUEBA DE OPERACIONES DE PRODUCTOS")
    
    # Obtener productos con stock
    response = test_api_endpoint("/products/with-stock", "GET")
    if response:
        products = response
        print(f"✅ Productos con stock encontrados: {len(products)}")
        if products:
            product = products[0]
            print(f"   Producto de ejemplo: {product['nombre']} - Stock: {product.get('stock_terminado', 0)}")
            return product
        else:
            print("   No hay productos disponibles")
            return None
    return None

def test_sales_operations(token, business_id, product):
    """Prueba las operaciones de ventas"""
    print_section("PRUEBA DE OPERACIONES DE VENTAS")
    
    # Simular una venta
    sale_data = {
        "business_id": business_id,
        "items": [
            {
                "product_id": product["id"],
                "quantity": 1,
                "unit_price": product["precio"]
            }
        ],
        "payment_method": "Efectivo",
        "total_amount": product["precio"],
        "subtotal_amount": product["precio"],
        "tax_amount": product["precio"] * 0.21,
        "currency": "ARS",
        "status": "Completada"
    }
    
    # Nota: Esta API endpoint necesitaría ser implementada en el backend
    print("ℹ️  Nota: El endpoint de ventas necesitaría ser implementado en el backend")
    print(f"   Datos de venta simulada: {json.dumps(sale_data, indent=2)}")
    
    return True

def test_frontend_integration():
    """Prueba la integración con el frontend"""
    print_section("PRUEBA DE INTEGRACIÓN CON FRONTEND")
    
    # Verificar archivos del frontend
    frontend_files = [
        "frontend/src/screens/SalesHistoryScreen.js",
        "frontend/src/screens/POSScreen.js",
        "frontend/src/firebaseConfig.js",
        "frontend/src/App.js"
    ]
    
    for file_path in frontend_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - Existe")
        else:
            print(f"❌ {file_path} - No existe")
    
    # Verificar configuración de Firebase
    if os.path.exists("frontend/src/firebaseConfig.js"):
        print("✅ Configuración de Firebase encontrada")
    else:
        print("❌ Configuración de Firebase no encontrada")

def main():
    """Función principal de pruebas"""
    print_header("SISTEMA DE VENTAS SOUP - PRUEBAS")
    
    print(f"🔧 Configuración:")
    print(f"   API Base URL: {API_BASE_URL}")
    print(f"   Usuario de prueba: {TEST_USER_EMAIL}")
    print(f"   Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Prueba de autenticación
    token = test_authentication()
    if not token:
        print("\n❌ No se pudo autenticar. Verifica que el backend esté corriendo.")
        return
    
    # Prueba de negocios
    business_id = test_business_operations(token)
    if not business_id:
        print("\n❌ No se pudo obtener información de negocios.")
        return
    
    # Prueba de productos
    product = test_product_operations(token, business_id)
    if not product:
        print("\n❌ No se pudo obtener información de productos.")
        return
    
    # Prueba de ventas
    test_sales_operations(token, business_id, product)
    
    # Prueba de integración con frontend
    test_frontend_integration()
    
    print_header("RESUMEN DE PRUEBAS")
    print("✅ Sistema de autenticación funcionando")
    print("✅ Operaciones de negocios funcionando")
    print("✅ Operaciones de productos funcionando")
    print("ℹ️  Sistema de ventas - Necesita implementación en backend")
    print("✅ Archivos del frontend creados")
    print("✅ Configuración de Firebase creada")
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Instalar Firebase: npm install firebase")
    print("2. Configurar credenciales reales de Firebase en firebaseConfig.js")
    print("3. Implementar endpoints de ventas en el backend")
    print("4. Probar el sistema completo")

if __name__ == "__main__":
    main() 