# backend/app/routers/business_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db # Importa la función para obtener la sesión de DB
from app.schemas import NegocioCreate, NegocioUpdate, NegocioResponse, UserResponse # Importa los esquemas
from app.crud import business as crud_business # <-- Volvemos a importar directamente
# Si business_router necesita crud_product en el futuro, se importaría aquí directamente también
from app.dependencies import get_current_user # Para obtener el usuario autenticado

# Crea un nuevo router de FastAPI
router = APIRouter()

# Endpoint para crear un nuevo negocio (protegido)
@router.post(
    "/",
    response_model=NegocioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo negocio",
    description="Permite a un usuario autenticado (microemprendimiento o freelancer) crear un nuevo negocio."
)
def create_business(
    business: NegocioCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Crea un nuevo negocio para el usuario autenticado.
    Solo los usuarios con tipo_tier 'microemprendimiento' o 'freelancer' pueden crear negocios.
    """
    # Verifica si el tipo de usuario tiene permiso para crear negocios
    if current_user.tipo_tier not in ["microemprendimiento", "freelancer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo microemprendimientos y freelancers pueden crear negocios."
        )
    
    db_business = crud_business.create_business(db, user_id=current_user.id, business=business)
    return db_business


# Endpoint para obtener todos los negocios del usuario autenticado (protegido)
@router.get(
    "/me",
    response_model=List[NegocioResponse],
    summary="Obtener mis negocios",
    description="Obtiene todos los negocios asociados al usuario autenticado."
)
def get_my_businesses(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Retorna una lista de todos los negocios que pertenecen al usuario autenticado.
    """
    businesses = crud_business.get_businesses_by_user_id(db, user_id=current_user.id)
    return businesses


# Endpoint para obtener un negocio específico por ID (protegido, debe ser del usuario)
@router.get(
    "/{business_id}",
    response_model=NegocioResponse,
    summary="Obtener detalle de un negocio",
    description="Obtiene los detalles de un negocio específico por su ID, si pertenece al usuario autenticado."
)
def get_business_detail(
    business_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Retorna los detalles de un negocio específico.
    Verifica que el negocio pertenezca al usuario autenticado.
    """
    db_business = crud_business.get_business_by_id(db, business_id=business_id)
    if not db_business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Negocio no encontrado."
        )
    if db_business.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este negocio."
        )
    return db_business


# Endpoint para actualizar un negocio existente (protegido, debe ser del usuario)
@router.put(
    "/{business_id}",
    response_model=NegocioResponse,
    summary="Actualizar un negocio",
    description="Actualiza los detalles de un negocio existente por su ID, si pertenece al usuario autenticado."
)
def update_business(
    business_id: UUID,
    business_update: NegocioUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Actualiza un negocio existente.
    Verifica que el negocio pertenezca al usuario autenticado.
    """
    db_business = crud_business.get_business_by_id(db, business_id=business_id)
    if not db_business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Negocio no encontrado."
        )
    if db_business.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar este negocio."
        )
    
    updated_business = crud_business.update_business(db, business_id=business_id, business_update=business_update)
    if not updated_business:
        # Esto solo debería ocurrir si el negocio fue eliminado justo antes de la actualización
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el negocio."
        )
    return updated_business


# Endpoint para eliminar un negocio (protegido, debe ser del usuario)
@router.delete(
    "/{business_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar un negocio",
    description="Elimina un negocio existente por su ID, si pertenece al usuario autenticado."
)
def delete_business(
    business_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Elimina un negocio existente.
    Verifica que el negocio pertenezca al usuario autenticado.
    """
    db_business = crud_business.get_business_by_id(db, business_id=business_id)
    if not db_business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Negocio no encontrado."
        )
    if db_business.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este negocio."
        )
    
    if not crud_business.delete_business(db, business_id=business_id):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el negocio."
        )
    return {"message": "Negocio eliminado exitosamente."}
