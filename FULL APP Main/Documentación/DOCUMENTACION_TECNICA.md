# DOCUMENTACIÓN TÉCNICA - SOUP Emprendimientos

**Versión:** 1.0  
**Fecha:** 7 de Julio de 2025  
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
7. [Diccionario de Referencia](#diccionario-de-referencia)
8. [Convenciones y Estándares](#convenciones-y-estándares)

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
    curriculum_vitae TEXT
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
    
    # Relaciones
    negocios: Mapped[List["Negocio"]] = relationship("Negocio", back_populates="propietario", cascade="all, delete-orphan")
    productos: Mapped[List["Producto"]] = relationship("Producto", back_populates="propietario", cascade="all, delete-orphan")
    insumos: Mapped[List["Insumo"]] = relationship("Insumo", back_populates="usuario", cascade="all, delete-orphan")
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