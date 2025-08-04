# backend/app/routers/venta_router.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime, timedelta

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Usuario, Negocio
from app.crud.venta import (
    create_venta, get_venta, get_ventas_by_negocio, get_analisis_ventas,
    get_alertas_stock, get_productos_por_vencer,
    create_carrito, add_item_to_carrito, get_carrito, get_carrito_by_cliente,
    remove_item_from_carrito, clear_carrito
)
from app.schemas import (
    VentaCreate, VentaResponse, DetalleVentaCreate,
    CarritoCompraCreate, CarritoCompraResponse,
    ItemCarritoCreate, ItemCarritoResponse,
    AnalisisVentas, AlertaStock, ProductoVencimiento
)

router = APIRouter(prefix="/ventas", tags=["ventas"])

@router.post("/", response_model=VentaResponse)
def crear_venta(
    venta_data: VentaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crea una nueva venta (POS)"""
    
    # Verificar que el usuario tenga acceso al negocio
    negocio = db.query(Negocio).filter(
        and_(
            Negocio.id == venta_data.negocio_id,
            Negocio.propietario_id == current_user.id
        )
    ).first()
    
    if not negocio:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear ventas en este negocio"
        )
    
    try:
        venta = create_venta(db, venta_data, current_user.id)
        return venta
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear la venta: {str(e)}"
        )

@router.get("/{venta_id}", response_model=VentaResponse)
def obtener_venta(
    venta_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene una venta específica"""
    venta = get_venta(db, venta_id)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada"
        )
    
    # Verificar permisos
    if venta.negocio.propietario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver esta venta"
        )
    
    return venta

@router.get("/negocio/{negocio_id}", response_model=List[VentaResponse])
def obtener_ventas_negocio(
    negocio_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene todas las ventas de un negocio"""
    
    # Verificar permisos
    negocio = db.query(Negocio).filter(
        and_(
            Negocio.id == negocio_id,
            Negocio.propietario_id == current_user.id
        )
    ).first()
    
    if not negocio:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver las ventas de este negocio"
        )
    
    ventas = get_ventas_by_negocio(db, negocio_id, skip, limit)
    return ventas

@router.get("/analisis/{negocio_id}")
def obtener_analisis_ventas(
    negocio_id: UUID,
    fecha_inicio: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_fin: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene análisis de ventas para un período"""
    
    # Verificar permisos
    negocio = db.query(Negocio).filter(
        and_(
            Negocio.id == negocio_id,
            Negocio.propietario_id == current_user.id
        )
    ).first()
    
    if not negocio:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver el análisis de este negocio"
        )
    
    # Validar fechas
    if fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio debe ser anterior a la fecha de fin"
        )
    
    analisis = get_analisis_ventas(db, negocio_id, fecha_inicio, fecha_fin)
    return analisis

@router.get("/alertas/stock/{negocio_id}")
def obtener_alertas_stock(
    negocio_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene alertas de stock bajo"""
    
    # Verificar permisos
    negocio = db.query(Negocio).filter(
        and_(
            Negocio.id == negocio_id,
            Negocio.propietario_id == current_user.id
        )
    ).first()
    
    if not negocio:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver las alertas de este negocio"
        )
    
    alertas = get_alertas_stock(db, negocio_id)
    return {"alertas": alertas, "total": len(alertas)}

@router.get("/alertas/vencimiento/{negocio_id}")
def obtener_productos_por_vencer(
    negocio_id: UUID,
    dias_limite: int = Query(7, ge=1, le=30, description="Días límite para alerta de vencimiento"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene productos próximos a vencer"""
    
    # Verificar permisos
    negocio = db.query(Negocio).filter(
        and_(
            Negocio.id == negocio_id,
            Negocio.propietario_id == current_user.id
        )
    ).first()
    
    if not negocio:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver las alertas de este negocio"
        )
    
    productos = get_productos_por_vencer(db, negocio_id, dias_limite)
    return {"productos": productos, "total": len(productos)}

# ENDPOINTS PARA CARRITO DE COMPRAS
@router.post("/carrito/", response_model=CarritoCompraResponse)
def crear_carrito(
    carrito_data: CarritoCompraCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crea un nuevo carrito de compras"""
    
    # Verificar permisos del negocio
    negocio = db.query(Negocio).filter(
        and_(
            Negocio.id == carrito_data.negocio_id,
            Negocio.propietario_id == current_user.id
        )
    ).first()
    
    if not negocio:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear carritos en este negocio"
        )
    
    carrito = create_carrito(db, carrito_data)
    return carrito

@router.get("/carrito/{carrito_id}", response_model=CarritoCompraResponse)
def obtener_carrito(
    carrito_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene un carrito específico"""
    carrito = get_carrito(db, carrito_id)
    if not carrito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrito no encontrado"
        )
    
    # Verificar permisos
    if carrito.negocio.propietario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver este carrito"
        )
    
    return carrito

@router.post("/carrito/{carrito_id}/items/", response_model=ItemCarritoResponse)
def agregar_item_carrito(
    carrito_id: UUID,
    item_data: ItemCarritoCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Añade un item al carrito"""
    
    # Verificar permisos del carrito
    carrito = get_carrito(db, carrito_id)
    if not carrito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrito no encontrado"
        )
    
    if carrito.negocio.propietario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para modificar este carrito"
        )
    
    try:
        item = add_item_to_carrito(db, carrito_id, item_data)
        return item
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/carrito/{carrito_id}/items/{item_id}")
def eliminar_item_carrito(
    carrito_id: UUID,
    item_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Elimina un item del carrito"""
    
    # Verificar permisos del carrito
    carrito = get_carrito(db, carrito_id)
    if not carrito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrito no encontrado"
        )
    
    if carrito.negocio.propietario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para modificar este carrito"
        )
    
    success = remove_item_from_carrito(db, carrito_id, item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado en el carrito"
        )
    
    return {"message": "Item eliminado del carrito"}

@router.delete("/carrito/{carrito_id}/limpiar")
def limpiar_carrito(
    carrito_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Limpia todos los items del carrito"""
    
    # Verificar permisos del carrito
    carrito = get_carrito(db, carrito_id)
    if not carrito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrito no encontrado"
        )
    
    if carrito.negocio.propietario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para modificar este carrito"
        )
    
    clear_carrito(db, carrito_id)
    return {"message": "Carrito limpiado exitosamente"}

# ENDPOINT PARA CONVERTIR CARRITO EN VENTA
@router.post("/carrito/{carrito_id}/finalizar", response_model=VentaResponse)
def finalizar_compra(
    carrito_id: UUID,
    metodo_pago: str = Query(..., description="Método de pago"),
    descuento: float = Query(0.0, ge=0.0, description="Descuento total"),
    impuestos: float = Query(0.0, ge=0.0, description="Impuestos totales"),
    notas: Optional[str] = Query(None, description="Notas adicionales"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Convierte un carrito en una venta"""
    
    # Verificar permisos del carrito
    carrito = get_carrito(db, carrito_id)
    if not carrito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrito no encontrado"
        )
    
    if carrito.negocio.propietario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para finalizar este carrito"
        )
    
    if not carrito.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El carrito está vacío"
        )
    
    # Calcular totales
    subtotal = sum(item.precio_unitario * item.cantidad for item in carrito.items)
    total = subtotal - descuento + impuestos
    
    # Crear detalles de venta
    detalles = []
    for item in carrito.items:
        detalle = DetalleVentaCreate(
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario,
            descuento_unitario=0.0  # Los descuentos se aplican al total
        )
        detalles.append(detalle)
    
    # Crear venta
    venta_data = VentaCreate(
        negocio_id=carrito.negocio_id,
        cliente_id=carrito.cliente_id,
        subtotal=subtotal,
        descuento=descuento,
        impuestos=impuestos,
        total=total,
        metodo_pago=metodo_pago,
        notas=notas,
        detalles=detalles
    )
    
    try:
        venta = create_venta(db, venta_data, current_user.id)
        
        # Marcar carrito como inactivo
        carrito.activo = False
        db.commit()
        
        return venta
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al finalizar la compra: {str(e)}"
        ) 