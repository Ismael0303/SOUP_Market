# debugging/migrations/migrate_add_niam_tables.py

import os
from sqlalchemy import create_engine, text

def migrate_add_niam_tables():
    """Migración para añadir tablas específicas de Panadería Ñiam"""
    
    # Usar variables de entorno directamente
    database_url = os.getenv("DATABASE_URL", "postgresql://soupuser:souppass@localhost:5432/soup_app_db")
    
    # Crear conexión a la base de datos
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            print("🥖 Iniciando migración: Añadir tablas específicas de Panadería Ñiam...")
            
            # 1. Añadir campos específicos de roles a usuarios
            print("\n1. 👥 Añadiendo campos de roles a usuarios...")
            campos_roles = [
                ("rol", "VARCHAR(50)"),
                ("negocio_asignado_id", "UUID REFERENCES negocios(id)"),
                ("fecha_contratacion", "DATE"),
                ("salario", "FLOAT"),
                ("horario_trabajo", "VARCHAR(50)"),
                ("permisos_especiales", "TEXT[]")
            ]
            
            for nombre_campo, tipo_campo in campos_roles:
                try:
                    conn.execute(text(f"ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS {nombre_campo} {tipo_campo}"))
                    print(f"   ✅ Campo {nombre_campo} añadido")
                except Exception as e:
                    print(f"   ⚠️ Campo {nombre_campo}: {e}")
            
            # 2. Crear tabla recetas
            print("\n2. 📖 Creando tabla recetas...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS recetas (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        nombre VARCHAR(255) NOT NULL,
                        descripcion TEXT,
                        producto_id UUID NOT NULL REFERENCES productos(id),
                        negocio_id UUID NOT NULL REFERENCES negocios(id),
                        creador_id UUID NOT NULL REFERENCES usuarios(id),
                        tiempo_preparacion INTEGER,
                        tiempo_coccion INTEGER,
                        temperatura_horno FLOAT,
                        rendimiento FLOAT,
                        unidad_rendimiento VARCHAR(50),
                        dificultad VARCHAR(20),
                        instrucciones TEXT,
                        fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    )
                """))
                print("   ✅ Tabla recetas creada")
            except Exception as e:
                print(f"   ⚠️ Tabla recetas: {e}")
            
            # 3. Crear tabla ingredientes_receta
            print("\n3. 🧂 Creando tabla ingredientes_receta...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS ingredientes_receta (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        receta_id UUID NOT NULL REFERENCES recetas(id) ON DELETE CASCADE,
                        insumo_id UUID NOT NULL REFERENCES insumos(id),
                        cantidad_necesaria FLOAT NOT NULL,
                        unidad_medida VARCHAR(20) NOT NULL,
                        orden INTEGER,
                        notas TEXT
                    )
                """))
                print("   ✅ Tabla ingredientes_receta creada")
            except Exception as e:
                print(f"   ⚠️ Tabla ingredientes_receta: {e}")
            
            # 4. Crear tabla producciones
            print("\n4. 🏭 Creando tabla producciones...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS producciones (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        receta_id UUID NOT NULL REFERENCES recetas(id),
                        negocio_id UUID NOT NULL REFERENCES negocios(id),
                        productor_id UUID NOT NULL REFERENCES usuarios(id),
                        fecha_produccion DATE NOT NULL,
                        hora_inicio TIMESTAMP WITH TIME ZONE,
                        hora_fin TIMESTAMP WITH TIME ZONE,
                        cantidad_producida FLOAT NOT NULL,
                        cantidad_esperada FLOAT NOT NULL,
                        rendimiento_real FLOAT,
                        calidad VARCHAR(20),
                        observaciones TEXT,
                        problemas TEXT,
                        costo_total FLOAT,
                        costo_unitario FLOAT,
                        estado VARCHAR(20) NOT NULL DEFAULT 'planificada',
                        fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    )
                """))
                print("   ✅ Tabla producciones creada")
            except Exception as e:
                print(f"   ⚠️ Tabla producciones: {e}")
            
            # 5. Crear tabla horarios_pico
            print("\n5. ⏰ Creando tabla horarios_pico...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS horarios_pico (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        negocio_id UUID NOT NULL REFERENCES negocios(id),
                        dia_semana INTEGER NOT NULL,
                        hora_inicio VARCHAR(5) NOT NULL,
                        hora_fin VARCHAR(5) NOT NULL,
                        ventas_promedio FLOAT,
                        productos_vendidos_promedio INTEGER,
                        clientes_promedio INTEGER,
                        activo BOOLEAN DEFAULT TRUE,
                        prioridad INTEGER,
                        fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    )
                """))
                print("   ✅ Tabla horarios_pico creada")
            except Exception as e:
                print(f"   ⚠️ Tabla horarios_pico: {e}")
            
            # 6. Crear índices para mejorar rendimiento
            print("\n6. 🚀 Creando índices...")
            indices = [
                "CREATE INDEX IF NOT EXISTS idx_recetas_negocio_id ON recetas(negocio_id)",
                "CREATE INDEX IF NOT EXISTS idx_recetas_producto_id ON recetas(producto_id)",
                "CREATE INDEX IF NOT EXISTS idx_ingredientes_receta_id ON ingredientes_receta(receta_id)",
                "CREATE INDEX IF NOT EXISTS idx_producciones_negocio_id ON producciones(negocio_id)",
                "CREATE INDEX IF NOT EXISTS idx_producciones_fecha ON producciones(fecha_produccion)",
                "CREATE INDEX IF NOT EXISTS idx_producciones_estado ON producciones(estado)",
                "CREATE INDEX IF NOT EXISTS idx_horarios_pico_negocio_id ON horarios_pico(negocio_id)",
                "CREATE INDEX IF NOT EXISTS idx_horarios_pico_dia ON horarios_pico(dia_semana)",
                "CREATE INDEX IF NOT EXISTS idx_usuarios_rol ON usuarios(rol)",
                "CREATE INDEX IF NOT EXISTS idx_usuarios_negocio_asignado ON usuarios(negocio_asignado_id)"
            ]
            
            for indice in indices:
                try:
                    conn.execute(text(indice))
                    print(f"   ✅ Índice creado")
                except Exception as e:
                    print(f"   ⚠️ Índice: {e}")
            
            # 7. Insertar datos de ejemplo para Panadería Ñiam
            print("\n7. 📝 Insertando datos de ejemplo...")
            try:
                # Insertar horarios pico típicos de una panadería
                conn.execute(text("""
                    INSERT INTO horarios_pico (negocio_id, dia_semana, hora_inicio, hora_fin, ventas_promedio, prioridad)
                    VALUES 
                    (1, 1, '07:00', '10:00', 150.0, 1),
                    (1, 1, '17:00', '20:00', 200.0, 1),
                    (1, 2, '07:00', '10:00', 140.0, 1),
                    (1, 2, '17:00', '20:00', 180.0, 1),
                    (1, 3, '07:00', '10:00', 160.0, 1),
                    (1, 3, '17:00', '20:00', 220.0, 1),
                    (1, 4, '07:00', '10:00', 130.0, 1),
                    (1, 4, '17:00', '20:00', 190.0, 1),
                    (1, 5, '07:00', '10:00', 170.0, 1),
                    (1, 5, '17:00', '20:00', 250.0, 1),
                    (1, 6, '08:00', '12:00', 300.0, 1),
                    (1, 0, '08:00', '12:00', 280.0, 1)
                    ON CONFLICT DO NOTHING
                """))
                print("   ✅ Horarios pico insertados")
            except Exception as e:
                print(f"   ⚠️ Datos de ejemplo: {e}")
            
            conn.commit()
            
            print("\n" + "=" * 70)
            print("✅ Migración completada exitosamente")
            print("🎯 Nuevas funcionalidades para Panadería Ñiam:")
            print("   - Sistema de roles específicos")
            print("   - Gestión de recetas de Chipá")
            print("   - Control de producción")
            print("   - Análisis de horarios pico")
            print("   - Dashboard especializado")
                
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        raise
    finally:
        engine.dispose()

if __name__ == "__main__":
    migrate_add_niam_tables() 