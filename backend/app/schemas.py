# backend/app/schemas.py

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID
from enum import Enum

from app.models import UserTier, BusinessType, ProductType, PublicidadTipo, ProductCategory

# Enums que coinciden con los modelos
class UserTier(str, Enum):
    CLIENTE = "cliente"
    MICROEMPRENDIMIENTO = "microemprendimiento"
    FREELANCER = "freelancer"

class BusinessType(str, Enum):
    PRODUCTOS = "PRODUCTOS"
    SERVICIOS = "SERVICIOS"
    AMBOS = "AMBOS"

class ProductType(str, Enum):
    PHYSICAL_GOOD = "PHYSICAL_GOOD"
    SERVICE_BY_HOUR = "SERVICE_BY_HOUR"
    SERVICE_BY_PROJECT = "SERVICE_BY_PROJECT"
    DIGITAL_GOOD = "DIGITAL_GOOD"

class PublicidadTipo(str, Enum):
    BANNER = "banner"
    LISTADO_DESTACADO = "listado_destacado"
    ANUNCIO_RED_SOCIAL = "anuncio_red_social"

# Schemas para Usuario
class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str
    tipo_tier: UserTier = UserTier.CLIENTE
    localizacion: Optional[str] = None
    curriculum_vitae: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6)

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    password: Optional[str] = None
    tipo_tier: Optional[UserTier] = None
    localizacion: Optional[str] = None
    curriculum_vitae: Optional[str] = None
    plugins_activos: Optional[List[str]] = None  # NUEVO: Para gestión de plugins

class UsuarioResponse(UsuarioBase):
    id: UUID
    is_active: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    plugins_activos: Optional[List[str]] = None  # NUEVO: Para mostrar plugins activos

    model_config = ConfigDict(from_attributes=True)

class UsuarioPublicResponse(BaseModel):
    """Esquema para respuestas públicas de usuario (sin información sensible)"""
    id: UUID
    nombre: str
    tipo_tier: UserTier
    localizacion: Optional[str] = None
    curriculum_vitae: Optional[str] = None
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)

# Schemas para Negocio
class NegocioBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo_negocio: BusinessType
    rubro: Optional[str] = None
    localizacion_geografica: Optional[str] = None
    fotos_urls: Optional[List[str]] = None

class NegocioCreate(NegocioBase):
    pass

class NegocioUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_negocio: Optional[BusinessType] = None
    rubro: Optional[str] = None
    localizacion_geografica: Optional[str] = None
    fotos_urls: Optional[List[str]] = None

class NegocioResponse(NegocioBase):
    id: UUID
    propietario_id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    calificacion_promedio: Optional[float] = Field(None, description="Calificación promedio del negocio.")
    ventas_completadas: Optional[int] = Field(None, description="Número de ventas/transacciones completadas.")
    model_config = ConfigDict(from_attributes=True)

# Schemas para Producto
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0, description="Precio base del producto/servicio")
    tipo_producto: ProductType
    negocio_id: UUID
    precio_venta: Optional[float] = Field(None, ge=0, description="Precio de venta final del producto/servicio")
    margen_ganancia_sugerido: Optional[float] = Field(None, ge=0, description="Margen de ganancia sugerido en porcentaje (ej. 20 para 20%)")

class ProductoCreate(ProductoBase):
    insumos: Optional[List["ProductoInsumoCreate"]] = None
    stock_terminado: Optional[float] = None

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = Field(None, gt=0)
    tipo_producto: Optional[ProductType] = None
    stock_terminado: Optional[float] = None
    negocio_id: Optional[UUID] = None
    precio_venta: Optional[float] = Field(None, ge=0)
    margen_ganancia_sugerido: Optional[float] = Field(None, ge=0)
    insumos: Optional[List["ProductoInsumoCreate"]] = None

class ProductoResponse(ProductoBase):
    id: UUID
    propietario_id: UUID
    precio_venta: Optional[float] = Field(None, description="Precio de venta final del producto/servicio")
    margen_ganancia_sugerido: Optional[float] = Field(None, description="Margen de ganancia sugerido en porcentaje")
    precio_sugerido: Optional[float] = Field(None, description="Precio sugerido calculado en base al COGS y margen de ganancia sugerido")

    stock_terminado: Optional[float] = None
    cogs: Optional[float] = Field(None, description="Costo de Bienes Vendidos calculado")
    margen_ganancia_real: Optional[float] = Field(None, description="Margen de ganancia real calculado en base al precio de venta y COGS")
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    insumos_asociados: List["ProductoInsumoResponse"] = []
    calificacion_promedio: Optional[float] = Field(None, description="Calificación promedio del producto.")
    ventas_completadas: Optional[int] = Field(None, description="Número de ventas/transacciones completadas.")
    model_config = ConfigDict(from_attributes=True)

# Schemas para Insumo
class InsumoBase(BaseModel):
    nombre: str
    cantidad_disponible: float = Field(..., ge=0)
    unidad_medida_compra: str
    costo_unitario_compra: float = Field(..., gt=0)

class InsumoCreate(InsumoBase):
    pass

class InsumoUpdate(BaseModel):
    nombre: Optional[str] = None
    cantidad_disponible: Optional[float] = Field(None, ge=0)
    unidad_medida_compra: Optional[str] = None
    costo_unitario_compra: Optional[float] = Field(None, gt=0)

class InsumoResponse(InsumoBase):
    id: UUID
    usuario_id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)

# Schemas para ProductoInsumo
class ProductoInsumoBase(BaseModel):
    insumo_id: UUID
    cantidad_necesaria: float = Field(..., gt=0)

class ProductoInsumoCreate(ProductoInsumoBase):
    pass

class ProductoInsumoUpdate(BaseModel):
    cantidad_necesaria: float = Field(..., gt=0)

class ProductoInsumoResponse(ProductoInsumoBase):
    producto_id: UUID
    fecha_asociacion: datetime
    insumo: InsumoResponse

    model_config = ConfigDict(from_attributes=True)

# Schemas para Publicidad
class PublicidadBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo_publicidad: PublicidadTipo
    fecha_inicio: datetime
    fecha_fin: datetime
    costo: float = Field(..., gt=0)
    item_publicitado_id: UUID
    item_publicitado_tipo: str

class PublicidadCreate(PublicidadBase):
    pass

class PublicidadUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_publicidad: Optional[PublicidadTipo] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    costo: Optional[float] = Field(None, gt=0)
    item_publicitado_id: Optional[UUID] = None
    item_publicitado_tipo: Optional[str] = None

class PublicidadResponse(PublicidadBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)

# Schemas para autenticación
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    tipo_tier: Optional[str] = None

# Schema para registro de ventas (Capítulo Ñiam)
class VentaCreate(BaseModel):
    product_id: UUID
    quantity_sold: float
    precio_unitario: float
    total_venta: float
    notas: Optional[str] = None

class VentaResponse(BaseModel):
    id: UUID
    product_id: UUID
    quantity_sold: float
    precio_unitario: float
    total_venta: float
    fecha_venta: datetime
    notas: Optional[str] = None
    usuario_id: UUID
    
    class Config:
        from_attributes = True

class VentaInDB(BaseModel):
    id: UUID
    product_id: UUID
    quantity_sold: float
    precio_unitario: float
    total_venta: float
    fecha_venta: datetime
    notas: Optional[str] = None
    usuario_id: UUID
    
    class Config:
        from_attributes = True

    user_id: Optional[str] = None
    email: Optional[str] = None
    tipo_tier: Optional[str] = None

# Forward references para evitar problemas de importación circular
ProductoCreate.model_rebuild()
ProductoUpdate.model_rebuild()
ProductoResponse.model_rebuild()
ProductoInsumoResponse.model_rebuild()

# NUEVOS SCHEMAS PARA PRODUCTOS MEJORADOS
class ProductoPanaderiaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    categoria: Optional[ProductCategory] = None
    codigo_lote: Optional[str] = None
    fecha_vencimiento: Optional[date] = None
    fecha_produccion: Optional[date] = None
    stock_minimo: Optional[float] = 0.0
    stock_maximo: Optional[float] = None
    unidad_venta: Optional[str] = "unidad"
    es_perecedero: Optional[bool] = True
    tiempo_vida_util: Optional[int] = None
    requiere_refrigeracion: Optional[bool] = False
    ingredientes: Optional[List[str]] = None
    alergenos: Optional[List[str]] = None
    calorias_por_porcion: Optional[float] = None
    peso_porcion: Optional[float] = None
    unidad_peso: Optional[str] = "g"

class ProductoPanaderiaCreate(ProductoPanaderiaBase):
    negocio_id: UUID
    tipo_producto: ProductType = ProductType.PHYSICAL_GOOD

class ProductoPanaderiaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    categoria: Optional[ProductCategory] = None
    codigo_lote: Optional[str] = None
    fecha_vencimiento: Optional[date] = None
    fecha_produccion: Optional[date] = None
    stock_minimo: Optional[float] = None
    stock_maximo: Optional[float] = None
    unidad_venta: Optional[str] = None
    es_perecedero: Optional[bool] = None
    tiempo_vida_util: Optional[int] = None
    requiere_refrigeracion: Optional[bool] = None
    ingredientes: Optional[List[str]] = None
    alergenos: Optional[List[str]] = None
    calorias_por_porcion: Optional[float] = None
    peso_porcion: Optional[float] = None
    unidad_peso: Optional[str] = None

class ProductoPanaderiaResponse(ProductoPanaderiaBase):
    id: UUID
    negocio_id: UUID
    propietario_id: UUID
    tipo_producto: ProductType
    stock_terminado: Optional[float] = None
    rating_promedio: float
    reviews_count: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    model_config = ConfigDict(from_attributes=True)

# NUEVOS SCHEMAS PARA SISTEMA DE VENTAS
class DetalleVentaBase(BaseModel):
    producto_id: UUID
    cantidad: float
    precio_unitario: float
    descuento_unitario: float = 0.0

class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVentaResponse(DetalleVentaBase):
    id: UUID
    venta_id: UUID
    subtotal: float
    costo_unitario: Optional[float] = None
    margen_ganancia: Optional[float] = None
    codigo_lote: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class VentaBase(BaseModel):
    negocio_id: UUID
    cliente_id: Optional[UUID] = None
    subtotal: float = 0.0
    descuento: float = 0.0
    impuestos: float = 0.0
    total: float = 0.0
    metodo_pago: Optional[str] = None
    estado: str = "completada"
    notas: Optional[str] = None

class VentaCreate(VentaBase):
    detalles: List[DetalleVentaCreate]

class VentaResponse(VentaBase):
    id: UUID
    numero_venta: str
    fecha_venta: datetime
    margen_ganancia_total: Optional[float] = None
    costo_total: Optional[float] = None
    detalles: List[DetalleVentaResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# SCHEMAS PARA CARRITO DE COMPRAS
class ItemCarritoBase(BaseModel):
    producto_id: UUID
    cantidad: float = 1.0

class ItemCarritoCreate(ItemCarritoBase):
    pass

class ItemCarritoResponse(ItemCarritoBase):
    id: UUID
    carrito_id: UUID
    precio_unitario: float
    fecha_agregado: datetime
    
    model_config = ConfigDict(from_attributes=True)

class CarritoCompraBase(BaseModel):
    negocio_id: UUID
    cliente_id: Optional[UUID] = None
    session_id: Optional[str] = None

class CarritoCompraCreate(CarritoCompraBase):
    pass

class CarritoCompraResponse(CarritoCompraBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    activo: bool
    items: List[ItemCarritoResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

# SCHEMAS PARA ANÁLISIS FINANCIERO
class AnalisisVentas(BaseModel):
    fecha_inicio: date
    fecha_fin: date
    total_ventas: float
    total_productos_vendidos: int
    margen_ganancia_total: float
    ventas_por_dia: List[Dict[str, Any]]
    productos_mas_vendidos: List[Dict[str, Any]]
    categorias_mas_vendidas: List[Dict[str, Any]]

class AlertaStock(BaseModel):
    producto_id: UUID
    nombre_producto: str
    stock_actual: float
    stock_minimo: float
    unidad_venta: str
    dias_sin_stock: Optional[int] = None

class ProductoVencimiento(BaseModel):
    producto_id: UUID
    nombre_producto: str
    fecha_vencimiento: date
    dias_para_vencer: int
    stock_disponible: float
    unidad_venta: str
