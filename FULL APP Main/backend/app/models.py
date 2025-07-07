from sqlalchemy import Column, String, DateTime, func, Enum as SQLEnum, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
# ELIMINA O COMENTA ESTA LÍNEA: from sqlalchemy.ext.declarative import declarative_base # <<< ELIMINA ESTA LÍNEA TAMBIÉN
import uuid
import enum

# IMPORTA Base DESDE app.database
from app.database import Base # <<< ESTO ES CRÍTICO Y DEBE SER LA ÚNICA FUENTE DE 'Base'

# Define enumerations for consistent data types
class UserTier(str, enum.Enum):
    """Enumeration for user types/tiers."""
    CLIENT = "client"
    FREELANCER = "freelancer"
    MICROEMPRENDIMIENTO = "microemprendimiento"

class ContactType(str, enum.Enum):
    """Enumeration for contact types (client or supplier)."""
    CLIENT = "cliente"
    SUPPLIER = "proveedor"

class MessageChannel(str, enum.Enum):
    """Enumeration for communication channels."""
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    INSTAGRAM_DM = "instagram_dm"
    PHONE_CALL = "llamada_registrada"
    COPIED_TO_CLIPBOARD = "copiado_portapapeles"

class ProductType(str, enum.Enum):
    """Enumeration for different types of products/services."""
    SERVICE_BY_HOUR = "servicio_por_hora"
    SERVICE_BY_PROJECT = "servicio_por_proyecto"
    PHYSICAL_GOOD = "bien_fisico"
    DIGITAL_GOOD = "bien_digital"

class EncargoState(str, enum.Enum):
    """Enumeration for the state of an 'encargo' (order/project)."""
    REQUESTED = "solicitado"
    IN_PROGRESS = "en_curso"
    COMPLETED = "completado"
    CANCELLED = "cancelado"
    PENDING_PAYMENT = "pendiente_pago"

class ShipmentProgress(str, enum.Enum):
    """Enumeration for the progress of a physical shipment."""
    DISPATCHED = "despachado"
    IN_TRANSIT = "en_transito"
    DELIVERED = "entregado"
    PENDING_PICKUP = "pendiente_retiro"

class AdvertisingType(str, enum.Enum):
    """Enumeration for different types of advertising."""
    FEATURED_MARKETPLACE = "destacado_marketplace"
    BANNER_CATEGORY = "banner_categoria"
    SEARCH_PROMOTION = "promocion_busqueda"

class AdvertisingStatus(str, enum.Enum):
    """Enumeration for the status of an advertisement."""
    ACTIVE = "activo"
    FINISHED = "finalizado"
    PENDING = "pendiente"
    PAUSED = "pausado"


# Define User model
class Usuario(Base): # Hereda de la Base importada
    """SQLAlchemy model for a user in the SOUP Emprendimientos platform."""
    __tablename__ = "usuarios"

    # Primary key, UUID automatically generated
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # User's name
    nombre = Column(String, nullable=False)
    # User's email, must be unique
    email = Column(String, unique=True, index=True, nullable=False)
    # Hashed password for security
    password_hash = Column(String, nullable=False)
    # General location of the user (can be expanded to PostGIS later)
    localizacion = Column(String, nullable=True)
    # JSONB field for flexible contact information (phone, WhatsApp, Instagram, etc.)
    info_contacto = Column(JSONB, nullable=True)
    # Type of user/tier (client, freelancer, microemprendimiento)
    tipo_tier = Column(SQLEnum(UserTier), default=UserTier.CLIENT, nullable=False)
    # Creation timestamp, automatically set
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    # Last update timestamp, automatically updated
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # JSONB field for freelancer's curriculum vitae details
    curriculum_vitae = Column(JSONB, nullable=True) # Only for UserTier.FREELANCER

    # Relationships:
    # A user can have multiple businesses (Tier 2)
    negocios = relationship("Negocio", back_populates="usuario")
    # A user can offer multiple products/services directly (Tier 1 primarily)
    productos_servicios = relationship("Producto", back_populates="usuario")
    # A user can have many contacts (clients/suppliers)
    contactos = relationship("Contacto", back_populates="usuario")
    # A user can have many message records (sent communications)
    mensajes_registrados = relationship("MensajeRegistro", back_populates="usuario")
    # A user can have many 'encargos' (orders/projects they receive)
    encargos_recibidos = relationship("Encargo", back_populates="usuario_emprendedor")
    # A user can create many advertisements
    publicidades = relationship("Publicidad", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}', tipo_tier='{self.tipo_tier}')>"


class Negocio(Base): # Hereda de la Base importada
    """SQLAlchemy model for a business (Tier 2 - Microemprendimiento)."""
    __tablename__ = "negocios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    nombre = Column(String, nullable=False)
    rubro = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    # Placeholder for geographical location, can be a String or PostGIS Point
    localizacion_geografica = Column(String, nullable=True) # TODO: Migrate to PostGIS Point type later
    fotos_urls = Column(JSONB, nullable=True) # Array of image URLs
    rating_promedio = Column(Float, default=0.0)
    reviews_totales = Column(Integer, default=0)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    usuario = relationship("Usuario", back_populates="negocios")
    productos = relationship("Producto", back_populates="negocio")


class Producto(Base): # Hereda de la Base importada
    """SQLAlchemy model for a Product or Service offered by a user/business."""
    __tablename__ = "productos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    negocio_id = Column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=True) # Nullable if offered by a Freelancer directly

    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    tipo_producto = Column(SQLEnum(ProductType), nullable=False)
    fotos_urls = Column(JSONB, nullable=True) # Array of image URLs

    # Attributes for calculator and pricing
    precio_sugerido = Column(Float, nullable=True) # Can be null until calculated
    cogs = Column(Float, nullable=True) # Cost of Goods Sold/Service Cost, can be null until calculated
    margen_ganancia_porcentaje = Column(Float, nullable=True) # Desired profit margin

    # Specific attributes for physical goods
    stock = Column(Integer, nullable=True) # Only for ProductType.PHYSICAL_GOOD

    # Common for all types
    unidad_medida = Column(String, nullable=True) # E.g., 'unidad', 'kg', 'litro', 'hora', 'proyecto'
    atributos_especificos = Column(JSONB, nullable=True) # Flexible JSONB for dynamic attributes (color, size, format, etc.)

    rating_promedio = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    usuario = relationship("Usuario", back_populates="productos_servicios")
    negocio = relationship("Negocio", back_populates="productos")
    insumos = relationship("Insumo", back_populates="producto")
    encargos = relationship("Encargo", back_populates="producto_encargado")


class Insumo(Base): # Hereda de la Base importada
    """SQLAlchemy model for an input/resource used in a Product/Service."""
    __tablename__ = "insumos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)

    nombre_insumo = Column(String, nullable=False) # E.g., 'naranjas', 'horas de diseño', 'arcilla'
    descripcion = Column(String, nullable=True)
    proveedor = Column(String, nullable=True) # Name of the supplier
    costo_unitario = Column(Float, nullable=False)
    cantidad = Column(Float, nullable=False)
    unidad_medida = Column(String, nullable=True) # E.g., 'kg', 'litro', 'hora', 'unidad'
    costo_neto = Column(Float, nullable=False) # Calculated: costo_unitario * cantidad

    # Relationship
    producto = relationship("Producto", back_populates="insumos")


class Contacto(Base): # Hereda de la Base importada
    """SQLAlchemy model for a contact (client or supplier) of an emprendedor."""
    __tablename__ = "contactos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False) # The emprendedor who owns this contact

    nombre = Column(String, nullable=False)
    tipo_contacto = Column(SQLEnum(ContactType), nullable=False)
    telefono = Column(String, nullable=True)
    whatsapp_url = Column(String, nullable=True) # Example: "https://wa.me/XXXXXXXXXXX"
    instagram_url = Column(String, nullable=True)
    email = Column(String, nullable=True)
    notas_personales = Column(String, nullable=True)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship
    usuario = relationship("Usuario", back_populates="contactos")
    mensajes_registrados = relationship("MensajeRegistro", back_populates="contacto")
    encargos_as_client = relationship("Encargo", back_populates="cliente_final")


class MensajeRegistro(Base): # Hereda de la Base importada
    """SQLAlchemy model to record messages sent by the emprendedor via external channels."""
    __tablename__ = "mensajes_registro"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contacto_id = Column(UUID(as_uuid=True), ForeignKey("contactos.id"), nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False) # The emprendedor who sent the message

    fecha_envio = Column(DateTime, default=func.now(), nullable=False)
    canal = Column(SQLEnum(MessageChannel), nullable=False)
    contenido = Column(String, nullable=False) # Full text of the message written in SOUP
    proposito = Column(String, nullable=True) # E.g., 'presupuesto', 'seguimiento', 'confirmacion_pedido'
    url_generada = Column(String, nullable=True) # The external link generated (e.g., wa.me link)

    # Relationships
    contacto = relationship("Contacto", back_populates="mensajes_registrados")
    usuario = relationship("Usuario", back_populates="mensajes_registrados")


class Encargo(Base): # Hereda de la Base importada
    """SQLAlchemy model for an 'Encargo' (order, project, or service request)."""
    __tablename__ = "encargos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False) # The emprendedor receiving the encargo
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("contactos.id"), nullable=False) # The client who made the encargo
    producto_id = Column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False) # The product/service being ordered

    fecha_solicitud = Column(DateTime, default=func.now(), nullable=False)
    estado = Column(SQLEnum(EncargoState), default=EncargoState.REQUESTED, nullable=False)
    descripcion_personalizada = Column(String, nullable=True) # Custom details for the order
    precio_final_acordado = Column(Float, nullable=True) # Price agreed for this specific encargo
    ganancia_neta_encargo = Column(Float, nullable=True) # Calculated net profit for this encargo

    # Attributes specific to services/digital goods
    progreso_porcentaje = Column(Integer, default=0, nullable=True) # Progress for projects (0-100)
    link_entrega_digital = Column(String, nullable=True) # URL for digital delivery

    # Attributes specific to physical products/shipments
    proveedor_encomienda = Column(String, nullable=True)
    costo_envio = Column(Float, nullable=True)
    progreso_envio = Column(SQLEnum(ShipmentProgress), nullable=True)
    tracking_number = Column(String, nullable=True)

    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    usuario_emprendedor = relationship("Usuario", back_populates="encargos_recibidos")
    cliente_final = relationship("Contacto", back_populates="encargos_as_client")
    producto_encargado = relationship("Producto", back_populates="encargos")
    reviews = relationship("Review", back_populates="encargo") # One encargo can have one review


class Review(Base): # Hereda de la Base importada
    """SQLAlchemy model for a review/rating left by a client."""
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # The client who left the review. Can be a SOUP user or a Contact.
    # For simplicity, let's link to the Encargo (which already links to the client)
    encargo_id = Column(UUID(as_uuid=True), ForeignKey("encargos.id"), nullable=False)

    rating = Column(Integer, nullable=False) # 1-5 stars
    comentario = Column(String, nullable=True)
    fecha_review = Column(DateTime, default=func.now(), nullable=False)

    # Relationships
    encargo = relationship("Encargo", back_populates="reviews")


class Publicidad(Base): # Hereda de la Base importada
    """SQLAlchemy model for a premium advertisement."""
    __tablename__ = "publicidades"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False) # The user who purchased the ad
    # The item being advertised (can be a Negocio or a Producto)
    item_publicitado_id = Column(UUID(as_uuid=True), nullable=False) # UUID of the Negocio or Producto

    tipo_publicidad = Column(SQLEnum(AdvertisingType), nullable=False)
    estado = Column(SQLEnum(AdvertisingStatus), default=AdvertisingStatus.PENDING, nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    costo = Column(Float, nullable=False)

    # Performance metrics
    visualizaciones = Column(Integer, default=0)
    clics = Column(Integer, default=0)
    conversiones = Column(Integer, default=0) # E.g., sales generated from the ad

    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship
    usuario = relationship("Usuario", back_populates="publicidades")
