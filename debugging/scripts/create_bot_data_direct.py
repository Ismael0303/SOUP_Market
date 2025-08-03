#!/usr/bin/env python3
"""
Script para crear datos de ejemplo directamente usando SQL.
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
    from app.database import get_db, engine
    from sqlalchemy import text
except ImportError as e:
    print(f"Error importando módulos del backend: {e}")
    sys.exit(1)


def create_bot_data_direct():
    """Crea datos de ejemplo directamente usando SQL."""
    print("🚀 Creando datos de ejemplo directamente...")
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # 1. Obtener IDs de usuarios bots
        result = db.execute(text("""
            SELECT id, email FROM usuarios 
            WHERE email IN ('disenador@ejemplo.com', 'panadero@ejemplo.com')
            ORDER BY email;
        """))
        
        users = {row[1]: row[0] for row in result}
        print(f"👥 Usuarios encontrados: {list(users.keys())}")
        
        if not users:
            print("❌ No se encontraron usuarios bots")
            return
        
        # 2. Crear negocios para cada usuario
        businesses_data = {
            'disenador@ejemplo.com': {
                'nombre': f"Estudio de Diseño 'Pixel Perfect' - {datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'descripcion': "Estudio creativo especializado en diseño gráfico, branding corporativo, diseño web y UX/UI.",
                'tipo_negocio': 'SERVICIOS',
                'rubro': 'Diseño y Tecnología',
                'localizacion_geografica': 'Córdoba, Argentina'
            },
            'panadero@ejemplo.com': {
                'nombre': f"Panadería Artesanal 'El Horno Mágico' - {datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'descripcion': "Panes de masa madre, facturas y pastelería fina elaborados con técnicas tradicionales.",
                'tipo_negocio': 'PRODUCTOS',
                'rubro': 'Alimentos y Bebidas',
                'localizacion_geografica': 'CABA, Argentina'
            }
        }
        
        business_ids = {}
        
        for email, business_data in businesses_data.items():
            if email in users:
                business_id = str(uuid.uuid4())
                
                db.execute(text("""
                    INSERT INTO negocios (id, nombre, descripcion, usuario_id, propietario_id, tipo_negocio, rubro, localizacion_geografica, rating_promedio, reviews_totales, fecha_creacion, fecha_actualizacion)
                    VALUES (:id, :nombre, :descripcion, :usuario_id, :propietario_id, :tipo_negocio, :rubro, :localizacion_geografica, 0.0, 0, NOW(), NOW())
                """), {
                    'id': business_id,
                    'nombre': business_data['nombre'],
                    'descripcion': business_data['descripcion'],
                    'usuario_id': users[email],
                    'propietario_id': users[email],
                    'tipo_negocio': business_data['tipo_negocio'],
                    'rubro': business_data['rubro'],
                    'localizacion_geografica': business_data['localizacion_geografica']
                })
                
                business_ids[email] = business_id
                print(f"✅ Negocio creado para {email}: {business_data['nombre']}")
        
        db.commit()
        
        # 3. Crear insumos para el panadero
        if 'panadero@ejemplo.com' in business_ids:
            panadero_user_id = users['panadero@ejemplo.com']
            insumos_panadero = [
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
            
            insumo_ids = {}
            for nombre, cantidad, unidad, costo in insumos_panadero:
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
                    'usuario_id': panadero_user_id
                })
                insumo_ids[nombre] = insumo_id
                print(f"✅ Insumo creado: {nombre}")
            
            # 4. Crear productos para el panadero
            productos_panadero = [
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
            
            for nombre, descripcion, precio, tipo, precio_venta, margen, insumos_necesarios in productos_panadero:
                producto_id = str(uuid.uuid4())
                
                db.execute(text("""
                    INSERT INTO productos (id, nombre, descripcion, precio, tipo_producto, negocio_id, propietario_id, precio_venta, margen_ganancia_sugerido, fecha_creacion, fecha_actualizacion)
                    VALUES (:id, :nombre, :descripcion, :precio, :tipo, :negocio_id, :propietario_id, :precio_venta, :margen, NOW(), NOW())
                """), {
                    'id': producto_id,
                    'nombre': nombre,
                    'descripcion': descripcion,
                    'precio': precio,
                    'tipo': tipo,
                    'negocio_id': business_ids['panadero@ejemplo.com'],
                    'propietario_id': panadero_user_id,
                    'precio_venta': precio_venta,
                    'margen_ganancia_sugerido': margen
                })
                
                # Asociar insumos al producto
                for insumo_nombre, cantidad in insumos_necesarios:
                    if insumo_nombre in insumo_ids:
                        db.execute(text("""
                            INSERT INTO producto_insumo (producto_id, insumo_id, cantidad_necesaria, fecha_asociacion)
                            VALUES (:producto_id, :insumo_id, :cantidad, NOW())
                        """), {
                            'producto_id': producto_id,
                            'insumo_id': insumo_ids[insumo_nombre],
                            'cantidad': cantidad
                        })
                
                print(f"✅ Producto creado: {nombre}")
        
        # 5. Crear insumos para el diseñador
        if 'disenador@ejemplo.com' in business_ids:
            disenador_user_id = users['disenador@ejemplo.com']
            insumos_disenador = [
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
            
            insumo_ids_disenador = {}
            for nombre, cantidad, unidad, costo in insumos_disenador:
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
                    'usuario_id': disenador_user_id
                })
                insumo_ids_disenador[nombre] = insumo_id
                print(f"✅ Insumo creado: {nombre}")
            
            # 6. Crear productos para el diseñador
            productos_disenador = [
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
            
            for nombre, descripcion, precio, tipo, precio_venta, margen, insumos_necesarios in productos_disenador:
                producto_id = str(uuid.uuid4())
                
                db.execute(text("""
                    INSERT INTO productos (id, nombre, descripcion, precio, tipo_producto, negocio_id, propietario_id, precio_venta, margen_ganancia_sugerido, fecha_creacion, fecha_actualizacion)
                    VALUES (:id, :nombre, :descripcion, :precio, :tipo, :negocio_id, :propietario_id, :precio_venta, :margen, NOW(), NOW())
                """), {
                    'id': producto_id,
                    'nombre': nombre,
                    'descripcion': descripcion,
                    'precio': precio,
                    'tipo': tipo,
                    'negocio_id': business_ids['disenador@ejemplo.com'],
                    'propietario_id': disenador_user_id,
                    'precio_venta': precio_venta,
                    'margen_ganancia_sugerido': margen
                })
                
                # Asociar insumos al producto
                for insumo_nombre, cantidad in insumos_necesarios:
                    if insumo_nombre in insumo_ids_disenador:
                        db.execute(text("""
                            INSERT INTO producto_insumo (producto_id, insumo_id, cantidad_necesaria, fecha_asociacion)
                            VALUES (:producto_id, :insumo_id, :cantidad, NOW())
                        """), {
                            'producto_id': producto_id,
                            'insumo_id': insumo_ids_disenador[insumo_nombre],
                            'cantidad': cantidad
                        })
                
                print(f"✅ Producto creado: {nombre}")
        
        db.commit()
        print("\n✅ ¡Datos de ejemplo creados exitosamente!")
        
    except Exception as e:
        print(f"❌ Error creando datos: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_bot_data_direct() 