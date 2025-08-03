#!/usr/bin/env python3
"""
Script para debugging de tokens JWT
Autor: Asistente AI
Fecha: 7 de Julio de 2025
"""

from jose import jwt
from datetime import datetime, timezone
import requests
import json

# Configuración
API_BASE_URL = "http://localhost:8000"
SECRET_KEY = "tu_secret_key_aqui"  # Reemplazar con la clave real

def decode_token_debug(token: str):
    """Decodificar token sin verificar para debug"""
    try:
        # Decodificar sin verificar para ver el contenido
        payload = jwt.decode(token, key="", options={"verify_signature": False})
        print("=== TOKEN DEBUG ===")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Verificar campos esperados
        expected_fields = ['user_id', 'email', 'tipo_tier', 'exp']
        for field in expected_fields:
            if field in payload:
                if field == 'exp':
                    exp_timestamp = payload[field]
                    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
                    now = datetime.now(timezone.utc)
                    print(f"✅ {field}: {exp_datetime}")
                    print(f"   Ahora: {now}")
                    print(f"   Expira en: {exp_datetime - now}")
                else:
                    print(f"✅ {field}: {payload[field]}")
            else:
                print(f"❌ {field}: NO encontrado")
        
        return payload
    except Exception as e:
        print(f"❌ Error decodificando token: {e}")
        return None

def verify_token_debug(token: str, secret_key: str):
    """Verificar token con la clave secreta"""
    try:
        payload = jwt.decode(token, key=secret_key, algorithms=["HS256"])
        print("✅ Token verificado correctamente")
        return payload
    except Exception as e:
        print(f"❌ Token inválido: {e}")
        return None

def test_token_creation():
    """Testear creación de token"""
    print("\n🔧 TESTING CREACIÓN DE TOKEN")
    print("=" * 40)
    
    # Datos de prueba
    test_data = {
        "user_id": "test-user-id",
        "email": "test@example.com",
        "tipo_tier": "cliente"
    }
    
    try:
        # Crear token
        token = jwt.encode(test_data, SECRET_KEY, algorithm="HS256")
        print(f"✅ Token creado: {token[:50]}...")
        
        # Decodificar para debug
        decode_token_debug(token)
        
        # Verificar
        verify_token_debug(token, SECRET_KEY)
        
        return token
    except Exception as e:
        print(f"❌ Error creando token: {e}")
        return None

def test_login_and_token():
    """Testear login y obtener token real"""
    print("\n🔐 TESTING LOGIN Y TOKEN REAL")
    print("=" * 40)
    
    # Datos de login
    login_data = {
        "username": "ismaeldimenza@hotmail.com",
        "password": "ismael38772433"
    }
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        response = requests.post(f"{API_BASE_URL}/users/login", data=login_data, headers=headers)
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            
            if token:
                print("✅ Login exitoso")
                print(f"Token: {token[:50]}...")
                
                # Debug del token
                decode_token_debug(token)
                
                # Testear endpoint protegido
                auth_headers = {"Authorization": f"Bearer {token}"}
                profile_response = requests.get(f"{API_BASE_URL}/profile/me", headers=auth_headers)
                
                print(f"\n🔒 Test endpoint protegido: {profile_response.status_code}")
                if profile_response.status_code == 200:
                    print("✅ Endpoint protegido funciona")
                else:
                    print(f"❌ Endpoint protegido falló: {profile_response.text}")
                
                return token
            else:
                print("❌ No se pudo obtener token del login")
                return None
        else:
            print(f"❌ Login falló: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return None

def main():
    """Función principal"""
    print("🔍 DEBUGGING DE TOKENS JWT")
    print("=" * 50)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Token de prueba
    test_token = test_token_creation()
    
    # Test 2: Token real del login
    real_token = test_login_and_token()
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN")
    print("=" * 50)
    print(f"🧪 Token de prueba: {'✅ OK' if test_token else '❌ FALLÓ'}")
    print(f"🔐 Token real: {'✅ OK' if real_token else '❌ FALLÓ'}")

if __name__ == "__main__":
    main() 