#!/usr/bin/env python3
"""
Script para crear insumos y productos para los negocios de los usuarios bots, evitando duplicados.
"""

import os
import sys
from pathlib import Path
import uuid
from datetime import datetime

# Agregar el directorio backend al path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))
os.chdir(backend_path)

try:
    from app.database import get_db
    from sqlalchemy import text
except ImportError as e:
    print(f"Error importando módulos del backend: {e}")
    sys.exit(1)


def get_user_and_business_ids(db, email):
    user_id = None
    business_id = None
    # Buscar usuario
    result = db.execute(text("SELECT id FROM usuarios WHERE email = :email"), {'email': email})
    row = result.fetchone()
    if row:
        user_id = row[0]
        # Buscar negocio asociado
        result2 = db.execute(text("SELECT id FROM negocios WHERE usuario_id = :uid ORDER BY fecha_creacion DESC"), {'uid': user_id})
        row2 = result2.fetchone()
        if row2:
            business_id = row2[0]
    return user_id, business_id


def insumo_exists(db, user_id, nombre):
    result = db.execute(text("SELECT id FROM insumos WHERE usuario_id = :uid AND nombre = :nombre"), {'uid': user_id, 'nombre': nombre})
    return result.fetchone() is not None


def producto_exists(db, business_id, nombre):
    result = db.execute(text("SELECT id FROM productos WHERE negocio_id = :bid AND nombre = :nombre"), {'bid': business_id, 'nombre': nombre})
    return result.fetchone() is not None


def create_insumos(db, user_id, insumos):
    insumo_ids = {}
    for nombre, cantidad, unidad, costo in insumos:
        if not insumo_exists(db, user_id, nombre):
            insumo_id = str(uuid.uuid4())
            db.execute(text("""
                INSERT INTO insumos (id, nombre, cantidad_disponible, unidad_medida_compra, costo_unitario_compra, usuario_id, fecha_creacion, fecha_actualizacion)
                VALUES (:id, :nombre, :cantidad, :unidad, :costo, :usuario_id, NOW(), NOW())
            """), {
                'id': insumo_id,
                'nombre': nombre,
                'cantidad': cantidad,
                'unidad': unidad,
                'costo': costo,
                'usuario_id': user_id
            })
            print(f"✅ Insumo creado: {nombre}")
        else:
            result = db.execute(text("SELECT id FROM insumos WHERE usuario_id = :uid AND nombre = :nombre"), {'uid': user_id, 'nombre': nombre})
            insumo_id = result.fetchone()[0]
            print(f"⚠️  Insumo ya existe: {nombre}")
        insumo_ids[nombre] = insumo_id
    return insumo_ids


def create_productos(db, business_id, user_id, productos, insumo_ids):
    for nombre, descripcion, precio, tipo, precio_venta, margen, insumos_necesarios in productos:
        if not producto_exists(db, business_id, nombre):
            producto_id = str(uuid.uuid4())
            db.execute(text("""
                INSERT INTO productos (
                    id, nombre, descripcion, precio, tipo_producto, usuario_id, negocio_id, precio_venta, margen_ganancia_sugerido, rating_promedio, reviews_count, fecha_creacion, fecha_actualizacion
                )
                VALUES (
                    :id, :nombre, :descripcion, :precio, :tipo, :usuario_id, :negocio_id, :precio_venta, :margen, 0.0, 0, NOW(), NOW()
                )
            """), {
                'id': producto_id,
                'nombre': nombre,
                'descripcion': descripcion,
                'precio': precio,
                'tipo': tipo,
                'usuario_id': user_id,
                'negocio_id': business_id,
                'precio_venta': precio_venta,
                'margen': margen
            })
            print(f"✅ Producto creado: {nombre}")
            # Asociar insumos
            for insumo_nombre, cantidad in insumos_necesarios:
                if insumo_nombre in insumo_ids:
                    db.execute(text("""
                        INSERT INTO producto_insumo (
                            id, producto_id, insumo_id, cantidad_necesaria, fecha_asociacion, fecha_actualizacion
                        )
                        VALUES (
                            :id, :producto_id, :insumo_id, :cantidad, NOW(), NOW()
                        )
                    """), {
                        'id': str(uuid.uuid4()),
                        'producto_id': producto_id,
                        'insumo_id': insumo_ids[insumo_nombre],
                        'cantidad': cantidad
                    })
        else:
            print(f"⚠️  Producto ya existe: {nombre}")


def main():
    print("🚀 Creando insumos y productos para bots...")
    db = next(get_db())
    try:
        # Panadero
        panadero_email = 'panadero@ejemplo.com'
        panadero_insumos = [
            ('Harina de Trigo 000', 50.0, 'kg', 0.8),
            ('Harina Integral', 30.0, 'kg', 1.2),
            ('Levadura Fresca', 2.0, 'kg', 2.5),
            ('Azúcar Blanca', 25.0, 'kg', 1.2),
            ('Manteca', 15.0, 'kg', 3.5),
            ('Huevos', 200.0, 'unidad', 0.15),
            ('Leche', 40.0, 'litro', 0.8),
            ('Sal Fina', 5.0, 'kg', 0.5),
            ('Aceite de Oliva', 10.0, 'litro', 2.8),
            ('Dulce de Leche', 8.0, 'kg', 4.0)
        ]
        panadero_productos = [
            ('Pan de Masa Madre Integral', 'Pan artesanal de masa madre con harina integral.', 3.0, 'PHYSICAL_GOOD', 6.5, 100.0, [
                ('Harina Integral', 0.5),
                ('Levadura Fresca', 0.01),
                ('Sal Fina', 0.01),
                ('Aceite de Oliva', 0.02)
            ]),
            ('Facturas Mixtas x Docena', 'Surtido de facturas frescas, ideales para el desayuno.', 5.0, 'PHYSICAL_GOOD', 12.0, 120.0, [
                ('Harina de Trigo 000', 0.8),
                ('Azúcar Blanca', 0.1),
                ('Manteca', 0.3),
                ('Huevos', 2.0),
                ('Leche', 0.2),
                ('Dulce de Leche', 0.2)
            ])
        ]
        panadero_uid, panadero_bid = get_user_and_business_ids(db, panadero_email)
        if panadero_uid and panadero_bid:
            insumo_ids = create_insumos(db, panadero_uid, panadero_insumos)
            create_productos(db, panadero_bid, panadero_uid, panadero_productos, insumo_ids)
        else:
            print(f"❌ No se encontró usuario o negocio para {panadero_email}")

        # Diseñador
        disenador_email = 'disenador@ejemplo.com'
        disenador_insumos = [
            ('Licencia Adobe Creative Suite', 1.0, 'licencia', 50.0),
            ('Licencia Figma Pro', 1.0, 'licencia', 15.0),
            ('Hosting Web', 12.0, 'mes', 8.0),
            ('Dominio Web', 1.0, 'año', 12.0),
            ('Stock de Imágenes', 100.0, 'imagen', 0.5),
            ('Fuentes Premium', 50.0, 'fuente', 2.0),
            ('Energía Eléctrica', 160.0, 'hora', 0.1),
            ('Internet', 160.0, 'hora', 0.05),
            ('Café', 160.0, 'taza', 0.3)
        ]
        disenador_productos = [
            ('Logo Corporativo', 'Diseño de logo profesional con 3 propuestas iniciales, 2 revisiones incluidas.', 15.0, 'SERVICE_BY_PROJECT', 300.0, 1900.0, [
                ('Licencia Adobe Creative Suite', 0.1),
                ('Energía Eléctrica', 8.0),
                ('Internet', 8.0),
                ('Café', 4.0)
            ]),
            ('Identidad Visual Completa', 'Branding completo incluyendo logo, paleta de colores, tipografías.', 25.0, 'SERVICE_BY_PROJECT', 800.0, 3100.0, [
                ('Licencia Adobe Creative Suite', 0.2),
                ('Fuentes Premium', 2.0),
                ('Energía Eléctrica', 20.0),
                ('Internet', 20.0),
                ('Café', 10.0)
            ])
        ]
        disenador_uid, disenador_bid = get_user_and_business_ids(db, disenador_email)
        if disenador_uid and disenador_bid:
            insumo_ids = create_insumos(db, disenador_uid, disenador_insumos)
            create_productos(db, disenador_bid, disenador_uid, disenador_productos, insumo_ids)
        else:
            print(f"❌ No se encontró usuario o negocio para {disenador_email}")

        db.commit()
        print("\n✅ ¡Insumos y productos creados exitosamente!")
    except Exception as e:
        print(f"❌ Error creando insumos/productos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 