#!/usr/bin/env python3
"""
Script simple para diagnosticar el endpoint público de productos
"""

import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Probar endpoints básicos"""
    print("🔍 DIAGNÓSTICO SIMPLE DE ENDPOINTS")
    print("=" * 40)
    
    # Probar endpoint raíz
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"✅ GET /: {response.status_code}")
    except Exception as e:
        print(f"❌ GET /: {e}")
    
    # Probar endpoint de negocios públicos
    try:
        response = requests.get(f"{API_BASE_URL}/public/businesses")
        print(f"✅ GET /public/businesses: {response.status_code}")
        if response.status_code == 200:
            businesses = response.json()
            print(f"   Negocios encontrados: {len(businesses)}")
    except Exception as e:
        print(f"❌ GET /public/businesses: {e}")
    
    # Probar endpoint de productos públicos
    try:
        response = requests.get(f"{API_BASE_URL}/public/products")
        print(f"✅ GET /public/products: {response.status_code}")
        if response.status_code == 200:
            products = response.json()
            print(f"   Productos encontrados: {len(products)}")
        elif response.status_code == 500:
            print(f"   Error 500: {response.text}")
    except Exception as e:
        print(f"❌ GET /public/products: {e}")
    
    # Probar endpoint de productos con autenticación
    try:
        # Login
        login_data = {
            "username": "test_auth@example.com",
            "password": "testpass123"
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        response = requests.post(f"{API_BASE_URL}/users/login", data=login_data, headers=headers)
        if response.status_code == 200:
            token = response.json()["access_token"]
            auth_headers = {"Authorization": f"Bearer {token}"}
            
            # Probar productos autenticados
            response = requests.get(f"{API_BASE_URL}/products", headers=auth_headers)
            print(f"✅ GET /products (auth): {response.status_code}")
            if response.status_code == 200:
                products = response.json()
                print(f"   Productos encontrados: {len(products)}")
        else:
            print(f"❌ Login falló: {response.status_code}")
    except Exception as e:
        print(f"❌ GET /products (auth): {e}")

if __name__ == "__main__":
    test_endpoints() 