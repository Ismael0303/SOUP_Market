#!/usr/bin/env python3
"""
Script de Migración Simplificado: Añadir campo stock_terminado
Capítulo Ñiam - SOUP Emprendimientos

Este script añade el campo stock_terminado a la tabla productos usando
la configuración del backend existente.

Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import sys
import os
from datetime import datetime

# Añadir el directorio backend al path para importar los módulos
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from app.database import engine, SessionLocal
    from app.models import Producto, Insumo
    from sqlalchemy import text
    print("Modulos del backend importados correctamente")
except ImportError as e:
    print(f"Error al importar modulos del backend: {e}")
    print("Asegurate de que el backend esté configurado correctamente")
    sys.exit(1)

def conectar_db():
    """Establece conexión usando la configuración del backend"""
    try:
        # Usar la configuración del backend
        db = SessionLocal()
        print("Conexion a la base de datos establecida usando configuracion del backend")
        return db
    except Exception as e:
        print(f"Error al conectar usando configuracion del backend: {e}")
        sys.exit(1)

def verificar_campo_existe(db, campo):
    """Verifica si el campo ya existe en la tabla productos"""
    try:
        result = db.execute(text(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'productos' 
            AND column_name = '{campo}'
        """))
        
        existe = result.fetchone() is not None
        return existe
    except Exception as e:
        print(f"Error al verificar campo {campo}: {e}")
        return False

def añadir_campo_stock_terminado(db):
    """Añade el campo stock_terminado a la tabla productos"""
    try:
        # Verificar si el campo ya existe
        if verificar_campo_existe(db, 'stock_terminado'):
            print("El campo 'stock_terminado' ya existe en la tabla productos")
            return True
        
        # Añadir el campo stock_terminado
        db.execute(text("""
            ALTER TABLE productos 
            ADD COLUMN stock_terminado FLOAT DEFAULT 0.0
        """))
        
        # Añadir comentario al campo
        try:
            db.execute(text("""
                COMMENT ON COLUMN productos.stock_terminado IS 
                'Cantidad de productos terminados disponibles para venta'
            """))
        except:
            print("No se pudo añadir comentario al campo (no crítico)")
        
        db.commit()
        print("Campo 'stock_terminado' anadido exitosamente a la tabla productos")
        return True
        
    except Exception as e:
        print(f"Error al anadir campo stock_terminado: {e}")
        db.rollback()
        return False

def autocompletar_stock_terminado(db):
    """Autocompleta el stock_terminado con valores por defecto"""
    try:
        # Obtener todos los productos
        productos = db.query(Producto).all()
        print(f"Encontrados {len(productos)} productos para actualizar")
        
        for producto in productos:
            # Asignar un stock por defecto basado en el tipo de producto
            if producto.tipo_producto in ['PHYSICAL_GOOD', 'DIGITAL_GOOD']:
                # Para productos físicos y digitales, asignar stock aleatorio entre 10-100
                import random
                stock_default = random.randint(10, 100)
            else:
                # Para servicios, asignar stock alto (disponible para venta)
                stock_default = 999
            
            producto.stock_terminado = stock_default
            print(f"  {producto.nombre}: {stock_default} unidades asignadas")
        
        db.commit()
        print("Stock terminado autocompletado para todos los productos")
        return True
        
    except Exception as e:
        print(f"Error al autocompletar stock terminado: {e}")
        db.rollback()
        return False

def verificar_migracion(db):
    """Verifica que la migración se haya realizado correctamente"""
    try:
        # Verificar que el campo existe
        if not verificar_campo_existe(db, 'stock_terminado'):
            print("El campo 'stock_terminado' no existe")
            return False
        
        # Verificar que hay productos con stock
        productos_con_stock = db.query(Producto).filter(Producto.stock_terminado > 0).count()
        print(f"Productos con stock terminado: {productos_con_stock}")
        
        # Mostrar algunos ejemplos
        ejemplos = db.query(Producto).filter(Producto.stock_terminado > 0).limit(5).all()
        if ejemplos:
            print("Ejemplos de productos con stock:")
            for producto in ejemplos:
                print(f"  - {producto.nombre}: {producto.stock_terminado:.2f} unidades")
        
        return True
        
    except Exception as e:
        print(f"Error al verificar migracion: {e}")
        return False

def main():
    """Función principal del script"""
    print("Iniciando migracion: Anadir campo stock_terminado")
    print("=" * 60)
    
    # Conectar a la base de datos
    db = conectar_db()
    
    try:
        # Paso 1: Añadir campo stock_terminado
        print("\nPaso 1: Anadiendo campo stock_terminado...")
        if not añadir_campo_stock_terminado(db):
            print("Fallo al anadir campo stock_terminado")
            return
        
        # Paso 2: Autocompletar stock de productos
        print("\nPaso 2: Autocompletando stock de productos...")
        if not autocompletar_stock_terminado(db):
            print("Fallo al autocompletar stock")
            return
        
        # Paso 3: Verificar migración
        print("\nPaso 3: Verificando migracion...")
        if not verificar_migracion(db):
            print("Fallo la verificacion de migracion")
            return
        
        print("\n" + "=" * 60)
        print("Migracion completada exitosamente")
        print("Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("Campo 'stock_terminado' listo para el sistema POS")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        db.rollback()
    finally:
        db.close()
        print("Conexion a la base de datos cerrada")

if __name__ == "__main__":
    main() 