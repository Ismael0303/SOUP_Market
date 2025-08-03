#!/usr/bin/env python3
"""
Script para verificar que los usuarios de ejemplo se crearon correctamente.
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
    
    print("🔍 Verificando usuarios creados...")
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Verificar usuarios creados
        result = db.execute(text("""
            SELECT id, email, nombre, tipo_tier, localizacion, is_active, fecha_creacion
            FROM usuarios 
            WHERE email IN ('panadero@ejemplo.com', 'disenador@ejemplo.com')
            ORDER BY email;
        """))
        
        print("\n📋 Usuarios encontrados:")
        print("=" * 80)
        for row in result:
            print(f"ID: {row[0]}")
            print(f"Email: {row[1]}")
            print(f"Nombre: {row[2]}")
            print(f"Tipo: {row[3]}")
            print(f"Ubicación: {row[4]}")
            print(f"Activo: {row[5]}")
            print(f"Creado: {row[6]}")
            print("-" * 40)
        
        # Verificar negocios existentes
        result = db.execute(text("""
            SELECT n.id, n.nombre, n.tipo_negocio, u.email as propietario
            FROM negocios n
            JOIN usuarios u ON n.propietario_id = u.id
            ORDER BY n.nombre;
        """))
        
        print("\n🏢 Negocios existentes:")
        print("=" * 80)
        negocios = list(result)
        if negocios:
            for row in negocios:
                print(f"ID: {row[0]}")
                print(f"Nombre: {row[1]}")
                print(f"Tipo: {row[2]}")
                print(f"Propietario: {row[3]}")
                print("-" * 40)
        else:
            print("No se encontraron negocios")
        
        print(f"\n✅ Verificación completada. Usuarios: {len(negocios)}")
        
    except Exception as e:
        print(f"❌ Error verificando datos: {e}")
    finally:
        db.close()
        
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1) 