# backend/app/schemas.py

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
import enum # Importar enum

# Importar enums desde models para consistencia
from app.models import (
    UserTier, ContactType, MessageChannel, ProductType, EncargoState, ShipmentProgress,
    AdvertisingType, AdvertisingStatus
)

# --- Base Schemas ---
class UserCreate(BaseModel):
    """Schema for user registration data."""
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    localizacion: Optional[str] = None
    info_contacto: Optional[Dict[str, str]] = None # Flexible contact info (phone, whatsapp, etc.)
    tipo_tier: Optional[UserTier] = UserTier.CLIENT # Default to CLIENT if not specified

class UserLogin(BaseModel):
    """Schema for user login credentials."""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Schema for JWT authentication token."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schema for data contained within the JWT token."""
    user_id: Optional[uuid.UUID] = None
    email: Optional[str] = None

class UserUpdate(BaseModel):
    """Schema for updating user profile data."""
    nombre: Optional[str] = None
    localizacion: Optional[str] = None
    info_contacto: Optional[Dict[str, str]] = None
    curriculum_vitae: Optional[str] = None # URL to CV document
    # tipo_tier no se actualiza directamente por el usuario
    password: Optional[str] = None # Para cambiar la contraseña

class UserResponse(BaseModel):
    """Schema for User data returned by the API (full profile)."""
    id: uuid.UUID
    nombre: str
    email: EmailStr
    localizacion: Optional[str] = None
    info_contacto: Optional[Dict[str, str]] = None
    tipo_tier: UserTier
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    curriculum_vitae: Optional[str] = None # Incluir CV para el propio usuario

    model_config = ConfigDict(from_attributes=True)

# --- NUEVO: User Public Response Schema ---
class UserPublicResponse(BaseModel):
    """
    Schema for public User data.
    Excludes sensitive information like email and password hash.
    """
    id: uuid.UUID
    nombre: str
    localizacion: Optional[str] = None
    tipo_tier: UserTier
    curriculum_vitae: Optional[str] = None # URL to CV document
    info_contacto: Optional[Dict[str, str]] = None # Puede ser útil para contacto público

    model_config = ConfigDict(from_attributes=True)


# --- Negocio Schemas ---
class NegocioBase(BaseModel):
    """Base schema for a Business."""
    nombre: str = Field(..., min_length=2, max_length=100)
    rubro: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = None
    localizacion_geografica: Optional[str] = None
    fotos_urls: Optional[List[str]] = None

class NegocioCreate(NegocioBase):
    """Schema for creating a new Business."""
    pass

class NegocioUpdate(NegocioBase):
    """Schema for updating an existing Business."""
    nombre: Optional[str] = None
    rubro: Optional[str] = None
    descripcion: Optional[str] = None
    localizacion_geografica: Optional[str] = None
    fotos_urls: Optional[List[str]] = None

class NegocioResponse(NegocioBase):
    """Schema for Business data returned by the API."""
    id: uuid.UUID
    usuario_id: uuid.UUID
    rating_promedio: float = 0.0
    reviews_totales: int = 0
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Insumo Schemas (for Products) ---
class InsumoBase(BaseModel):
    nombre: str
    cantidad: float
    unidad_medida: str
    costo_unitario: float = Field(..., gt=0)

class InsumoCreate(InsumoBase):
    pass

class InsumoResponse(InsumoBase):
    id: uuid.UUID
    producto_id: uuid.UUID
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Producto Schemas ---
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo_producto: ProductType
    fotos_urls: Optional[List[str]] = None
    stock: Optional[int] = None # Only for physical goods
    unidad_medida: Optional[str] = None
    atributos_especificos: Optional[Dict[str, Any]] = None # Flexible JSON for dynamic attributes

class ProductoCreate(ProductoBase):
    negocio_id: Optional[uuid.UUID] = None # Link to a business if applicable
    # insumos: Optional[List[InsumoCreate]] = None # List of insumos to create with the product (descomentar en fase 4)
    margen_ganancia_porcentaje: Optional[float] = Field(None, ge=0, le=100) # Expected margin

class ProductoUpdate(ProductoBase):
    negocio_id: Optional[uuid.UUID] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_producto: Optional[ProductType] = None
    fotos_urls: Optional[List[str]] = None
    stock: Optional[int] = None
    unidad_medida: Optional[str] = None
    atributos_especificos: Optional[Dict[str, Any]] = None
    margen_ganancia_porcentaje: Optional[float] = Field(None, ge=0, le=100)

class ProductoResponse(ProductoBase):
    id: uuid.UUID
    usuario_id: uuid.UUID
    negocio_id: Optional[uuid.UUID] = None
    precio_sugerido: Optional[float] = None
    cogs: Optional[float] = None
    margen_ganancia_porcentaje: Optional[float] = None
    rating_promedio: float = 0.0
    reviews_count: int = 0
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    # insumos: List[InsumoResponse] = [] # Include insumos when retrieving product details (descomentar en fase 4)

    model_config = ConfigDict(from_attributes=True)


# --- Contacto Schemas ---
class ContactoBase(BaseModel):
    nombre: str
    tipo_contacto: ContactType
    info_contacto: Dict[str, str] # Ej: {"email": "a@b.com", "telefono": "123"}
    empresa: Optional[str] = None
    notas: Optional[str] = None

class ContactoCreate(ContactoBase):
    pass

class ContactoUpdate(ContactoBase):
    nombre: Optional[str] = None
    tipo_contacto: Optional[ContactType] = None
    info_contacto: Optional[Dict[str, str]] = None
    empresa: Optional[str] = None
    notas: Optional[str] = None

class ContactoResponse(ContactoBase):
    id: uuid.UUID
    usuario_id: uuid.UUID
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)


# --- MensajeRegistro Schemas ---
class MensajeRegistroBase(BaseModel):
    contacto_id: uuid.UUID
    canal: MessageChannel
    contenido: str
    fecha_envio: datetime

class MensajeRegistroCreate(MensajeRegistroBase):
    pass

class MensajeRegistroResponse(MensajeRegistroBase):
    id: uuid.UUID
    usuario_id: uuid.UUID # Usuario que envió/registró el mensaje
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Encargo Schemas ---
class EncargoBase(BaseModel):
    cliente_id: uuid.UUID # ID del contacto que es cliente
    producto_id: uuid.UUID # ID del producto/servicio encargado
    cantidad: float
    precio_total: float
    fecha_encargo: datetime
    fecha_entrega_estimada: Optional[datetime] = None
    estado: EncargoState = EncargoState.PENDING_PAYMENT # Estado inicial
    notas: Optional[str] = None
    direccion_envio: Optional[str] = None
    progreso_envio: Optional[ShipmentProgress] = None

class EncargoCreate(EncargoBase):
    pass

class EncargoUpdate(EncargoBase):
    cliente_id: Optional[uuid.UUID] = None
    producto_id: Optional[uuid.UUID] = None
    cantidad: Optional[float] = None
    precio_total: Optional[float] = None
    fecha_encargo: Optional[datetime] = None
    fecha_entrega_estimada: Optional[datetime] = None
    estado: Optional[EncargoState] = None
    notas: Optional[str] = None
    direccion_envio: Optional[str] = None
    progreso_envio: Optional[ShipmentProgress] = None

class EncargoResponse(EncargoBase):
    id: uuid.UUID
    usuario_id: uuid.UUID # Usuario que gestiona el encargo
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Review Schemas ---
class ReviewCreate(BaseModel):
    """Schema for creating a new Review."""
    encargo_id: uuid.UUID
    rating: int = Field(..., ge=1, le=5)
    comentario: Optional[str] = None

class ReviewResponse(BaseModel):
    """Schema for Review data returned by the API."""
    id: uuid.UUID
    encargo_id: uuid.UUID
    rating: int
    comentario: Optional[str] = None
    fecha_review: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Publicidad Schemas ---
class PublicidadBase(BaseModel):
    """Base schema for an Advertisement."""
    item_publicitado_id: uuid.UUID # ID of the Negocio or Producto being advertised
    tipo_publicidad: AdvertisingType
    fecha_inicio: datetime
    fecha_fin: datetime
    costo: float = Field(..., gt=0)

class PublicidadCreate(PublicidadBase):
    """Schema for creating a new Advertisement."""
    pass

class PublicidadResponse(PublicidadBase):
    """Schema for Advertisement data returned by the API."""
    id: uuid.UUID
    usuario_id: uuid.UUID
    estado: AdvertisingStatus
    visualizaciones: int
    clics: int
    conversiones: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)

# Forward references for relationships to avoid circular imports
# (No es estrictamente necesario si los modelos no se referencian en los esquemas de esta manera)
# UserResponse.model_rebuild()
# NegocioResponse.model_rebuild()
# ProductoResponse.model_rebuild()
# EncargoResponse.model_rebuild()
