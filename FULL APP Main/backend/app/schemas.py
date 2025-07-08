# backend/app/schemas.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from enum import Enum

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
    email: str
    nombre: str
    tipo_tier: UserTier = UserTier.CLIENTE
    localizacion: Optional[str] = None
    curriculum_vitae: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    email: Optional[str] = None
    nombre: Optional[str] = None
    password: Optional[str] = None
    tipo_tier: Optional[UserTier] = None
    localizacion: Optional[str] = None
    curriculum_vitae: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: uuid.UUID
    is_active: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)

class UsuarioPublicResponse(BaseModel):
    """Esquema para respuestas públicas de usuario (sin información sensible)"""
    id: uuid.UUID
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
    id: uuid.UUID
    propietario_id: uuid.UUID
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)

# Schemas para Producto
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0, description="Precio base del producto/servicio")
    tipo_producto: ProductType
    negocio_id: uuid.UUID
    precio_venta: Optional[float] = Field(None, ge=0, description="Precio de venta final del producto/servicio")
    margen_ganancia_sugerido: Optional[float] = Field(None, ge=0, description="Margen de ganancia sugerido en porcentaje (ej. 20 para 20%)")

class ProductoCreate(ProductoBase):
    insumos: Optional[List["ProductoInsumoCreate"]] = None

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = Field(None, gt=0)
    tipo_producto: Optional[ProductType] = None
    negocio_id: Optional[uuid.UUID] = None
    precio_venta: Optional[float] = Field(None, ge=0)
    margen_ganancia_sugerido: Optional[float] = Field(None, ge=0)
    insumos: Optional[List["ProductoInsumoCreate"]] = None

class ProductoResponse(ProductoBase):
    id: uuid.UUID
    propietario_id: uuid.UUID
    precio_venta: Optional[float] = Field(None, description="Precio de venta final del producto/servicio")
    margen_ganancia_sugerido: Optional[float] = Field(None, description="Margen de ganancia sugerido en porcentaje")
    precio_sugerido: Optional[float] = Field(None, description="Precio sugerido calculado en base al COGS y margen de ganancia sugerido")
    cogs: Optional[float] = Field(None, description="Costo de Bienes Vendidos calculado")
    margen_ganancia_real: Optional[float] = Field(None, description="Margen de ganancia real calculado en base al precio de venta y COGS")
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    insumos_asociados: List["ProductoInsumoResponse"] = []

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
    id: uuid.UUID
    usuario_id: uuid.UUID
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)

# Schemas para ProductoInsumo
class ProductoInsumoBase(BaseModel):
    insumo_id: uuid.UUID
    cantidad_necesaria: float = Field(..., gt=0)

class ProductoInsumoCreate(ProductoInsumoBase):
    pass

class ProductoInsumoUpdate(BaseModel):
    cantidad_necesaria: float = Field(..., gt=0)

class ProductoInsumoResponse(ProductoInsumoBase):
    producto_id: uuid.UUID
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
    item_publicitado_id: uuid.UUID
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
    item_publicitado_id: Optional[uuid.UUID] = None
    item_publicitado_tipo: Optional[str] = None

class PublicidadResponse(PublicidadBase):
    id: uuid.UUID
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

# Forward references para evitar problemas de importación circular
ProductoCreate.model_rebuild()
ProductoUpdate.model_rebuild()
ProductoResponse.model_rebuild()
ProductoInsumoResponse.model_rebuild()
