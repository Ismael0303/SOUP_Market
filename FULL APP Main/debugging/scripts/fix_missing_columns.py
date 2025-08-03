#!/usr/bin/env python3
"""
Script para añadir columnas faltantes a la tabla productos
Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de la base de datos
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "soup_app_db",
    "user": "soupuser",
    "password": "soup123"
}

def add_missing_columns():
    """Añadir columnas faltantes a la tabla productos"""
    print("🔧 AÑADIENDO COLUMNAS FALTANTES A LA TABLA PRODUCTOS")
    print("=" * 60)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Verificar columnas existentes
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'productos' 
            ORDER BY ordinal_position
        """)
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        print("📋 Columnas existentes en tabla productos:")
        for col in existing_columns:
            print(f"  - {col}")
        
        # Columnas que deberían existir según el modelo
        required_columns = {
            'margen_ganancia_real': 'DOUBLE PRECISION',
            'cogs': 'DOUBLE PRECISION',
            'precio_sugerido': 'DOUBLE PRECISION',
            'calificacion_promedio': 'DOUBLE PRECISION',
            'ventas_completadas': 'INTEGER'
        }
        
        # Añadir columnas faltantes
        for column_name, data_type in required_columns.items():
            if column_name not in existing_columns:
                print(f"\n➕ Añadiendo columna: {column_name}")
                try:
                    cursor.execute(f"""
                        ALTER TABLE productos 
                        ADD COLUMN {column_name} {data_type}
                    """)
                    print(f"   ✅ Columna {column_name} añadida exitosamente")
                except Exception as e:
                    print(f"   ❌ Error añadiendo {column_name}: {e}")
            else:
                print(f"   ✅ Columna {column_name} ya existe")
        
        # Confirmar cambios
        conn.commit()
        
        # Verificar columnas después de la actualización
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'productos' 
            ORDER BY ordinal_position
        """)
        updated_columns = cursor.fetchall()
        
        print(f"\n📊 Columnas después de la actualización ({len(updated_columns)} total):")
        for col in updated_columns:
            print(f"  - {col[0]}: {col[1]} (nullable: {col[2]})")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Actualización de columnas completada")
        return True
        
    except Exception as e:
        print(f"❌ Error en la actualización: {e}")
        return False

def verify_model_consistency():
    """Verificar que el modelo coincida con la base de datos"""
    print("\n🔍 VERIFICANDO CONSISTENCIA DEL MODELO")
    print("=" * 50)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Obtener todas las columnas de la tabla productos
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'productos' 
            ORDER BY ordinal_position
        """)
        db_columns = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Columnas esperadas del modelo Producto
        expected_columns = {
            'id': 'uuid',
            'nombre': 'character varying',
            'descripcion': 'text',
            'precio': 'double precision',
            'tipo_producto': 'character varying',
            'negocio_id': 'uuid',
            'propietario_id': 'uuid',
            'fecha_creacion': 'timestamp without time zone',
            'fecha_actualizacion': 'timestamp without time zone',
            'stock_terminado': 'double precision',
            'precio_venta': 'double precision',
            'margen_ganancia_sugerido': 'double precision',
            'precio_sugerido': 'double precision',
            'cogs': 'double precision',
            'margen_ganancia_real': 'double precision',
            'calificacion_promedio': 'double precision',
            'ventas_completadas': 'integer'
        }
        
        print("📋 Verificación de columnas:")
        all_match = True
        
        for expected_col, expected_type in expected_columns.items():
            if expected_col in db_columns:
                db_type = db_columns[expected_col]
                if expected_type in db_type or db_type in expected_type:
                    print(f"   ✅ {expected_col}: {db_type}")
                else:
                    print(f"   ⚠️  {expected_col}: tipo esperado {expected_type}, encontrado {db_type}")
                    all_match = False
            else:
                print(f"   ❌ {expected_col}: NO ENCONTRADA")
                all_match = False
        
        if all_match:
            print("\n🎉 Todas las columnas coinciden con el modelo")
        else:
            print("\n⚠️  Algunas columnas no coinciden")
        
        cursor.close()
        conn.close()
        return all_match
        
    except Exception as e:
        print(f"❌ Error en la verificación: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 REPARACIÓN DE COLUMNAS FALTANTES")
    print("=" * 60)
    
    # Añadir columnas faltantes
    success = add_missing_columns()
    
    if success:
        # Verificar consistencia
        verify_model_consistency()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE REPARACIÓN")
    print("=" * 60)
    print(f"Reparación: {'✅ EXITOSA' if success else '❌ FALLÓ'}")

if __name__ == "__main__":
    main() 