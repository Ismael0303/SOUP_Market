#!/usr/bin/env python3
"""
Script para cargar ejemplos de datos en la base de datos de SOUP Emprendimientos.

Este script lee archivos JSON de la carpeta Tutoriales/Ejemplos/bots/ y los carga
en la base de datos usando las funciones CRUD del backend.

Uso:
    python debugging/scripts/load_examples.py

Autor: Equipo SOUP Emprendimientos
Fecha: 8 de Julio de 2025
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import uuid

# Agregar el directorio backend al path para importar los módulos
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Cambiar al directorio backend para importaciones correctas
os.chdir(backend_path)

try:
    from app.database import get_db, engine
    from app.models import Base
    from app.crud import user as crud_user
    from app.crud import business as crud_business
    from app.crud import product as crud_product
    from app.crud import insumo as crud_insumo
    from app.schemas import UsuarioCreate, NegocioCreate, ProductoCreate, InsumoCreate
    from app.auth import get_password_hash
except ImportError as e:
    print(f"Error importando módulos del backend: {e}")
    print("Asegúrate de que el backend esté configurado correctamente.")
    print(f"Directorio actual: {os.getcwd()}")
    print(f"Backend path: {backend_path}")
    sys.exit(1)


def load_bot_data(file_path: Path) -> Dict[str, Any]:
    """
    Carga los datos de un archivo JSON de bot.
    
    Args:
        file_path: Ruta al archivo JSON
        
    Returns:
        Diccionario con los datos del bot
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error leyendo {file_path}: {e}")
        return None


def create_user_with_data(db, user_data: Dict[str, Any]):
    """
    Crea un usuario con los datos proporcionados.
    
    Args:
        db: Sesión de base de datos
        user_data: Datos del usuario
        
    Returns:
        Usuario creado o None si hay error
    """
    try:
        # Verificar si el usuario ya existe
        existing_user = crud_user.get_user_by_email(db, email=user_data["email"])
        if existing_user:
            print(f"⚠️  Usuario {user_data['email']} ya existe, saltando...")
            return existing_user
        
        # Crear usuario con contraseña hasheada
        user_create = UsuarioCreate(
            email=user_data["email"],
            nombre=user_data["nombre"],
            password=user_data["password_raw"],
            tipo_tier=user_data["tipo_tier"],
            localizacion=user_data.get("localizacion"),
            curriculum_vitae=user_data.get("curriculum_vitae")
        )
        
        user = crud_user.create_user(db, user=user_create)
        print(f"✅ Usuario creado: {user.email}")
        return user
        
    except Exception as e:
        print(f"❌ Error creando usuario {user_data['email']}: {e}")
        return None


def create_business_with_data(db, business_data: Dict[str, Any], user_id: uuid.UUID):
    """
    Crea un negocio con los datos proporcionados.
    
    Args:
        db: Sesión de base de datos
        business_data: Datos del negocio
        user_id: ID del usuario propietario
        
    Returns:
        Negocio creado o None si hay error
    """
    try:
        business_create = NegocioCreate(
            nombre=business_data["nombre"],
            descripcion=business_data.get("descripcion"),
            tipo_negocio=business_data["tipo_negocio"],
            rubro=business_data.get("rubro"),
            localizacion_geografica=business_data.get("localizacion_geografica"),
            fotos_urls=business_data.get("fotos_urls", [])
        )
        
        business = crud_business.create_business(db, user_id=user_id, business=business_create)
        print(f"✅ Negocio creado: {business.nombre}")
        return business
        
    except Exception as e:
        print(f"❌ Error creando negocio {business_data['nombre']}: {e}")
        return None


def create_insumos_with_data(db, insumos_data: List[Dict[str, Any]], user_id: uuid.UUID):
    """
    Crea insumos con los datos proporcionados.
    
    Args:
        db: Sesión de base de datos
        insumos_data: Lista de datos de insumos
        user_id: ID del usuario propietario
        
    Returns:
        Diccionario con nombre de insumo -> ID del insumo creado
    """
    insumos_map = {}
    
    for insumo_data in insumos_data:
        try:
            insumo_create = InsumoCreate(
                nombre=insumo_data["nombre"],
                cantidad_disponible=insumo_data["cantidad_disponible"],
                unidad_medida_compra=insumo_data["unidad_medida_compra"],
                costo_unitario_compra=insumo_data["costo_unitario_compra"]
            )
            
            insumo = crud_insumo.create_insumo(db, user_id=user_id, insumo=insumo_create)
            insumos_map[insumo.nombre] = insumo.id
            print(f"✅ Insumo creado: {insumo.nombre}")
            
        except Exception as e:
            print(f"❌ Error creando insumo {insumo_data['nombre']}: {e}")
    
    return insumos_map


def create_products_with_data(db, products_data: List[Dict[str, Any]], 
                            business_id: uuid.UUID, user_id: uuid.UUID, 
                            insumos_map: Dict[str, uuid.UUID]):
    """
    Crea productos con los datos proporcionados.
    
    Args:
        db: Sesión de base de datos
        products_data: Lista de datos de productos
        business_id: ID del negocio
        user_id: ID del usuario propietario
        insumos_map: Mapeo de nombre de insumo -> ID del insumo
    """
    for product_data in products_data:
        try:
            # Preparar datos de insumos asociados
            insumos_asociados = []
            if "insumos_asociados" in product_data:
                for insumo_asoc in product_data["insumos_asociados"]:
                    insumo_nombre = insumo_asoc["insumo_nombre"]
                    if insumo_nombre in insumos_map:
                        insumos_asociados.append({
                            "insumo_id": insumos_map[insumo_nombre],
                            "cantidad_necesaria": insumo_asoc["cantidad_necesaria"]
                        })
                    else:
                        print(f"⚠️  Insumo '{insumo_nombre}' no encontrado para producto {product_data['nombre']}")
            
            product_create = ProductoCreate(
                nombre=product_data["nombre"],
                descripcion=product_data.get("descripcion"),
                precio=product_data["precio"],
                tipo_producto=product_data["tipo_producto"],
                negocio_id=business_id,
                precio_venta=product_data.get("precio_venta"),
                margen_ganancia_sugerido=product_data.get("margen_ganancia_sugerido"),
                insumos=insumos_asociados
            )
            
            product = crud_product.create_product(db, user_id=user_id, product=product_create)
            print(f"✅ Producto creado: {product.nombre}")
            
        except Exception as e:
            print(f"❌ Error creando producto {product_data['nombre']}: {e}")


def process_bot_file(file_path: Path):
    """
    Procesa un archivo JSON de bot completo.
    
    Args:
        file_path: Ruta al archivo JSON del bot
    """
    print(f"\n🔄 Procesando: {file_path.name}")
    print("=" * 50)
    
    # Cargar datos del bot
    bot_data = load_bot_data(file_path)
    if not bot_data:
        return
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # 1. Crear usuario
        user = create_user_with_data(db, bot_data["usuario"])
        if not user:
            return
        
        # 2. Crear negocio
        business = create_business_with_data(db, bot_data["negocio"], user.id)
        if not business:
            return
        
        # 3. Crear insumos (si existen)
        insumos_map = {}
        if "insumos" in bot_data and bot_data["insumos"]:
            insumos_map = create_insumos_with_data(db, bot_data["insumos"], user.id)
        
        # 4. Crear productos
        if "productos" in bot_data and bot_data["productos"]:
            create_products_with_data(db, bot_data["productos"], business.id, user.id, insumos_map)
        
        print(f"✅ Bot '{file_path.stem}' cargado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error procesando bot {file_path.name}: {e}")
    finally:
        db.close()


def main():
    """
    Función principal del script.
    """
    print("🚀 SOUP Emprendimientos - Cargador de Ejemplos")
    print("=" * 60)
    
    # Verificar que la base de datos esté disponible
    try:
        # Crear tablas si no existen
        Base.metadata.create_all(bind=engine)
        print("✅ Conexión a base de datos establecida")
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        print("Asegúrate de que PostgreSQL esté corriendo y configurado correctamente.")
        sys.exit(1)
    
    # Ruta a la carpeta de bots
    bots_dir = Path(__file__).parent.parent.parent / "Tutoriales" / "Ejemplos" / "bots"
    
    if not bots_dir.exists():
        print(f"❌ Directorio de bots no encontrado: {bots_dir}")
        print("Asegúrate de que exista la carpeta Tutoriales/Ejemplos/bots/")
        sys.exit(1)
    
    # Buscar archivos JSON
    json_files = list(bots_dir.glob("*.json"))
    
    if not json_files:
        print(f"❌ No se encontraron archivos JSON en {bots_dir}")
        sys.exit(1)
    
    print(f"📁 Encontrados {len(json_files)} archivos de bot:")
    for file in json_files:
        print(f"   - {file.name}")
    
    # Confirmar con el usuario
    response = input(f"\n¿Deseas cargar estos {len(json_files)} bots? (y/N): ")
    if response.lower() not in ['y', 'yes', 'sí', 'si']:
        print("❌ Operación cancelada por el usuario")
        sys.exit(0)
    
    # Procesar cada archivo
    success_count = 0
    for file_path in json_files:
        try:
            process_bot_file(file_path)
            success_count += 1
        except Exception as e:
            print(f"❌ Error procesando {file_path.name}: {e}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN:")
    print(f"   Total de archivos: {len(json_files)}")
    print(f"   Cargados exitosamente: {success_count}")
    print(f"   Errores: {len(json_files) - success_count}")
    
    if success_count > 0:
        print(f"\n✅ ¡Ejemplos cargados exitosamente!")
        print("Puedes iniciar el backend y frontend para ver los datos de ejemplo.")
    else:
        print(f"\n❌ No se pudo cargar ningún ejemplo.")
        print("Revisa los errores anteriores y verifica la configuración.")


if __name__ == "__main__":
    main() 