# backend/app/crud/insumo.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from typing import List, Optional

from app.models import Insumo # Importar el modelo Insumo
from app.schemas import InsumoCreate, InsumoUpdate # Importar los esquemas Pydantic

def create_insumo(db: Session, user_id: UUID, insumo: InsumoCreate) -> Insumo:
    """
    Crea un nuevo insumo en la base de datos asociado a un usuario.
    """
    db_insumo = Insumo(**insumo.model_dump(), usuario_id=user_id)
    try:
        db.add(db_insumo)
        db.commit()
        db.refresh(db_insumo)
        return db_insumo
    except IntegrityError:
        db.rollback()
        raise ValueError("Error de integridad al crear el insumo. Podría haber un duplicado o datos inválidos.")

def get_insumo_by_id(db: Session, insumo_id: UUID) -> Optional[Insumo]:
    """
    Obtiene un insumo de la base de datos por su ID.
    """
    return db.query(Insumo).filter(Insumo.id == insumo_id).first()

def get_all_insumos_by_user_id(db: Session, user_id: UUID) -> List[Insumo]:
    """
    Obtiene una lista de todos los insumos asociados a un usuario específico.
    """
    return db.query(Insumo).filter(Insumo.usuario_id == user_id).all()

def update_insumo(db: Session, insumo_id: UUID, insumo_update: InsumoUpdate) -> Optional[Insumo]:
    """
    Actualiza los campos de un insumo existente.
    """
    db_insumo = db.query(Insumo).filter(Insumo.id == insumo_id).first()
    if db_insumo:
        update_data = insumo_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_insumo, key, value)
        try:
            db.add(db_insumo)
            db.commit()
            db.refresh(db_insumo)
            return db_insumo
        except IntegrityError:
            db.rollback()
            raise ValueError("Error de integridad al actualizar el insumo.")
    return None

def delete_insumo(db: Session, insumo_id: UUID) -> bool:
    """
    Elimina un insumo de la base de datos por su ID.
    """
    db_insumo = db.query(Insumo).filter(Insumo.id == insumo_id).first()
    if db_insumo:
        db.delete(db_insumo)
        db.commit()
        return True
    return False 