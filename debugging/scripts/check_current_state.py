#!/usr/bin/env python3
"""
Script para verificar el estado actual de la base de datos.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))
os.chdir(backend_path)

try:
    from app.database import get_db, engine
    from sqlalchemy import text
    
    print("🔍 Verificando estado actual de la base de datos...")
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Verificar usuarios
        result = db.execute(text("SELECT COUNT(*) FROM usuarios;"))
        user_count = result.fetchone()[0]
        print(f"👥 Total de usuarios: {user_count}")
        
        # Verificar negocios
        result = db.execute(text("SELECT COUNT(*) FROM negocios;"))
        business_count = result.fetchone()[0]
        print(f"🏢 Total de negocios: {business_count}")
        
        # Verificar insumos
        result = db.execute(text("SELECT COUNT(*) FROM insumos;"))
        insumo_count = result.fetchone()[0]
        print(f"📦 Total de insumos: {insumo_count}")
        
        # Verificar productos
        result = db.execute(text("SELECT COUNT(*) FROM productos;"))
        product_count = result.fetchone()[0]
        print(f"🛍️  Total de productos: {product_count}")
        
        # Verificar usuarios de ejemplo
        result = db.execute(text("""
            SELECT u.email, u.nombre, COUNT(n.id) as negocios_count, COUNT(i.id) as insumos_count
            FROM usuarios u
            LEFT JOIN negocios n ON u.id = n.propietario_id
            LEFT JOIN insumos i ON u.id = i.usuario_id
            WHERE u.email IN ('panadero@ejemplo.com', 'disenador@ejemplo.com')
            GROUP BY u.id, u.email, u.nombre;
        """))
        
        print("\n📋 Estado de usuarios de ejemplo:")
        print("=" * 60)
        for row in result:
            print(f"Email: {row[0]}")
            print(f"Nombre: {row[1]}")
            print(f"Negocios: {row[2]}")
            print(f"Insumos: {row[3]}")
            print("-" * 30)
        
        # Verificar todos los negocios
        result = db.execute(text("""
            SELECT n.nombre, u.email as propietario, n.tipo_negocio
            FROM negocios n
            JOIN usuarios u ON n.propietario_id = u.id
            ORDER BY n.nombre;
        """))
        
        print("\n🏢 Todos los negocios:")
        print("=" * 60)
        for row in result:
            print(f"Nombre: {row[0]}")
            print(f"Propietario: {row[1]}")
            print(f"Tipo: {row[2]}")
            print("-" * 30)
        
        print(f"\n✅ Verificación completada!")
        
    except Exception as e:
        print(f"❌ Error verificando estado: {e}")
    finally:
        db.close()
        
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1) 