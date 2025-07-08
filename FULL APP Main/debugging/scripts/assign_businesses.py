#!/usr/bin/env python3
"""
Script para asignar negocios a usuarios de ejemplo o crear nuevos con nombres únicos.
"""

import os
import sys
from pathlib import Path
import uuid

# Agregar el directorio backend al path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))
os.chdir(backend_path)

try:
    from app.database import get_db, engine
    from app.crud import user as crud_user
    from app.crud import business as crud_business
    from app.schemas import NegocioCreate
    from app.models import BusinessType
    from sqlalchemy import text
except ImportError as e:
    print(f"Error importando módulos del backend: {e}")
    sys.exit(1)


def assign_or_create_business(db, user_email: str, business_data: dict):
    """Asigna un negocio existente o crea uno nuevo para un usuario."""
    try:
        # Buscar usuario
        user = crud_user.get_user_by_email(db, email=user_email)
        if not user:
            print(f"❌ Usuario {user_email} no encontrado")
            return None
        
        # Verificar si ya tiene negocios
        if user.negocios:
            print(f"✅ Usuario {user_email} ya tiene negocio: {user.negocios[0].nombre}")
            return user.negocios[0]
        
        # Crear negocio con nombre único
        business_name = f"{business_data['nombre']} - {user.nombre}"
        
        business_create = NegocioCreate(
            nombre=business_name,
            descripcion=business_data.get("descripcion"),
            tipo_negocio=business_data["tipo_negocio"],
            rubro=business_data.get("rubro"),
            localizacion_geografica=business_data.get("localizacion_geografica"),
            fotos_urls=business_data.get("fotos_urls", [])
        )
        
        business = crud_business.create_business(db, user_id=user.id, business=business_create)
        print(f"✅ Negocio creado: {business.nombre} para {user_email}")
        return business
        
    except Exception as e:
        print(f"❌ Error creando negocio para {user_email}: {e}")
        return None


def main():
    """Función principal."""
    print("🏢 SOUP Emprendimientos - Asignador de Negocios")
    print("=" * 50)
    
    # Datos de negocios para crear
    businesses_data = {
        "disenador@ejemplo.com": {
            "nombre": "Estudio de Diseño 'Pixel Perfect'",
            "descripcion": "Estudio creativo especializado en diseño gráfico, branding corporativo, diseño web y UX/UI. Creamos identidades visuales únicas que conectan con tu audiencia.",
            "tipo_negocio": BusinessType.SERVICIOS,
            "rubro": "Diseño y Tecnología",
            "localizacion_geografica": "Córdoba, Argentina",
            "fotos_urls": [
                "https://placehold.co/600x400/4A90E2/FFFFFF?text=Pixel+Perfect+Studio",
                "https://placehold.co/600x400/7B68EE/FFFFFF?text=Diseño+Creativo",
                "https://placehold.co/600x400/20B2AA/FFFFFF?text=Branding+Corporativo"
            ]
        },
        "panadero@ejemplo.com": {
            "nombre": "Panadería Artesanal 'El Horno Mágico'",
            "descripcion": "Panes de masa madre, facturas y pastelería fina elaborados con técnicas tradicionales y ingredientes de primera calidad. Especialistas en panes integrales y sin gluten.",
            "tipo_negocio": BusinessType.PRODUCTOS,
            "rubro": "Alimentos y Bebidas",
            "localizacion_geografica": "CABA, Argentina",
            "fotos_urls": [
                "https://placehold.co/600x400/FFD700/000000?text=Panaderia+El+Horno+Magico",
                "https://placehold.co/600x400/8B4513/FFFFFF?text=Panes+Artesanales",
                "https://placehold.co/600x400/DEB887/000000?text=Facturas+Frescas"
            ]
        }
    }
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        for user_email, business_data in businesses_data.items():
            print(f"\n🔄 Procesando: {user_email}")
            assign_or_create_business(db, user_email, business_data)
        
        print("\n" + "=" * 50)
        print("✅ ¡Negocios asignados exitosamente!")
        
    except Exception as e:
        print(f"❌ Error asignando negocios: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main() 