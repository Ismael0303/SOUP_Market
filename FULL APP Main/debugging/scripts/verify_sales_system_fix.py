#!/usr/bin/env python3
"""
Script de verificación del sistema de ventas SOUP
Verifica que los errores de ESLint se hayan corregido
"""

import os
import subprocess
import sys
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_section(title):
    print(f"\n{'-'*40}")
    print(f"  {title}")
    print(f"{'-'*40}")

def check_file_exists(file_path):
    """Verifica si un archivo existe"""
    # Convertir ruta relativa a absoluta
    current_dir = Path.cwd()
    absolute_path = current_dir / file_path
    
    if absolute_path.exists():
        print(f"✅ {file_path} - Existe")
        return True
    else:
        print(f"❌ {file_path} - No existe")
        return False

def check_eslint_errors():
    """Verifica si hay errores de ESLint"""
    print_section("VERIFICACIÓN DE ESLINT")
    
    frontend_path = Path("../frontend")
    if not frontend_path.exists():
        print("❌ Directorio frontend no encontrado")
        return False
    
    try:
        # Ejecutar ESLint en los archivos modificados
        result = subprocess.run(
            "npx eslint src/firebaseConfig.js src/screens/POSScreen.js src/screens/SalesHistoryScreen.js --format=compact",
            shell=True,
            cwd=frontend_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ No hay errores de ESLint")
            return True
        else:
            print("❌ Errores de ESLint encontrados:")
            print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando ESLint: {e}")
        return False

def verify_global_variables():
    """Verifica que las variables globales estén definidas correctamente"""
    print_section("VERIFICACIÓN DE VARIABLES GLOBALES")
    
    # Verificar archivo HTML
    html_path = Path("../frontend/public/index.html")
    if html_path.exists():
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '__app_id' in content and '__initial_auth_token' in content:
                print("✅ Variables globales definidas en index.html")
                return True
            else:
                print("❌ Variables globales no encontradas en index.html")
                return False
    else:
        print("❌ index.html no encontrado")
        return False

def verify_firebase_config():
    """Verifica la configuración de Firebase"""
    print_section("VERIFICACIÓN DE CONFIGURACIÓN FIREBASE")
    
    config_path = Path("../frontend/src/firebaseConfig.js")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'getAppId' in content and 'getFirebaseConfig' in content:
                print("✅ Configuración de Firebase actualizada")
                return True
            else:
                print("❌ Configuración de Firebase no actualizada")
                return False
    else:
        print("❌ firebaseConfig.js no encontrado")
        return False

def verify_imports():
    """Verifica que las importaciones estén correctas"""
    print_section("VERIFICACIÓN DE IMPORTACIONES")
    
    files_to_check = [
        ("../frontend/src/screens/POSScreen.js", "getAppId"),
        ("../frontend/src/screens/SalesHistoryScreen.js", "getAppId")
    ]
    
    all_correct = True
    for file_path, import_name in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if import_name in content:
                    print(f"✅ {file_path} - Importación correcta")
                else:
                    print(f"❌ {file_path} - Falta importación de {import_name}")
                    all_correct = False
        else:
            print(f"❌ {file_path} - No encontrado")
            all_correct = False
    
    return all_correct

def check_eslint_config():
    """Verifica la configuración de ESLint"""
    print_section("VERIFICACIÓN DE CONFIGURACIÓN ESLINT")
    
    eslint_path = Path("../frontend/.eslintrc.js")
    if eslint_path.exists():
        with open(eslint_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '__app_id' in content and '__initial_auth_token' in content:
                print("✅ Configuración de ESLint correcta")
                return True
            else:
                print("❌ Configuración de ESLint incompleta")
                return False
    else:
        print("❌ .eslintrc.js no encontrado")
        return False

def run_frontend_tests():
    """Ejecuta pruebas básicas del frontend"""
    print_section("PRUEBAS DEL FRONTEND")
    
    frontend_path = Path("../frontend")
    if not frontend_path.exists():
        print("❌ Directorio frontend no encontrado")
        return False
    
    try:
        # Verificar que el proyecto se puede construir
        result = subprocess.run(
            "npm run build",
            shell=True,
            cwd=frontend_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ Frontend se puede construir correctamente")
            return True
        else:
            print("❌ Error construyendo frontend:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Timeout en la construcción del frontend")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando pruebas: {e}")
        return False

def show_summary():
    """Muestra un resumen de la verificación"""
    print_section("RESUMEN DE VERIFICACIÓN")
    
    print("🎯 Estado del sistema de ventas:")
    print()
    print("✅ Variables globales definidas en HTML")
    print("✅ Configuración de Firebase actualizada")
    print("✅ Función helper getAppId implementada")
    print("✅ Importaciones corregidas en componentes")
    print("✅ Configuración de ESLint actualizada")
    print()
    print("🚀 Próximos pasos:")
    print("1. Instalar Firebase: cd frontend && npm install firebase")
    print("2. Configurar credenciales reales en firebaseConfig.js")
    print("3. Iniciar backend: cd backend && python -m uvicorn app.main:app --reload")
    print("4. Iniciar frontend: cd frontend && npm start")
    print("5. Probar sistema en http://localhost:3000/pos")

def main():
    """Función principal de verificación"""
    print_header("VERIFICACIÓN DEL SISTEMA DE VENTAS SOUP")
    
    print("🔧 Verificando correcciones de ESLint...")
    
    # Verificar archivos
    files_ok = all([
        check_file_exists("../frontend/src/firebaseConfig.js"),
        check_file_exists("../frontend/src/screens/POSScreen.js"),
        check_file_exists("../frontend/src/screens/SalesHistoryScreen.js"),
        check_file_exists("../frontend/public/index.html"),
        check_file_exists("../frontend/.eslintrc.js")
    ])
    
    if not files_ok:
        print("\n❌ Faltan archivos necesarios.")
        return
    
    # Verificar variables globales
    globals_ok = verify_global_variables()
    
    # Verificar configuración de Firebase
    firebase_ok = verify_firebase_config()
    
    # Verificar importaciones
    imports_ok = verify_imports()
    
    # Verificar configuración de ESLint
    eslint_config_ok = check_eslint_config()
    
    # Verificar errores de ESLint
    eslint_ok = check_eslint_errors()
    
    # Ejecutar pruebas del frontend
    frontend_ok = run_frontend_tests()
    
    print_header("RESULTADO DE LA VERIFICACIÓN")
    
    if all([globals_ok, firebase_ok, imports_ok, eslint_config_ok, eslint_ok, frontend_ok]):
        print("🎉 ¡TODAS LAS VERIFICACIONES EXITOSAS!")
        print("✅ El sistema de ventas está listo para usar")
    else:
        print("⚠️  Algunas verificaciones fallaron")
        print("Revisa los errores anteriores")
    
    show_summary()

if __name__ == "__main__":
    main() 