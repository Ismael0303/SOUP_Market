# backend/app/crud/product.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from typing import List, Optional

from app.models import Producto, Negocio # Importa los modelos Producto y Negocio
from app.schemas import ProductoCreate, ProductoUpdate # Importa los esquemas Pydantic

# Función para crear un nuevo producto
def create_product(db: Session, user_id: UUID, product: ProductoCreate) -> Producto:
    """
    Crea un nuevo producto/servicio en la base de datos.
    Requiere el user_id al que se asociará el producto.
    Opcionalmente, puede asociarse a un negocio_id del mismo usuario.
    """
    # Importar crud_business localmente dentro de la función si es necesario
    from app.crud import business as crud_business

    # Si se proporciona un negocio_id, verificar que pertenezca al usuario
    if product.negocio_id:
        db_negocio = crud_business.get_business_by_id(db, business_id=product.negocio_id)
        if not db_negocio:
            raise ValueError("El negocio_id proporcionado no existe o no pertenece a este usuario.")
        if db_negocio.usuario_id != user_id: # Asegurar que el negocio pertenece al usuario actual
            raise ValueError("El negocio_id proporcionado no pertenece a este usuario.")

    # Crea una instancia del modelo Producto con los datos del esquema y el user_id
    db_product = Producto(
        **product.model_dump(exclude_unset=True, exclude={'insumos', 'margen_ganancia_porcentaje'}),
        usuario_id=user_id
    )
    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError:
        db.rollback()
        raise ValueError("Error de integridad al crear el producto.")

# Función para obtener un producto por su ID
def get_product_by_id(db: Session, product_id: UUID) -> Optional[Producto]:
    """
    Obtiene un producto de la base de datos por su ID.
    Retorna el objeto Producto si se encuentra, de lo contrario, None.
    """
    return db.query(Producto).filter(Producto.id == product_id).first()

# Función para obtener todos los productos de un usuario específico
def get_products_by_user_id(db: Session, user_id: UUID) -> List[Producto]:
    """
    Obtiene una lista de todos los productos/servicios asociados a un usuario específico.
    """
    return db.query(Producto).filter(Producto.usuario_id == user_id).all()

# Función para obtener todos los productos de un negocio específico
def get_products_by_business_id(db: Session, business_id: UUID) -> List[Producto]:
    """
    Obtiene una lista de todos los productos/servicios asociados a un negocio específico.
    """
    return db.query(Producto).filter(Producto.negocio_id == business_id).all()

# NUEVA FUNCIÓN: Obtener todos los productos (para listado público)
def get_all_products(db: Session) -> List[Producto]:
    """
    Obtiene una lista de todos los productos/servicios en la base de datos.
    Utilizado para el listado público.
    """
    return db.query(Producto).all()

# Función para actualizar un producto existente
def update_product(db: Session, product_id: UUID, product_update: ProductoUpdate) -> Optional[Producto]:
    """
    Actualiza los campos de un producto existente.
    Retorna el objeto Producto actualizado si se encuentra, de lo contrario, None.
    """
    db_product = db.query(Producto).filter(Producto.id == product_id).first()
    if db_product:
        update_data = product_update.model_dump(exclude_unset=True, exclude={'insumos', 'margen_ganancia_porcentaje'})
        for key, value in update_data.items():
            setattr(db_product, key, value)
        try:
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            return db_product
        except IntegrityError:
            db.rollback()
            raise ValueError("Error de integridad al actualizar el producto.")
    return None

# Función para eliminar un producto
def delete_product(db: Session, product_id: UUID) -> bool:
    """
    Elimina un producto de la base de datos por su ID.
    Retorna True si el producto fue eliminado, False si no se encontró.
    """
    db_product = db.query(Producto).filter(Producto.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False
