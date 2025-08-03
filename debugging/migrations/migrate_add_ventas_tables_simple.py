# debugging/migrations/migrate_add_ventas_tables_simple.py

import os
from sqlalchemy import create_engine, text

def migrate_add_ventas_tables_simple():
    """Migración simplificada para añadir tablas de ventas"""
    
    # Usar variables de entorno directamente
    database_url = os.getenv("DATABASE_URL", "postgresql://soupuser:souppass@localhost:5432/soup_app_db")
    
    # Crear conexión a la base de datos
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            print("🛒 Iniciando migración: Añadir tablas de ventas...")
            
            # 1. Crear tabla ventas
            print("\n1. 💰 Creando tabla ventas...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS ventas (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        negocio_id UUID NOT NULL REFERENCES negocios(id),
                        cliente_id UUID REFERENCES usuarios(id),
                        numero_venta VARCHAR(50) UNIQUE NOT NULL,
                        fecha_venta TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        subtotal FLOAT NOT NULL DEFAULT 0.0,
                        descuento FLOAT NOT NULL DEFAULT 0.0,
                        impuestos FLOAT NOT NULL DEFAULT 0.0,
                        total FLOAT NOT NULL DEFAULT 0.0,
                        metodo_pago VARCHAR(50),
                        estado VARCHAR(20) NOT NULL DEFAULT 'completada',
                        notas TEXT,
                        margen_ganancia_total FLOAT,
                        costo_total FLOAT,
                        fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    )
                """))
                print("   ✅ Tabla ventas creada")
            except Exception as e:
                print(f"   ⚠️ Tabla ventas: {e}")
            
            # 2. Crear tabla detalles_venta
            print("\n2. 📋 Creando tabla detalles_venta...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS detalles_venta (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        venta_id UUID NOT NULL REFERENCES ventas(id) ON DELETE CASCADE,
                        producto_id UUID NOT NULL REFERENCES productos(id),
                        cantidad FLOAT NOT NULL,
                        precio_unitario FLOAT NOT NULL,
                        descuento_unitario FLOAT NOT NULL DEFAULT 0.0,
                        subtotal FLOAT NOT NULL,
                        costo_unitario FLOAT,
                        margen_ganancia FLOAT,
                        codigo_lote VARCHAR(100)
                    )
                """))
                print("   ✅ Tabla detalles_venta creada")
            except Exception as e:
                print(f"   ⚠️ Tabla detalles_venta: {e}")
            
            # 3. Crear tabla carritos_compra
            print("\n3. 🛒 Creando tabla carritos_compra...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS carritos_compra (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        negocio_id UUID NOT NULL REFERENCES negocios(id),
                        cliente_id UUID REFERENCES usuarios(id),
                        session_id VARCHAR(100),
                        fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        activo BOOLEAN DEFAULT TRUE
                    )
                """))
                print("   ✅ Tabla carritos_compra creada")
            except Exception as e:
                print(f"   ⚠️ Tabla carritos_compra: {e}")
            
            # 4. Crear tabla items_carrito
            print("\n4. 📦 Creando tabla items_carrito...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS items_carrito (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        carrito_id UUID NOT NULL REFERENCES carritos_compra(id) ON DELETE CASCADE,
                        producto_id UUID NOT NULL REFERENCES productos(id),
                        cantidad FLOAT NOT NULL DEFAULT 1.0,
                        precio_unitario FLOAT NOT NULL,
                        fecha_agregado TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    )
                """))
                print("   ✅ Tabla items_carrito creada")
            except Exception as e:
                print(f"   ⚠️ Tabla items_carrito: {e}")
            
            # 5. Añadir campos específicos de panadería a productos
            print("\n5. 🥖 Añadiendo campos de panadería a productos...")
            campos_panaderia = [
                ("categoria", "VARCHAR(50)"),
                ("codigo_lote", "VARCHAR(100)"),
                ("fecha_vencimiento", "DATE"),
                ("fecha_produccion", "DATE"),
                ("stock_minimo", "FLOAT DEFAULT 0.0"),
                ("stock_maximo", "FLOAT"),
                ("unidad_venta", "VARCHAR(50) DEFAULT 'unidad'"),
                ("es_perecedero", "BOOLEAN DEFAULT TRUE"),
                ("tiempo_vida_util", "INTEGER"),
                ("requiere_refrigeracion", "BOOLEAN DEFAULT FALSE"),
                ("ingredientes", "TEXT[]"),
                ("alergenos", "TEXT[]"),
                ("calorias_por_porcion", "FLOAT"),
                ("peso_porcion", "FLOAT"),
                ("unidad_peso", "VARCHAR(10) DEFAULT 'g'")
            ]
            
            for nombre_campo, tipo_campo in campos_panaderia:
                try:
                    conn.execute(text(f"ALTER TABLE productos ADD COLUMN IF NOT EXISTS {nombre_campo} {tipo_campo}"))
                    print(f"   ✅ Campo {nombre_campo} añadido")
                except Exception as e:
                    print(f"   ⚠️ Campo {nombre_campo}: {e}")
            
            # 6. Crear índices
            print("\n6. 🚀 Creando índices...")
            indices = [
                "CREATE INDEX IF NOT EXISTS idx_ventas_negocio_id ON ventas(negocio_id)",
                "CREATE INDEX IF NOT EXISTS idx_ventas_fecha ON ventas(fecha_venta)",
                "CREATE INDEX IF NOT EXISTS idx_detalles_venta_id ON detalles_venta(venta_id)",
                "CREATE INDEX IF NOT EXISTS idx_carritos_negocio_id ON carritos_compra(negocio_id)",
                "CREATE INDEX IF NOT EXISTS idx_productos_categoria ON productos(categoria)",
                "CREATE INDEX IF NOT EXISTS idx_productos_fecha_vencimiento ON productos(fecha_vencimiento)"
            ]
            
            for indice in indices:
                try:
                    conn.execute(text(indice))
                    print(f"   ✅ Índice creado")
                except Exception as e:
                    print(f"   ⚠️ Índice: {e}")
            
            conn.commit()
            
            print("\n" + "=" * 60)
            print("✅ Migración completada exitosamente")
            print("🎯 Nuevas funcionalidades disponibles:")
            print("   - Sistema de ventas completo")
            print("   - Carrito de compras")
            print("   - Campos específicos para panadería")
            print("   - Análisis financiero")
            print("   - Alertas de stock y vencimiento")
                
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        raise
    finally:
        engine.dispose()

if __name__ == "__main__":
    migrate_add_ventas_tables_simple() 