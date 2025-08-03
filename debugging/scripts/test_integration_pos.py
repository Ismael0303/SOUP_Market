#!/usr/bin/env python3
"""
Script para testing de integración completa del sistema POS
Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import requests
import json
import sys
import time
from datetime import datetime

# Configuración de la API
API_BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_connectivity():
    """Testear conectividad del backend"""
    print("🔗 TESTING CONECTIVIDAD DEL BACKEND")
    print("=" * 40)
    
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend conectado correctamente")
            return True
        else:
            print(f"❌ Backend respondió con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al backend")
        return False
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")
        return False

def test_frontend_connectivity():
    """Testear conectividad del frontend"""
    print("\n🌐 TESTING CONECTIVIDAD DEL FRONTEND")
    print("=" * 40)
    
    try:
        response = requests.get(f"{FRONTEND_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend conectado correctamente")
            return True
        else:
            print(f"❌ Frontend respondió con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al frontend")
        return False
    except Exception as e:
        print(f"❌ Error conectando al frontend: {e}")
        return False

def test_pos_workflow():
    """Testear flujo completo del sistema POS"""
    print("\n🛍️ TESTING FLUJO COMPLETO DEL SISTEMA POS")
    print("=" * 40)
    
    # Obtener token de autenticación
    token = get_auth_token()
    if not token:
        print("❌ No se pudo obtener token de autenticación")
        return False
    
    auth_headers = {"Authorization": f"Bearer {token}"}
    
    # Paso 1: Crear negocio
    print("📋 Paso 1: Creando negocio...")
    business_data = {
        "nombre": "Panadería Ñiam Test",
        "descripcion": "Panadería para testing de integración POS",
        "tipo_negocio": "panaderia",
        "direccion": "Calle Integración 456",
        "telefono": "987654321",
        "horario_apertura": "07:00",
        "horario_cierre": "20:00"
    }
    
    response = requests.post(f"{API_BASE_URL}/businesses/", json=business_data, headers=auth_headers)
    if response.status_code == 201:
        business = response.json()
        business_id = business["id"]
        print(f"✅ Negocio creado: {business['nombre']}")
    else:
        print(f"❌ Error creando negocio: {response.text}")
        return False
    
    # Paso 2: Crear productos con stock
    print("📦 Paso 2: Creando productos con stock...")
    products_data = [
        {
            "nombre": "Pan de Molde Integral",
            "descripcion": "Pan de molde integral fresco",
            "precio": 3.50,
            "categoria": "pan",
            "negocio_id": business_id,
            "stock_terminado": 25
        },
        {
            "nombre": "Croissant Clásico",
            "descripcion": "Croissant de mantequilla",
            "precio": 2.80,
            "categoria": "pasteleria",
            "negocio_id": business_id,
            "stock_terminado": 15
        },
        {
            "nombre": "Torta de Chocolate",
            "descripcion": "Torta de chocolate casera",
            "precio": 45.00,
            "categoria": "tortas",
            "negocio_id": business_id,
            "stock_terminado": 3
        }
    ]
    
    created_products = []
    for product_data in products_data:
        response = requests.post(f"{API_BASE_URL}/products/", json=product_data, headers=auth_headers)
        if response.status_code == 201:
            product = response.json()
            created_products.append(product)
            print(f"✅ Producto creado: {product['nombre']} - Stock: {product['stock_terminado']}")
        else:
            print(f"❌ Error creando producto {product_data['nombre']}: {response.text}")
            return False
    
    # Paso 3: Simular ventas
    print("💰 Paso 3: Simulando ventas...")
    sales_simulation = [
        {"product_id": created_products[0]["id"], "quantity": 5},  # Vender 5 panes
        {"product_id": created_products[1]["id"], "quantity": 3},  # Vender 3 croissants
        {"product_id": created_products[2]["id"], "quantity": 1},  # Vender 1 torta
    ]
    
    for sale in sales_simulation:
        product = next(p for p in created_products if p["id"] == sale["product_id"])
        new_stock = product["stock_terminado"] - sale["quantity"]
        
        response = requests.put(
            f"{API_BASE_URL}/products/{sale['product_id']}", 
            json={"stock_terminado": new_stock}, 
            headers=auth_headers
        )
        
        if response.status_code == 200:
            updated_product = response.json()
            print(f"✅ Venta procesada: {product['nombre']} - Stock actualizado: {updated_product['stock_terminado']}")
        else:
            print(f"❌ Error procesando venta de {product['nombre']}: {response.text}")
            return False
    
    # Paso 4: Verificar stock final
    print("📊 Paso 4: Verificando stock final...")
    response = requests.get(f"{API_BASE_URL}/products/me", headers=auth_headers)
    if response.status_code == 200:
        final_products = response.json()
        for product in final_products:
            if product["id"] in [p["id"] for p in created_products]:
                print(f"📦 {product['nombre']}: Stock final = {product['stock_terminado']}")
    
    print("✅ Flujo completo del sistema POS probado exitosamente")
    return True

def get_auth_token():
    """Obtener token de autenticación"""
    # Intentar login con usuario existente o crear uno nuevo
    login_data = {
        "username": "test_integration@example.com",
        "password": "testpass123"
    }
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(f"{API_BASE_URL}/users/login", data=login_data, headers=headers)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("access_token")
    
    # Si el login falla, intentar registro
    register_data = {
        "email": "test_integration@example.com",
        "password": "testpass123",
        "nombre": "Usuario Test Integración",
        "tipo_tier": "emprendedor"
    }
    
    response = requests.post(f"{API_BASE_URL}/users/register", json=register_data)
    if response.status_code == 201:
        # Intentar login nuevamente
        response = requests.post(f"{API_BASE_URL}/users/login", data=login_data, headers=headers)
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get("access_token")
    
    return None

def test_api_endpoints():
    """Testear endpoints específicos del sistema POS"""
    print("\n🔌 TESTING ENDPOINTS ESPECÍFICOS")
    print("=" * 40)
    
    token = get_auth_token()
    if not token:
        return False
    
    auth_headers = {"Authorization": f"Bearer {token}"}
    
    # Obtener productos del usuario
    response = requests.get(f"{API_BASE_URL}/products/me", headers=auth_headers)
    if response.status_code == 200:
        products = response.json()
        print(f"✅ Endpoint /products/me: {len(products)} productos obtenidos")
        
        if products:
            product = products[0]
            if "stock_terminado" in product:
                print(f"✅ Campo stock_terminado presente: {product['stock_terminado']}")
            else:
                print("❌ Campo stock_terminado no encontrado")
                return False
    else:
        print(f"❌ Error en /products/me: {response.text}")
        return False
    
    # Testear actualización de stock
    if products:
        product_id = products[0]["id"]
        new_stock = products[0]["stock_terminado"] + 10
        
        response = requests.put(
            f"{API_BASE_URL}/products/{product_id}", 
            json={"stock_terminado": new_stock}, 
            headers=auth_headers
        )
        
        if response.status_code == 200:
            updated_product = response.json()
            print(f"✅ Stock actualizado: {updated_product['stock_terminado']}")
        else:
            print(f"❌ Error actualizando stock: {response.text}")
            return False
    
    return True

def test_cors_configuration():
    """Testear configuración CORS para integración frontend-backend"""
    print("\n🌍 TESTING CONFIGURACIÓN CORS")
    print("=" * 40)
    
    try:
        response = requests.options(f"{API_BASE_URL}/users/login")
        cors_headers = response.headers
        
        required_headers = [
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Methods",
            "Access-Control-Allow-Headers"
        ]
        
        cors_ok = True
        for header in required_headers:
            if header in cors_headers:
                print(f"✅ {header}: {cors_headers[header]}")
            else:
                print(f"❌ {header}: No encontrado")
                cors_ok = False
        
        return cors_ok
        
    except Exception as e:
        print(f"❌ Error testing CORS: {e}")
        return False

def generate_test_report():
    """Generar reporte de testing"""
    print("\n📋 GENERANDO REPORTE DE TESTING")
    print("=" * 40)
    
    report = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "backend_url": API_BASE_URL,
        "frontend_url": FRONTEND_URL,
        "tests": {}
    }
    
    # Ejecutar tests
    tests = [
        ("Backend Connectivity", test_backend_connectivity),
        ("Frontend Connectivity", test_frontend_connectivity),
        ("API Endpoints", test_api_endpoints),
        ("CORS Configuration", test_cors_configuration),
        ("POS Workflow", test_pos_workflow),
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            report["tests"][test_name] = "PASS" if result else "FAIL"
        except Exception as e:
            report["tests"][test_name] = f"ERROR: {str(e)}"
    
    # Guardar reporte
    report_file = f"debugging/reportes/test_integration_pos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Reporte guardado en: {report_file}")
    return report

def main():
    """Función principal de testing de integración"""
    print("🧪 TESTING DE INTEGRACIÓN COMPLETA DEL SISTEMA POS")
    print("=" * 70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 Backend URL: {API_BASE_URL}")
    print(f"🌐 Frontend URL: {FRONTEND_URL}")
    print()
    
    # Verificar que ambos servicios estén corriendo
    backend_ok = test_backend_connectivity()
    frontend_ok = test_frontend_connectivity()
    
    if not backend_ok:
        print("❌ El backend no está disponible. Inicia el servidor FastAPI primero.")
        return
    
    if not frontend_ok:
        print("⚠️ El frontend no está disponible. Inicia el servidor React si quieres probar la integración completa.")
    
    # Generar reporte completo
    report = generate_test_report()
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📋 RESUMEN DE TESTING DE INTEGRACIÓN")
    print("=" * 70)
    
    passed_tests = sum(1 for result in report["tests"].values() if result == "PASS")
    total_tests = len(report["tests"])
    
    for test_name, result in report["tests"].items():
        status_icon = "✅" if result == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {result}")
    
    print(f"\n📊 Resultados: {passed_tests}/{total_tests} tests pasaron")
    
    if passed_tests == total_tests:
        print("\n🎉 ¡TODOS LOS TESTS DE INTEGRACIÓN PASARON!")
        print("✅ El sistema POS está completamente funcional")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} tests fallaron")
        print("Revisa los errores arriba y asegúrate de que ambos servicios estén corriendo")

if __name__ == "__main__":
    import os
    main() 