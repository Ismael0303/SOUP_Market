#!/usr/bin/env python3
"""
Script: Actualizar Modelo Producto con campo stock_terminado
Capítulo Ñiam - SOUP Emprendimientos

Este script actualiza el modelo Producto en backend/app/models.py para incluir
el campo stock_terminado necesario para el sistema de punto de venta.

Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import os
import shutil
from datetime import datetime

# Rutas de archivos
BACKEND_MODELS_PATH = "backend/app/models.py"
BACKUP_PATH = "backend/app/models_backup.py"

def crear_backup():
    """Crea una copia de seguridad del archivo models.py"""
    try:
        if os.path.exists(BACKEND_MODELS_PATH):
            shutil.copy2(BACKEND_MODELS_PATH, BACKUP_PATH)
            print(f"✅ Backup creado: {BACKUP_PATH}")
            return True
        else:
            print(f"❌ No se encontró el archivo: {BACKEND_MODELS_PATH}")
            return False
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return False

def leer_archivo_actual():
    """Lee el contenido actual del archivo models.py"""
    try:
        with open(BACKEND_MODELS_PATH, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"❌ Error al leer archivo: {e}")
        return None

def actualizar_modelo_producto(contenido_actual):
    """Actualiza el modelo Producto con el campo stock_terminado"""
    
    # Buscar la definición del modelo Producto
    if 'class Producto(Base):' not in contenido_actual:
        print("❌ No se encontró la clase Producto en el archivo")
        return None
    
    # Definir el campo stock_terminado a añadir
    campo_stock_terminado = """    stock_terminado: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=0.0)"""
    
    # Buscar la línea donde añadir el campo (después de los campos existentes)
    lineas = contenido_actual.split('\n')
    nueva_linea = []
    producto_encontrado = False
    campos_producto = 0
    
    for i, linea in enumerate(lineas):
        nueva_linea.append(linea)
        
        # Detectar inicio de clase Producto
        if 'class Producto(Base):' in linea:
            producto_encontrado = True
            print("📝 Encontrada clase Producto")
            continue
        
        # Si estamos en la clase Producto, contar campos
        if producto_encontrado:
            # Detectar campos del modelo (líneas con mapped_column)
            if 'mapped_column' in linea and ':' in linea:
                campos_producto += 1
                print(f"  📋 Campo encontrado: {linea.strip()}")
            
            # Detectar fin de campos (línea con # Relaciones o línea vacía después de campos)
            if ('# Relaciones' in linea or 
                ('relationship' in linea and campos_producto > 0) or
                (linea.strip() == '' and campos_producto > 0)):
                
                # Añadir el campo stock_terminado antes de las relaciones
                nueva_linea.insert(i, campo_stock_terminado)
                nueva_linea.insert(i, "")
                print(f"✅ Campo stock_terminado añadido en línea {i}")
                producto_encontrado = False
                break
    
    return '\n'.join(nueva_linea)

def escribir_archivo_actualizado(contenido_actualizado):
    """Escribe el contenido actualizado al archivo models.py"""
    try:
        with open(BACKEND_MODELS_PATH, 'w', encoding='utf-8') as file:
            file.write(contenido_actualizado)
        print(f"✅ Archivo actualizado: {BACKEND_MODELS_PATH}")
        return True
    except Exception as e:
        print(f"❌ Error al escribir archivo: {e}")
        return False

def verificar_actualizacion():
    """Verifica que la actualización se haya realizado correctamente"""
    try:
        contenido = leer_archivo_actual()
        if contenido and 'stock_terminado: Mapped[Optional[float]]' in contenido:
            print("✅ Verificación exitosa: Campo stock_terminado encontrado en el modelo")
            return True
        else:
            print("❌ Verificación fallida: Campo stock_terminado no encontrado")
            return False
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        return False

def mostrar_diferencias():
    """Muestra las diferencias entre el archivo original y el actualizado"""
    try:
        if os.path.exists(BACKUP_PATH):
            with open(BACKUP_PATH, 'r', encoding='utf-8') as file:
                contenido_original = file.read()
            
            with open(BACKEND_MODELS_PATH, 'r', encoding='utf-8') as file:
                contenido_actual = file.read()
            
            print("\n📋 Resumen de cambios:")
            print("-" * 40)
            
            # Contar líneas
            lineas_original = len(contenido_original.split('\n'))
            lineas_actual = len(contenido_actual.split('\n'))
            
            print(f"Líneas originales: {lineas_original}")
            print(f"Líneas actuales: {lineas_actual}")
            print(f"Diferencia: +{lineas_actual - lineas_original} líneas")
            
            # Mostrar el campo añadido
            if 'stock_terminado: Mapped[Optional[float]]' in contenido_actual:
                print("✅ Campo añadido: stock_terminado: Mapped[Optional[float]]")
            
            return True
        else:
            print("❌ No se encontró el archivo de backup para comparar")
            return False
    except Exception as e:
        print(f"❌ Error al mostrar diferencias: {e}")
        return False

def main():
    """Función principal del script"""
    print("🚀 Actualizando Modelo Producto con campo stock_terminado")
    print("=" * 60)
    
    # Paso 1: Crear backup
    print("\n📝 Paso 1: Creando backup del archivo original...")
    if not crear_backup():
        return
    
    # Paso 2: Leer archivo actual
    print("\n📝 Paso 2: Leyendo archivo models.py...")
    contenido_actual = leer_archivo_actual()
    if not contenido_actual:
        return
    
    # Paso 3: Actualizar modelo
    print("\n📝 Paso 3: Actualizando modelo Producto...")
    contenido_actualizado = actualizar_modelo_producto(contenido_actual)
    if not contenido_actualizado:
        print("❌ Falló la actualización del modelo")
        return
    
    # Paso 4: Escribir archivo actualizado
    print("\n📝 Paso 4: Escribiendo archivo actualizado...")
    if not escribir_archivo_actualizado(contenido_actualizado):
        return
    
    # Paso 5: Verificar actualización
    print("\n📝 Paso 5: Verificando actualización...")
    if not verificar_actualizacion():
        return
    
    # Paso 6: Mostrar diferencias
    print("\n📝 Paso 6: Mostrando resumen de cambios...")
    mostrar_diferencias()
    
    print("\n" + "=" * 60)
    print("✅ Actualización del modelo Producto completada")
    print("📅 Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("🎯 Campo stock_terminado listo para el sistema POS")
    print("\n📋 Próximos pasos:")
    print("  1. Actualizar schemas.py")
    print("  2. Actualizar crud/product.py")
    print("  3. Crear endpoint de ventas")

if __name__ == "__main__":
    main() 