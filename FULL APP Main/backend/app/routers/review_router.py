# backend/app/routers/review_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.schemas import ReviewCreate, ReviewResponse
from app.dependencies import get_current_user
from app.models import Usuario, Producto
from app.crud import review as crud_review

router = APIRouter(tags=["Reviews"])


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review_endpoint(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    product = db.query(Producto).filter(Producto.id == review.producto_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    db_review = crud_review.create_review(db, usuario_id=current_user.id, review=review)
    return db_review


@router.get("/product/{product_id}", response_model=List[ReviewResponse])
def list_reviews_for_product(
    product_id: UUID,
    db: Session = Depends(get_db),
):
    product = db.query(Producto).filter(Producto.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return crud_review.get_reviews_by_product(db, producto_id=product_id)
