# backend/app/models.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, Enum, ARRAY, Date
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

# NUEVA: Roles específicos para Panadería Ñiam
class UserRole(str, enum.Enum):
    TRABAJADOR_ATENCION = "trabajador_atencion"  # Atención al cliente
    COCINERO = "cocinero"  # Productor de insumos
    MANAGER = "manager"  # Dueños/Managers
    ADMIN = "admin"  # Administrador del sistema

class BusinessType(str, enum.Enum):
    PRODUCTOS = "PRODUCTOS"
    SERVICIOS = "SERVICIOS"
    AMBOS = "AMBOS"

class ProductType(str, enum.Enum):
    PHYSICAL_GOOD = "PHYSICAL_GOOD"
    SERVICE_BY_HOUR = "SERVICE_BY_HOUR"
    SERVICE_BY_PROJECT = "SERVICE_BY_PROJECT"
    DIGITAL_GOOD = "DIGITAL_GOOD"

# NUEVA: Categorías específicas para panadería
class ProductCategory(str, enum.Enum):
    PAN = "pan"
    PASTEL = "pastel"
    GALLETA = "galleta"
    BOLLO = "bollo"
    TARTA = "tarta"
    EMPANADA = "empanada"
    CHIPA = "chipa"  # Específico para Panadería Ñiam
    OTRO = "otro"

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
    
    # NUEVO: Campo para plugins activos
    plugins_activos: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=list)
    
    # NUEVO: Campo para roles específicos de Panadería Ñiam
    rol: Mapped[Optional[UserRole]] = mapped_column(Enum(UserRole), nullable=True)
    
    # NUEVO: Campos específicos para empleados
    negocio_asignado_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=True)
    fecha_contratacion: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    salario: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    horario_trabajo: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # "8:00-16:00", etc.
    permisos_especiales: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)  # Lista de permisos específicos

    # Relaciones
    negocios: Mapped[List["Negocio"]] = relationship(
        "Negocio",
        back_populates="propietario",
        foreign_keys="[Negocio.propietario_id]",
        cascade="all, delete-orphan"
    )
    productos: Mapped[List["Producto"]] = relationship("Producto", back_populates="propietario", cascade="all, delete-orphan")
    insumos: Mapped[List["Insumo"]] = relationship("Insumo", back_populates="usuario", cascade="all, delete-orphan")
    negocio_asignado: Mapped[Optional["Negocio"]] = relationship(
        "Negocio",
        foreign_keys=[negocio_asignado_id]
    )


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
    # Nuevos campos para IA
    calificacion_promedio: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_calificaciones: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ventas_completadas: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relaciones
    propietario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="negocios",
        foreign_keys="[Negocio.propietario_id]"
    )
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

    stock_terminado: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=0.0)

    # Campos para cálculo de costos y precios
    precio_venta: Mapped[Optional[float]] = mapped_column(Float, nullable=True) # Precio de venta final
    margen_ganancia_sugerido: Mapped[Optional[float]] = mapped_column(Float, nullable=True) # Margen de ganancia sugerido en porcentaje
    precio_sugerido: Mapped[Optional[float]] = mapped_column(Float, nullable=True) # Precio sugerido calculado
    cogs: Mapped[Optional[float]] = mapped_column(Float, nullable=True) # Costo de Bienes Vendidos
    margen_ganancia_real: Mapped[Optional[float]] = mapped_column(Float, nullable=True) # Margen de ganancia real

    # NUEVOS CAMPOS para coincidir con la base de datos
    rating_promedio: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    reviews_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # NUEVOS CAMPOS ESPECÍFICOS PARA PANADERÍA
    categoria: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    codigo_lote: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Código de lote para trazabilidad
    fecha_vencimiento: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)  # Fecha de vencimiento
    fecha_produccion: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)  # Fecha de producción
    stock_minimo: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=0.0)  # Stock mínimo para alertas
    stock_maximo: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Stock máximo recomendado
    unidad_venta: Mapped[Optional[str]] = mapped_column(String, nullable=True, default="unidad")  # unidad, kg, docena, etc.
    es_perecedero: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=True)  # Si es perecedero
    tiempo_vida_util: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Días de vida útil
    requiere_refrigeracion: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
    ingredientes: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)  # Lista de ingredientes principales
    alergenos: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)  # Lista de alérgenos
    calorias_por_porcion: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    peso_porcion: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unidad_peso: Mapped[Optional[str]] = mapped_column(String, nullable=True, default="g")  # g, kg, etc.

    # Relaciones
    propietario: Mapped["Usuario"] = relationship("Usuario", back_populates="productos")
    negocio: Mapped["Negocio"] = relationship("Negocio", back_populates="productos")
    insumos_asociados: Mapped[List["ProductoInsumo"]] = relationship("ProductoInsumo", back_populates="producto", cascade="all, delete-orphan")


class Insumo(Base):
    __tablename__ = "insumos"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, index=True, nullable=False)
    cantidad_disponible: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    unidad_medida_compra: Mapped[str] = mapped_column(String, nullable=False)
    costo_unitario_compra: Mapped[float] = mapped_column(Float, nullable=False)
    usuario_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="insumos")
    productos_asociados: Mapped[List["ProductoInsumo"]] = relationship("ProductoInsumo", back_populates="insumo", cascade="all, delete-orphan")


class ProductoInsumo(Base):
    __tablename__ = "producto_insumos"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    producto_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)
    insumo_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("insumos.id"), nullable=False)
    cantidad_necesaria: Mapped[float] = mapped_column(Float, nullable=False)
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
    item_publicitado_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    item_publicitado_tipo: Mapped[str] = mapped_column(String, nullable=False) # 'producto', 'negocio', etc.
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# NUEVOS MODELOS PARA SISTEMA DE VENTAS MEJORADO

class Venta(Base):
    __tablename__ = "ventas"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    negocio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=False)
    cliente_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True)  # Cliente registrado o anónimo
    numero_venta: Mapped[str] = mapped_column(String, nullable=False, unique=True)  # Número de venta único
    fecha_venta: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    subtotal: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    descuento: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    impuestos: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    total: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    metodo_pago: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # efectivo, tarjeta, transferencia, etc.
    estado: Mapped[str] = mapped_column(String, nullable=False, default="completada")  # completada, cancelada, pendiente
    notas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Campos para análisis
    margen_ganancia_total: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    costo_total: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Relaciones
    negocio: Mapped["Negocio"] = relationship("Negocio")
    cliente: Mapped[Optional["Usuario"]] = relationship("Usuario", foreign_keys=[cliente_id])
    detalles: Mapped[List["DetalleVenta"]] = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")


class DetalleVenta(Base):
    __tablename__ = "detalles_venta"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    venta_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ventas.id"), nullable=False)
    producto_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)
    cantidad: Mapped[float] = mapped_column(Float, nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)
    descuento_unitario: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    subtotal: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Campos para análisis
    costo_unitario: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    margen_ganancia: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    codigo_lote: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Lote específico vendido
    
    # Relaciones
    venta: Mapped["Venta"] = relationship("Venta", back_populates="detalles")
    producto: Mapped["Producto"] = relationship("Producto")


class CarritoCompra(Base):
    __tablename__ = "carritos_compra"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    negocio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=False)
    cliente_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True)
    session_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Para clientes no registrados
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relaciones
    negocio: Mapped["Negocio"] = relationship("Negocio")
    cliente: Mapped[Optional["Usuario"]] = relationship("Usuario", foreign_keys=[cliente_id])
    items: Mapped[List["ItemCarrito"]] = relationship("ItemCarrito", back_populates="carrito", cascade="all, delete-orphan")


class ItemCarrito(Base):
    __tablename__ = "items_carrito"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    carrito_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("carritos_compra.id"), nullable=False)
    producto_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)
    cantidad: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)
    fecha_agregado: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    carrito: Mapped["CarritoCompra"] = relationship("CarritoCompra", back_populates="items")
    producto: Mapped["Producto"] = relationship("Producto")

# NUEVOS MODELOS ESPECÍFICOS PARA PANADERÍA ÑIAM

class Receta(Base):
    __tablename__ = "recetas"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    producto_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)
    negocio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=False)
    creador_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    
    # Campos específicos para recetas
    tiempo_preparacion: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Minutos
    tiempo_coccion: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Minutos
    temperatura_horno: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Grados Celsius
    rendimiento: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Cantidad que produce la receta
    unidad_rendimiento: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # "unidades", "kg", etc.
    dificultad: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # "fácil", "medio", "difícil"
    instrucciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Instrucciones paso a paso
    
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    producto: Mapped["Producto"] = relationship("Producto")
    negocio: Mapped["Negocio"] = relationship("Negocio")
    creador: Mapped["Usuario"] = relationship("Usuario", foreign_keys=[creador_id])
    ingredientes: Mapped[List["IngredienteReceta"]] = relationship("IngredienteReceta", back_populates="receta", cascade="all, delete-orphan")


class IngredienteReceta(Base):
    __tablename__ = "ingredientes_receta"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    receta_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("recetas.id"), nullable=False)
    insumo_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("insumos.id"), nullable=False)
    cantidad_necesaria: Mapped[float] = mapped_column(Float, nullable=False)
    unidad_medida: Mapped[str] = mapped_column(String, nullable=False)  # "g", "kg", "unidades", etc.
    orden: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Orden de agregado en la receta
    notas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Notas específicas del ingrediente
    
    # Relaciones
    receta: Mapped["Receta"] = relationship("Receta", back_populates="ingredientes")
    insumo: Mapped["Insumo"] = relationship("Insumo")


class Produccion(Base):
    __tablename__ = "producciones"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    receta_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("recetas.id"), nullable=False)
    negocio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=False)
    productor_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    
    # Campos de producción
    fecha_produccion: Mapped[Date] = mapped_column(Date, nullable=False)
    hora_inicio: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)
    hora_fin: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)
    cantidad_producida: Mapped[float] = mapped_column(Float, nullable=False)
    cantidad_esperada: Mapped[float] = mapped_column(Float, nullable=False)
    rendimiento_real: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Porcentaje de rendimiento
    
    # Campos de calidad
    calidad: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # "excelente", "buena", "regular", "mala"
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    problemas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Problemas durante la producción
    
    # Campos de costos
    costo_total: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    costo_unitario: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    estado: Mapped[str] = mapped_column(String, nullable=False, default="planificada")  # planificada, en_proceso, completada, cancelada
    
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    receta: Mapped["Receta"] = relationship("Receta")
    negocio: Mapped["Negocio"] = relationship("Negocio")
    productor: Mapped["Usuario"] = relationship("Usuario", foreign_keys=[productor_id])


class HorarioPico(Base):
    __tablename__ = "horarios_pico"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    negocio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=False)
    
    # Campos de horario
    dia_semana: Mapped[int] = mapped_column(Integer, nullable=False)  # 0=Lunes, 1=Martes, ..., 6=Domingo
    hora_inicio: Mapped[str] = mapped_column(String, nullable=False)  # "08:00"
    hora_fin: Mapped[str] = mapped_column(String, nullable=False)  # "12:00"
    
    # Métricas del horario pico
    ventas_promedio: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    productos_vendidos_promedio: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    clientes_promedio: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Configuración
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    prioridad: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1=alta, 2=media, 3=baja
    
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    negocio: Mapped["Negocio"] = relationship("Negocio")
