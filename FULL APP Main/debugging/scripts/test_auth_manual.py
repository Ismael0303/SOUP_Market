#!/usr/bin/env python3
"""
Script para probar manualmente el registro y login
Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import requests
import json

# Configuración de la API
API_BASE_URL = "http://localhost:8000"

def test_register():
    """Probar registro de usuario"""
    print("🔐 TESTING REGISTRO DE USUARIO")
    print("=" * 40)
    
    register_data = {
        "email": "test_auth@example.com",
        "password": "testpass123",
        "nombre": "Usuario Test Auth",
        "tipo_tier": "microemprendimiento"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/users/register", json=register_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registro exitoso")
            return True
        else:
            print("❌ Registro falló")
            return False
            
    except Exception as e:
        print(f"❌ Error en registro: {e}")
        return False

def test_login():
    """Probar login de usuario"""
    print("\n🔑 TESTING LOGIN DE USUARIO")
    print("=" * 40)
    
    login_data = {
        "username": "test_auth@example.com",
        "password": "testpass123"
    }
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        response = requests.post(f"{API_BASE_URL}/users/login", data=login_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            if "access_token" in token_data:
                print("✅ Login exitoso")
                print(f"Token: {token_data['access_token'][:50]}...")
                return token_data["access_token"]
            else:
                print("❌ No se encontró access_token en la respuesta")
                return None
        else:
            print("❌ Login falló")
            return None
            
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return None

def test_protected_endpoint(token):
    """Probar endpoint protegido con token"""
    print("\n🔒 TESTING ENDPOINT PROTEGIDO")
    print("=" * 40)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_BASE_URL}/profile/me", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Endpoint protegido accesible")
            return True
        else:
            print("❌ Endpoint protegido falló")
            return False
            
    except Exception as e:
        print(f"❌ Error en endpoint protegido: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 TESTING MANUAL DE AUTENTICACIÓN")
    print("=" * 50)
    
    # Probar registro
    register_success = test_register()
    
    # Probar login
    token = test_login()
    
    # Probar endpoint protegido si tenemos token
    if token:
        protected_success = test_protected_endpoint(token)
    else:
        protected_success = False
    
    # Resumen
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE TESTS DE AUTENTICACIÓN")
    print("=" * 50)
    print(f"Registro: {'✅ OK' if register_success else '❌ FALLÓ'}")
    print(f"Login: {'✅ OK' if token else '❌ FALLÓ'}")
    print(f"Endpoint Protegido: {'✅ OK' if protected_success else '❌ FALLÓ'}")

if __name__ == "__main__":
    main() 