#!/usr/bin/env python3
"""
Script para cargar insumos y productos para usuarios existentes.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import uuid

# Agregar el directorio backend al path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))
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
    sys.exit(1)


def load_bot_data(file_path: Path) -> Dict[str, Any]:
    """Carga los datos de un archivo JSON de bot."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error leyendo {file_path}: {e}")
        return None


def create_insumos_for_user(db, insumos_data: List[Dict[str, Any]], user_id: uuid.UUID):
    """Crea insumos para un usuario específico."""
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


def create_products_for_user(db, products_data: List[Dict[str, Any]], 
                           user_id: uuid.UUID, insumos_map: Dict[str, uuid.UUID]):
    """Crea productos para un usuario específico."""
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
            
            # Obtener el primer negocio del usuario
            user = crud_user.get_user_by_id(db, user_id)
            if not user.negocios:
                print(f"⚠️  Usuario {user.email} no tiene negocios, saltando productos")
                continue
            
            business_id = user.negocios[0].id
            
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


def main():
    """Función principal."""
    print("🚀 SOUP Emprendimientos - Cargador de Insumos y Productos")
    print("=" * 60)
    
    # Verificar conexión a base de datos
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Conexión a base de datos establecida")
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        sys.exit(1)
    
    # Ruta a la carpeta de bots
    bots_dir = Path(__file__).parent.parent.parent / "Tutoriales" / "Ejemplos" / "bots"
    
    if not bots_dir.exists():
        print(f"❌ Directorio de bots no encontrado: {bots_dir}")
        sys.exit(1)
    
    # Buscar archivos JSON
    json_files = list(bots_dir.glob("*.json"))
    
    if not json_files:
        print(f"❌ No se encontraron archivos JSON en {bots_dir}")
        sys.exit(1)
    
    print(f"📁 Encontrados {len(json_files)} archivos de bot")
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        for file_path in json_files:
            print(f"\n🔄 Procesando: {file_path.name}")
            print("=" * 50)
            
            # Cargar datos del bot
            bot_data = load_bot_data(file_path)
            if not bot_data:
                continue
            
            # Buscar usuario por email
            user_email = bot_data["usuario"]["email"]
            user = crud_user.get_user_by_email(db, email=user_email)
            
            if not user:
                print(f"❌ Usuario {user_email} no encontrado, saltando...")
                continue
            
            print(f"✅ Usuario encontrado: {user.email}")
            
            # Crear insumos
            if "insumos" in bot_data and bot_data["insumos"]:
                print(f"📦 Creando {len(bot_data['insumos'])} insumos...")
                insumos_map = create_insumos_for_user(db, bot_data["insumos"], user.id)
                
                # Crear productos
                if "productos" in bot_data and bot_data["productos"]:
                    print(f"🛍️  Creando {len(bot_data['productos'])} productos...")
                    create_products_for_user(db, bot_data["productos"], user.id, insumos_map)
            
            print(f"✅ Bot '{file_path.stem}' procesado exitosamente!")
        
        print("\n" + "=" * 60)
        print("✅ ¡Insumos y productos cargados exitosamente!")
        
    except Exception as e:
        print(f"❌ Error procesando bots: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main() 