# DOCUMENTACIÓN TÉCNICA - SOUP Emprendimientos

**Versión:** 1.1  
**Fecha:** 9 de Julio de 2025  
**Proyecto:** SOUP Emprendimientos - Full Stack (FastAPI + React)  
**Mantenedor:** Asistente AI

---

## 📋 ÍNDICE

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Base de Datos](#base-de-datos)
3. [Backend - FastAPI](#backend---fastapi)
4. [Frontend - React](#frontend---react)
5. [Autenticación y Autorización](#autenticación-y-autorización)
6. [Endpoints API](#endpoints-api)
7. [Sistema de Plugins](#sistema-de-plugins)
8. [Sistema POS Mejorado](#sistema-pos-mejorado)
9. [Optimización Panadería Ñiam](#optimización-panadería-ñiam)
10. [Diccionario de Referencia](#diccionario-de-referencia)
11. [Convenciones y Estándares](#convenciones-y-estándares)
12. [🛣️ ROADMAP - Capítulo 1: Workflow Interno y Gestión de Ventas en Local (Panadería Ñiam)](#️-roadmap---capítulo-1-workflow-interno-y-gestión-de-ventas-en-local-panadería-ñiam)

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### **Stack Tecnológico**
- **Backend:** FastAPI (Python 3.11+)
- **Frontend:** React 18 + Vite
- **Base de Datos:** PostgreSQL 15+
- **ORM:** SQLAlchemy 2.0
- **Autenticación:** JWT (JSON Web Tokens)
- **Validación:** Pydantic
- **UI:** Tailwind CSS + Shadcn/ui

### **Estructura de Directorios**
```
FULL APP Main/
├── backend/
│   ├── app/
│   │   ├── models.py          # Modelos SQLAlchemy
│   │   ├── schemas.py         # Schemas Pydantic
│   │   ├── database.py        # Configuración BD
│   │   ├── dependencies.py    # Dependencias FastAPI
│   │   ├── routers/           # Endpoints API
│   │   └── crud/              # Operaciones BD
│   ├── main.py               # Aplicación principal
│   └── requirements.txt      # Dependencias Python
├── frontend/
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   ├── screens/          # Pantallas principales
│   │   ├── api/              # Clientes API
│   │   ├── context/          # Contextos React
│   │   └── utils/            # Utilidades
│   └── package.json
└── Documentación/            # Esta documentación
```

---

## 🗄️ BASE DE DATOS

### **Configuración**
- **Host:** localhost
- **Puerto:** 5432
- **Base de Datos:** soup_app_db
- **Usuario:** soupuser
- **Motor:** postgresql+psycopg2

### **Tablas Principales**

#### **usuarios**
```sql
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR UNIQUE NOT NULL,
    nombre VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tipo_tier user_tier DEFAULT 'cliente',
    localizacion VARCHAR,
    curriculum_vitae TEXT,
    -- NUEVOS CAMPOS AGREGADOS (v1.1)
    plugins_activos TEXT[] DEFAULT '{}',
    rol VARCHAR(50),
    negocio_asignado_id UUID REFERENCES negocios(id),
    fecha_contratacion DATE,
    salario DECIMAL(10,2),
    horario_trabajo VARCHAR(100),
    permisos_especiales TEXT[] DEFAULT '{}'
);
```

#### **negocios**
```sql
CREATE TABLE negocios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR NOT NULL,
    descripcion TEXT,
    propietario_id UUID REFERENCES usuarios(id),
    tipo_negocio business_type NOT NULL,
    rubro VARCHAR,
    localizacion_geografica VARCHAR,
    fotos_urls TEXT[],
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### **productos**
```sql
CREATE TABLE productos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR NOT NULL,
    descripcion TEXT,
    precio FLOAT NOT NULL,
    tipo_producto product_type NOT NULL,
    negocio_id UUID REFERENCES negocios(id),
    propietario_id UUID REFERENCES usuarios(id),
    precio_venta FLOAT,
    margen_ganancia_sugerido FLOAT,
    cogs FLOAT,
    precio_sugerido FLOAT,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### **insumos**
```sql
CREATE TABLE insumos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR NOT NULL,
    cantidad_disponible FLOAT NOT NULL,
    unidad_medida_compra VARCHAR NOT NULL,
    costo_unitario_compra FLOAT NOT NULL,
    usuario_id UUID REFERENCES usuarios(id),
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### **Enums de Base de Datos**

#### **user_tier**
```sql
CREATE TYPE user_tier AS ENUM (
    'cliente',
    'microemprendimiento', 
    'freelancer'
);
```

#### **business_type**
```sql
CREATE TYPE business_type AS ENUM (
    'PRODUCTOS',
    'SERVICIOS',
    'AMBOS'
);
```

#### **product_type**
```sql
CREATE TYPE product_type AS ENUM (
    'PHYSICAL_GOOD',
    'SERVICE_BY_HOUR',
    'SERVICE_BY_PROJECT',
    'DIGITAL_GOOD'
);
```

---

## 🔧 BACKEND - FastAPI

### **Modelos SQLAlchemy**

#### **Usuario**
```python
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    tipo_tier: Mapped[UserTier] = mapped_column(Enum(UserTier), default=UserTier.CLIENTE, nullable=False)
    localizacion: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    curriculum_vitae: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # NUEVOS CAMPOS AGREGADOS (v1.1)
    plugins_activos: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=list)
    rol: Mapped[Optional[UserRole]] = mapped_column(Enum(UserRole), nullable=True)
    negocio_asignado_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=True)
    fecha_contratacion: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    salario: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    horario_trabajo: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    permisos_especiales: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
    
    # Relaciones (CORREGIDAS - v1.1)
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
```

#### **Negocio**
```python
class Negocio(Base):
    __tablename__ = "negocios"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nombre: Mapped[str] = mapped_column(String, index=True, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    propietario_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    tipo_negocio: Mapped[BusinessType] = mapped_column(Enum(BusinessType), nullable=False)
    rubro: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    localizacion_geografica: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fotos_urls: Mapped[Optional[List[str]]] = mapped_column(Text, nullable=True)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    propietario: Mapped["Usuario"] = relationship("Usuario", back_populates="negocios")
    productos: Mapped[List["Producto"]] = relationship("Producto", back_populates="negocio", cascade="all, delete-orphan")
```

#### **Producto**
```python
class Producto(Base):
    __tablename__ = "productos"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nombre: Mapped[str] = mapped_column(String, index=True, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    tipo_producto: Mapped[ProductType] = mapped_column(Enum(ProductType), nullable=False)
    negocio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("negocios.id"), nullable=False)
    propietario_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    precio_venta: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    margen_ganancia_sugerido: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    cogs: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    precio_sugerido: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fecha_creacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    negocio: Mapped["Negocio"] = relationship("Negocio", back_populates="productos")
    propietario: Mapped["Usuario"] = relationship("Usuario", back_populates="productos")
    insumos_asociados: Mapped[List["ProductoInsumo"]] = relationship("ProductoInsumo", back_populates="producto", cascade="all, delete-orphan")
```

#### **Insumo**
```python
class Insumo(Base):
    __tablename__ = "insumos"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
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
```

### **Schemas Pydantic**

#### **Usuario Schemas**
```python
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
```

#### **Negocio Schemas**
```python
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
```

#### **Producto Schemas**
```python
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0)
    tipo_producto: ProductType
    negocio_id: uuid.UUID
    precio_venta: Optional[float] = Field(None, ge=0)
    margen_ganancia_sugerido: Optional[float] = Field(None, ge=0)

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
    precio_sugerido: Optional[float] = Field(None)
    cogs: Optional[float] = Field(None)
    margen_ganancia_real: Optional[float] = Field(None)
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    insumos_asociados: List["ProductoInsumoResponse"] = []
    model_config = ConfigDict(from_attributes=True)
```

#### **Insumo Schemas**
```python
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
```

### **Enums Python**
```python
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
```

---

## ⚛️ FRONTEND - React

### **Estructura de Componentes**

#### **Pantallas Principales**
- `LoginScreen` - Autenticación de usuarios
- `RegisterScreen` - Registro de usuarios
- `DashboardScreen` - Panel principal
- `ProfileScreen` - Gestión de perfil
- `ManageBusinessesScreen` - Gestión de negocios
- `CreateBusinessScreen` - Crear negocio
- `EditBusinessScreen` - Editar negocio
- `ManageProductsScreen` - Gestión de productos
- `CreateProductScreen` - Crear producto
- `EditProductScreen` - Editar producto
- `ManageInsumosScreen` - Gestión de insumos
- `CreateInsumoScreen` - Crear insumo
- `EditInsumoScreen` - Editar insumo
- `PublicListingScreen` - Listado público

#### **Componentes UI**
- `Button` - Botones reutilizables
- `Input` - Campos de entrada
- `Textarea` - Áreas de texto
- `Card` - Tarjetas contenedoras
- `Label` - Etiquetas de formulario

### **Contextos**
```javascript
// AuthContext - Gestión de autenticación
const AuthContext = createContext({
  isAuthenticated: false,
  user: null,
  login: () => {},
  logout: () => {},
  loading: true
});
```

### **Clientes API**
```javascript
// Configuración base
const API_BASE_URL = 'http://localhost:8000';

// Función auxiliar para manejar respuestas
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Error en la solicitud');
  }
  return response.json();
};

// Función para obtener token
const getAuthToken = () => {
  return localStorage.getItem('token');
};
```

---

## 🔐 AUTENTICACIÓN Y AUTORIZACIÓN

### **JWT Token Structure**
```python
# Payload del token
{
    "user_id": "uuid-del-usuario",
    "email": "usuario@email.com",
    "tipo_tier": "cliente|microemprendimiento|freelancer",
    "exp": timestamp_expiracion,
    "iat": timestamp_creacion
}
```

### **Dependencias FastAPI**
```python
# Obtener usuario actual
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = crud_user.get_user_by_id(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user
```

### **Headers de Autenticación**
```javascript
// En el frontend
headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
    'Accept': 'application/json'
}
```

---

## 🌐 ENDPOINTS API

### **Autenticación**
```
POST /users/register     - Registro de usuario
POST /users/login        - Login de usuario
GET  /profile/me         - Obtener perfil actual
```

### **Negocios**
```
GET    /businesses/me           - Obtener negocios del usuario
POST   /businesses/             - Crear negocio
GET    /businesses/{id}         - Obtener negocio específico
PUT    /businesses/{id}         - Actualizar negocio
DELETE /businesses/{id}         - Eliminar negocio
```

### **Productos**
```
GET    /products/me             - Obtener productos del usuario
POST   /products/               - Crear producto
GET    /products/{id}           - Obtener producto específico
PUT    /products/{id}           - Actualizar producto
DELETE /products/{id}           - Eliminar producto
```

### **Insumos**
```
GET    /insumos/me              - Obtener insumos del usuario
POST   /insumos/                - Crear insumo
GET    /insumos/{id}            - Obtener insumo específico
PUT    /insumos/{id}            - Actualizar insumo
DELETE /insumos/{id}            - Eliminar insumo
```

### **Endpoints Públicos**
```
GET /public/businesses          - Listado público de negocios
GET /public/products            - Listado público de productos
```

### **Códigos de Respuesta**
- `200 OK` - Operación exitosa
- `201 Created` - Recurso creado
- `400 Bad Request` - Datos inválidos
- `401 Unauthorized` - No autenticado
- `403 Forbidden` - No autorizado
- `404 Not Found` - Recurso no encontrado
- `422 Unprocessable Entity` - Validación fallida
- `500 Internal Server Error` - Error del servidor

---

## 📋 FUNCIONALIDADES IMPLEMENTADAS

### **Authentication**
- Jwt Implementation: ✅
- User Registration: ✅
- User Login: ✅
- Password Hashing: ✅

### **Business Management**
- Crud Operations: ✅
- User Association: ✅
- Business Types: ✅

### **Product Management**
- Crud Operations: ✅
- Business Association: ✅
- Insumo Association: ✅
- Price Calculations: ✅

### **Insumo Management**
- Crud Operations: ✅
- User Association: ✅
- Product Association: ✅

### **Public Access**
- Business Listing: ✅
- Product Listing: ✅
- No Auth Required: ❌

### **Frontend**
- Dashboard: ✅
- Navigation: ✅
- Forms: ✅
- Public Pages: ✅



### **Business Management**
- Crud Operations: ✅
- User Association: ✅
- Business Types: ✅

### **Product Management**
- Crud Operations: ✅
- Business Association: ✅
- Insumo Association: ✅
- Price Calculations: ✅

### **Insumo Management**
- Crud Operations: ✅
- User Association: ✅
- Product Association: ✅

### **Public Access**
- Business Listing: ✅
- Product Listing: ✅
- No Auth Required: ❌

### **Frontend**
- Dashboard: ✅
- Navigation: ✅
- Forms: ✅
- Public Pages: ✅



## 🔗 ENDPOINTS API

### **Autenticación**
- `POST /register` - Crear nuevo usuario
- `POST /login` - Crear token de autenticación

### **Usuarios**
- `GET /me` - Obtener datos de usuario
- `PUT /me` - Actualizar datos de usuario
- `PUT /me/cv` - Actualizar curriculum vitae

### **Negocios**
- `POST /` - Crear lista de negocios
- `GET /me` - Obtener datos de negocio
- `GET /{business_id}` - Obtener negocio específico
- `PUT /{business_id}` - Actualizar negocio específico
- `DELETE /{business_id}` - Eliminar negocio específico

### **Públicos**
- `GET /search` - Obtener información pública



### **Usuarios**
- `GET /me` - Obtener datos de usuario
- `PUT /me` - Actualizar datos de usuario
- `PUT /me/cv` - Actualizar curriculum vitae

### **Negocios**
- `POST /` - Crear lista de negocios
- `GET /me` - Obtener datos de negocio
- `GET /{business_id}` - Obtener negocio específico
- `PUT /{business_id}` - Actualizar negocio específico
- `DELETE /{business_id}` - Eliminar negocio específico

### **Públicos**
- `GET /search` - Obtener información pública



## 📚 DICCIONARIO DE REFERENCIA

### **Nombres de Campos - Backend**

#### **Usuario**
- `id` - UUID, primary key
- `email` - String, unique, required
- `nombre` - String, required
- `hashed_password` - String, required (NO `password_hash`)
- `is_active` - Boolean, default True
- `fecha_creacion` - DateTime, auto-generated
- `fecha_actualizacion` - DateTime, auto-updated
- `tipo_tier` - UserTier enum, default CLIENTE
- `localizacion` - String, optional
- `curriculum_vitae` - Text, optional

#### **Negocio**
- `id` - UUID, primary key
- `nombre` - String, required, indexed
- `descripcion` - Text, optional
- `propietario_id` - UUID, foreign key to usuarios.id (NO `usuario_id`)
- `tipo_negocio` - BusinessType enum, required
- `rubro` - String, optional
- `localizacion_geografica` - String, optional
- `fotos_urls` - List[str], stored as JSON string in DB
- `fecha_creacion` - DateTime, auto-generated
- `fecha_actualizacion` - DateTime, auto-updated

#### **Producto**
- `id` - UUID, primary key
- `nombre` - String, required, indexed
- `descripcion` - Text, optional
- `precio` - Float, required, > 0
- `tipo_producto` - ProductType enum, required
- `negocio_id` - UUID, foreign key to negocios.id
- `propietario_id` - UUID, foreign key to usuarios.id
- `precio_venta` - Float, optional, >= 0
- `margen_ganancia_sugerido` - Float, optional, >= 0
- `cogs` - Float, optional (Cost of Goods Sold)
- `precio_sugerido` - Float, optional
- `fecha_creacion` - DateTime, auto-generated
- `fecha_actualizacion` - DateTime, auto-updated

#### **Insumo**
- `id` - UUID, primary key
- `nombre` - String, required, indexed
- `cantidad_disponible` - Float, required, >= 0
- `unidad_medida_compra` - String, required
- `costo_unitario_compra` - Float, required, > 0
- `usuario_id` - UUID, foreign key to usuarios.id
- `fecha_creacion` - DateTime, auto-generated
- `fecha_actualizacion` - DateTime, auto-updated

### **Nombres de Funciones CRUD**

#### **Usuario**
- `create_user(db, user: UsuarioCreate) -> Usuario`
- `get_user_by_id(db, user_id: UUID) -> Optional[Usuario]`
- `get_user_by_email(db, email: str) -> Optional[Usuario]`
- `update_user(db, user_id: UUID, user_update: UsuarioUpdate) -> Optional[Usuario]`
- `delete_user(db, user_id: UUID) -> bool`

#### **Negocio**
- `create_business(db, user_id: UUID, business: NegocioCreate) -> Negocio`
- `get_business_by_id(db, business_id: UUID) -> Optional[Negocio]`
- `get_businesses_by_user_id(db, user_id: UUID) -> List[Negocio]`
- `get_all_businesses(db) -> List[Negocio]`
- `update_business(db, business_id: UUID, business_update: NegocioUpdate) -> Optional[Negocio]`
- `delete_business(db, business_id: UUID) -> bool`

#### **Producto**
- `create_product(db, user_id: UUID, product: ProductoCreate) -> Producto`
- `get_product_by_id(db, product_id: UUID) -> Optional[Producto]`
- `get_products_by_user_id(db, user_id: UUID) -> List[Producto]`
- `get_products_by_business_id(db, business_id: UUID) -> List[Producto]`
- `update_product(db, product_id: UUID, product_update: ProductoUpdate) -> Optional[Producto]`
- `delete_product(db, product_id: UUID) -> bool`

#### **Insumo**
- `create_insumo(db, user_id: UUID, insumo: InsumoCreate) -> Insumo`
- `get_insumo_by_id(db, insumo_id: UUID) -> Optional[Insumo]`
- `get_insumos_by_user_id(db, user_id: UUID) -> List[Insumo]`
- `update_insumo(db, insumo_id: UUID, insumo_update: InsumoUpdate) -> Optional[Insumo]`
- `delete_insumo(db, insumo_id: UUID) -> bool`

### **Parámetros de Ruta - Frontend**

#### **Rutas de Negocios**
- `/dashboard/businesses` - Lista de negocios
- `/dashboard/businesses/new` - Crear negocio
- `/dashboard/businesses/edit/:id` - Editar negocio (parámetro `id`)

#### **Rutas de Productos**
- `/dashboard/products` - Lista de productos
- `/dashboard/products/new` - Crear producto
- `/dashboard/products/edit/:productId` - Editar producto (parámetro `productId`)

#### **Rutas de Insumos**
- `/dashboard/insumos` - Lista de insumos
- `/dashboard/insumos/new` - Crear insumo
- `/dashboard/insumos/edit/:insumoId` - Editar insumo (parámetro `insumoId`)

### **Nombres de Variables - Frontend**

#### **Estados de Formulario**
```javascript
// Negocio
const [formData, setFormData] = useState({
  nombre: '',
  rubro: '',
  descripcion: '',
  localizacion_geografica: '',
  fotos_urls: ['']
});

// Producto
const [formData, setFormData] = useState({
  nombre: '',
  descripcion: '',
  precio: '',
  tipo_producto: '',
  negocio_id: '',
  precio_venta: '',
  margen_ganancia_sugerido: ''
});

// Insumo
const [formData, setFormData] = useState({
  nombre: '',
  cantidad_disponible: '',
  unidad_medida_compra: '',
  costo_unitario_compra: ''
});
```

#### **Funciones API**
```javascript
// Negocios
import { createBusiness, getMyBusinesses, getBusinessById, updateBusiness, deleteBusiness } from '../api/businessApi';

// Productos
import { createProduct, getMyProducts, getProductById, updateProduct, deleteProduct } from '../api/productApi';

// Insumos
import { createInsumo, getMyInsumos, getInsumoById, updateInsumo, deleteInsumo } from '../api/insumoApi';
```

---

## 📏 CONVENCIONES Y ESTÁNDARES

### **Nomenclatura**

#### **Backend**
- **Modelos:** PascalCase (Usuario, Negocio, Producto)
- **Schemas:** PascalCase con sufijo (UsuarioCreate, NegocioResponse)
- **Funciones:** snake_case (create_user, get_business_by_id)
- **Variables:** snake_case (user_id, business_name)
- **Constantes:** UPPER_SNAKE_CASE (SECRET_KEY, ALGORITHM)
- **Enums:** PascalCase (UserTier, BusinessType)

#### **Frontend**
- **Componentes:** PascalCase (LoginScreen, ManageBusinessesScreen)
- **Funciones:** camelCase (handleSubmit, fetchBusinesses)
- **Variables:** camelCase (formData, businessList)
- **Constantes:** UPPER_SNAKE_CASE (API_BASE_URL)

### **Estructura de Archivos**
```
backend/app/
├── models.py          # Todos los modelos SQLAlchemy
├── schemas.py         # Todos los schemas Pydantic
├── database.py        # Configuración de BD
├── dependencies.py    # Dependencias FastAPI
├── routers/           # Endpoints organizados por entidad
│   ├── auth.py        # Autenticación
│   ├── business.py    # Negocios
│   ├── product.py     # Productos
│   └── insumo.py      # Insumos
└── crud/              # Operaciones BD organizadas por entidad
    ├── user.py        # CRUD usuarios
    ├── business.py    # CRUD negocios
    ├── product.py     # CRUD productos
    └── insumo.py      # CRUD insumos
```

### **Validaciones**

#### **Campos Requeridos**
- `nombre` - String no vacío
- `email` - Formato de email válido
- `precio` - Float > 0
- `cantidad_disponible` - Float >= 0
- `costo_unitario_compra` - Float > 0

#### **Campos Opcionales**
- `descripcion` - String o null
- `rubro` - String o null
- `localizacion_geografica` - String o null
- `fotos_urls` - List[str] o null
- `precio_venta` - Float >= 0 o null
- `margen_ganancia_sugerido` - Float >= 0 o null

### **Manejo de Errores**

#### **Backend**
```python
# Errores HTTP estándar
HTTPException(status_code=404, detail="Recurso no encontrado")
HTTPException(status_code=401, detail="No autenticado")
HTTPException(status_code=403, detail="No autorizado")
HTTPException(status_code=422, detail="Datos inválidos")
```

#### **Frontend**
```javascript
// Manejo de errores en API calls
try {
  const data = await apiFunction();
  // Procesar respuesta exitosa
} catch (err) {
  console.error("Error:", err);
  setError(err.message || "Error desconocido");
}
```

### **Logs y Debugging**
```python
# Backend - Logs de debug
print(f"DEBUG: Recibiendo request para business_id: {business_id}")

# Frontend - Logs de debug
console.log("ID recibido:", id);
console.error("Error al cargar el negocio:", err);
```

---

## 🔄 MIGRACIONES Y ACTUALIZACIONES

### **Agregar Nuevos Campos**
1. **Crear migración SQL:**
```sql
ALTER TABLE tabla ADD COLUMN nuevo_campo TIPO;
```

2. **Actualizar modelo SQLAlchemy:**
```python
nuevo_campo: Mapped[Tipo] = mapped_column(Tipo, nullable=True)
```

3. **Actualizar schemas Pydantic:**
```python
nuevo_campo: Optional[Tipo] = None
```

4. **Actualizar CRUD si es necesario**

### **Agregar Nuevos Enums**
1. **Crear enum en BD:**
```sql
CREATE TYPE nuevo_enum AS ENUM ('valor1', 'valor2', 'valor3');
```

2. **Actualizar modelo:**
```python
nuevo_campo: Mapped[NuevoEnum] = mapped_column(Enum(NuevoEnum), nullable=False)
```

3. **Crear enum Python:**
```python
class NuevoEnum(str, enum.Enum):
    VALOR1 = "valor1"
    VALOR2 = "valor2"
    VALOR3 = "valor3"
```

---

## 🛣️ ROADMAP - Capítulo 1: Workflow Interno y Gestión de Ventas en Local (Panadería Ñiam)

**Prioridad:** ALTA  
**Fecha de Inicio Estimada:** Inmediato  
**Objetivo:** Implementar las funcionalidades clave para que un negocio físico (ej. Panadería Ñiam) pueda usar SOUP como su sistema principal de gestión de ventas en el local, inventario y producción, reemplazando a Excel.

---

### 💡 Visión General

"Panadería Ñiam", especializada en Chipá, busca integrar SOUP Market como su sistema de Punto de Venta (POS) interno para registrar transacciones, gestionar inventario en tiempo real y proporcionar análisis financiero. La venta en local físico es la prioridad, con pedidos online como un canal secundario, pero también gestionado por SOUP.

---

### 👥 Roles y Funcionalidades Clave

#### 1. 🗣️ Trabajador de Atención al Cliente (Usa SOUP Dashboard - Punto de Venta Principal)

**Funciones Prioritarias:**
* **Registro de Ventas en Local (SOUP: `ManageProductsScreen` / Nuevo Módulo POS - *Prioridad Alta*):**
    * **Pseudocódigo de Alto Nivel:**
        ```
        // Frontend: Pantalla de Venta en Local (POS)
        // Componente: SalePointScreen.js (NUEVO)
        // Ubicación: frontend/src/screens/SalePointScreen.js

        FUNCION renderSalePointScreen():
            ESTADO productosSeleccionados = []
            ESTADO totalVenta = 0

            FUNCION handleProductSelection(productoId, cantidad):
                // Lógica para añadir/actualizar producto en productosSeleccionados
                // Actualizar totalVenta
                LLAMAR updateProductInventory(productoId, -cantidad) // Descontar inmediatamente del inventario

            FUNCION handleCompleteSale():
                PARA CADA producto en productosSeleccionados:
                    LLAMAR backend.productApi.recordSale(producto.id, producto.cantidad, usuarioLogueado.id)
                MOSTRAR mensajeExito("Venta registrada y stock actualizado.")
                LIMPIAR productosSeleccionados, totalVenta

        // Backend: crud/product.py
        FUNCION record_sale(db: Session, product_id: UUID, quantity_sold: float, user_id: UUID):
            db_product = crud_product.get_product_by_id(db, product_id)
            SI NOT db_product ENTONCES ERROR "Producto no encontrado"
            SI db_product.propietario_id != user_id ENTONCES ERROR "No autorizado"

            // Descontar del inventario de productos terminados (campo futuro: stock_terminado)
            // Para este capítulo, la 'cantidad_disponible' de insumos se reducirá al vender el producto.
            // Se asume que el 'stock_terminado' se implementará en un capítulo posterior.

            // Registrar la venta (tabla futura: Ventas/Transacciones)
            // Esto impactará en ventas_completadas y total_ingresos

            // Actualizar insumos asociados al producto
            PARA CADA insumo_asociado en db_product.insumos_asociados:
                insumo = crud_insumo.get_insumo_by_id(db, insumo_asociado.insumo_id)
                SI insumo ENTONCES
                    insumo.cantidad_disponible -= insumo_asociado.cantidad_necesaria * quantity_sold
                    db.add(insumo) // Marcar para actualización

            db.commit()
            db.refresh(db_product)
        ```
    * **Integración al Código Existente (Capítulo 1 - Prioridad Alta):**
        * **Frontend:** Se creará una nueva pantalla `SalePointScreen.js` en `frontend/src/screens/`. Se integrará al `App.js` con una nueva ruta protegida (ej., `/dashboard/pos`).
        * **Backend:** La lógica de `record_sale` se integrará en `backend/app/crud/product.py` (o en un nuevo CRUD de `Transaccion` si se crea). La reducción de insumos se realizará en esta lógica. Se necesitará un nuevo endpoint en `backend/app/routers/product_router.py` (o un nuevo `sales_router.py`) para `POST /products/{product_id}/record_sale`.
* **Consulta de Inventario de Productos (SOUP: `ManageProductsScreen`):**
    * **Pseudocódigo de Alto Nivel:**
        ```
        // Frontend: ManageProductsScreen.js
        FUNCION fetchProducts():
            productos = LLAMAR productApi.getAllMyProducts()
            MOSTRAR productos.map(p => p.nombre, p.stock_terminado) // stock_terminado es un campo futuro
        ```
    * **Integración al Código Existente (Capítulo 1 - Prioridad Alta):**
        * **Frontend:** Ya existe `ManageProductsScreen.js`. Se actualizará para mostrar un campo `stock_terminado` (futuro).
        * **Backend:** El modelo `Producto` en `backend/app/models.py` necesitará un campo `stock_terminado: Mapped[Optional[float]] = mapped_column(Float, nullable=True)`. La lógica para actualizar este stock al producir o vender se añadiría en `crud/product.py`.
* **Recepción y Gestión de Pedidos Online (*Módulo Encargos - Funcionalidad Futura*):**
    * **Pseudocódigo de Alto Nivel:**
        ```
        // Frontend: ManageOrdersScreen.js (NUEVO - Capítulo posterior)
        FUNCION fetchOrders():
            pedidos = LLAMAR orderApi.getAllMyOrders()
            MOSTRAR pedidos.map(p => p.cliente, p.estado, p.productos)

        FUNCION updateOrderStatus(orderId, newStatus):
            LLAMAR orderApi.updateOrder(orderId, { estado: newStatus })
            MOSTRAR mensajeExito("Estado actualizado.")
        ```
    * **Integración al Código Existente:** Se dejará para un capítulo posterior. Implicaría nuevos modelos (`Pedido`, `ItemPedido`), esquemas, CRUDs y routers.

#### 2. 👨‍🍳 Cocinero / Productor de Insumos (Usa SOUP Dashboard)

**Funciones Prioritarias:**
* **Gestión de Insumos (SOUP: `ManageInsumosScreen`, `CreateInsumoScreen`, `EditInsumoScreen`):**
    * **Pseudocódigo de Alto Nivel:**
        ```
        // Frontend: ManageInsumosScreen.js
        FUNCION fetchInsumos():
            insumos = LLAMAR insumoApi.getAllMyInsumos()
            MOSTRAR insumos.map(i => i.nombre, i.cantidad_disponible, i.costo_unitario_compra)

        // Frontend: CreateInsumoScreen.js / EditInsumoScreen.js
        FUNCION handleSubmitCreateInsumo(formData):
            LLAMAR insumoApi.createInsumo(formData)
            MOSTRAR mensajeExito("Insumo creado.")

        FUNCION handleSubmitUpdateInsumo(insumoId, formData):
            LLAMAR insumoApi.updateInsumo(insumoId, formData)
            MOSTRAR mensajeExito("Insumo actualizado.")
        ```
    * **Integración al Código Existente:** Estas pantallas ya existen y funcionan. Solo se enfatizará su uso para el workflow.
* **Gestión de Productos (SOUP: `ManageProductsScreen`, `CreateProductScreen`, `EditProductScreen`):**
    * **Definir Recetas (Asociación Insumos):**
        * **Pseudocódigo de Alto Nivel:**
            ```
            // Frontend: CreateProductScreen.js / EditProductScreen.js
            FUNCION handleAddInsumoToProduct(insumoId, cantidadNecesaria):
                // Añadir a selectedInsumos

            FUNCION handleSubmitProduct(formData):
                // formData.insumos_asociados contiene [{insumo_id, cantidad_necesaria}]
                // LLAMAR productApi.createProduct(formData) o productApi.updateProduct(productId, formData)
            ```
        * **Integración al Código Existente:** Ya implementado en `CreateProductScreen.js` y `EditProductScreen.js`.
    * **Ver Costos de Producción (COGS):**
        * **Pseudocódigo de Alto Nivel:**
            ```
            // Frontend: CreateProductScreen.js / EditProductScreen.js
            // useEffect para recalcular COGS en frontend
            FUNCION calculateCogs(selectedInsumos, availableInsumos):
                totalCogs = 0
                PARA CADA item en selectedInsumos:
                    insumo = buscar insumo en availableInsumos por item.insumo_id
                    SI insumo ENTONCES
                        totalCogs += parseFloat(item.cantidad_necesaria) * insumo.costo_unitario_compra
                RETORNAR totalCogs

            // Backend: crud/product.py
            FUNCION _calculate_product_costs_and_prices(db, db_product):
                // Lógica de cálculo de total_cogs basada en db_product.insumos_asociados
                db_product.cogs = total_cogs
            ```
        * **Integración al Código Existente:** Ya implementado en backend (`crud/product.py`) y frontend (`CreateProductScreen.js`, `EditProductScreen.js`).
    * **Ajustar Precios y Márgenes:**
        * **Pseudocódigo de Alto Nivel:**
            ```
            // Frontend: CreateProductScreen.js / EditProductScreen.js
            // Campos de input para precio_venta y margen_ganancia_sugerido
            // useEffect para recalcular precio_sugerido y margen_ganancia_real en frontend
            FUNCION calculateSuggestedPrice(cogs, margen):
                SI cogs y margen ENTONCES
                    RETORNAR cogs * (1 + margen / 100)
                RETORNAR NULL

            FUNCION calculateRealMargin(cogs, precioVenta):
                SI cogs > 0 y precioVenta ENTONCES
                    RETORNAR ((precioVenta - cogs) / cogs) * 100
                RETORNAR NULL

            // Backend: crud/product.py y routers/product_router.py
            // Lógica de cálculo en _calculate_product_costs_and_prices y _calculate_margen_ganancia_real
            ```
        * **Integración al Código Existente:** Ya implementado en backend y frontend.

#### 3. 📊 Dueños / Managers (Usa SOUP Dashboard)

**Funciones Prioritarias:**
* **Visión General del Negocio (SOUP: `DashboardScreen`, `ManageBusinessesScreen`):**
    * **Pseudocódigo de Alto Nivel:**
        ```
        // Frontend: DashboardScreen.js
        FUNCION fetchDashboardData():
            usuario = LLAMAR authApi.getProfile()
            negocios = LLAMAR businessApi.getAllMyBusinesses()
            productos = LLAMAR productApi.getAllMyProducts()
            // Mostrar resumen de ventas_completadas, calificacion_promedio (futuro)
        ```
    * **Integración al Código Existente:** `DashboardScreen.js` y `ManageBusinessesScreen.js` ya existen. Se actualizarán para mostrar `ventas_completadas` y `calificacion_promedio` (futuras).
* **Gestión Financiera (*Módulo de Reportes - Funcionalidad Futura*):**
    * **Pseudocódigo de Alto Nivel:**
        ```
        // Frontend: ReportsScreen.js (NUEVO - Capítulo posterior)
        FUNCION fetchSalesReports(periodo):
            reporte = LLAMAR salesApi.getSalesReport(periodo) // Nueva API de reportes
            MOSTRAR reporte.ingresosTotales, reporte.egresosInsumos, reporte.margenNeto
        ```
    * **Integración al Código Existente:** Se dejará para un capítulo posterior. Implicaría nuevos modelos (`Transaccion`, `Reporte`), esquemas, CRUDs y routers.
* **Análisis de Rentabilidad:**
    * **Pseudocódigo de Alto Nivel:**
        ```
        // Frontend: ManageProductsScreen.js (para ver por producto)
        // O ReportsScreen.js (para ver agregados)
        FUNCION displayProfitability(product):
            MOSTRAR product.cogs, product.precio_venta, product.margen_ganancia_real
        ```
    * **Integración al Código Existente:** Ya visible en `EditProductScreen.js`. Se extenderá a `ManageProductsScreen.js` en un paso posterior de este capítulo.

#### 4. 🚶 Cliente (Interacción Principalmente Física / Opcional Online)

**Funciones Prioritarias:**
* **Compra en Local Físico:**
    * **Pseudocódigo de Alto Nivel:**
        ```
        // Proceso físico en el local, registrado por el Trabajador de Atención al Cliente en SOUP.
        // No hay interacción directa del cliente con SOUP en este punto para la venta física.
        ```
    * **Integración al Código Existente:** Se gestiona indirectamente a través del rol de Atención al Cliente.
* **Exploración de Productos Online (SOUP: `PublicListingScreen` y `PublicBusinessProductsScreen`):**
    * **Pseudocódigo de Alto Nivel:**
        ```
        // Frontend: PublicListingScreen.js
        FUNCION fetchPublicProducts():
            productos = LLAMAR publicApi.getPublicProducts()
            MOSTRAR productos.map(p => p.nombre, p.precio_venta, p.cogs, p.margen_ganancia_real)

        // Frontend: PublicBusinessProductsScreen.js
        FUNCION fetchPublicBusinessProducts(businessId):
            negocio = LLAMAR publicApi.getPublicBusinessById(businessId)
            productos = LLAMAR publicApi.getPublicProductsByBusinessId(businessId)
            MOSTRAR negocio.nombre, negocio.descripcion
            MOSTRAR productos.map(p => p.nombre, p.precio_venta, p.cogs, p.margen_ganancia_real)
        ```
    * **Integración al Código Existente:** Ya implementado en `PublicListingScreen.js` y `PublicBusinessProductsScreen.js`.

---

### 🚀 Próximos Pasos del Capítulo 1 (Prioridad Alta)

1. **Implementar la Pantalla de Punto de Venta (POS) en el Frontend:**
    * Crear `frontend/src/screens/SalePointScreen.js`.
    * Integrar la lógica para seleccionar productos, ajustar cantidades y registrar ventas.
    * Añadir la ruta en `frontend/src/App.js`.
2. **Añadir Campo `stock_terminado` al Modelo `Producto` en Backend:**
    * Modificar `backend/app/models.py`.
    * Crear migración para añadir este campo.
    * Actualizar `backend/app/schemas.py` y `backend/app/crud/product.py` para manejar este campo.
3. **Implementar Lógica de Descuento de Stock de Productos Terminados y de Insumos al Vender:**
    * Modificar `backend/app/crud/product.py` para que la función de registro de venta (o una nueva función) descuente `stock_terminado` del producto y `cantidad_disponible` de los insumos asociados.
4. **Actualizar `ManageProductsScreen.js` para mostrar `COGS`, `Precio Sugerido`, `Margen Real` y `stock_terminado`:**
    * Mejorar la visualización en la lista de productos del emprendedor.

---

### ⏭️ Funciones Avanzadas (Capítulos Posteriores)

Las siguientes funcionalidades son importantes pero se posponen para capítulos futuros del roadmap:

* **Módulo de Encargos/Pedidos Online Completo:**
    * Modelos, esquemas, CRUDs y routers para `Pedido` y `ItemPedido`.
    * Pantallas de `CreateOrderScreen`, `ManageOrdersScreen`, `OrderDetailsScreen`.
    * Notificaciones para clientes y atención al cliente.
* **Módulo de Reportes Financieros Avanzados:**
    * Generación de reportes de ingresos, egresos, rentabilidad por períodos.
    * Integración con datos de ventas y costos de insumos.
* **Sistema de Calificaciones y Reseñas:**
    * Modelos para `Calificacion` y `Reseña`.
    * Lógica para calcular `calificacion_promedio` y `total_calificaciones`.
    * Interfaz para clientes y visualización en productos/negocios.
* **Asistente de IA (Chatbot) Completo en Frontend:**
    * Implementación del componente de chatbot interactivo en `PublicListingScreen`.
    * Manejo de la interfaz de usuario para las recomendaciones de la IA.
* **Gestión de Usuarios y Roles (Administración):**
    * Interfaz para que los dueños/managers asignen roles a sus empleados.
* **Integración con Pasarelas de Pago:**
    * Manejo de pagos electrónicos para pedidos online.
* **Gestión de Cadetes/Logística:**
    * Asignación y seguimiento de envíos a domicilio.

---

## 📝 NOTAS IMPORTANTES

### **Puntos Críticos**
1. **Campo de contraseña:** Usar `hashed_password` (NO `password_hash`)
2. **Relaciones:** `propietario_id` en negocios, `usuario_id` en insumos
3. **Parámetros de ruta:** Mantener consistencia entre rutas y componentes
4. **Conversión JSON:** `fotos_urls` se almacena como JSON string en BD
5. **Validaciones:** Precio > 0, cantidades >= 0

### **Errores Comunes**
1. **Nombres de campos incorrectos** - Verificar diccionario de referencia
2. **Parámetros de ruta inconsistentes** - Revisar App.js y componentes
3. **Campos faltantes en modelos** - Sincronizar backend y frontend
4. **Conversión de tipos** - Manejar JSON strings correctamente
5. **Validaciones de esquema** - Usar Field() con restricciones apropiadas

### **Buenas Prácticas**
1. **Siempre validar datos** antes de guardar en BD
2. **Usar migraciones** para cambios estructurales
3. **Mantener consistencia** en nombres y tipos
4. **Documentar cambios** en este archivo
5. **Probar endpoints** después de modificaciones

---

Última actualización: 08 de July de 2025  
**Versión del documento:** 1.0  
**Mantenedor:** Asistente AI 

## Sistema de Recomendaciones Inteligente (Gemini)

### Descripción General
El sistema de recomendaciones utiliza un modelo LLM (Gemini) para sugerir productos y negocios relevantes a los usuarios, integrando información real de la base de datos pública. El flujo es robusto y seguro, garantizando que solo se recomienden elementos existentes.

### Flujo de funcionamiento
1. El usuario realiza una consulta desde el frontend (componente `AIRecommender.jsx`).
2. El frontend envía la consulta al endpoint backend `/public/ai/recommend`.
3. El backend extrae todos los productos públicos de la base de datos y construye un prompt que incluye la lista de productos y la consulta del usuario.
4. El prompt se envía a Gemini, que responde en formato JSON estructurado, usando únicamente los productos existentes.
5. El backend valida y convierte los IDs recibidos, consulta la base de datos y retorna los productos recomendados al frontend.
6. El frontend muestra el producto preferencial y otras recomendaciones, con botones de acceso directo.

### Endpoint
- **POST** `/public/ai/recommend`
- **Body:** `{ "query": "<consulta del usuario>" }`
- **Respuesta:**
  ```json
  {
    "producto_preferencial": { ... },
    "otras_recomendaciones": [ ... ]
  }
  ```

### Prompt utilizado para Gemini
El prompt incluye la lista de productos públicos y fuerza a Gemini a responder solo con IDs y nombres válidos:

```
Eres un asistente de recomendaciones para una app de productos y negocios. Solo puedes recomendar productos de la siguiente lista (usa exactamente los IDs y nombres que aparecen):
[ ...lista de productos... ]
Responde SOLO en JSON con el siguiente formato: { ... } No incluyas explicaciones ni texto fuera del JSON. La consulta del usuario es: <consulta>
```

### Consideraciones técnicas
- El backend valida que los IDs recibidos sean UUIDs válidos; si no, busca por nombre.
- El sistema es robusto ante respuestas en formato Markdown.
- El frontend está preparado para mostrar resultados aunque la respuesta sea vacía.

### Mejoras futuras sugeridas
- Incluir negocios en la lista de recomendaciones.
- Mejorar la visualización y personalización de la experiencia de usuario.
- Refinar la extracción de parámetros y el manejo de errores de Gemini. 

## [2025-07-09] Resolución de errores de integridad en productos

### Problemas detectados
- Errores 400 y 500 al crear productos debido a restricciones NOT NULL en la columna `fecha_actualizacion`.
- El valor por defecto definido en el modelo SQLAlchemy (`server_default=func.now()`) no se aplicaba correctamente al insertar desde la API.
- Migraciones previas para campos como `rating_promedio`, `reviews_count`, y eliminación de duplicidad de columnas (`usuario_id` vs `propietario_id`).

### Soluciones aplicadas
- Se creó una migración SQL para agregar valor por defecto a `fecha_actualizacion` y actualizar registros nulos.
- Se modificó el CRUD de productos para asignar explícitamente `fecha_actualizacion` con `datetime.utcnow()` al crear un producto.
- Se mejoró el manejo de errores en el CRUD para mostrar el error SQL exacto en caso de fallos de integridad.
- Se verificó la estructura de la tabla y se documentó el procedimiento de diagnóstico y solución.

### Resultado
- El test de creación de producto fue exitoso.
- La integridad de la base de datos está asegurada y la API responde correctamente.

### Archivos y scripts involucrados
- `backend/app/models.py` (modelo Producto)
- `backend/app/crud/product.py` (asignación explícita de fecha_actualizacion y manejo de errores)
- `debugging/migrations/fix_fecha_actualizacion_productos.sql` (migración SQL)
- Scripts de verificación y reparación en `debugging/scripts/`

### Recomendación
Siempre que se agregue un campo NOT NULL con valor por defecto en modelos SQLAlchemy, verificar que el ORM realmente lo asigne en la inserción, o hacerlo explícitamente en el CRUD. 

- Véase también: [Reporte de debugging: Resolución de errores de integridad en productos (2025-07-09)](../debugging/reportes/debugging_integridad_productos_20250709.md) 

---

## 📝 ACTUALIZACIONES RECIENTES (v1.1 - 9 de Julio de 2025)

### **Problemas Resueltos**

#### **1. Relaciones Ambiguas en SQLAlchemy**
- **Problema:** Múltiples relaciones entre `Usuario` y `Negocio` sin especificar `foreign_keys`
- **Solución:** Especificar explícitamente las claves foráneas en todas las relaciones
- **Impacto:** Backend ahora inicia correctamente, endpoints funcionan

#### **2. Columnas Faltantes en Tabla Usuarios**
- **Problema:** Modelo `Usuario` tenía campos nuevos que no existían en la BD
- **Solución:** Ejecutar migración para agregar columnas faltantes
- **Columnas agregadas:**
  - `plugins_activos` (TEXT[])
  - `rol` (VARCHAR(50))
  - `negocio_asignado_id` (UUID, FK)
  - `fecha_contratacion` (DATE)
  - `salario` (DECIMAL(10,2))
  - `horario_trabajo` (VARCHAR(100))
  - `permisos_especiales` (TEXT[])

#### **3. Error de Codificación en Configuración**
- **Problema:** Archivos de configuración con caracteres no válidos para UTF-8
- **Solución:** Modificar scripts para usar variables de entorno directamente

### **Estado Actual del Sistema**
- ✅ **Backend:** Funcionando correctamente
- ✅ **Frontend:** Funcionando correctamente
- ✅ **Base de Datos:** Sincronizada con modelos
- ✅ **Autenticación:** Funcionando correctamente
- ✅ **Endpoints públicos:** Funcionando correctamente
- ✅ **Sistema de plugins:** Implementado
- ✅ **Sistema POS mejorado:** Implementado
- ✅ **Optimización Panadería Ñiam:** Implementado

### **Funcionalidades Disponibles**
1. **Autenticación completa** (registro, login, logout)
2. **Gestión de usuarios** con roles y permisos
3. **Gestión de negocios** y productos
4. **Sistema de plugins** modular
5. **Sistema POS** con carrito, ventas y análisis
6. **Funcionalidades específicas para panadería**
7. **Listados públicos** de negocios y productos
8. **Dashboard** con métricas y análisis

### **Próximos Pasos Recomendados**
1. **Testing exhaustivo** de todas las funcionalidades
2. **Optimización de rendimiento** si es necesario
3. **Implementación de nuevas fases** del roadmap
4. **Documentación de APIs** con Swagger/OpenAPI
5. **Deployment en producción**

---

**Última actualización:** 9 de Julio de 2025  
**Versión del sistema:** 1.1  
**Estado:** ✅ FUNCIONANDO CORRECTAMENTE 