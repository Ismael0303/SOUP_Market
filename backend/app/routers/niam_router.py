# backend/app/routers/niam_router.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, extract
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import date, datetime, timedelta

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Usuario, Negocio, Producto, Venta, DetalleVenta, Receta, Produccion, HorarioPico, UserRole
from app.crud.venta import get_analisis_ventas, get_alertas_stock, get_productos_por_vencer
from app.schemas import VentaResponse

router = APIRouter(prefix="/niam", tags=["Panadería Ñiam"])

# FUNCIONES DE VERIFICACIÓN DE ROLES
def verify_role(current_user: Usuario, required_roles: List[UserRole]) -> bool:
    """Verifica si el usuario tiene uno de los roles requeridos"""
    return current_user.rol in required_roles

def get_niam_business(db: Session, current_user: Usuario) -> Negocio:
    """Obtiene el negocio Panadería Ñiam del usuario"""
    # Buscar negocio con nombre que contenga "Ñiam" o "Niam"
    negocio = db.query(Negocio).filter(
        and_(
            Negocio.propietario_id == current_user.id,
            or_(
                func.lower(Negocio.nombre).contains("ñiam"),
                func.lower(Negocio.nombre).contains("niam"),
                func.lower(Negocio.nombre).contains("chipa")
            )
        )
    ).first()
    
    if not negocio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el negocio Panadería Ñiam"
        )
    
    return negocio

# DASHBOARD ESPECIALIZADO PARA PANADERÍA ÑIAM
@router.get("/dashboard")
def get_niam_dashboard(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Dashboard especializado para Panadería Ñiam"""
    
    # Verificar roles permitidos
    if not verify_role(current_user, [UserRole.TRABAJADOR_ATENCION, UserRole.COCINERO, UserRole.MANAGER, UserRole.ADMIN]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder al dashboard"
        )
    
    negocio = get_niam_business(db, current_user)
    
    # Obtener fecha actual
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    
    # 1. Métricas específicas para Chipá
    chipa_ventas = db.query(func.sum(DetalleVenta.cantidad)).join(Venta).join(Producto).filter(
        and_(
            Venta.negocio_id == negocio.id,
            func.date(Venta.fecha_venta) >= inicio_mes,
            or_(
                func.lower(Producto.nombre).contains("chipa"),
                Producto.categoria == "chipa"
            )
        )
    ).scalar() or 0
    
    # 2. Ventas totales del mes
    ventas_mes = db.query(func.sum(Venta.total)).filter(
        and_(
            Venta.negocio_id == negocio.id,
            func.date(Venta.fecha_venta) >= inicio_mes
        )
    ).scalar() or 0
    
    # 3. Productos más vendidos
    productos_mas_vendidos = db.query(
        Producto.nombre,
        func.sum(DetalleVenta.cantidad).label("cantidad_vendida"),
        func.sum(DetalleVenta.subtotal).label("total_ventas")
    ).join(DetalleVenta).join(Venta).filter(
        and_(
            Venta.negocio_id == negocio.id,
            func.date(Venta.fecha_venta) >= inicio_mes
        )
    ).group_by(Producto.id, Producto.nombre).order_by(desc("cantidad_vendida")).limit(5).all()
    
    # 4. Alertas de stock
    alertas_stock = get_alertas_stock(db, negocio.id)
    
    # 5. Productos por vencer
    productos_vencimiento = get_productos_por_vencer(db, negocio.id, 7)
    
    # 6. Horarios pico
    horarios_pico = db.query(HorarioPico).filter(
        and_(
            HorarioPico.negocio_id == negocio.id,
            HorarioPico.activo == True
        )
    ).order_by(HorarioPico.dia_semana, HorarioPico.hora_inicio).all()
    
    return {
        "negocio": {
            "id": negocio.id,
            "nombre": negocio.nombre,
            "calificacion_promedio": negocio.calificacion_promedio,
            "total_calificaciones": negocio.total_calificaciones
        },
        "metricas_mes": {
            "ventas_chipa": chipa_ventas,
            "ventas_totales": ventas_mes,
            "inicio_mes": inicio_mes.isoformat(),
            "hoy": hoy.isoformat()
        },
        "productos_mas_vendidos": [
            {
                "nombre": p.nombre,
                "cantidad_vendida": p.cantidad_vendida,
                "total_ventas": p.total_ventas
            }
            for p in productos_mas_vendidos
        ],
        "alertas": {
            "stock_bajo": len(alertas_stock),
            "por_vencer": len(productos_vencimiento)
        },
        "horarios_pico": [
            {
                "dia_semana": h.dia_semana,
                "hora_inicio": h.hora_inicio,
                "hora_fin": h.hora_fin,
                "ventas_promedio": h.ventas_promedio,
                "prioridad": h.prioridad
            }
            for h in horarios_pico
        ]
    }

# GESTIÓN DE RECETAS ESPECÍFICAS PARA CHIPÁ
@router.get("/recetas")
def get_recetas_chipa(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene las recetas de Chipá y otros productos"""
    
    # Verificar roles permitidos
    if not verify_role(current_user, [UserRole.COCINERO, UserRole.MANAGER, UserRole.ADMIN]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver recetas"
        )
    
    negocio = get_niam_business(db, current_user)
    
    recetas = db.query(Receta).filter(
        and_(
            Receta.negocio_id == negocio.id,
            or_(
                func.lower(Receta.nombre).contains("chipa"),
                func.lower(Producto.nombre).contains("chipa")
            )
        )
    ).join(Producto).all()
    
    return {
        "recetas": [
            {
                "id": r.id,
                "nombre": r.nombre,
                "descripcion": r.descripcion,
                "producto": r.producto.nombre,
                "tiempo_preparacion": r.tiempo_preparacion,
                "tiempo_coccion": r.tiempo_coccion,
                "temperatura_horno": r.temperatura_horno,
                "rendimiento": r.rendimiento,
                "unidad_rendimiento": r.unidad_rendimiento,
                "dificultad": r.dificultad,
                "ingredientes_count": len(r.ingredientes)
            }
            for r in recetas
        ]
    }

@router.get("/recetas/{receta_id}")
def get_receta_detalle(
    receta_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene el detalle completo de una receta"""
    
    # Verificar roles permitidos
    if not verify_role(current_user, [UserRole.COCINERO, UserRole.MANAGER, UserRole.ADMIN]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver recetas"
        )
    
    receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receta no encontrada"
        )
    
    # Verificar que pertenece al negocio del usuario
    negocio = get_niam_business(db, current_user)
    if receta.negocio_id != negocio.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver esta receta"
        )
    
    return {
        "id": receta.id,
        "nombre": receta.nombre,
        "descripcion": receta.descripcion,
        "producto": {
            "id": receta.producto.id,
            "nombre": receta.producto.nombre,
            "precio": receta.producto.precio
        },
        "tiempo_preparacion": receta.tiempo_preparacion,
        "tiempo_coccion": receta.tiempo_coccion,
        "temperatura_horno": receta.temperatura_horno,
        "rendimiento": receta.rendimiento,
        "unidad_rendimiento": receta.unidad_rendimiento,
        "dificultad": receta.dificultad,
        "instrucciones": receta.instrucciones,
        "ingredientes": [
            {
                "id": i.id,
                "insumo": {
                    "id": i.insumo.id,
                    "nombre": i.insumo.nombre,
                    "stock_disponible": i.insumo.cantidad_disponible,
                    "unidad_medida": i.insumo.unidad_medida_compra
                },
                "cantidad_necesaria": i.cantidad_necesaria,
                "unidad_medida": i.unidad_medida,
                "orden": i.orden,
                "notas": i.notas
            }
            for i in receta.ingredientes
        ]
    }

# GESTIÓN DE PRODUCCIÓN
@router.get("/produccion")
def get_producciones(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene las producciones recientes"""
    
    # Verificar roles permitidos
    if not verify_role(current_user, [UserRole.COCINERO, UserRole.MANAGER, UserRole.ADMIN]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver producciones"
        )
    
    negocio = get_niam_business(db, current_user)
    
    producciones = db.query(Produccion).filter(
        and_(
            Produccion.negocio_id == negocio.id,
            Produccion.fecha_produccion >= date.today() - timedelta(days=30)
        )
    ).order_by(desc(Produccion.fecha_produccion)).limit(20).all()
    
    return {
        "producciones": [
            {
                "id": p.id,
                "receta": p.receta.nombre,
                "producto": p.receta.producto.nombre,
                "fecha_produccion": p.fecha_produccion.isoformat(),
                "cantidad_producida": p.cantidad_producida,
                "cantidad_esperada": p.cantidad_esperada,
                "rendimiento_real": p.rendimiento_real,
                "calidad": p.calidad,
                "estado": p.estado,
                "productor": p.productor.nombre
            }
            for p in producciones
        ]
    }

# ANÁLISIS ESPECÍFICO DE CHIPÁ
@router.get("/analisis/chipa")
def get_analisis_chipa(
    fecha_inicio: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_fin: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Análisis específico de ventas de Chipá"""
    
    # Verificar roles permitidos
    if not verify_role(current_user, [UserRole.MANAGER, UserRole.ADMIN]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver análisis"
        )
    
    negocio = get_niam_business(db, current_user)
    
    # Ventas de Chipá en el período
    ventas_chipa = db.query(
        func.date(Venta.fecha_venta).label("fecha"),
        func.sum(DetalleVenta.cantidad).label("cantidad_vendida"),
        func.sum(DetalleVenta.subtotal).label("total_ventas"),
        func.avg(DetalleVenta.precio_unitario).label("precio_promedio")
    ).join(DetalleVenta).join(Producto).filter(
        and_(
            Venta.negocio_id == negocio.id,
            func.date(Venta.fecha_venta) >= fecha_inicio,
            func.date(Venta.fecha_venta) <= fecha_fin,
            or_(
                func.lower(Producto.nombre).contains("chipa"),
                Producto.categoria == "chipa"
            )
        )
    ).group_by(func.date(Venta.fecha_venta)).order_by(func.date(Venta.fecha_venta)).all()
    
    # Análisis por hora del día
    ventas_por_hora = db.query(
        extract('hour', Venta.fecha_venta).label("hora"),
        func.sum(DetalleVenta.cantidad).label("cantidad_vendida")
    ).join(DetalleVenta).join(Producto).filter(
        and_(
            Venta.negocio_id == negocio.id,
            func.date(Venta.fecha_venta) >= fecha_inicio,
            func.date(Venta.fecha_venta) <= fecha_fin,
            or_(
                func.lower(Producto.nombre).contains("chipa"),
                Producto.categoria == "chipa"
            )
        )
    ).group_by(extract('hour', Venta.fecha_venta)).order_by(extract('hour', Venta.fecha_venta)).all()
    
    # Totales
    total_cantidad = sum(v.cantidad_vendida for v in ventas_chipa)
    total_ventas = sum(v.total_ventas for v in ventas_chipa)
    
    return {
        "periodo": {
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin.isoformat()
        },
        "totales": {
            "cantidad_vendida": total_cantidad,
            "total_ventas": total_ventas,
            "precio_promedio": total_ventas / total_cantidad if total_cantidad > 0 else 0
        },
        "ventas_por_dia": [
            {
                "fecha": v.fecha.isoformat(),
                "cantidad_vendida": v.cantidad_vendida,
                "total_ventas": v.total_ventas,
                "precio_promedio": v.precio_promedio
            }
            for v in ventas_chipa
        ],
        "ventas_por_hora": [
            {
                "hora": v.hora,
                "cantidad_vendida": v.cantidad_vendida
            }
            for v in ventas_por_hora
        ]
    }

# ALERTAS ESPECÍFICAS PARA PANADERÍA ÑIAM
@router.get("/alertas")
def get_alertas_niam(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene alertas específicas para Panadería Ñiam"""
    
    negocio = get_niam_business(db, current_user)
    
    # Alertas de stock de insumos críticos para Chipá
    insumos_criticos = ["almidón", "mandioca", "queso", "huevo", "leche"]
    alertas_insumos = db.query(Insumo).filter(
        and_(
            Insumo.usuario_id == current_user.id,
            or_(
                *[func.lower(Insumo.nombre).contains(insumo) for insumo in insumos_criticos]
            ),
            Insumo.cantidad_disponible <= 10  # Stock bajo
        )
    ).all()
    
    # Productos por vencer
    productos_vencimiento = get_productos_por_vencer(db, negocio.id, 3)  # 3 días
    
    # Producciones pendientes
    producciones_pendientes = db.query(Produccion).filter(
        and_(
            Produccion.negocio_id == negocio.id,
            Produccion.estado == "planificada",
            Produccion.fecha_produccion <= date.today() + timedelta(days=1)
        )
    ).all()
    
    return {
        "insumos_criticos": [
            {
                "id": i.id,
                "nombre": i.nombre,
                "stock_disponible": i.cantidad_disponible,
                "unidad_medida": i.unidad_medida_compra
            }
            for i in alertas_insumos
        ],
        "productos_por_vencer": productos_vencimiento,
        "producciones_pendientes": [
            {
                "id": p.id,
                "receta": p.receta.nombre,
                "fecha_produccion": p.fecha_produccion.isoformat(),
                "cantidad_esperada": p.cantidad_esperada
            }
            for p in producciones_pendientes
        ]
    } 