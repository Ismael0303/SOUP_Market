from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from uuid import UUID

from app.models import Usuario
from app.schemas import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash, verify_password

def get_user(db: Session, user_id: UUID) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
    return db.query(Usuario).offset(skip).limit(limit).all()

def create_user(db: Session, user: UsuarioCreate) -> Usuario:
    hashed_password = get_password_hash(user.password)
    db_user = Usuario(
        email=user.email,
        nombre=user.nombre,
        hashed_password=hashed_password,
        tipo_tier=user.tipo_tier,
        localizacion=user.localizacion,
        curriculum_vitae=user.curriculum_vitae,
        plugins_activos=[]  # Inicializar lista vacía de plugins
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: UUID, user_update: UsuarioUpdate) -> Optional[Usuario]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    
    # Manejar actualización de contraseña
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    # Actualizar plugins_activos si se proporciona
    if "plugins_activos" in update_data:
        db_user.plugins_activos = update_data["plugins_activos"]
    
    # Actualizar otros campos
    for field, value in update_data.items():
        if hasattr(db_user, field):
            setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: UUID) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

def authenticate_user(db: Session, email: str, password: str) -> Optional[Usuario]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# NUEVAS FUNCIONES PARA GESTIÓN DE PLUGINS
def activate_plugin(db: Session, user_id: UUID, plugin_name: str) -> Optional[Usuario]:
    """Activa un plugin para un usuario específico"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    if db_user.plugins_activos is None:
        db_user.plugins_activos = []
    
    if plugin_name not in db_user.plugins_activos:
        db_user.plugins_activos.append(plugin_name)
        db.commit()
        db.refresh(db_user)
    
    return db_user

def deactivate_plugin(db: Session, user_id: UUID, plugin_name: str) -> Optional[Usuario]:
    """Desactiva un plugin para un usuario específico"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    if db_user.plugins_activos and plugin_name in db_user.plugins_activos:
        db_user.plugins_activos.remove(plugin_name)
        db.commit()
        db.refresh(db_user)
    
    return db_user

def get_user_plugins(db: Session, user_id: UUID) -> List[str]:
    """Obtiene la lista de plugins activos de un usuario"""
    db_user = get_user(db, user_id)
    if not db_user:
        return []
    
    return db_user.plugins_activos or []
