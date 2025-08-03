#!/usr/bin/env python3
"""
Script de instalación rápida del sistema de ventas SOUP
Automatiza la configuración y verificación del sistema
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_section(title):
    print(f"\n{'-'*40}")
    print(f"  {title}")
    print(f"{'-'*40}")

def run_command(command, cwd=None, check=True):
    """Ejecuta un comando y maneja errores"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            check=check,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ {command}")
            return True
        else:
            print(f"❌ {command}")
            print(f"   Error: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"   Error: {e}")
        return False
    except Exception as e:
        print(f"❌ {command}")
        print(f"   Error: {e}")
        return False

def check_file_exists(file_path):
    """Verifica si un archivo existe"""
    if os.path.exists(file_path):
        print(f"✅ {file_path} - Existe")
        return True
    else:
        print(f"❌ {file_path} - No existe")
        return False

def install_firebase():
    """Instala Firebase en el frontend"""
    print_section("INSTALACIÓN DE FIREBASE")
    
    frontend_path = Path("../frontend")
    if not frontend_path.exists():
        print("❌ Directorio frontend no encontrado")
        return False
    
    # Verificar si Firebase ya está instalado
    package_json_path = frontend_path / "package.json"
    if package_json_path.exists():
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
            if 'firebase' in package_data.get('dependencies', {}):
                print("✅ Firebase ya está instalado")
                return True
    
    # Instalar Firebase
    print("📦 Instalando Firebase...")
    success = run_command("npm install firebase", cwd=frontend_path)
    
    if success:
        print("✅ Firebase instalado correctamente")
        return True
    else:
        print("❌ Error instalando Firebase")
        return False

def verify_files():
    """Verifica que todos los archivos necesarios existan"""
    print_section("VERIFICACIÓN DE ARCHIVOS")
    
    required_files = [
        "../frontend/src/screens/SalesHistoryScreen.js",
        "../frontend/src/screens/POSScreen.js",
        "../frontend/src/firebaseConfig.js",
        "../frontend/src/App.js",
        "../frontend/src/context/AppContext.js"
    ]
    
    all_exist = True
    for file_path in required_files:
        if not check_file_exists(file_path):
            all_exist = False
    
    return all_exist

def check_backend():
    """Verifica que el backend esté funcionando"""
    print_section("VERIFICACIÓN DEL BACKEND")
    
    try:
        import requests
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend funcionando en http://localhost:8000")
            return True
        else:
            print("❌ Backend no responde correctamente")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend no está corriendo")
        print("   Ejecuta: cd backend && python -m uvicorn app.main:app --reload")
        return False
    except ImportError:
        print("❌ requests no está instalado")
        print("   Ejecuta: pip install requests")
        return False

def create_firebase_config_template():
    """Crea un template de configuración de Firebase"""
    print_section("CONFIGURACIÓN DE FIREBASE")
    
    config_template = '''// frontend/src/firebaseConfig.js
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

// CONFIGURACIÓN DE FIREBASE - REEMPLAZA CON TUS CREDENCIALES
const firebaseConfig = {
  apiKey: "TU_API_KEY_AQUI",
  authDomain: "tu-proyecto.firebaseapp.com",
  projectId: "tu-proyecto-id",
  storageBucket: "tu-proyecto.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdefghijklmnop"
};

// Inicializar Firebase
const app = initializeApp(firebaseConfig);

// Obtener servicios de Firebase
export const auth = getAuth(app);
export const db = getFirestore(app);

// Configurar autenticación con token inicial si existe
if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
  console.log('Token inicial disponible:', __initial_auth_token);
}

export default app;
'''
    
    config_path = Path("../frontend/src/firebaseConfig.js")
    if config_path.exists():
        print("✅ Configuración de Firebase ya existe")
        return True
    
    try:
        with open(config_path, 'w') as f:
            f.write(config_template)
        print("✅ Template de configuración de Firebase creado")
        print("   Edita frontend/src/firebaseConfig.js con tus credenciales")
        return True
    except Exception as e:
        print(f"❌ Error creando configuración: {e}")
        return False

def show_next_steps():
    """Muestra los próximos pasos"""
    print_section("PRÓXIMOS PASOS")
    
    print("🎯 Para completar la instalación:")
    print()
    print("1. 📝 Configurar Firebase:")
    print("   - Ve a https://console.firebase.google.com")
    print("   - Crea un nuevo proyecto o usa uno existente")
    print("   - Obtén las credenciales de configuración")
    print("   - Edita frontend/src/firebaseConfig.js")
    print()
    print("2. 🚀 Iniciar el backend:")
    print("   cd backend")
    print("   python -m uvicorn app.main:app --reload")
    print()
    print("3. 🌐 Iniciar el frontend:")
    print("   cd frontend")
    print("   npm start")
    print()
    print("4. 🧪 Probar el sistema:")
    print("   - Ve a http://localhost:3000/pos")
    print("   - Crea una venta de prueba")
    print("   - Ve a http://localhost:3000/dashboard/ventas")
    print("   - Verifica que la venta aparezca en el historial")
    print()
    print("5. 📊 Generar informes:")
    print("   - En la pantalla de ventas, ve a la pestaña 'Informes'")
    print("   - Selecciona un rango de fechas")
    print("   - Genera un informe")
    print()

def main():
    """Función principal de instalación"""
    print_header("INSTALACIÓN DEL SISTEMA DE VENTAS SOUP")
    
    print("🔧 Verificando requisitos...")
    
    # Verificar archivos
    files_ok = verify_files()
    if not files_ok:
        print("\n❌ Faltan archivos necesarios. Verifica la estructura del proyecto.")
        return
    
    # Instalar Firebase
    firebase_ok = install_firebase()
    if not firebase_ok:
        print("\n❌ Error instalando Firebase.")
        return
    
    # Crear configuración de Firebase
    config_ok = create_firebase_config_template()
    if not config_ok:
        print("\n❌ Error creando configuración de Firebase.")
        return
    
    # Verificar backend
    backend_ok = check_backend()
    if not backend_ok:
        print("\n⚠️  Backend no está corriendo. Inícialo antes de probar.")
    
    print_header("INSTALACIÓN COMPLETADA")
    print("✅ Sistema de ventas instalado correctamente")
    print("✅ Firebase configurado")
    print("✅ Archivos verificados")
    
    if backend_ok:
        print("✅ Backend funcionando")
    else:
        print("⚠️  Backend necesita ser iniciado")
    
    show_next_steps()

if __name__ == "__main__":
    main() 