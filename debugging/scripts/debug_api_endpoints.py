#!/usr/bin/env python3
"""
Script para testing de endpoints de la API
Autor: Asistente AI
Fecha: 7 de Julio de 2025
"""

import requests
import json
import sys
from datetime import datetime

# Configuración de la API
API_BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, headers=None, expected_status=200):
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
        
        print(f"{status_icon} {method} {endpoint}: {response.status_code}")
        
        if not status_ok:
            print(f"   Error: {response.text}")
        
        return status_ok
        
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {endpoint}: No se pudo conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ {method} {endpoint}: Error - {e}")
        return False

def test_public_endpoints():
    """Testear endpoints públicos"""
    print("🌐 TESTING ENDPOINTS PÚBLICOS")
    print("=" * 40)
    
    endpoints = [
        ("GET", "/"),
        ("GET", "/public/businesses"),
        ("GET", "/public/products"),
    ]
    
    success_count = 0
    for method, endpoint in endpoints:
        if test_endpoint(method, endpoint):
            success_count += 1
    
    print(f"\n📊 Resultados públicos: {success_count}/{len(endpoints)} exitosos")
    return success_count == len(endpoints)

def test_auth_endpoints():
    """Testear endpoints de autenticación"""
    print("\n🔐 TESTING ENDPOINTS DE AUTENTICACIÓN")
    print("=" * 40)
    
    # Test de registro
    test_user = {
        "email": "test@example.com",
        "password": "testpass123",
        "nombre": "Usuario Test",
        "tipo_tier": "cliente"
    }
    
    # Intentar registro (puede fallar si el usuario ya existe)
    test_endpoint("POST", "/users/register", data=test_user, expected_status=201)
    
    # Test de login
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(f"{API_BASE_URL}/users/login", data=login_data, headers=headers)
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get("access_token")
        
        if token:
            print("✅ Login exitoso, token obtenido")
            
            # Test de endpoints protegidos
            auth_headers = {"Authorization": f"Bearer {token}"}
            
            protected_endpoints = [
                ("GET", "/profile/me"),
                ("GET", "/businesses/me"),
                ("GET", "/products/me"),
            ]
            
            print("\n🔒 TESTING ENDPOINTS PROTEGIDOS")
            print("=" * 40)
            
            success_count = 0
            for method, endpoint in protected_endpoints:
                if test_endpoint(method, endpoint, headers=auth_headers):
                    success_count += 1
            
            print(f"\n📊 Resultados protegidos: {success_count}/{len(protected_endpoints)} exitosos")
            return success_count == len(protected_endpoints)
        else:
            print("❌ No se pudo obtener token del login")
            return False
    else:
        print(f"❌ Login falló: {response.status_code} - {response.text}")
        return False

def test_cors():
    """Testear configuración CORS"""
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

def main():
    """Función principal de testing"""
    print("🧪 TESTING COMPLETO DE LA API")
    print("=" * 50)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API URL: {API_BASE_URL}")
    print()
    
    # Verificar que el servidor esté corriendo
    if not test_endpoint("GET", "/"):
        print("❌ El servidor no está corriendo. Inicia el backend primero.")
        return
    
    # Ejecutar tests
    public_ok = test_public_endpoints()
    auth_ok = test_auth_endpoints()
    cors_ok = test_cors()
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE TESTS")
    print("=" * 50)
    print(f"🌐 Endpoints públicos: {'✅ OK' if public_ok else '❌ FALLÓ'}")
    print(f"🔐 Autenticación: {'✅ OK' if auth_ok else '❌ FALLÓ'}")
    print(f"🌍 CORS: {'✅ OK' if cors_ok else '❌ FALLÓ'}")
    
    if public_ok and auth_ok and cors_ok:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
    else:
        print("\n⚠️ Algunos tests fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main() 