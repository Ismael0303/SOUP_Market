#!/usr/bin/env python3
"""
Script simple para probar el endpoint y CORS.
"""

import requests
import json

def test_endpoints():
    """Prueba los endpoints del backend"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Probando endpoints del backend...")
    
    # Test 1: Endpoint raíz
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ GET / - Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ GET / - Error: {e}")
    
    # Test 2: Endpoint público con CORS headers
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.get(f"{base_url}/public/businesses", headers=headers)
        print(f"✅ GET /public/businesses - Status: {response.status_code}")
        
        # Verificar headers CORS
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        print(f"   CORS Headers: {cors_headers}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {len(data)} businesses found")
        else:
            print(f"   Error Response: {response.text}")
            
    except Exception as e:
        print(f"❌ GET /public/businesses - Error: {e}")
    
    # Test 3: OPTIONS request (preflight)
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.options(f"{base_url}/public/businesses", headers=headers)
        print(f"✅ OPTIONS /public/businesses - Status: {response.status_code}")
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        print(f"   CORS Headers: {cors_headers}")
        
    except Exception as e:
        print(f"❌ OPTIONS /public/businesses - Error: {e}")

if __name__ == "__main__":
    test_endpoints() 