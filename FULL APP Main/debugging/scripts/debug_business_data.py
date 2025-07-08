# backend/debug_business_data.py

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud.business import get_businesses_by_user_id
import json

def debug_business_data():
    """Verifica los datos de negocios que se están devolviendo"""
    db = SessionLocal()
    try:
        # Obtener todos los negocios (para debugging)
        from app.models import Negocio
        all_businesses = db.query(Negocio).all()
        
        print(f"Total de negocios en la base de datos: {len(all_businesses)}")
        
        for i, business in enumerate(all_businesses):
            print(f"\nNegocio {i+1}:")
            print(f"  ID: {business.id}")
            print(f"  Nombre: {business.nombre}")
            print(f"  Propietario ID: {business.propietario_id}")
            print(f"  Tipo negocio: {business.tipo_negocio}")
            print(f"  Rubro: {business.rubro}")
            print(f"  Localización: {business.localizacion_geografica}")
            print(f"  Fotos URLs: {business.fotos_urls}")
            print(f"  Descripción: {business.descripcion}")
            
            # Verificar si el ID es válido
            if business.id:
                print(f"  ✅ ID válido: {business.id}")
            else:
                print(f"  ❌ ID inválido: {business.id}")
        
        # Probar con un usuario específico (si existe)
        if all_businesses:
            user_id = all_businesses[0].propietario_id
            print(f"\n\nProbando con usuario ID: {user_id}")
            
            user_businesses = get_businesses_by_user_id(db, user_id)
            print(f"Negocios del usuario: {len(user_businesses)}")
            
            for i, business in enumerate(user_businesses):
                print(f"\nNegocio del usuario {i+1}:")
                print(f"  ID: {business.id}")
                print(f"  Nombre: {business.nombre}")
                print(f"  Rubro: {business.rubro}")
                print(f"  Fotos URLs: {business.fotos_urls}")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    debug_business_data() 