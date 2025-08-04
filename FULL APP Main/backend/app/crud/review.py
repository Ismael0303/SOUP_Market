# backend/app/crud/review.py

from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.models import Review, Producto
from app.schemas import ReviewCreate


def create_review(db: Session, usuario_id: UUID, review: ReviewCreate) -> Review:
    """Create a new review and update product rating statistics."""
    product = db.query(Producto).filter(Producto.id == review.producto_id).first()
    if not product:
        raise ValueError("Producto no encontrado")

    db_review = Review(
        usuario_id=usuario_id,
        producto_id=review.producto_id,
        rating=review.rating,
        comentario=review.comentario,
    )
    db.add(db_review)

    # Update product rating statistics
    product.reviews_count += 1
    product.rating_promedio = (
        (product.rating_promedio * (product.reviews_count - 1)) + review.rating
    ) / product.reviews_count

    db.commit()
    db.refresh(db_review)
    return db_review


def get_reviews_by_product(db: Session, producto_id: UUID) -> List[Review]:
    """Retrieve all reviews for a given product."""
    return db.query(Review).filter(Review.producto_id == producto_id).all()
