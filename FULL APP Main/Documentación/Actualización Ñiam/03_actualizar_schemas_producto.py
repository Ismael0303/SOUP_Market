#!/usr/bin/env python3
"""
Script: Actualizar Schemas de Producto con campo stock_terminado
Capítulo Ñiam - SOUP Emprendimientos

Este script actualiza los schemas de Producto en backend/app/schemas.py para incluir
el campo stock_terminado necesario para el sistema de punto de venta.

Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import os
import shutil
from datetime import datetime

# Rutas de archivos
BACKEND_SCHEMAS_PATH = "backend/app/schemas.py"
BACKUP_PATH = "backend/app/schemas_backup.py"

def crear_backup():
    """Crea una copia de seguridad del archivo schemas.py"""
    try:
        if os.path.exists(BACKEND_SCHEMAS_PATH):
            shutil.copy2(BACKEND_SCHEMAS_PATH, BACKUP_PATH)
            print(f"✅ Backup creado: {BACKUP_PATH}")
            return True
        else:
            print(f"❌ No se encontró el archivo: {BACKEND_SCHEMAS_PATH}")
            return False
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return False

def leer_archivo_actual():
    """Lee el contenido actual del archivo schemas.py"""
    try:
        with open(BACKEND_SCHEMAS_PATH, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"❌ Error al leer archivo: {e}")
        return None

def actualizar_schemas_producto(contenido_actual):
    """Actualiza los schemas de Producto con el campo stock_terminado"""
    
    # Buscar los schemas de Producto
    schemas_producto = [
        'ProductoCreate',
        'ProductoUpdate', 
        'ProductoResponse',
        'ProductoInDB'
    ]
    
    lineas = contenido_actual.split('\n')
    nueva_linea = []
    
    for i, linea in enumerate(lineas):
        nueva_linea.append(linea)
        
        # Buscar cada schema de Producto
        for schema in schemas_producto:
            if f'class {schema}(' in linea:
                print(f"📝 Encontrado schema: {schema}")
                
                # Buscar el final del schema (línea con solo ')' o línea vacía después de campos)
                j = i + 1
                while j < len(lineas):
                    nueva_linea.append(lineas[j])
                    
                    # Si encontramos el final del schema
                    if (lineas[j].strip() == ')' or 
                        (lineas[j].strip() == '' and j > i + 1 and ':' in lineas[j-1])):
                        
                        # Añadir el campo stock_terminado antes del cierre
                        if schema in ['ProductoCreate', 'ProductoUpdate']:
                            # Para Create y Update, el campo es opcional
                            campo = "    stock_terminado: Optional[float] = None"
                        else:
                            # Para Response e InDB, el campo es requerido
                            campo = "    stock_terminado: float"
                        
                        nueva_linea.insert(j, campo)
                        nueva_linea.insert(j, "")
                        print(f"  ✅ Campo stock_terminado añadido a {schema}")
                        break
                    
                    j += 1
                break
    
    return '\n'.join(nueva_linea)

def añadir_schema_venta():
    """Añade el schema para registrar ventas"""
    try:
        with open(BACKEND_SCHEMAS_PATH, 'r', encoding='utf-8') as file:
            contenido = file.read()
        
        # Definir el schema para ventas
        schema_venta = """

# Schema para registro de ventas (Capítulo Ñiam)
class VentaCreate(BaseModel):
    product_id: UUID
    quantity_sold: float
    precio_unitario: float
    total_venta: float
    notas: Optional[str] = None

class VentaResponse(BaseModel):
    id: UUID
    product_id: UUID
    quantity_sold: float
    precio_unitario: float
    total_venta: float
    fecha_venta: datetime
    notas: Optional[str] = None
    usuario_id: UUID
    
    class Config:
        from_attributes = True

class VentaInDB(BaseModel):
    id: UUID
    product_id: UUID
    quantity_sold: float
    precio_unitario: float
    total_venta: float
    fecha_venta: datetime
    notas: Optional[str] = None
    usuario_id: UUID
    
    class Config:
        from_attributes = True
"""
        
        # Añadir al final del archivo, antes de las últimas líneas
        lineas = contenido.split('\n')
        
        # Buscar el final del archivo (después del último schema)
        for i in range(len(lineas) - 1, -1, -1):
            if 'class ' in lineas[i] and 'BaseModel' in lineas[i]:
                # Insertar después del último schema
                lineas.insert(i + 1, schema_venta)
                break
        
        contenido_actualizado = '\n'.join(lineas)
        
        with open(BACKEND_SCHEMAS_PATH, 'w', encoding='utf-8') as file:
            file.write(contenido_actualizado)
        
        print("✅ Schema de ventas añadido")
        return True
        
    except Exception as e:
        print(f"❌ Error al añadir schema de ventas: {e}")
        return False

def verificar_actualizacion():
    """Verifica que la actualización se haya realizado correctamente"""
    try:
        with open(BACKEND_SCHEMAS_PATH, 'r', encoding='utf-8') as file:
            contenido = file.read()
        
        # Verificar que los campos se añadieron correctamente
        schemas_verificar = {
            'ProductoCreate': 'stock_terminado: Optional[float] = None',
            'ProductoUpdate': 'stock_terminado: Optional[float] = None',
            'ProductoResponse': 'stock_terminado: float',
            'VentaCreate': 'class VentaCreate(BaseModel):'
        }
        
        for schema, campo in schemas_verificar.items():
            if campo in contenido:
                print(f"✅ Schema {schema} actualizado correctamente")
            else:
                print(f"❌ Schema {schema} no se actualizó correctamente")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        return False

def mostrar_resumen_cambios():
    """Muestra un resumen de los cambios realizados"""
    print("\n📋 Resumen de cambios en schemas.py:")
    print("-" * 50)
    print("✅ Campo stock_terminado añadido a:")
    print("   - ProductoCreate (opcional)")
    print("   - ProductoUpdate (opcional)")
    print("   - ProductoResponse (requerido)")
    print("   - ProductoInDB (requerido)")
    print("\n✅ Nuevos schemas añadidos:")
    print("   - VentaCreate")
    print("   - VentaResponse")
    print("   - VentaInDB")
    print("\n🎯 Campos del schema VentaCreate:")
    print("   - product_id: UUID")
    print("   - quantity_sold: float")
    print("   - precio_unitario: float")
    print("   - total_venta: float")
    print("   - notas: Optional[str]")

def main():
    """Función principal del script"""
    print("🚀 Actualizando Schemas de Producto con campo stock_terminado")
    print("=" * 60)
    
    # Paso 1: Crear backup
    print("\n📝 Paso 1: Creando backup del archivo original...")
    if not crear_backup():
        return
    
    # Paso 2: Leer archivo actual
    print("\n📝 Paso 2: Leyendo archivo schemas.py...")
    contenido_actual = leer_archivo_actual()
    if not contenido_actual:
        return
    
    # Paso 3: Actualizar schemas de Producto
    print("\n📝 Paso 3: Actualizando schemas de Producto...")
    contenido_actualizado = actualizar_schemas_producto(contenido_actual)
    if not contenido_actualizado:
        print("❌ Falló la actualización de schemas")
        return
    
    # Paso 4: Escribir archivo actualizado
    print("\n📝 Paso 4: Escribiendo archivo actualizado...")
    try:
        with open(BACKEND_SCHEMAS_PATH, 'w', encoding='utf-8') as file:
            file.write(contenido_actualizado)
        print(f"✅ Archivo actualizado: {BACKEND_SCHEMAS_PATH}")
    except Exception as e:
        print(f"❌ Error al escribir archivo: {e}")
        return
    
    # Paso 5: Añadir schema de ventas
    print("\n📝 Paso 5: Añadiendo schema de ventas...")
    if not añadir_schema_venta():
        return
    
    # Paso 6: Verificar actualización
    print("\n📝 Paso 6: Verificando actualización...")
    if not verificar_actualizacion():
        return
    
    # Paso 7: Mostrar resumen
    print("\n📝 Paso 7: Mostrando resumen de cambios...")
    mostrar_resumen_cambios()
    
    print("\n" + "=" * 60)
    print("✅ Actualización de schemas completada")
    print("📅 Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("🎯 Schemas listos para el sistema POS")
    print("\n📋 Próximos pasos:")
    print("  1. Actualizar crud/product.py")
    print("  2. Crear endpoint de ventas")
    print("  3. Actualizar frontend")

if __name__ == "__main__":
    main() 