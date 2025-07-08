from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from app.database import get_db
from app.schemas import UsuarioResponse
from app.crud import user as crud_user
from app.dependencies import get_current_user
from app.models import Usuario

# Create an API router specifically for user-related endpoints
router = APIRouter()

@router.get("/me", response_model=UsuarioResponse)
def get_current_user_profile(current_user: Usuario = Depends(get_current_user)):
    """
    Retrieves the current user's profile information.
    Args:
        current_user: The current authenticated user (injected by dependency).
    Returns:
        The current user's data as a UsuarioResponse.
    """
    return current_user

@router.put("/me", response_model=UsuarioResponse)
def update_current_user_profile(
    user_update: dict,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates the current user's profile information.
    Args:
        user_update: A dictionary containing the fields to update.
        current_user: The current authenticated user (injected by dependency).
        db: The SQLAlchemy database session dependency.
    Returns:
        The updated user's data as a UsuarioResponse.
    Raises:
        HTTPException 404: If the user is not found.
    """
    # Update the user's profile in the database
    updated_user = crud_user.update_user_profile(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

@router.put("/me/cv", response_model=UsuarioResponse)
def update_current_user_cv(
    cv_data: dict,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates the current freelancer's curriculum vitae.
    Args:
        cv_data: A dictionary containing CV details.
        current_user: The current authenticated user (injected by dependency).
        db: The SQLAlchemy database session dependency.
    Returns:
        The updated user's data with CV details as a UsuarioResponse.
    Raises:
        HTTPException 404: If the user is not found.
        HTTPException 403: If the user is not a freelancer.
    """
    # Update the user's CV in the database
    updated_user = crud_user.update_user_cv(db, current_user.id, cv_data)
    if not updated_user:
        # Check if user exists but is not a freelancer
        user = crud_user.get_user_by_id(db, current_user.id)
        if user and user.tipo_tier.value != "freelancer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only freelancers can update their CV"
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

