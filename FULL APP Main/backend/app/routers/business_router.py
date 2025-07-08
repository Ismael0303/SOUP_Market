# backend/app/routers/business_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database import get_db
from app.schemas import NegocioCreate, NegocioUpdate, NegocioResponse, UsuarioResponse # Importa los esquemas
from app.crud import business as crud_business
from app.dependencies import get_current_user

# Create an API router specifically for business-related endpoints
router = APIRouter()

@router.post("/", response_model=NegocioResponse, status_code=status.HTTP_201_CREATED)
def create_business(
    business: NegocioCreate,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Creates a new business for the current user.
    Args:
        business: NegocioCreate Pydantic model containing business data.
        current_user: The current authenticated user (injected by dependency).
        db: The SQLAlchemy database session dependency.
    Returns:
        The newly created business as a NegocioResponse.
    """
    return crud_business.create_business(db=db, user_id=current_user.id, business=business)

@router.get("/me", response_model=List[NegocioResponse])
def get_my_businesses(
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves all businesses owned by the current user.
    Args:
        current_user: The current authenticated user (injected by dependency).
        db: The SQLAlchemy database session dependency.
    Returns:
        A list of businesses owned by the current user.
    """
    return crud_business.get_businesses_by_user_id(db, user_id=current_user.id)

@router.get("/{business_id}", response_model=NegocioResponse)
def get_business(
    business_id: uuid.UUID,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves a specific business by its ID.
    Args:
        business_id: The UUID of the business to retrieve.
        current_user: The current authenticated user (injected by dependency).
        db: The SQLAlchemy database session dependency.
    Returns:
        The business details as a NegocioResponse.
    Raises:
        HTTPException 404: If the business is not found.
        HTTPException 403: If the user doesn't own the business.
    """
    print(f"DEBUG: Recibiendo request para business_id: {business_id}")
    business = crud_business.get_business_by_id(db, business_id=business_id)
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    # Ensure the current user owns this business
    if business.propietario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this business"
        )
    
    return business

@router.put("/{business_id}", response_model=NegocioResponse)
def update_business(
    business_id: uuid.UUID,
    business_update: NegocioUpdate,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates a specific business by its ID.
    Args:
        business_id: The UUID of the business to update.
        business_update: NegocioUpdate Pydantic model containing the fields to update.
        current_user: The current authenticated user (injected by dependency).
        db: The SQLAlchemy database session dependency.
    Returns:
        The updated business as a NegocioResponse.
    Raises:
        HTTPException 404: If the business is not found.
        HTTPException 403: If the user doesn't own the business.
    """
    # First, get the business to check ownership
    business = crud_business.get_business_by_id(db, business_id=business_id)
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    # Ensure the current user owns this business
    if business.propietario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this business"
        )
    
    return crud_business.update_business(db, business_id=business_id, business_update=business_update)

@router.delete("/{business_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_business(
    business_id: uuid.UUID,
    current_user: UsuarioResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deletes a specific business by its ID.
    Args:
        business_id: The UUID of the business to delete.
        current_user: The current authenticated user (injected by dependency).
        db: The SQLAlchemy database session dependency.
    Raises:
        HTTPException 404: If the business is not found.
        HTTPException 403: If the user doesn't own the business.
    """
    # First, get the business to check ownership
    business = crud_business.get_business_by_id(db, business_id=business_id)
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    # Ensure the current user owns this business
    if business.propietario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this business"
        )
    
    crud_business.delete_business(db, business_id=business_id)
