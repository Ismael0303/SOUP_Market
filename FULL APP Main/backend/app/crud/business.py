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
    db_business = Negocio(**business.model_dump(), usuario_id=user_id)
    try:
        db.add(db_business)
        db.commit()
        db.refresh(db_business)
        return db_business
    except IntegrityError:
        db.rollback()
        raise ValueError("Error de integridad al crear el negocio. Podría haber un duplicado.")

# Función para obtener un negocio por su ID
def get_business_by_id(db: Session, business_id: UUID) -> Optional[Negocio]:
    """
    Obtiene un negocio de la base de datos por su ID.
    """
    return db.query(Negocio).filter(Negocio.id == business_id).first()

# Función para obtener todos los negocios de un usuario específico
def get_businesses_by_user_id(db: Session, user_id: UUID) -> List[Negocio]:
    """
    Obtiene una lista de todos los negocios asociados a un usuario específico.
    """
    return db.query(Negocio).filter(Negocio.usuario_id == user_id).all()

# NUEVA FUNCIÓN: Obtener todos los negocios (para listado público)
def get_all_businesses(db: Session) -> List[Negocio]:
    """
    Obtiene una lista de todos los negocios en la base de datos.
    Utilizado para el listado público.
    """
    return db.query(Negocio).all()

# Función para actualizar un negocio existente
def update_business(db: Session, business_id: UUID, business_update: NegocioUpdate) -> Optional[Negocio]:
    """
    Actualiza los campos de un negocio existente.
    """
    db_business = db.query(Negocio).filter(Negocio.id == business_id).first()
    if db_business:
        update_data = business_update.model_dump(exclude_unset=True)
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
