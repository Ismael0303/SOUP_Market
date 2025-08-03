#!/usr/bin/env python3
"""
Script Principal: Ejecución Completa de Actualización Capítulo Ñiam
SOUP Emprendimientos

Este script ejecuta todos los scripts de actualización necesarios para implementar
el Capítulo Ñiam (Workflow Interno y Gestión de Ventas en Local) en el orden correcto.

Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import os
import sys
import subprocess
import time
from datetime import datetime

# Configuración
SCRIPTS_DIR = "Documentación/Actualización Ñiam"
WORKSPACE_ROOT = os.getcwd()

# Lista de scripts en orden de ejecución
SCRIPTS_ORDER = [
    "01_migracion_stock_terminado.py",
    "02_actualizar_modelo_producto.py", 
    "03_actualizar_schemas_producto.py",
    "04_actualizar_crud_producto.py",
    "05_crear_endpoint_ventas.py"
]

# Scripts de frontend (manuales)
FRONTEND_SCRIPTS = [
    "06_crear_pantalla_pos.jsx",
    "07_actualizar_api_producto.js", 
    "08_actualizar_rutas_app.js",
    "09_actualizar_manage_products.jsx"
]

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"ACTUALIZACION - {title}")
    print("="*60)

def print_step(step_num, description):
    """Imprime un paso de ejecución"""
    print(f"\nPaso {step_num}: {description}")
    print("-" * 40)

def check_prerequisites():
    """Verifica los prerequisitos antes de ejecutar"""
    print_header("VERIFICACION DE PREREQUISITOS")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print("Error: No se encontraron las carpetas 'backend' y 'frontend'")
        print("   Asegurate de estar en el directorio raiz del proyecto SOUP")
        return False
    
    # Verificar que existe la carpeta de scripts
    if not os.path.exists(SCRIPTS_DIR):
        print("Error: No se encontro la carpeta de scripts de actualizacion")
        return False
    
    # Verificar que todos los scripts existen
    for script in SCRIPTS_ORDER:
        script_path = os.path.join(SCRIPTS_DIR, script)
        if not os.path.exists(script_path):
            print(f"Error: No se encontro el script {script}")
            return False
    
    print("Todos los prerequisitos estan cumplidos")
    return True

def execute_script(script_name, step_num):
    """Ejecuta un script individual"""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    
    print_step(step_num, f"Ejecutando {script_name}")
    print(f"Script: {script_path}")
    
    try:
        # Ejecutar el script
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            cwd=WORKSPACE_ROOT
        )
        
        # Mostrar salida
        if result.stdout:
            print("Salida:")
            print(result.stdout)
        
        if result.stderr:
            print("Advertencias/Errores:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("Script ejecutado exitosamente")
            return True
        else:
            print(f"Script fallo con codigo de salida: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"Error al ejecutar script: {e}")
        return False

def execute_backend_scripts():
    """Ejecuta todos los scripts del backend"""
    print_header("EJECUTANDO SCRIPTS DEL BACKEND")
    
    success_count = 0
    total_scripts = len(SCRIPTS_ORDER)
    
    for i, script in enumerate(SCRIPTS_ORDER, 1):
        if execute_script(script, i):
            success_count += 1
        else:
            print(f"Fallo la ejecucion de {script}")
            print("Deteniendo ejecucion...")
            return False
        
        # Pausa entre scripts
        if i < total_scripts:
            print("Esperando 2 segundos antes del siguiente script...")
            time.sleep(2)
    
    print(f"\nBackend completado: {success_count}/{total_scripts} scripts exitosos")
    return True

def show_frontend_instructions():
    """Muestra las instrucciones para el frontend"""
    print_header("INSTRUCCIONES PARA EL FRONTEND")
    
    print("Los siguientes archivos deben ser creados/actualizados manualmente:")
    print()
    
    for i, script in enumerate(FRONTEND_SCRIPTS, 1):
        print(f"{i}. {script}")
    
    print("\nPasos para completar el frontend:")
    print("1. Crear archivo: frontend/src/screens/SalePointScreen.jsx")
    print("   - Usar el contenido de: 06_crear_pantalla_pos.jsx")
    print()
    print("2. Actualizar archivo: frontend/src/api/productApi.js")
    print("   - Anadir las nuevas funciones de: 07_actualizar_api_producto.js")
    print()
    print("3. Actualizar archivo: frontend/src/App.js")
    print("   - Anadir la ruta del POS usando: 08_actualizar_rutas_app.js")
    print()
    print("4. Actualizar archivo: frontend/src/screens/ManageProductsScreen.js")
    print("   - Integrar las metricas financieras de: 09_actualizar_manage_products.jsx")
    print()
    print("5. Actualizar archivo: frontend/src/screens/DashboardScreen.js")
    print("   - Anadir boton 'Punto de Venta' que navegue a /dashboard/pos")

def create_summary_report():
    """Crea un reporte de resumen de la actualización"""
    report_path = os.path.join(SCRIPTS_DIR, f"reporte_actualizacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    
    report_content = f"""# Reporte de Actualización - Capítulo Ñiam

**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Proyecto:** SOUP Emprendimientos
**Capítulo:** Workflow Interno y Gestión de Ventas en Local (Panadería Ñiam)

## Scripts Ejecutados Exitosamente

### Backend
1. **01_migracion_stock_terminado.py** - Migración de base de datos
2. **02_actualizar_modelo_producto.py** - Actualización del modelo Producto
3. **03_actualizar_schemas_producto.py** - Actualización de schemas
4. **04_actualizar_crud_producto.py** - Nuevas funciones CRUD
5. **05_crear_endpoint_ventas.py** - Endpoints de ventas

### Frontend (Manual)
- [ ] Crear SalePointScreen.jsx
- [ ] Actualizar productApi.js
- [ ] Actualizar App.js con rutas
- [ ] Actualizar ManageProductsScreen.js
- [ ] Actualizar DashboardScreen.js

## Funcionalidades Implementadas

### Backend
- Campo `stock_terminado` en modelo Producto
- Función `record_sale` para registrar ventas
- Función `update_product_stock` para ajustar inventario
- Función `get_products_low_stock` para alertas
- Función `get_products_out_of_stock` para gestión
- Endpoint `POST /products/{id}/record_sale`
- Endpoint `PUT /products/{id}/stock`
- Endpoint `GET /products/low_stock`
- Endpoint `GET /products/out_of_stock`

### Frontend (Pendiente)
- [ ] Pantalla de Punto de Venta (POS)
- [ ] Integración con API de ventas
- [ ] Métricas financieras en lista de productos
- [ ] Navegación al POS desde dashboard

## Próximos Pasos

1. **Completar Frontend:**
   - Crear SalePointScreen.jsx
   - Actualizar APIs del frontend
   - Integrar rutas en App.js
   - Añadir métricas en ManageProductsScreen

2. **Probar Funcionalidad:**
   - Probar registro de ventas
   - Verificar actualización de inventario
   - Probar interfaz de punto de venta
   - Validar métricas financieras

3. **Documentación:**
   - Actualizar documentación técnica
   - Crear guía de usuario para POS
   - Documentar flujo de trabajo

## Comandos Útiles

### Probar Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Probar Frontend
```bash
cd frontend
npm start
```

### Verificar Base de Datos
```bash
psql -U soupuser -d soup_app_db -h localhost -p 5432
```

## Notas Importantes

- Los scripts del frontend deben aplicarse manualmente
- Verificar que todos los imports estén correctos
- Probar cada funcionalidad antes de continuar
- Mantener backups de archivos modificados

---
**Generado automáticamente por el script de actualización**
"""
    
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"Reporte creado: {report_path}")
        return report_path
    except Exception as e:
        print(f"Error al crear reporte: {e}")
        return None

def main():
    """Función principal del script"""
    print_header("ACTUALIZACION COMPLETA - CAPITULO ÑIAM")
    print("SOUP Emprendimientos - Workflow Interno y Gestión de Ventas en Local")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar prerequisitos
    if not check_prerequisites():
        print("\nNo se pueden cumplir los prerequisitos. Abortando...")
        sys.exit(1)
    
    # Confirmar ejecución
    print("\nADVERTENCIA: Este script modificará archivos del proyecto.")
    print("   Se recomienda hacer backup antes de continuar.")
    
    confirm = input("\n¿Deseas continuar con la actualización? (s/N): ")
    if confirm.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
        print("Actualización cancelada por el usuario")
        sys.exit(0)
    
    # Ejecutar scripts del backend
    if not execute_backend_scripts():
        print("\nFallo la ejecucion de scripts del backend")
        sys.exit(1)
    
    # Mostrar instrucciones del frontend
    show_frontend_instructions()
    
    # Crear reporte de resumen
    report_path = create_summary_report()
    
    print_header("ACTUALIZACION COMPLETADA")
    print("Backend actualizado exitosamente")
    print("Frontend requiere actualizacion manual")
    print("Revisa las instrucciones anteriores")
    
    if report_path:
        print(f"Reporte detallado: {report_path}")
    
    print("\nPróximos pasos:")
    print("1. Completar actualización del frontend")
    print("2. Probar funcionalidad completa")
    print("3. Documentar cambios realizados")
    
    print("\n¡El Capítulo Ñiam está listo para implementar!")

if __name__ == "__main__":
    main() 