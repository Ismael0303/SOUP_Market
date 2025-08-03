#!/usr/bin/env python3
"""
Script para probar directamente la consulta de productos usando SQLAlchemy
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings
from app.models import Producto, ProductType

def test_product_query():
    """Probar la consulta de productos directamente"""
    
    try:
        # Crear una nueva conexión
        engine = create_engine(settings.DATABASE_URL, echo=True)
        
        print("=== PRUEBA DE CONSULTA DE PRODUCTOS ===\n")
        
        with engine.connect() as conn:
            # 1. Probar consulta SQL directa
            print("1. Consulta SQL directa:")
            result = conn.execute(text("SELECT id, nombre, tipo_producto FROM productos;"))
            products_sql = result.fetchall()
            print(f"   Productos encontrados: {len(products_sql)}")
            for product in products_sql:
                print(f"   - {product[1]}: {product[2]}")
            
            # 2. Probar consulta con SQLAlchemy ORM
            print("\n2. Consulta con SQLAlchemy ORM:")
            from sqlalchemy.orm import sessionmaker
            Session = sessionmaker(bind=engine)
            session = Session()
            
            try:
                products_orm = session.query(Producto).all()
                print(f"   Productos encontrados: {len(products_orm)}")
                for product in products_orm:
                    print(f"   - {product.nombre}: {product.tipo_producto}")
            except Exception as e:
                print(f"   ❌ Error en consulta ORM: {e}")
                import traceback
                traceback.print_exc()
            finally:
                session.close()
            
            # 3. Verificar el enum ProductType
            print("\n3. Verificando enum ProductType:")
            print(f"   Valores del enum: {[e.value for e in ProductType]}")
            
            # 4. Probar conversión de valores
            print("\n4. Probando conversión de valores:")
            for product in products_sql:
                try:
                    enum_value = ProductType(product[2])
                    print(f"   ✅ {product[2]} -> {enum_value}")
                except ValueError as e:
                    print(f"   ❌ {product[2]} -> Error: {e}")
        
        print("\n=== PRUEBA COMPLETADA ===")
        
    except Exception as e:
        print(f"Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_product_query() 