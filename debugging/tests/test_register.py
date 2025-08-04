#!/usr/bin/env python3
"""
Script para probar el endpoint de registro de usuarios
"""

import urllib.request
import json

def test_register():
    """Probar el endpoint de registro"""
    
    # Datos de prueba para el registro
    test_user = {
        "email": "test@example.com",
        "nombre": "Usuario de Prueba",
        "password": "password123",
        "tipo_tier": "cliente",
        "localizacion": "Buenos Aires, Argentina"
    }
    
    try:
        print("Probando endpoint /users/register...")
        
        # Crear la petición
        req = urllib.request.Request("http://127.0.0.1:8000/users/register")
        req.add_header('Content-Type', 'application/json')
        req.add_header('accept', 'application/json')
        
        # Convertir datos a JSON
        data = json.dumps(test_user).encode('utf-8')
        req.data = data
        req.method = 'POST'
        
        # Enviar petición
        with urllib.request.urlopen(req) as response:
            print(f"Status Code: {response.status}")
            print(f"Headers: {dict(response.headers)}")
            response_text = response.read().decode()
            print(f"Response: {response_text}")
            
            # Intentar parsear JSON
            try:
                data = json.loads(response_text)
                print(f"JSON parsed successfully. User ID: {data.get('id', 'N/A')}")
            except json.JSONDecodeError:
                print("Response is not valid JSON")
                
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        print(f"Error response: {e.read().decode()}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_register() 

input("Press Enter to exit...")