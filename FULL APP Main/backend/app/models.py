# backend/app/models.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4
import enum
from typing import List, Optional

from app.database import Base

# Enumeraciones
class UserTier(str, enum.Enum):
    CLIENTE = "cliente"
    MICROEMPRENDIMIENTO = "microemprendimiento"
    FREELANCER = "freelancer"

class BusinessType(str, enum.Enum):
    PRODUCTOS = "PRODUCTOS"
    SERVICIOS = "SERVICIOS"
    AMBOS = "AMBOS"

class ProductType(str, enum.Enum):
    PHYSICAL_GOOD = "PHYSICAL_GOOD"
    SERVICE_BY_HOUR = "SERVICE_BY_HOUR"
    SERVICE_BY_PROJECT = "SERVICE_BY_PROJECT"
    DIGITAL_GOOD = "DIGITAL_GOOD"

class PublicidadTipo(str, enum.Enum):
    BANNER = "banner"
    LISTADO_DESTACADO = "listado_destacado"
    ANUNCIO_RED_SOCIAL = "anuncio_red_social"

# Modelos de la Base de Datos

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    tipo_tier: Mapped[UserTier] = mapped_column(Enum(UserTier), default=UserTier.CLIENTE, nullable=False)
    localizacion: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    curriculum_vitae: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # Para freelancers

    # Relaciones
    negocios: Mapped[List["Negocio"]] = relationship("Negocio", back_populates="propietario", cascade="all, delete-orphan")
    productos: Mapped[List["Producto"]] = relationship("Producto", back_populates="propietario", cascade="all, delete-orphan")
    insumos: Mapped[List["Insumo"]] = relationship("Insumo", back_populates="usuario", cascade="all, delete-orphan")


class Negocio(Base):
    __tablename__ = "negocios"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, index=True, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    propietario_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    tipo_negocio: Mapped[BusinessType] = mapped_column(Enum(BusinessType), nullable=False)
    rubro: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    localizacion_geografica: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fotos_urls: Mapped[Optional[List[str]]] = mapped_column(Text, nullable=True)  # Se almacenará como JSON
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    propietario: Mapped["Usuario"] = relationship("Usuario", back_populates="negocios")
    productos: Mapped[List["Producto"]] = relationship("Producto", back_populates="negocio", cascade="all, delete-orphan")
    publicidades: Mapped[List["Publicidad"]] = relationship(
        "Publicidad",
        primaryjoin="and_(Publicidad.item_publicitado_id == Negocio.id, Publicidad.item_publicitado_tipo.in_(['banner', 'listado_destacado']))",
        foreign_keys="[Publicidad.item_publicitado_id]",
        viewonly=True,
        overlaps="producto_publicitado" # Añadido overlaps
    )


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, index=True, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    precio: Mapped[float] = mapped_column(Float, nullable=False) # Precio base del producto/servicio
    tipo_producto: Mapped[ProductType] = mapped_column(Enum(ProductType), nullable=False)
    negocio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=False)
    propietario_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False) # Para asegurar propiedad directa
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Nuevos campos para cálculo de costos y precios
    precio_venta: Mapped[Optional[float]] = mapped_column(Float, nullable=True) # Precio de venta final del producto/servicio
    margen_ganancia_sugerido: Mapped[Optional[float]] = mapped_column(Float, nullable=True) # Margen de ganancia sugerido en porcentaje (ej. 20 para 20%)
    cogs: Mapped[Optional[float]] = mapped_column(Float, nullable=True) # Costo de Bienes Vendidos (calculado)
    precio_sugerido: Mapped[Optional[float]] = mapped_column(Float, nullable=True) # Precio sugerido calculado en base al COGS y margen de ganancia sugerido

    # Relaciones
    negocio: Mapped["Negocio"] = relationship("Negocio", back_populates="productos")
    propietario: Mapped["Usuario"] = relationship("Usuario", back_populates="productos")
    insumos_asociados: Mapped[List["ProductoInsumo"]] = relationship("ProductoInsumo", back_populates="producto", cascade="all, delete-orphan")
    publicidades: Mapped[List["Publicidad"]] = relationship(
        "Publicidad",
        primaryjoin="and_(Publicidad.item_publicitado_id == Producto.id, Publicidad.item_publicitado_tipo == 'anuncio_red_social')",
        foreign_keys="[Publicidad.item_publicitado_id]",
        viewonly=True,
        overlaps="negocio_publicitado" # Añadido overlaps
    )


class Insumo(Base):
    __tablename__ = "insumos"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, index=True, nullable=False)
    cantidad_disponible: Mapped[float] = mapped_column(Float, nullable=False)
    unidad_medida_compra: Mapped[str] = mapped_column(String, nullable=False)
    costo_unitario_compra: Mapped[float] = mapped_column(Float, nullable=False)
    usuario_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="insumos")
    productos_asociados: Mapped[List["ProductoInsumo"]] = relationship("ProductoInsumo", back_populates="insumo", cascade="all, delete-orphan")


class ProductoInsumo(Base):
    __tablename__ = "producto_insumo"

    producto_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("productos.id"), primary_key=True, nullable=False)
    insumo_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("insumos.id"), primary_key=True, nullable=False)
    cantidad_necesaria: Mapped[float] = mapped_column(Float, nullable=False) # Cantidad de este insumo necesaria para una unidad del producto
    fecha_asociacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    producto: Mapped["Producto"] = relationship("Producto", back_populates="insumos_asociados")
    insumo: Mapped["Insumo"] = relationship("Insumo", back_populates="productos_asociados")


class Publicidad(Base):
    __tablename__ = "publicidades"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tipo_publicidad: Mapped[PublicidadTipo] = mapped_column(Enum(PublicidadTipo), nullable=False)
    fecha_inicio: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    fecha_fin: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    costo: Mapped[float] = mapped_column(Float, nullable=False)
    item_publicitado_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False) # ID del negocio o producto
    item_publicitado_tipo: Mapped[str] = mapped_column(String, nullable=False) # 'negocio' o 'producto'
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones polimórficas
    negocio_publicitado: Mapped[Optional["Negocio"]] = relationship(
        "Negocio",
        primaryjoin="and_(Publicidad.item_publicitado_id == Negocio.id, Publicidad.item_publicitado_tipo.in_(['banner', 'listado_destacado']))",
        foreign_keys="[Publicidad.item_publicitado_id]",
        viewonly=True,
        overlaps="publicidades" # Añadido overlaps
    )
    producto_publicitado: Mapped[Optional["Producto"]] = relationship(
        "Producto",
        primaryjoin="and_(Publicidad.item_publicitado_id == Producto.id, Publicidad.item_publicitado_tipo == 'anuncio_red_social')",
        foreign_keys="[Publicidad.item_publicitado_id]",
        viewonly=True,
        overlaps="publicidades" # Añadido overlaps
    )
