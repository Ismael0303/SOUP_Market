#!/usr/bin/env python3
"""
Script para testing de endpoints del sistema POS y capítulo Ñiam
Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import requests
import json
import sys
from datetime import datetime

# Configuración de la API
API_BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, headers=None, expected_status=200, description=""):
    """Testear un endpoint específico"""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            print(f"❌ Método no soportado: {method}")
            return False
        
        status_ok = response.status_code == expected_status
        status_icon = "✅" if status_ok else "❌"
        
        desc = f" - {description}" if description else ""
        print(f"{status_icon} {method} {endpoint}{desc}: {response.status_code}")
        
        if not status_ok:
            print(f"   Error: {response.text}")
        elif response.status_code != 204:  # No content
            try:
                response_data = response.json()
                if isinstance(response_data, dict) and 'stock_terminado' in response_data:
                    print(f"   ✅ Campo stock_terminado presente: {response_data['stock_terminado']}")
            except:
                pass
        
        return status_ok
        
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {endpoint}: No se pudo conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ {method} {endpoint}: Error - {e}")
        return False

def get_auth_token():
    """Obtener token de autenticación"""
    # Intentar login con usuario existente o crear uno nuevo
    login_data = {
        "username": "test_pos@example.com",
        "password": "testpass123"
    }
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(f"{API_BASE_URL}/users/login", data=login_data, headers=headers)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("access_token")
    
    # Si el login falla, intentar registro
    register_data = {
        "email": "test_pos@example.com",
        "password": "testpass123",
        "nombre": "Usuario Test POS",
        "tipo_tier": "microemprendimiento"
    }
    
    response = requests.post(f"{API_BASE_URL}/users/register", json=register_data)
    if response.status_code == 201:
        # Intentar login nuevamente
        response = requests.post(f"{API_BASE_URL}/users/login", data=login_data, headers=headers)
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get("access_token")
    
    return None

def test_pos_product_endpoints():
    """Testear endpoints de productos con funcionalidad POS"""
    print("🛍️ TESTING ENDPOINTS DE PRODUCTOS POS")
    print("=" * 50)
    
    token = get_auth_token()
    if not token:
        print("❌ No se pudo obtener token de autenticación")
        return False
    
    auth_headers = {"Authorization": f"Bearer {token}"}
    
    # Crear un negocio primero
    business_data = {
        "nombre": "Panadería Test POS",
        "descripcion": "Panadería para testing del sistema POS",
        "tipo_negocio": "PRODUCTOS"
    }
    
    response = requests.post(f"{API_BASE_URL}/businesses/", json=business_data, headers=auth_headers)
    if response.status_code == 201:
        business = response.json()
        business_id = business["id"]
        print(f"✅ Negocio creado: {business['nombre']}")
    else:
        print(f"❌ Error creando negocio: {response.text}")
        return False
    
    # Crear producto con stock_terminado
    product_data = {
        "nombre": "Pan de Molde",
        "descripcion": "Pan de molde fresco",
        "precio": 2.50,
        "tipo_producto": "PHYSICAL_GOOD",
        "negocio_id": business_id,
        "stock_terminado": 50  # Nuevo campo del sistema POS
    }
    
    response = requests.post(f"{API_BASE_URL}/products/", json=product_data, headers=auth_headers)
    if response.status_code == 201:
        product = response.json()
        product_id = product["id"]
        print(f"✅ Producto creado con stock_terminado: {product['stock_terminado']}")
    else:
        print(f"❌ Error creando producto: {response.text}")
        return False
    
    # Testear endpoints
    endpoints = [
        ("GET", f"/products/{product_id}", None, auth_headers, 200, "Obtener producto con stock"),
        ("GET", "/products/me", None, auth_headers, 200, "Listar productos del usuario"),
        ("PUT", f"/products/{product_id}", {"stock_terminado": 30}, auth_headers, 200, "Actualizar stock"),
        ("GET", f"/products/{product_id}", None, auth_headers, 200, "Verificar actualización stock"),
    ]
    
    success_count = 0
    for method, endpoint, data, headers, expected_status, description in endpoints:
        if test_endpoint(method, endpoint, data, headers, expected_status, description):
            success_count += 1
    
    print(f"\n📊 Resultados productos POS: {success_count}/{len(endpoints)} exitosos")
    return success_count == len(endpoints)

def test_stock_management():
    """Testear gestión de stock específica del POS"""
    print("\n📦 TESTING GESTIÓN DE STOCK")
    print("=" * 50)
    
    token = get_auth_token()
    if not token:
        return False
    
    auth_headers = {"Authorization": f"Bearer {token}"}
    
    # Obtener productos del usuario
    response = requests.get(f"{API_BASE_URL}/products/me", headers=auth_headers)
    if response.status_code != 200:
        print("❌ No se pudieron obtener productos")
        return False
    
    products = response.json()
    if not products:
        print("❌ No hay productos para testear")
        return False
    
    product = products[0]
    product_id = product["id"]
    
    # Testear operaciones de stock
    stock_tests = [
        ("PUT", f"/products/{product_id}", {"stock_terminado": 100}, auth_headers, 200, "Aumentar stock"),
        ("PUT", f"/products/{product_id}", {"stock_terminado": 0}, auth_headers, 200, "Vaciar stock"),
        ("PUT", f"/products/{product_id}", {"stock_terminado": 25}, auth_headers, 200, "Restaurar stock"),
    ]
    
    success_count = 0
    for method, endpoint, data, headers, expected_status, description in stock_tests:
        if test_endpoint(method, endpoint, data, headers, expected_status, description):
            success_count += 1
    
    print(f"\n📊 Resultados gestión stock: {success_count}/{len(stock_tests)} exitosos")
    return success_count == len(stock_tests)

def test_public_endpoints():
    """Testear endpoints públicos con productos que tienen stock"""
    print("\n🌐 TESTING ENDPOINTS PÚBLICOS CON STOCK")
    print("=" * 50)
    
    endpoints = [
        ("GET", "/public/businesses", None, None, 200, "Listar negocios"),
        ("GET", "/public/products", None, None, 200, "Listar productos públicos"),
    ]
    
    success_count = 0
    for method, endpoint, data, headers, expected_status, description in endpoints:
        if test_endpoint(method, endpoint, data, headers, expected_status, description):
            success_count += 1
    
    print(f"\n📊 Resultados públicos: {success_count}/{len(endpoints)} exitosos")
    return success_count == len(endpoints)

def test_database_structure():
    """Verificar que el campo stock_terminado existe en la base de datos"""
    print("\n🗄️ VERIFICANDO ESTRUCTURA DE BASE DE DATOS")
    print("=" * 50)
    
    token = get_auth_token()
    if not token:
        return False
    
    auth_headers = {"Authorization": f"Bearer {token}"}
    
    # Obtener productos y verificar estructura
    response = requests.get(f"{API_BASE_URL}/products/me", headers=auth_headers)
    if response.status_code == 200:
        products = response.json()
        if products:
            product = products[0]
            if "stock_terminado" in product:
                print(f"✅ Campo stock_terminado presente en producto: {product['stock_terminado']}")
                return True
            else:
                print("❌ Campo stock_terminado no encontrado en producto")
                return False
        else:
            print("⚠️ No hay productos para verificar estructura")
            return True
    else:
        print(f"❌ Error obteniendo productos: {response.text}")
        return False

def main():
    """Función principal de testing"""
    print("🧪 TESTING SISTEMA POS Y CAPÍTULO ÑIAM")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API URL: {API_BASE_URL}")
    print()
    
    # Verificar que el servidor esté corriendo
    if not test_endpoint("GET", "/"):
        print("❌ El servidor no está corriendo. Inicia el backend primero.")
        return
    
    # Ejecutar tests
    db_structure_ok = test_database_structure()
    pos_products_ok = test_pos_product_endpoints()
    stock_management_ok = test_stock_management()
    public_endpoints_ok = test_public_endpoints()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE TESTS SISTEMA POS")
    print("=" * 60)
    print(f"🗄️ Estructura BD: {'✅ OK' if db_structure_ok else '❌ FALLÓ'}")
    print(f"🛍️ Productos POS: {'✅ OK' if pos_products_ok else '❌ FALLÓ'}")
    print(f"📦 Gestión Stock: {'✅ OK' if stock_management_ok else '❌ FALLÓ'}")
    print(f"🌐 Endpoints Públicos: {'✅ OK' if public_endpoints_ok else '❌ FALLÓ'}")
    
    all_tests_passed = all([db_structure_ok, pos_products_ok, stock_management_ok, public_endpoints_ok])
    
    if all_tests_passed:
        print("\n🎉 ¡TODOS LOS TESTS DEL SISTEMA POS PASARON!")
        print("✅ El backend está listo para el sistema POS")
    else:
        print("\n⚠️ Algunos tests fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main() 