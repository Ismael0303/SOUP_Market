# backend/app/routers/insumo_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.schemas import InsumoCreate, InsumoUpdate, InsumoResponse
from app.crud import insumo as crud_insumo
from app.dependencies import get_current_user
from app.models import Usuario, UserTier # Importar Usuario y UserTier para validación de rol

# Create a new FastAPI router for insumos
router = APIRouter(
    prefix="/insumos",
    tags=["Insumos"]
)

@router.post(
    "/",
    response_model=InsumoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new insumo",
    description="Allows an authenticated user to create a new insumo (material/resource)."
)
def create_insumo_endpoint(
    insumo: InsumoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Creates a new insumo associated with the current authenticated user.
    Only users with 'microemprendimiento' or 'freelancer' tier can create insumos.
    """
    if current_user.tipo_tier not in [UserTier.MICROEMPRENDIMIENTO, UserTier.FREELANCER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only micro-entrepreneurs or freelancers can create insumos."
        )
    try:
        db_insumo = crud_insumo.create_insumo(db, user_id=current_user.id, insumo=insumo)
        return db_insumo
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/me",
    response_model=List[InsumoResponse],
    summary="Get all insumos for the current user",
    description="Retrieves a list of all insumos owned by the current authenticated user."
)
def get_my_insumos_endpoint(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Returns a list of all insumos belonging to the authenticated user.
    """
    insumos = crud_insumo.get_all_insumos_by_user_id(db, user_id=current_user.id)
    return insumos


@router.get(
    "/{insumo_id}",
    response_model=InsumoResponse,
    summary="Get insumo details by ID",
    description="Retrieves the details of a specific insumo by its ID. Only accessible by the owner."
)
def get_insumo_by_id_endpoint(
    insumo_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Returns the details of a specific insumo.
    Ensures the insumo belongs to the authenticated user.
    """
    db_insumo = crud_insumo.get_insumo_by_id(db, insumo_id=insumo_id)
    if not db_insumo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insumo not found."
        )
    if db_insumo.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this insumo."
        )
    return db_insumo


@router.put(
    "/{insumo_id}",
    response_model=InsumoResponse,
    summary="Update an existing insumo",
    description="Updates the details of an existing insumo by its ID. Only accessible by the owner."
)
def update_insumo_endpoint(
    insumo_id: UUID,
    insumo_update: InsumoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Updates an existing insumo.
    Ensures the insumo belongs to the authenticated user.
    """
    db_insumo = crud_insumo.get_insumo_by_id(db, insumo_id=insumo_id)
    if not db_insumo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insumo not found."
        )
    if db_insumo.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this insumo."
        )
    try:
        updated_insumo = crud_insumo.update_insumo(db, insumo_id=insumo_id, insumo_update=insumo_update)
        return updated_insumo
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/{insumo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an insumo",
    description="Deletes an insumo by its ID. Only accessible by the owner."
)
def delete_insumo_endpoint(
    insumo_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Deletes an insumo.
    Ensures the insumo belongs to the authenticated user.
    """
    db_insumo = crud_insumo.get_insumo_by_id(db, insumo_id=insumo_id)
    if not db_insumo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insumo not found."
        )
    if db_insumo.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this insumo."
        )
    crud_insumo.delete_insumo(db, insumo_id=insumo_id)
    return {"message": "Insumo deleted successfully."} 