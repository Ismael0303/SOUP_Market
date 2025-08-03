# backend/app/crud/venta.py

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, date, timedelta
import uuid

from app.models import Venta, DetalleVenta, CarritoCompra, ItemCarrito, Producto
from app.schemas import VentaCreate, DetalleVentaCreate, CarritoCompraCreate, ItemCarritoCreate

def generate_venta_number() -> str:
    """Genera un número único de venta"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = str(uuid.uuid4())[:8]
    return f"V{timestamp}{random_suffix}"

def create_venta(db: Session, venta_data: VentaCreate, propietario_id: UUID) -> Venta:
    """Crea una nueva venta con sus detalles"""
    
    # Generar número de venta único
    numero_venta = generate_venta_number()
    
    # Crear la venta
    db_venta = Venta(
        negocio_id=venta_data.negocio_id,
        cliente_id=venta_data.cliente_id,
        numero_venta=numero_venta,
        subtotal=venta_data.subtotal,
        descuento=venta_data.descuento,
        impuestos=venta_data.impuestos,
        total=venta_data.total,
        metodo_pago=venta_data.metodo_pago,
        estado=venta_data.estado,
        notas=venta_data.notas
    )
    
    db.add(db_venta)
    db.flush()  # Para obtener el ID de la venta
    
    # Calcular costos y márgenes
    costo_total = 0.0
    margen_total = 0.0
    
    # Crear detalles de venta
    for detalle_data in venta_data.detalles:
        # Obtener información del producto
        producto = db.query(Producto).filter(Producto.id == detalle_data.producto_id).first()
        if not producto:
            continue
        
        # Calcular subtotal del detalle
        subtotal_detalle = (detalle_data.precio_unitario - detalle_data.descuento_unitario) * detalle_data.cantidad
        
        # Calcular costo y margen
        costo_unitario = producto.cogs or 0.0
        costo_detalle = costo_unitario * detalle_data.cantidad
        margen_detalle = subtotal_detalle - costo_detalle
        
        costo_total += costo_detalle
        margen_total += margen_detalle
        
        # Crear detalle de venta
        db_detalle = DetalleVenta(
            venta_id=db_venta.id,
            producto_id=detalle_data.producto_id,
            cantidad=detalle_data.cantidad,
            precio_unitario=detalle_data.precio_unitario,
            descuento_unitario=detalle_data.descuento_unitario,
            subtotal=subtotal_detalle,
            costo_unitario=costo_unitario,
            margen_ganancia=margen_detalle,
            codigo_lote=producto.codigo_lote
        )
        
        db.add(db_detalle)
        
        # Actualizar stock del producto
        if producto.stock_terminado is not None:
            producto.stock_terminado -= detalle_data.cantidad
            if producto.stock_terminado < 0:
                producto.stock_terminado = 0
    
    # Actualizar costos y márgenes totales de la venta
    db_venta.costo_total = costo_total
    db_venta.margen_ganancia_total = margen_total
    
    db.commit()
    db.refresh(db_venta)
    
    return db_venta

def get_venta(db: Session, venta_id: UUID) -> Optional[Venta]:
    """Obtiene una venta por ID"""
    return db.query(Venta).filter(Venta.id == venta_id).first()

def get_ventas_by_negocio(db: Session, negocio_id: UUID, skip: int = 0, limit: int = 100) -> List[Venta]:
    """Obtiene todas las ventas de un negocio"""
    return db.query(Venta).filter(Venta.negocio_id == negocio_id).offset(skip).limit(limit).all()

def get_ventas_by_date_range(db: Session, negocio_id: UUID, fecha_inicio: date, fecha_fin: date) -> List[Venta]:
    """Obtiene ventas en un rango de fechas"""
    return db.query(Venta).filter(
        and_(
            Venta.negocio_id == negocio_id,
            func.date(Venta.fecha_venta) >= fecha_inicio,
            func.date(Venta.fecha_venta) <= fecha_fin
        )
    ).all()

def get_analisis_ventas(db: Session, negocio_id: UUID, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
    """Obtiene análisis de ventas para un período"""
    
    ventas = get_ventas_by_date_range(db, negocio_id, fecha_inicio, fecha_fin)
    
    # Calcular totales
    total_ventas = sum(venta.total for venta in ventas)
    total_productos = sum(sum(detalle.cantidad for detalle in venta.detalles) for venta in ventas)
    margen_total = sum(venta.margen_ganancia_total or 0 for venta in ventas)
    
    # Ventas por día
    ventas_por_dia = {}
    for venta in ventas:
        fecha = venta.fecha_venta.date()
        if fecha not in ventas_por_dia:
            ventas_por_dia[fecha] = {"total": 0, "cantidad": 0}
        ventas_por_dia[fecha]["total"] += venta.total
        ventas_por_dia[fecha]["cantidad"] += len(venta.detalles)
    
    # Productos más vendidos
    productos_vendidos = {}
    for venta in ventas:
        for detalle in venta.detalles:
            producto_id = str(detalle.producto_id)
            if producto_id not in productos_vendidos:
                productos_vendidos[producto_id] = {
                    "producto_id": detalle.producto_id,
                    "nombre": detalle.producto.nombre,
                    "cantidad": 0,
                    "total": 0
                }
            productos_vendidos[producto_id]["cantidad"] += detalle.cantidad
            productos_vendidos[producto_id]["total"] += detalle.subtotal
    
    productos_mas_vendidos = sorted(
        productos_vendidos.values(),
        key=lambda x: x["cantidad"],
        reverse=True
    )[:10]
    
    return {
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "total_ventas": total_ventas,
        "total_productos_vendidos": total_productos,
        "margen_ganancia_total": margen_total,
        "ventas_por_dia": [
            {"fecha": str(fecha), **datos}
            for fecha, datos in ventas_por_dia.items()
        ],
        "productos_mas_vendidos": productos_mas_vendidos
    }

def get_alertas_stock(db: Session, negocio_id: UUID) -> List[Dict[str, Any]]:
    """Obtiene alertas de stock bajo"""
    productos = db.query(Producto).filter(
        and_(
            Producto.negocio_id == negocio_id,
            Producto.stock_terminado <= Producto.stock_minimo
        )
    ).all()
    
    alertas = []
    for producto in productos:
        dias_sin_stock = None
        if producto.stock_terminado == 0:
            # Calcular días desde la última venta
            ultima_venta = db.query(DetalleVenta).join(Venta).filter(
                and_(
                    DetalleVenta.producto_id == producto.id,
                    Venta.negocio_id == negocio_id
                )
            ).order_by(desc(DetalleVenta.id)).first()
            
            if ultima_venta:
                dias_sin_stock = (datetime.now() - ultima_venta.venta.fecha_venta).days
        
        alertas.append({
            "producto_id": producto.id,
            "nombre_producto": producto.nombre,
            "stock_actual": producto.stock_terminado or 0,
            "stock_minimo": producto.stock_minimo or 0,
            "unidad_venta": producto.unidad_venta or "unidad",
            "dias_sin_stock": dias_sin_stock
        })
    
    return alertas

def get_productos_por_vencer(db: Session, negocio_id: UUID, dias_limite: int = 7) -> List[Dict[str, Any]]:
    """Obtiene productos próximos a vencer"""
    fecha_limite = date.today() + timedelta(days=dias_limite)
    
    productos = db.query(Producto).filter(
        and_(
            Producto.negocio_id == negocio_id,
            Producto.fecha_vencimiento <= fecha_limite,
            Producto.fecha_vencimiento >= date.today(),
            Producto.stock_terminado > 0
        )
    ).all()
    
    productos_vencimiento = []
    for producto in productos:
        dias_para_vencer = (producto.fecha_vencimiento - date.today()).days
        
        productos_vencimiento.append({
            "producto_id": producto.id,
            "nombre_producto": producto.nombre,
            "fecha_vencimiento": producto.fecha_vencimiento,
            "dias_para_vencer": dias_para_vencer,
            "stock_disponible": producto.stock_terminado or 0,
            "unidad_venta": producto.unidad_venta or "unidad"
        })
    
    return sorted(productos_vencimiento, key=lambda x: x["dias_para_vencer"])

# FUNCIONES PARA CARRITO DE COMPRAS
def create_carrito(db: Session, carrito_data: CarritoCompraCreate) -> CarritoCompra:
    """Crea un nuevo carrito de compras"""
    db_carrito = CarritoCompra(**carrito_data.dict())
    db.add(db_carrito)
    db.commit()
    db.refresh(db_carrito)
    return db_carrito

def add_item_to_carrito(db: Session, carrito_id: UUID, item_data: ItemCarritoCreate) -> ItemCarrito:
    """Añade un item al carrito"""
    
    # Verificar si el producto ya está en el carrito
    existing_item = db.query(ItemCarrito).filter(
        and_(
            ItemCarrito.carrito_id == carrito_id,
            ItemCarrito.producto_id == item_data.producto_id
        )
    ).first()
    
    if existing_item:
        # Actualizar cantidad
        existing_item.cantidad += item_data.cantidad
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        # Obtener precio del producto
        producto = db.query(Producto).filter(Producto.id == item_data.producto_id).first()
        if not producto:
            raise ValueError("Producto no encontrado")
        
        # Crear nuevo item
        db_item = ItemCarrito(
            carrito_id=carrito_id,
            producto_id=item_data.producto_id,
            cantidad=item_data.cantidad,
            precio_unitario=producto.precio
        )
        
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

def get_carrito(db: Session, carrito_id: UUID) -> Optional[CarritoCompra]:
    """Obtiene un carrito por ID"""
    return db.query(CarritoCompra).filter(CarritoCompra.id == carrito_id).first()

def get_carrito_by_cliente(db: Session, negocio_id: UUID, cliente_id: Optional[UUID] = None, session_id: Optional[str] = None) -> Optional[CarritoCompra]:
    """Obtiene el carrito activo de un cliente"""
    query = db.query(CarritoCompra).filter(
        and_(
            CarritoCompra.negocio_id == negocio_id,
            CarritoCompra.activo == True
        )
    )
    
    if cliente_id:
        query = query.filter(CarritoCompra.cliente_id == cliente_id)
    elif session_id:
        query = query.filter(CarritoCompra.session_id == session_id)
    else:
        return None
    
    return query.first()

def remove_item_from_carrito(db: Session, carrito_id: UUID, item_id: UUID) -> bool:
    """Elimina un item del carrito"""
    item = db.query(ItemCarrito).filter(
        and_(
            ItemCarrito.carrito_id == carrito_id,
            ItemCarrito.id == item_id
        )
    ).first()
    
    if item:
        db.delete(item)
        db.commit()
        return True
    return False

def clear_carrito(db: Session, carrito_id: UUID) -> bool:
    """Limpia todos los items del carrito"""
    items = db.query(ItemCarrito).filter(ItemCarrito.carrito_id == carrito_id).all()
    
    for item in items:
        db.delete(item)
    
    db.commit()
    return True 