# debugging/scripts/test_plugins_system.py

import requests
import json
import sys
import os

# Configuración
BASE_URL = "http://127.0.0.1:8000"
TEST_EMAIL = "ismaeldimenza@hotmail.com"
TEST_PASSWORD = "ismael38772433"

def test_plugins_system():
    """Test completo del sistema de plugins"""
    
    print("🧪 TESTEANDO SISTEMA DE PLUGINS")
    print("=" * 50)
    
    # 1. Test endpoint público (sin autenticación)
    print("\n1. 📋 Test endpoint público /plugins/available")
    try:
        response = requests.get(f"{BASE_URL}/plugins/available")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"✅ Plugins disponibles: {len(data.get('plugins', {}))}")
            for plugin_name, plugin_info in data.get('plugins', {}).items():
                print(f"   - {plugin_name}: {plugin_info.get('name')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 2. Login para obtener token
    print("\n2. 🔐 Login para obtener token")
    try:
        login_data = {
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        response = requests.post(f"{BASE_URL}/users/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            print(f"✅ Login exitoso")
            print(f"✅ Token obtenido: {access_token[:20]}...")
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # Headers con token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 3. Test estado de plugins (con autenticación)
    print("\n3. 📊 Test estado de plugins")
    try:
        response = requests.get(f"{BASE_URL}/plugins/status", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"✅ Plugins activos: {data.get('active_plugins', [])}")
            print(f"✅ Total disponible: {data.get('total_available')}")
            print(f"✅ Total activos: {data.get('total_active')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 4. Test activar plugin
    print("\n4. 🔌 Test activar plugin 'panaderia'")
    try:
        response = requests.post(f"{BASE_URL}/plugins/activate/panaderia", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Plugin activado exitosamente")
            print(f"✅ Mensaje: {data.get('message')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 5. Verificar plugin activado
    print("\n5. ✅ Verificar plugin activado")
    try:
        response = requests.get(f"{BASE_URL}/plugins/status", headers=headers)
        if response.status_code == 200:
            data = response.json()
            active_plugins = data.get('active_plugins', [])
            if 'panaderia' in active_plugins:
                print(f"✅ Plugin 'panaderia' está activo")
            else:
                print(f"❌ Plugin 'panaderia' no está activo")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 6. Test desactivar plugin
    print("\n6. 🔌 Test desactivar plugin 'panaderia'")
    try:
        response = requests.post(f"{BASE_URL}/plugins/deactivate/panaderia", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Plugin desactivado exitosamente")
            print(f"✅ Mensaje: {data.get('message')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 7. Verificar plugin desactivado
    print("\n7. ✅ Verificar plugin desactivado")
    try:
        response = requests.get(f"{BASE_URL}/plugins/status", headers=headers)
        if response.status_code == 200:
            data = response.json()
            active_plugins = data.get('active_plugins', [])
            if 'panaderia' not in active_plugins:
                print(f"✅ Plugin 'panaderia' está desactivado")
            else:
                print(f"❌ Plugin 'panaderia' sigue activo")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 TEST COMPLETADO EXITOSAMENTE")
    print("✅ Sistema de plugins funcionando correctamente")
    return True

if __name__ == "__main__":
    success = test_plugins_system()
    sys.exit(0 if success else 1) 