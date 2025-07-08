# backend/app/routers/public_router.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.schemas import NegocioResponse, ProductoResponse, UsuarioPublicResponse # Import public schemas
from app.crud import business as crud_business
from app.crud import product as crud_product
from app.crud import user as crud_user # Import user CRUD for public profile

# Create a new FastAPI router for public access
router = APIRouter()

# --- Public Business Endpoints ---

@router.get(
    "/businesses",
    response_model=List[NegocioResponse],
    summary="Get all public businesses",
    description="Retrieves a list of all publicly available businesses."
)
def get_all_public_businesses(db: Session = Depends(get_db)):
    """
    Returns a list of all businesses.
    (Currently, all businesses are considered public for simplicity in this phase).
    """
    businesses = crud_business.get_all_businesses(db) # Assuming a get_all_businesses in crud/business.py
    return businesses

@router.get(
    "/businesses/{business_id}",
    response_model=NegocioResponse,
    summary="Get public business details by ID",
    description="Retrieves the details of a specific publicly available business by its ID."
)
def get_public_business_detail(business_id: UUID, db: Session = Depends(get_db)):
    """
    Returns the details of a specific business by its ID.
    """
    db_business = crud_business.get_business_by_id(db, business_id=business_id)
    if not db_business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found."
        )
    return db_business

# --- Public Product Endpoints ---

@router.get(
    "/products",
    response_model=List[ProductoResponse],
    summary="Get all public products/services",
    description="Retrieves a list of all publicly available products or services."
)
def get_all_public_products(db: Session = Depends(get_db)):
    """
    Returns a list of all products/services.
    (Currently, all products are considered public for simplicity in this phase).
    """
    products = crud_product.get_all_products(db) # Assuming a get_all_products in crud/product.py
    return products

@router.get(
    "/products/{product_id}",
    response_model=ProductoResponse,
    summary="Get public product/service details by ID",
    description="Retrieves the details of a specific publicly available product or service by its ID."
)
def get_public_product_detail(product_id: UUID, db: Session = Depends(get_db)):
    """
    Returns the details of a specific product/service by its ID.
    """
    db_product = crud_product.get_product_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product or service not found."
        )
    return db_product

# --- Public User Profile Endpoints ---

@router.get(
    "/users/{user_id}",
    response_model=UsuarioPublicResponse,
    summary="Get public user profile by ID",
    description="Retrieves the public profile details of a specific user by their ID."
)
def get_public_user_profile(user_id: UUID, db: Session = Depends(get_db)):
    """
    Returns the public profile details of a specific user.
    """
    db_user = crud_user.get_user_by_id(db, user_id=user_id) # Assuming get_user_by_id in crud/user.py
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return db_user

# --- Public Search Endpoint (Future Expansion) ---
# @router.get("/search", ...)
# def public_search(...):
#    ...
