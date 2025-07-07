# backend/app/routers/product_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.schemas import ProductoCreate, ProductoUpdate, ProductoResponse, UserResponse
from app.crud import product as crud_product # <-- Volvemos a importar directamente
from app.crud import business as crud_business # <-- Volvemos a importar directamente
from app.dependencies import get_current_user

router = APIRouter()

# Endpoint to create a new product (protected)
@router.post(
    "/",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product or service",
    description="Allows an authenticated user (microenterprise or freelancer) to create a new product or service, optionally associating it with one of their businesses."
)
def create_product(
    product: ProductoCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
    # Ya no inyectamos crud_product o crud_business aquí
):
    """
    Creates a new product/service for the authenticated user.
    If a business_id is provided, it verifies that the business belongs to the current user.
    """
    if current_user.tipo_tier == "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clients cannot create products or services."
        )

    if product.negocio_id:
        db_business = crud_business.get_business_by_id(db, business_id=product.negocio_id)
        if not db_business or db_business.usuario_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The specified business does not exist or does not belong to the current user."
            )

    db_product = crud_product.create_product(db, user_id=current_user.id, product=product)
    return db_product


# Endpoint to get all products/services of the authenticated user (protected)
@router.get(
    "/me",
    response_model=List[ProductoResponse],
    summary="Get my products/services",
    description="Retrieves all products or services associated with the authenticated user."
)
def get_my_products(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    products = crud_product.get_products_by_user_id(db, user_id=current_user.id)
    return products


# Endpoint to get a specific product/service by ID (protected, must belong to the user)
@router.get(
    "/{product_id}",
    response_model=ProductoResponse,
    summary="Get product/service details",
    description="Retrieves the details of a specific product or service by its ID, if it belongs to the authenticated user."
)
def get_product_detail(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    db_product = crud_product.get_product_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product or service not found."
        )
    if db_product.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this product or service."
        )
    return db_product


# Endpoint to update an existing product/service (protected, must belong to the user)
@router.put(
    "/{product_id}",
    response_model=ProductoResponse,
    summary="Update a product/service",
    description="Updates the details of an existing product or service by its ID, if it belongs to the authenticated user."
)
def update_product(
    product_id: UUID,
    product_update: ProductoUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    db_product = crud_product.get_product_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product or service not found."
        )
    if db_product.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this product or service."
        )
    
    updated_product = crud_product.update_product(db, product_id=product_id, product_update=product_update)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating the product or service."
        )
    return updated_product


# Endpoint to delete a product/service (protected, must belong to the user)
@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a product/service",
    description="Deletes an existing product or service by its ID, if it belongs to the authenticated user."
)
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    db_product = crud_product.get_product_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product or service not found."
        )
    if db_product.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this product or service."
        )
    
    if not crud_product.delete_product(db, product_id=product_id):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting the product or service."
        )
    return {"message": "Product or service deleted successfully."}
