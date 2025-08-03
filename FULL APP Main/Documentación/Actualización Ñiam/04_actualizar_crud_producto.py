#!/usr/bin/env python3
"""
Script: Actualizar CRUD de Producto con función record_sale
Capítulo Ñiam - SOUP Emprendimientos

Este script actualiza el archivo backend/app/crud/product.py para incluir
la función record_sale necesaria para el sistema de punto de venta.

Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import os
import shutil
from datetime import datetime

# Rutas de archivos
BACKEND_CRUD_PATH = "backend/app/crud/product.py"
BACKUP_PATH = "backend/app/crud/product_backup.py"

def crear_backup():
    """Crea una copia de seguridad del archivo product.py"""
    try:
        if os.path.exists(BACKEND_CRUD_PATH):
            shutil.copy2(BACKEND_CRUD_PATH, BACKUP_PATH)
            print(f"✅ Backup creado: {BACKUP_PATH}")
            return True
        else:
            print(f"❌ No se encontró el archivo: {BACKEND_CRUD_PATH}")
            return False
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return False

def leer_archivo_actual():
    """Lee el contenido actual del archivo product.py"""
    try:
        with open(BACKEND_CRUD_PATH, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"❌ Error al leer archivo: {e}")
        return None

def actualizar_crud_producto(contenido_actual):
    """Actualiza el CRUD de Producto con la función record_sale"""
    
    # Función record_sale a añadir
    funcion_record_sale = '''
def record_sale(db: Session, product_id: UUID, quantity_sold: float, user_id: UUID, precio_unitario: float = None):
    """
    Registra una venta de producto y actualiza el inventario
    
    Args:
        db: Sesión de base de datos
        product_id: ID del producto vendido
        quantity_sold: Cantidad vendida
        user_id: ID del usuario que registra la venta
        precio_unitario: Precio unitario de la venta (opcional, usa precio_venta del producto si no se proporciona)
    
    Returns:
        dict: Información de la venta registrada
    """
    from sqlalchemy.orm import joinedload
    from ..models import Producto, Insumo
    from ..schemas import VentaCreate
    
    # Obtener el producto con sus insumos asociados
    db_product = db.query(Producto).options(
        joinedload(Producto.insumos_asociados)
    ).filter(Producto.id == product_id).first()
    
    if not db_product:
        raise ValueError("Producto no encontrado")
    
    if db_product.propietario_id != user_id:
        raise ValueError("No autorizado para vender este producto")
    
    # Verificar stock disponible
    if db_product.stock_terminado is not None and db_product.stock_terminado < quantity_sold:
        raise ValueError(f"Stock insuficiente. Disponible: {db_product.stock_terminado}, Solicitado: {quantity_sold}")
    
    # Usar precio_venta del producto si no se proporciona precio_unitario
    if precio_unitario is None:
        precio_unitario = db_product.precio_venta or 0.0
    
    total_venta = precio_unitario * quantity_sold
    
    # Actualizar stock terminado del producto
    if db_product.stock_terminado is not None:
        db_product.stock_terminado -= quantity_sold
    
    # Actualizar insumos asociados al producto
    insumos_actualizados = []
    for insumo_asociado in db_product.insumos_asociados:
        insumo = db.query(Insumo).filter(Insumo.id == insumo_asociado.insumo_id).first()
        if insumo:
            cantidad_necesaria = insumo_asociado.cantidad_necesaria * quantity_sold
            insumo.cantidad_disponible -= cantidad_necesaria
            insumos_actualizados.append({
                'nombre': insumo.nombre,
                'cantidad_descontada': cantidad_necesaria,
                'stock_restante': insumo.cantidad_disponible
            })
    
    # TODO: Registrar la venta en tabla de transacciones (implementar en capítulo posterior)
    # Por ahora, solo actualizamos el inventario
    
    # Actualizar fecha_actualizacion del producto
    from sqlalchemy import func
    db_product.fecha_actualizacion = func.now()
    
    try:
        db.commit()
        db.refresh(db_product)
        
        return {
            'producto_id': product_id,
            'producto_nombre': db_product.nombre,
            'quantity_sold': quantity_sold,
            'precio_unitario': precio_unitario,
            'total_venta': total_venta,
            'stock_restante': db_product.stock_terminado,
            'insumos_actualizados': insumos_actualizados,
            'fecha_venta': datetime.now()
        }
        
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error al registrar la venta: {str(e)}")

def update_product_stock(db: Session, product_id: UUID, new_stock: float, user_id: UUID):
    """
    Actualiza el stock terminado de un producto
    
    Args:
        db: Sesión de base de datos
        product_id: ID del producto
        new_stock: Nueva cantidad de stock
        user_id: ID del usuario que actualiza
    
    Returns:
        Producto: Producto actualizado
    """
    db_product = get_product_by_id(db, product_id)
    
    if not db_product:
        raise ValueError("Producto no encontrado")
    
    if db_product.propietario_id != user_id:
        raise ValueError("No autorizado para actualizar este producto")
    
    db_product.stock_terminado = new_stock
    db_product.fecha_actualizacion = func.now()
    
    try:
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error al actualizar stock: {str(e)}")

def get_products_low_stock(db: Session, user_id: UUID, threshold: float = 5.0):
    """
    Obtiene productos con stock bajo
    
    Args:
        db: Sesión de base de datos
        user_id: ID del usuario
        threshold: Umbral de stock bajo (por defecto 5.0)
    
    Returns:
        List[Producto]: Lista de productos con stock bajo
    """
    return db.query(Producto).filter(
        Producto.propietario_id == user_id,
        Producto.stock_terminado <= threshold,
        Producto.stock_terminado > 0
    ).all()

def get_products_out_of_stock(db: Session, user_id: UUID):
    """
    Obtiene productos sin stock
    
    Args:
        db: Sesión de base de datos
        user_id: ID del usuario
    
    Returns:
        List[Producto]: Lista de productos sin stock
    """
    return db.query(Producto).filter(
        Producto.propietario_id == user_id,
        (Producto.stock_terminado == 0) | (Producto.stock_terminado.is_(None))
    ).all()
'''
    
    # Buscar el final del archivo para añadir las nuevas funciones
    lineas = contenido_actual.split('\n')
    
    # Buscar la última función existente
    ultima_funcion = -1
    for i, linea in enumerate(lineas):
        if linea.strip().startswith('def ') and ':' in linea:
            ultima_funcion = i
    
    if ultima_funcion == -1:
        print("❌ No se encontraron funciones en el archivo")
        return None
    
    # Añadir las nuevas funciones después de la última función
    lineas.insert(ultima_funcion + 1, funcion_record_sale)
    
    return '\n'.join(lineas)

def añadir_imports_necesarios(contenido_actual):
    """Añade los imports necesarios para las nuevas funciones"""
    
    # Verificar si ya están los imports necesarios
    imports_necesarios = [
        'from datetime import datetime',
        'from sqlalchemy import func'
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
        with open(BACKEND_CRUD_PATH, 'r', encoding='utf-8') as file:
            contenido = file.read()
        
        # Verificar que las funciones se añadieron correctamente
        funciones_verificar = [
            'def record_sale(',
            'def update_product_stock(',
            'def get_products_low_stock(',
            'def get_products_out_of_stock('
        ]
        
        for funcion in funciones_verificar:
            if funcion in contenido:
                print(f"✅ Función {funcion.split('(')[0]} añadida correctamente")
            else:
                print(f"❌ Función {funcion.split('(')[0]} no se añadió correctamente")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        return False

def mostrar_resumen_funciones():
    """Muestra un resumen de las nuevas funciones añadidas"""
    print("\n📋 Nuevas funciones añadidas al CRUD de Producto:")
    print("-" * 50)
    print("✅ record_sale(db, product_id, quantity_sold, user_id, precio_unitario=None)")
    print("   - Registra una venta y actualiza inventario")
    print("   - Descuenta stock terminado del producto")
    print("   - Actualiza cantidad disponible de insumos")
    print("   - Retorna información detallada de la venta")
    print("\n✅ update_product_stock(db, product_id, new_stock, user_id)")
    print("   - Actualiza el stock terminado de un producto")
    print("   - Verifica autorización del usuario")
    print("\n✅ get_products_low_stock(db, user_id, threshold=5.0)")
    print("   - Obtiene productos con stock bajo")
    print("   - Útil para alertas de inventario")
    print("\n✅ get_products_out_of_stock(db, user_id)")
    print("   - Obtiene productos sin stock")
    print("   - Para gestión de inventario")

def main():
    """Función principal del script"""
    print("🚀 Actualizando CRUD de Producto con función record_sale")
    print("=" * 60)
    
    # Paso 1: Crear backup
    print("\n📝 Paso 1: Creando backup del archivo original...")
    if not crear_backup():
        return
    
    # Paso 2: Leer archivo actual
    print("\n📝 Paso 2: Leyendo archivo product.py...")
    contenido_actual = leer_archivo_actual()
    if not contenido_actual:
        return
    
    # Paso 3: Añadir imports necesarios
    print("\n📝 Paso 3: Añadiendo imports necesarios...")
    contenido_actual = añadir_imports_necesarios(contenido_actual)
    
    # Paso 4: Actualizar CRUD con nuevas funciones
    print("\n📝 Paso 4: Añadiendo nuevas funciones...")
    contenido_actualizado = actualizar_crud_producto(contenido_actual)
    if not contenido_actualizado:
        print("❌ Falló la actualización del CRUD")
        return
    
    # Paso 5: Escribir archivo actualizado
    print("\n📝 Paso 5: Escribiendo archivo actualizado...")
    try:
        with open(BACKEND_CRUD_PATH, 'w', encoding='utf-8') as file:
            file.write(contenido_actualizado)
        print(f"✅ Archivo actualizado: {BACKEND_CRUD_PATH}")
    except Exception as e:
        print(f"❌ Error al escribir archivo: {e}")
        return
    
    # Paso 6: Verificar actualización
    print("\n📝 Paso 6: Verificando actualización...")
    if not verificar_actualizacion():
        return
    
    # Paso 7: Mostrar resumen
    print("\n📝 Paso 7: Mostrando resumen de funciones...")
    mostrar_resumen_funciones()
    
    print("\n" + "=" * 60)
    print("✅ Actualización del CRUD de Producto completada")
    print("📅 Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("🎯 Funciones listas para el sistema POS")
    print("\n📋 Próximos pasos:")
    print("  1. Crear endpoint de ventas en routers")
    print("  2. Actualizar frontend con pantalla POS")
    print("  3. Probar funcionalidad completa")

if __name__ == "__main__":
    main() 