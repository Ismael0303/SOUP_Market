#!/usr/bin/env python3
"""
Script: Crear Endpoint de Ventas en Router de Productos
Capítulo Ñiam - SOUP Emprendimientos

Este script añade el endpoint POST /products/{product_id}/record_sale al router
de productos para permitir el registro de ventas desde el sistema POS.

Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import os
import shutil
from datetime import datetime

# Rutas de archivos
BACKEND_ROUTER_PATH = "backend/app/routers/product_router.py"
BACKUP_PATH = "backend/app/routers/product_router_backup.py"

def crear_backup():
    """Crea una copia de seguridad del archivo product_router.py"""
    try:
        if os.path.exists(BACKEND_ROUTER_PATH):
            shutil.copy2(BACKEND_ROUTER_PATH, BACKUP_PATH)
            print(f"✅ Backup creado: {BACKUP_PATH}")
            return True
        else:
            print(f"❌ No se encontró el archivo: {BACKEND_ROUTER_PATH}")
            return False
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return False

def leer_archivo_actual():
    """Lee el contenido actual del archivo product_router.py"""
    try:
        with open(BACKEND_ROUTER_PATH, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"❌ Error al leer archivo: {e}")
        return None

def añadir_endpoint_ventas(contenido_actual):
    """Añade el endpoint de ventas al router"""
    
    # Endpoint de ventas a añadir
    endpoint_ventas = '''
@router.post("/{product_id}/record_sale", response_model=dict)
def record_product_sale(
    product_id: UUID,
    sale_data: VentaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Registra una venta de producto y actualiza el inventario
    
    Args:
        product_id: ID del producto a vender
        sale_data: Datos de la venta (cantidad, precio, etc.)
        db: Sesión de base de datos
        current_user: Usuario autenticado
    
    Returns:
        dict: Información de la venta registrada
    """
    try:
        # Verificar que el usuario tiene permisos para vender este producto
        db_product = crud_product.get_product_by_id(db, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        if db_product.propietario_id != current_user.id:
            raise HTTPException(status_code=403, detail="No autorizado para vender este producto")
        
        # Registrar la venta
        venta_info = crud_product.record_sale(
            db=db,
            product_id=product_id,
            quantity_sold=sale_data.quantity_sold,
            user_id=current_user.id,
            precio_unitario=sale_data.precio_unitario
        )
        
        return {
            "success": True,
            "message": "Venta registrada exitosamente",
            "venta_info": venta_info
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put("/{product_id}/stock", response_model=ProductoResponse)
def update_product_stock(
    product_id: UUID,
    stock_data: dict,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualiza el stock terminado de un producto
    
    Args:
        product_id: ID del producto
        stock_data: {"new_stock": float} - Nueva cantidad de stock
        db: Sesión de base de datos
        current_user: Usuario autenticado
    
    Returns:
        ProductoResponse: Producto actualizado
    """
    try:
        new_stock = stock_data.get("new_stock")
        if new_stock is None or new_stock < 0:
            raise HTTPException(status_code=400, detail="new_stock debe ser un número positivo")
        
        db_product = crud_product.update_product_stock(
            db=db,
            product_id=product_id,
            new_stock=new_stock,
            user_id=current_user.id
        )
        
        return db_product
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/low_stock", response_model=List[ProductoResponse])
def get_products_low_stock(
    threshold: float = Query(5.0, description="Umbral de stock bajo"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene productos con stock bajo
    
    Args:
        threshold: Umbral de stock bajo (por defecto 5.0)
        db: Sesión de base de datos
        current_user: Usuario autenticado
    
    Returns:
        List[ProductoResponse]: Lista de productos con stock bajo
    """
    try:
        productos = crud_product.get_products_low_stock(
            db=db,
            user_id=current_user.id,
            threshold=threshold
        )
        return productos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/out_of_stock", response_model=List[ProductoResponse])
def get_products_out_of_stock(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene productos sin stock
    
    Args:
        db: Sesión de base de datos
        current_user: Usuario autenticado
    
    Returns:
        List[ProductoResponse]: Lista de productos sin stock
    """
    try:
        productos = crud_product.get_products_out_of_stock(
            db=db,
            user_id=current_user.id
        )
        return productos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
'''
    
    # Buscar el final del archivo para añadir los nuevos endpoints
    lineas = contenido_actual.split('\n')
    
    # Buscar la última función de endpoint
    ultimo_endpoint = -1
    for i, linea in enumerate(lineas):
        if '@router.' in linea:
            ultimo_endpoint = i
    
    if ultimo_endpoint == -1:
        print("❌ No se encontraron endpoints en el archivo")
        return None
    
    # Buscar el final de la última función de endpoint
    fin_ultima_funcion = ultimo_endpoint
    for i in range(ultimo_endpoint + 1, len(lineas)):
        if lineas[i].strip() == '' and i > ultimo_endpoint + 1:
            fin_ultima_funcion = i
            break
    
    # Añadir los nuevos endpoints después del último
    lineas.insert(fin_ultima_funcion + 1, endpoint_ventas)
    
    return '\n'.join(lineas)

def añadir_imports_necesarios(contenido_actual):
    """Añade los imports necesarios para los nuevos endpoints"""
    
    # Verificar si ya están los imports necesarios
    imports_necesarios = [
        'from typing import List',
        'from fastapi import Query',
        'from ..schemas import VentaCreate'
    ]
    
    lineas = contenido_actual.split('\n')
    imports_faltantes = []
    
    for import_line in imports_necesarios:
        if import_line not in contenido_actual:
            imports_faltantes.append(import_line)
    
    if not imports_faltantes:
        print("✅ Todos los imports necesarios ya están presentes")
        return contenido_actual
    
    # Añadir imports faltantes al final de la sección de imports
    for i, linea in enumerate(lineas):
        if linea.startswith('from ') or linea.startswith('import '):
            continue
        elif linea.strip() == '':
            # Encontrar el final de los imports
            for j in range(i, len(lineas)):
                if lineas[j].strip() != '':
                    # Insertar imports faltantes antes de la primera línea no vacía
                    for import_line in imports_faltantes:
                        lineas.insert(j, import_line)
                    print(f"✅ Imports añadidos: {imports_faltantes}")
                    break
            break
    
    return '\n'.join(lineas)

def verificar_actualizacion():
    """Verifica que la actualización se haya realizado correctamente"""
    try:
        with open(BACKEND_ROUTER_PATH, 'r', encoding='utf-8') as file:
            contenido = file.read()
        
        # Verificar que los endpoints se añadieron correctamente
        endpoints_verificar = [
            '@router.post("/{product_id}/record_sale"',
            '@router.put("/{product_id}/stock"',
            '@router.get("/low_stock"',
            '@router.get("/out_of_stock"'
        ]
        
        for endpoint in endpoints_verificar:
            if endpoint in contenido:
                print(f"✅ Endpoint {endpoint.split('(')[0]} añadido correctamente")
            else:
                print(f"❌ Endpoint {endpoint.split('(')[0]} no se añadió correctamente")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        return False

def mostrar_resumen_endpoints():
    """Muestra un resumen de los nuevos endpoints añadidos"""
    print("\n📋 Nuevos endpoints añadidos al Router de Productos:")
    print("-" * 50)
    print("✅ POST /products/{product_id}/record_sale")
    print("   - Registra una venta de producto")
    print("   - Actualiza inventario automáticamente")
    print("   - Requiere autenticación y autorización")
    print("\n✅ PUT /products/{product_id}/stock")
    print("   - Actualiza el stock terminado de un producto")
    print("   - Útil para ajustes manuales de inventario")
    print("\n✅ GET /products/low_stock?threshold=5.0")
    print("   - Obtiene productos con stock bajo")
    print("   - Parámetro threshold opcional (default: 5.0)")
    print("\n✅ GET /products/out_of_stock")
    print("   - Obtiene productos sin stock")
    print("   - Para alertas de inventario")

def main():
    """Función principal del script"""
    print("🚀 Creando Endpoint de Ventas en Router de Productos")
    print("=" * 60)
    
    # Paso 1: Crear backup
    print("\n📝 Paso 1: Creando backup del archivo original...")
    if not crear_backup():
        return
    
    # Paso 2: Leer archivo actual
    print("\n📝 Paso 2: Leyendo archivo product_router.py...")
    contenido_actual = leer_archivo_actual()
    if not contenido_actual:
        return
    
    # Paso 3: Añadir imports necesarios
    print("\n📝 Paso 3: Añadiendo imports necesarios...")
    contenido_actual = añadir_imports_necesarios(contenido_actual)
    
    # Paso 4: Añadir endpoints de ventas
    print("\n📝 Paso 4: Añadiendo endpoints de ventas...")
    contenido_actualizado = añadir_endpoint_ventas(contenido_actual)
    if not contenido_actualizado:
        print("❌ Falló la adición de endpoints")
        return
    
    # Paso 5: Escribir archivo actualizado
    print("\n📝 Paso 5: Escribiendo archivo actualizado...")
    try:
        with open(BACKEND_ROUTER_PATH, 'w', encoding='utf-8') as file:
            file.write(contenido_actualizado)
        print(f"✅ Archivo actualizado: {BACKEND_ROUTER_PATH}")
    except Exception as e:
        print(f"❌ Error al escribir archivo: {e}")
        return
    
    # Paso 6: Verificar actualización
    print("\n📝 Paso 6: Verificando actualización...")
    if not verificar_actualizacion():
        return
    
    # Paso 7: Mostrar resumen
    print("\n📝 Paso 7: Mostrando resumen de endpoints...")
    mostrar_resumen_endpoints()
    
    print("\n" + "=" * 60)
    print("✅ Endpoints de ventas creados exitosamente")
    print("📅 Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("🎯 Backend listo para el sistema POS")
    print("\n📋 Próximos pasos:")
    print("  1. Crear pantalla POS en frontend")
    print("  2. Actualizar API del frontend")
    print("  3. Probar funcionalidad completa")

if __name__ == "__main__":
    main() 