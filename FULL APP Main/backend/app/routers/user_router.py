from typing import Optional, Dict, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserResponse
from app.crud import user as crud_user # Alias for CRUD operations
from app.dependencies import get_current_user # Dependency to get the current authenticated user
from app.models import Usuario, UserTier # Import UserTier enum

# Create an API router specifically for user profile related endpoints
router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: Usuario = Depends(get_current_user)):
    """
    Retrieves the profile of the currently authenticated user.
    Args:
        current_user: The Usuario object obtained from the get_current_user dependency.
    Returns:
        The current user's data as a UserResponse.
    """
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_data: Dict[str, Any], # Use Dict[str, Any] for partial updates
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates the profile of the currently authenticated user.
    Allowed fields for update: nombre, localizacion, info_contacto, password.
    Args:
        user_data: Dictionary with the fields to update (e.g., {"nombre": "Nuevo Nombre"}).
        current_user: The Usuario object of the authenticated user.
        db: The SQLAlchemy database session dependency.
    Returns:
        The updated user's data as a UserResponse.
    Raises:
        HTTPException 400: If the email is being updated to an existing email or other invalid data.
        HTTPException 403: If trying to change the user's tier.
    """
    # Prevent changing email through this endpoint for simplicity and security (requires re-verification)
    if "email" in user_data and user_data["email"] != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email cannot be changed via this endpoint. Please contact support or use a dedicated email change process."
        )
    
    # Prevent changing user tier through this endpoint
    if "tipo_tier" in user_data and user_data["tipo_tier"] != current_user.tipo_tier.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User tier cannot be changed directly."
        )

    # Filter allowed fields to prevent arbitrary updates
    allowed_fields = {"nombre", "localizacion", "info_contacto", "password"}
    update_data = {k: v for k, v in user_data.items() if k in allowed_fields}

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields provided for update."
        )

    updated_user = crud_user.update_user_profile(db, current_user.id, update_data)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update user profile.")
    return updated_user

@router.put("/me/cv", response_model=UserResponse)
async def update_current_user_cv(
    cv_data: Dict[str, Any],
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates the curriculum vitae (CV) of the currently authenticated freelancer user.
    Args:
        cv_data: Dictionary containing CV details (education, experience, skills, etc.).
        current_user: The Usuario object of the authenticated user.
        db: The SQLAlchemy database session dependency.
    Returns:
        The updated user's data with CV details as a UserResponse.
    Raises:
        HTTPException 403: If the user is not a freelancer.
        HTTPException 500: If the CV update fails.
    """
    # Ensure only freelancers can update their CV
    if current_user.tipo_tier != UserTier.FREELANCER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only freelancer users can update their CV."
        )
    
    updated_user = crud_user.update_user_cv(db, current_user.id, cv_data)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update CV.")
    return updated_user

