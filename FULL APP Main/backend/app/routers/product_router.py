# backend/app/routers/product_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database import get_db
from app.schemas import ProductoCreate, ProductoUpdate, ProductoResponse
from app.crud import product as crud_product
from app.dependencies import get_current_user
from app.models import Usuario, UserTier

router = APIRouter(
    tags=["Products & Services"]
)

def _calculate_margen_ganancia_real(db_product) -> Optional[float]:
    if db_product.cogs is not None and db_product.precio_venta is not None and db_product.cogs > 0:
        return ((db_product.precio_venta - db_product.cogs) / db_product.cogs) * 100
    return None

@router.post(
    "/",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product or service",
    description="Allows an authenticated user to create a new product or service, associating it with a business and optional insumos."
)
def create_product_endpoint(
    product: ProductoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.tipo_tier not in [UserTier.MICROEMPRENDIMIENTO, UserTier.FREELANCER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only micro-entrepreneurs and freelancers can create products/services."
        )
    # Validar propiedad del negocio
    business = db.query(current_user.__class__).filter_by(id=product.negocio_id, propietario_id=current_user.id).first()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Business not found or does not belong to the current user."
        )
    try:
        db_product = crud_product.create_product(db, propietario_id=current_user.id, product=product)
        response_data = ProductoResponse.model_validate(db_product)
        response_data.margen_ganancia_real = _calculate_margen_ganancia_real(db_product)
        return response_data
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get(
    "/me",
    response_model=List[ProductoResponse],
    summary="Get all products/services for the current user",
    description="Retrieves a list of all products or services owned by the current authenticated user."
)
def get_all_my_products_endpoint(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    products = crud_product.get_all_products_by_user_id(db, propietario_id=current_user.id)
    response_products = []
    for p in products:
        response_data = ProductoResponse.model_validate(p)
        response_data.margen_ganancia_real = _calculate_margen_ganancia_real(p)
        response_products.append(response_data)
    return response_products

@router.get(
    "/{product_id}",
    response_model=ProductoResponse,
    summary="Get product/service details by ID",
    description="Retrieves the details of a specific product or service by its ID. Only accessible by the owner."
)
def get_product_endpoint(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    db_product = crud_product.get_product_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product/Service not found."
        )
    if db_product.propietario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this product/service."
        )
    response_data = ProductoResponse.model_validate(db_product)
    response_data.margen_ganancia_real = _calculate_margen_ganancia_real(db_product)
    return response_data

@router.put(
    "/{product_id}",
    response_model=ProductoResponse,
    summary="Update an existing product or service",
    description="Updates the details of an existing product or service by its ID. Only accessible by the owner."
)
def update_product_endpoint(
    product_id: UUID,
    product_update: ProductoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    db_product = crud_product.get_product_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product/Service not found."
        )
    if db_product.propietario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this product/service."
        )
    if product_update.negocio_id and product_update.negocio_id != db_product.negocio_id:
        business = db.query(current_user.__class__).filter_by(id=product_update.negocio_id, propietario_id=current_user.id).first()
        if not business:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="New business not found or does not belong to the current user."
            )
    try:
        updated_product = crud_product.update_product(db, product_id=product_id, product_update=product_update)
        response_data = ProductoResponse.model_validate(updated_product)
        response_data.margen_ganancia_real = _calculate_margen_ganancia_real(updated_product)
        return response_data
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product or service",
    description="Deletes a product or service by its ID. Only accessible by the owner."
)
def delete_product_endpoint(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    db_product = crud_product.get_product_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product/Service not found."
        )
    if db_product.propietario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this product/service."
        )
    if not crud_product.delete_product(db, product_id=product_id):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product/service."
        )
