# backend/app/crud/product.py

from sqlalchemy import func
from datetime import datetime
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
        insumo = db.get(Insumo, producto_insumo.insumo_id)
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
    # Asignar valores por defecto para rating_promedio y reviews_count
    if "rating_promedio" not in product_data or product_data["rating_promedio"] is None:
        product_data["rating_promedio"] = 0.0
    if "reviews_count" not in product_data or product_data["reviews_count"] is None:
        product_data["reviews_count"] = 0
    
    # Asignar fecha_actualizacion explícitamente
    from datetime import datetime
    product_data["fecha_actualizacion"] = datetime.utcnow()
    
    db_product = Producto(**product_data, propietario_id=propietario_id)
    try:
        db.add(db_product)
        db.flush()
        _sync_product_insumos(db, db_product, insumos_data)
        _calculate_product_costs_and_prices(db, db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError as e:
        db.rollback()
        # Mostrar el error SQL exacto para diagnóstico
        error_msg = f"Error de integridad al crear el producto: {str(e)}"
        print(f"DEBUG - Error SQL: {error_msg}")
        raise ValueError(error_msg)
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

def record_sale(db: Session, product_id: UUID, quantity_sold: float, user_id: UUID, precio_unitario: float = None):
    """
    Registra una venta de producto y actualiza el inventario
    
    Args:
        db: Sesión de base de datos
        product_id: ID del producto vendido
        quantity_sold: Cantidad vendida
        user_id: ID del usuario que registra la venta
        precio_unitario: Precio unitario de la venta (opcional, usa precio_venta del producto si no se proporciona)
    
    Returns:
        dict: Información de la venta registrada
    """
    from sqlalchemy.orm import joinedload
    from ..models import Producto, Insumo
    from ..schemas import VentaCreate
    
    # Obtener el producto con sus insumos asociados
    db_product = db.query(Producto).options(
        joinedload(Producto.insumos_asociados)
    ).filter(Producto.id == product_id).first()
    
    if not db_product:
        raise ValueError("Producto no encontrado")
    
    if db_product.propietario_id != user_id:
        raise ValueError("No autorizado para vender este producto")
    
    # Verificar stock disponible
    if db_product.stock_terminado is not None and db_product.stock_terminado < quantity_sold:
        raise ValueError(f"Stock insuficiente. Disponible: {db_product.stock_terminado}, Solicitado: {quantity_sold}")
    
    # Usar precio_venta del producto si no se proporciona precio_unitario
    if precio_unitario is None:
        precio_unitario = db_product.precio_venta or 0.0
    
    total_venta = precio_unitario * quantity_sold
    
    # Actualizar stock terminado del producto
    if db_product.stock_terminado is not None:
        db_product.stock_terminado -= quantity_sold
    
    # Actualizar insumos asociados al producto
    insumos_actualizados = []
    for insumo_asociado in db_product.insumos_asociados:
        insumo = db.query(Insumo).filter(Insumo.id == insumo_asociado.insumo_id).first()
        if insumo:
            cantidad_necesaria = insumo_asociado.cantidad_necesaria * quantity_sold
            insumo.cantidad_disponible -= cantidad_necesaria
            insumos_actualizados.append({
                'nombre': insumo.nombre,
                'cantidad_descontada': cantidad_necesaria,
                'stock_restante': insumo.cantidad_disponible
            })
    
    # TODO: Registrar la venta en tabla de transacciones (implementar en capítulo posterior)
    # Por ahora, solo actualizamos el inventario
    
    # Actualizar fecha_actualizacion del producto
    from sqlalchemy import func
    db_product.fecha_actualizacion = func.now()
    
    try:
        db.commit()
        db.refresh(db_product)
        
        return {
            'producto_id': product_id,
            'producto_nombre': db_product.nombre,
            'quantity_sold': quantity_sold,
            'precio_unitario': precio_unitario,
            'total_venta': total_venta,
            'stock_restante': db_product.stock_terminado,
            'insumos_actualizados': insumos_actualizados,
            'fecha_venta': datetime.now()
        }
        
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error al registrar la venta: {str(e)}")

def update_product_stock(db: Session, product_id: UUID, new_stock: float, user_id: UUID):
    """
    Actualiza el stock terminado de un producto
    
    Args:
        db: Sesión de base de datos
        product_id: ID del producto
        new_stock: Nueva cantidad de stock
        user_id: ID del usuario que actualiza
    
    Returns:
        Producto: Producto actualizado
    """
    db_product = get_product_by_id(db, product_id)
    
    if not db_product:
        raise ValueError("Producto no encontrado")
    
    if db_product.propietario_id != user_id:
        raise ValueError("No autorizado para actualizar este producto")
    
    db_product.stock_terminado = new_stock
    db_product.fecha_actualizacion = func.now()
    
    try:
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error al actualizar stock: {str(e)}")

def get_products_low_stock(db: Session, user_id: UUID, threshold: float = 5.0):
    """
    Obtiene productos con stock bajo
    
    Args:
        db: Sesión de base de datos
        user_id: ID del usuario
        threshold: Umbral de stock bajo (por defecto 5.0)
    
    Returns:
        List[Producto]: Lista de productos con stock bajo
    """
    return db.query(Producto).filter(
        Producto.propietario_id == user_id,
        Producto.stock_terminado <= threshold,
        Producto.stock_terminado > 0
    ).all()

def get_products_out_of_stock(db: Session, user_id: UUID):
    """
    Obtiene productos sin stock
    
    Args:
        db: Sesión de base de datos
        user_id: ID del usuario
    
    Returns:
        List[Producto]: Lista de productos sin stock
    """
    return db.query(Producto).filter(
        Producto.propietario_id == user_id,
        (Producto.stock_terminado == 0) | (Producto.stock_terminado.is_(None))
    ).all()
