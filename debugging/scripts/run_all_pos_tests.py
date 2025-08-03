#!/usr/bin/env python3
"""
Script principal para ejecutar todos los tests y actualizaciones del sistema POS
Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import os
import sys
import subprocess
from datetime import datetime

def run_script(script_name, description):
    """Ejecutar un script específico"""
    print(f"\n🔄 EJECUTANDO: {description}")
    print("=" * 60)
    
    script_path = f"debugging/scripts/{script_name}"
    
    if not os.path.exists(script_path):
        print(f"❌ Script no encontrado: {script_path}")
        return False
    
    try:
        # Ejecutar el script
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, 
                              text=True, 
                              encoding='utf-8')
        
        # Mostrar salida
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("⚠️ Errores:")
            print(result.stderr)
        
        # Verificar resultado
        if result.returncode == 0:
            print(f"✅ {description} completado exitosamente")
            return True
        else:
            print(f"❌ {description} falló con código: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando {script_name}: {e}")
        return False

def check_prerequisites():
    """Verificar prerequisitos antes de ejecutar los tests"""
    print("🔍 VERIFICANDO PREREQUISITOS")
    print("=" * 40)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print("❌ No se encontraron los directorios backend y frontend")
        print("   Asegúrate de estar en el directorio raíz del proyecto")
        return False
    
    # Verificar que existe el directorio de scripts
    if not os.path.exists("debugging/scripts"):
        print("❌ No se encontró el directorio debugging/scripts")
        return False
    
    print("✅ Prerequisitos verificados")
    return True

def main():
    """Función principal"""
    print("🚀 EJECUTOR COMPLETO DE TESTS Y ACTUALIZACIONES DEL SISTEMA POS")
    print("=" * 80)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Verificar prerequisitos
    if not check_prerequisites():
        print("❌ Prerequisitos no cumplidos. Abortando ejecución.")
        return
    
    # Lista de scripts a ejecutar en orden
    scripts = [
        ("test_pos_endpoints.py", "Testing de endpoints del sistema POS"),
        ("update_frontend_pos.py", "Actualización del frontend con funcionalidades POS"),
        ("test_integration_pos.py", "Testing de integración completa"),
    ]
    
    print("📋 SCRIPTS A EJECUTAR:")
    for i, (script, description) in enumerate(scripts, 1):
        print(f"   {i}. {script} - {description}")
    
    print(f"\n⏱️ Iniciando ejecución de {len(scripts)} scripts...")
    
    # Ejecutar scripts
    results = []
    for script, description in scripts:
        success = run_script(script, description)
        results.append((script, description, success))
        
        if not success:
            print(f"\n⚠️ El script {script} falló. ¿Deseas continuar con los siguientes?")
            print("   Presiona Enter para continuar o Ctrl+C para abortar...")
            try:
                input()
            except KeyboardInterrupt:
                print("\n❌ Ejecución abortada por el usuario")
                return
    
    # Resumen final
    print("\n" + "=" * 80)
    print("📋 RESUMEN FINAL DE EJECUCIÓN")
    print("=" * 80)
    
    successful_scripts = sum(1 for _, _, success in results if success)
    total_scripts = len(results)
    
    for script, description, success in results:
        status_icon = "✅" if success else "❌"
        print(f"{status_icon} {script}: {description}")
    
    print(f"\n📊 Resultados: {successful_scripts}/{total_scripts} scripts exitosos")
    
    if successful_scripts == total_scripts:
        print("\n🎉 ¡TODOS LOS SCRIPTS SE EJECUTARON EXITOSAMENTE!")
        print("✅ El sistema POS está completamente configurado y probado")
        print("\n📋 Próximos pasos:")
        print("   1. Inicia el backend: cd backend && python -m uvicorn app.main:app --reload")
        print("   2. Inicia el frontend: cd frontend && npm start")
        print("   3. Accede al sistema POS en: http://localhost:3000/pos")
    else:
        print(f"\n⚠️ {total_scripts - successful_scripts} scripts fallaron")
        print("Revisa los errores arriba y ejecuta manualmente los scripts fallidos")
    
    # Generar reporte final
    report_file = f"debugging/reportes/ejecucion_completa_pos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("REPORTE DE EJECUCIÓN COMPLETA DEL SISTEMA POS\n")
        f.write("=" * 50 + "\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for script, description, success in results:
            status = "EXITOSO" if success else "FALLÓ"
            f.write(f"{script}: {description} - {status}\n")
        
        f.write(f"\nResumen: {successful_scripts}/{total_scripts} scripts exitosos\n")
    
    print(f"\n📄 Reporte guardado en: {report_file}")

if __name__ == "__main__":
    main() 