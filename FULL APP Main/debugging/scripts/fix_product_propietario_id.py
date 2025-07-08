#!/usr/bin/env python3
"""
Script para corregir el campo propietario_id en productos que solo tienen usuario_id.
"""

import os
import sys
from pathlib import Path

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

def fix_product_propietario_id():
    """Corregir el campo propietario_id en productos"""
    print("🔧 Corrigiendo campo propietario_id en productos...")
    
    db = next(get_db())
    try:
        # Verificar productos que tienen usuario_id pero no propietario_id
        result = db.execute(text("""
            SELECT id, nombre, usuario_id, propietario_id 
            FROM productos 
            WHERE usuario_id IS NOT NULL AND propietario_id IS NULL
        """))
        
        products_to_fix = result.fetchall()
        print(f"📋 Productos que necesitan corrección: {len(products_to_fix)}")
        
        if products_to_fix:
            for product in products_to_fix:
                print(f"  - {product[1]} (usuario_id: {product[2]})")
            
            # Actualizar propietario_id con el valor de usuario_id
            result = db.execute(text("""
                UPDATE productos 
                SET propietario_id = usuario_id 
                WHERE usuario_id IS NOT NULL AND propietario_id IS NULL
            """))
            
            print(f"✅ Productos actualizados: {len(products_to_fix)}")
        else:
            print("✅ No hay productos que necesiten corrección")
        
        # Verificar el resultado
        result = db.execute(text("""
            SELECT id, nombre, usuario_id, propietario_id 
            FROM productos 
            WHERE propietario_id IS NULL
        """))
        
        remaining_null = result.fetchall()
        if remaining_null:
            print(f"⚠️  Productos que aún tienen propietario_id NULL: {len(remaining_null)}")
            for product in remaining_null:
                print(f"  - {product[1]} (usuario_id: {product[2]})")
        else:
            print("✅ Todos los productos tienen propietario_id válido")
        
        db.commit()
        print("\n✅ ¡Corrección completada!")
        
    except Exception as e:
        print(f"❌ Error corrigiendo productos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_product_propietario_id() 