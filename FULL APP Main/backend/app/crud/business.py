# backend/app/crud/business.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from typing import List, Optional

from app.models import Negocio, Usuario # Importa los modelos Negocio y Usuario
from app.schemas import NegocioCreate, NegocioUpdate # Importa los esquemas Pydantic

# Función para crear un nuevo negocio
def create_business(db: Session, user_id: UUID, business: NegocioCreate) -> Negocio:
    """
    Crea un nuevo negocio en la base de datos asociado a un usuario.
    """
    business_data = business.model_dump()
    # Convertir fotos_urls a JSON string si existe
    if business_data.get('fotos_urls'):
        import json
        business_data['fotos_urls'] = json.dumps(business_data['fotos_urls'])
    
    db_business = Negocio(**business_data, propietario_id=user_id)
    try:
        db.add(db_business)
        db.commit()
        db.refresh(db_business)
        return db_business
    except IntegrityError:
        db.rollback()
        raise ValueError("Error de integridad al crear el negocio. Podría haber un duplicado.")

# Función auxiliar para convertir fotos_urls de JSON a lista
def _convert_fotos_urls(business):
    """
    Convierte fotos_urls de JSON string a lista si es necesario.
    """
    if hasattr(business, 'fotos_urls'):
        import json
        try:
            if business.fotos_urls is None:
                business.fotos_urls = []
            elif isinstance(business.fotos_urls, str):
                if business.fotos_urls.strip():
                    business.fotos_urls = json.loads(business.fotos_urls)
                else:
                    business.fotos_urls = []
            elif not isinstance(business.fotos_urls, list):
                business.fotos_urls = []
        except (json.JSONDecodeError, TypeError, AttributeError):
            business.fotos_urls = []
    else:
        business.fotos_urls = []
    return business

# Función para obtener un negocio por su ID
def get_business_by_id(db: Session, business_id: UUID) -> Optional[Negocio]:
    """
    Obtiene un negocio de la base de datos por su ID.
    """
    business = db.query(Negocio).filter(Negocio.id == business_id).first()
    if business:
        return _convert_fotos_urls(business)
    return None

# Función para obtener todos los negocios de un usuario específico
def get_businesses_by_user_id(db: Session, user_id: UUID) -> List[Negocio]:
    """
    Obtiene una lista de todos los negocios asociados a un usuario específico.
    """
    businesses = db.query(Negocio).filter(Negocio.propietario_id == user_id).all()
    return [_convert_fotos_urls(business) for business in businesses]

# NUEVA FUNCIÓN: Obtener todos los negocios (para listado público)
def get_all_businesses(db: Session) -> List[Negocio]:
    """
    Obtiene una lista de todos los negocios en la base de datos.
    Utilizado para el listado público.
    """
    businesses = db.query(Negocio).all()
    return [_convert_fotos_urls(business) for business in businesses]

# Función para actualizar un negocio existente
def update_business(db: Session, business_id: UUID, business_update: NegocioUpdate) -> Optional[Negocio]:
    """
    Actualiza los campos de un negocio existente.
    """
    db_business = db.query(Negocio).filter(Negocio.id == business_id).first()
    if db_business:
        update_data = business_update.model_dump(exclude_unset=True)
        # Convertir fotos_urls a JSON string si existe
        if 'fotos_urls' in update_data and update_data['fotos_urls'] is not None:
            import json
            update_data['fotos_urls'] = json.dumps(update_data['fotos_urls'])
        
        for key, value in update_data.items():
            setattr(db_business, key, value)
        try:
            db.add(db_business)
            db.commit()
            db.refresh(db_business)
            return db_business
        except IntegrityError:
            db.rollback()
            raise ValueError("Error de integridad al actualizar el negocio.")
    return None

# Función para eliminar un negocio
def delete_business(db: Session, business_id: UUID) -> bool:
    """
    Elimina un negocio de la base de datos por su ID.
    """
    db_business = db.query(Negocio).filter(Negocio.id == business_id).first()
    if db_business:
        db.delete(db_business)
        db.commit()
        return True
    return False


