#!/usr/bin/env python3
"""
Script para probar el endpoint público de negocios
"""

import requests
import json

def test_public_businesses():
    """Prueba el endpoint público de negocios"""
    try:
        url = "http://localhost:8000/public/businesses"
        print(f"Probando endpoint: {url}")
        
        response = requests.get(url, headers={"accept": "application/json"})
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Respuesta exitosa: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"Error en la respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que esté ejecutándose en localhost:8000")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    test_public_businesses() 