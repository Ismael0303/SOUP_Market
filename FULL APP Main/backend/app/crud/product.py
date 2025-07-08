# backend/app/crud/product.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from typing import List, Optional

from app.models import Producto, Insumo, ProductoInsumo, Usuario
from app.schemas import ProductoCreate, ProductoUpdate, ProductoInsumoCreate

# Función auxiliar para sincronizar insumos asociados a un producto
def _sync_product_insumos(db: Session, db_product: Producto, insumos_data: List[ProductoInsumoCreate]):
    existing_insumo_ids = {pi.insumo_id for pi in db_product.insumos_asociados}
    incoming_insumo_ids = {pi.insumo_id for pi in insumos_data}
    # Insumos a eliminar
    insumos_to_remove = [
        pi for pi in db_product.insumos_asociados
        if pi.insumo_id not in incoming_insumo_ids
    ]
    for pi in insumos_to_remove:
        db.delete(pi)
    # Insumos a actualizar o crear
    for insumo_data in insumos_data:
        insumo = db.query(Insumo).filter(
            Insumo.id == insumo_data.insumo_id,
            Insumo.usuario_id == db_product.propietario_id
        ).first()
        if not insumo:
            raise ValueError(f"Insumo con ID {insumo_data.insumo_id} no encontrado o no pertenece al usuario.")
        if insumo_data.insumo_id in existing_insumo_ids:
            db_producto_insumo = next(
                pi for pi in db_product.insumos_asociados
                if pi.insumo_id == insumo_data.insumo_id
            )
            db_producto_insumo.cantidad_necesaria = insumo_data.cantidad_necesaria
        else:
            new_producto_insumo = ProductoInsumo(
                producto_id=db_product.id,
                insumo_id=insumo_data.insumo_id,
                cantidad_necesaria=insumo_data.cantidad_necesaria
            )
            db.add(new_producto_insumo)
    db.flush()

def _calculate_product_costs_and_prices(db: Session, db_product: Producto) -> None:
    total_cogs = 0.0
    db.refresh(db_product, attribute_names=['insumos_asociados'])
    for producto_insumo in db_product.insumos_asociados:
        insumo = db.query(Insumo).get(producto_insumo.insumo_id)
        if insumo:
            total_cogs += producto_insumo.cantidad_necesaria * insumo.costo_unitario_compra
    db_product.cogs = total_cogs
    if db_product.cogs is not None and db_product.margen_ganancia_sugerido is not None and db_product.margen_ganancia_sugerido >= 0:
        db_product.precio_sugerido = db_product.cogs * (1 + db_product.margen_ganancia_sugerido / 100)
    else:
        db_product.precio_sugerido = None

def create_product(db: Session, propietario_id: UUID, product: ProductoCreate) -> Producto:
    insumos_data = product.insumos if product.insumos is not None else []
    product_data = product.model_dump(exclude_unset=True, exclude={"insumos"})
    db_product = Producto(**product_data, propietario_id=propietario_id)
    try:
        db.add(db_product)
        db.flush()
        _sync_product_insumos(db, db_product, insumos_data)
        _calculate_product_costs_and_prices(db, db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError:
        db.rollback()
        raise ValueError("Error de integridad al crear el producto. Podría haber un duplicado o datos inválidos.")
    except ValueError as e:
        db.rollback()
        raise e

def get_product_by_id(db: Session, product_id: UUID) -> Optional[Producto]:
    return db.query(Producto).filter(Producto.id == product_id).first()

def get_all_products(db: Session) -> List[Producto]:
    """Obtiene todos los productos públicos (para endpoints públicos)"""
    return db.query(Producto).all()

def get_all_products_by_user_id(db: Session, propietario_id: UUID) -> List[Producto]:
    return db.query(Producto).filter(Producto.propietario_id == propietario_id).all()

def get_products_by_business_id(db: Session, business_id: UUID) -> List[Producto]:
    return db.query(Producto).filter(Producto.negocio_id == business_id).all()

def update_product(db: Session, product_id: UUID, product_update: ProductoUpdate) -> Optional[Producto]:
    db_product = db.query(Producto).filter(Producto.id == product_id).first()
    if not db_product:
        return None
    insumos_data = product_update.insumos
    product_data = product_update.model_dump(exclude_unset=True, exclude={"insumos"})
    for key, value in product_data.items():
        setattr(db_product, key, value)
    try:
        db.add(db_product)
        db.flush()
        if insumos_data is not None:
            _sync_product_insumos(db, db_product, insumos_data)
        _calculate_product_costs_and_prices(db, db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError:
        db.rollback()
        raise ValueError("Error de integridad al actualizar el producto. Podría haber un duplicado o datos inválidos.")
    except ValueError as e:
        db.rollback()
        raise e

def delete_product(db: Session, product_id: UUID) -> bool:
    db_product = db.query(Producto).filter(Producto.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False
