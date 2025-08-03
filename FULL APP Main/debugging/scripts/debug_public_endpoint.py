#!/usr/bin/env python3
"""
Script de debugging para el endpoint público
"""

import requests
import json
import sys
import os

# Agregar el directorio backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_server_health():
    """Prueba si el servidor está respondiendo"""
    try:
        response = requests.get("http://localhost:8000/")
        print(f"Servidor saludable: {response.status_code}")
        print(f"Respuesta: {response.json()}")
        return True
    except Exception as e:
        print(f"Error conectando al servidor: {e}")
        return False

def test_public_businesses():
    """Prueba el endpoint público de negocios"""
    try:
        url = "http://localhost:8000/public/businesses"
        print(f"\nProbando endpoint: {url}")
        
        response = requests.get(url, headers={"accept": "application/json"})
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Respuesta exitosa: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"Error en la respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor")
    except Exception as e:
        print(f"Error inesperado: {e}")

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    try:
        from app.database import engine
        from app.models import Negocio
        from sqlalchemy import text
        
        print("\nProbando conexión a la base de datos...")
        
        # Intentar una consulta simple
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM negocios"))
            count = result.scalar()
            print(f"Número de negocios en la base de datos: {count}")
            
        return True
    except Exception as e:
        print(f"Error en la base de datos: {e}")
        return False

def test_crud_function():
    """Prueba la función CRUD directamente"""
    try:
        from app.database import get_db
        from app.crud import business as crud_business
        
        print("\nProbando función CRUD directamente...")
        
        # Obtener una sesión de base de datos
        db = next(get_db())
        
        # Intentar obtener todos los negocios
        businesses = crud_business.get_all_businesses(db)
        print(f"Negocios obtenidos: {len(businesses)}")
        
        for business in businesses:
            print(f"- {business.nombre} (ID: {business.id})")
            
        return True
    except Exception as e:
        print(f"Error en CRUD: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Debugging del Endpoint Público ===")
    
    # Probar salud del servidor
    if not test_server_health():
        print("El servidor no está respondiendo. Asegúrate de que esté ejecutándose.")
        sys.exit(1)
    
    # Probar conexión a la base de datos
    if not test_database_connection():
        print("Problema con la base de datos.")
        sys.exit(1)
    
    # Probar función CRUD
    if not test_crud_function():
        print("Problema con la función CRUD.")
        sys.exit(1)
    
    # Probar endpoint
    test_public_businesses() 