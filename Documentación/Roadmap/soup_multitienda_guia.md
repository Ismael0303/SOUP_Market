# 🏪 SOUP Multitienda: Guía de Implementación

## Índice

1. [¿Qué es “Multitienda”?](#qué-es-multitienda)
2. [Resumen de la Arquitectura](#resumen-de-la-arquitectura)
3. [Modelo de Datos: Cómo estructurar las tiendas](#modelo-de-datos-cómo-estructurar-las-tiendas)
4. [Middleware: Detección automática de la tienda](#middleware-detección-automática-de-la-tienda)
5. [Rutas y Queries: Aislamiento de datos por tienda](#rutas-y-queries-aislamiento-de-datos-por-tienda)
6. [Autenticación y Roles Multi-Tienda](#autenticación-y-roles-multi-tienda)
7. [Personalización por tienda (branding, settings, etc.)](#personalización-por-tienda-branding-settings-etc)
8. [Tips y buenas prácticas](#tips-y-buenas-prácticas)
9. [Recursos útiles](#recursos-útiles)

---

## 1. ¿Qué es “Multitienda”?

El concepto **multi-tenant** (multitienda/multisucursal/multimarca) significa que tu app permite a *varios grupos independientes de usuarios* tener **su propia tienda, productos y administración**, todo sobre la misma plataforma, pero aislados unos de otros.

Ejemplos:

- Shopify: cada “tienda” es independiente, aunque todas usan el mismo sistema.
- MercadoShops, Tiendanube, etc.

---

## 2. Resumen de la Arquitectura

- Cada tienda tiene su propia configuración, branding, productos, usuarios y ventas.
- Los datos de cada tienda NO deben mezclarse.
- Se pueden distinguir tiendas por subdominio, dominio o parámetro.
- Los usuarios y admins pueden estar asociados a una o varias tiendas.

---

## 3. Modelo de Datos: Cómo estructurar las tiendas

Crea el modelo `Tienda` y enlaza todo lo que deba ser “por tienda” (usuarios, productos, ventas, etc):

```python
# models/tienda.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class Tienda(Base):
    __tablename__ = "tiendas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    dominio = Column(String, unique=True, index=True)
    logo_url = Column(String, nullable=True)
    # Otros campos de configuración
```

Ahora, en tus otros modelos (negocios, productos, ventas, etc):

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    tienda_id = Column(Integer, ForeignKey("tiendas.id"))
    tienda = relationship("Tienda", back_populates="productos")
    # Otros campos

Tienda.productos = relationship("Producto", back_populates="tienda")
```

Haz lo mismo con usuarios, ventas, etc.

---

## 4. Middleware: Detección automática de la tienda

El middleware te permite detectar la tienda automáticamente según el dominio/subdominio:

```python
from starlette.middleware.base import BaseHTTPMiddleware

class MultiTiendaMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        host = request.headers.get("host", "")
        subdominio = host.split(".")[0]
        # Consulta la tienda por subdominio (o dominio) en la BD
        # tienda = db.query(Tienda).filter_by(dominio=subdominio).first()
        request.state.tienda_actual = subdominio  # O instancia real
        return await call_next(request)

# Añade el middleware a la app
app.add_middleware(MultiTiendaMiddleware)
```

En tus endpoints, accede así:

```python
def obtener_productos(request: Request, db: Session = Depends(get_db)):
    tienda = request.state.tienda_actual
    return db.query(Producto).filter(Producto.tienda_id == tienda.id).all()
```

---

## 5. Rutas y Queries: Aislamiento de datos por tienda

Siempre filtra los datos por `tienda_id` en tus consultas, y asegúrate de que las acciones de creación, edición y eliminación también estén asociadas a la tienda correspondiente.

---

## 6. Autenticación y Roles Multi-Tienda

### ¿Cómo restringir usuarios a su tienda?

- **Asocia cada usuario a una tienda** mediante un campo `tienda_id` en tu modelo de usuario, o una tabla intermedia para permitir usuarios en varias tiendas.
- En tu middleware/auth, **valida que el usuario sólo vea/administre su tienda**.

Ejemplo simple:

```python
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    tienda_id = Column(Integer, ForeignKey("tiendas.id"))
    # ... otros campos

# En endpoints protegidos
def perfil_usuario(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request)  # Tu método habitual de auth
    tienda = request.state.tienda_actual
    if user.tienda_id != tienda.id:
        raise HTTPException(status_code=403, detail="No autorizado para esta tienda")
```

**Roles**: Añade un campo “rol” (admin, staff, vendedor, etc.) y controla permisos según el rol y la tienda.

---

## 7. Personalización por tienda (branding, settings, etc.)

Guarda los parámetros visuales y configuraciones en el modelo `Tienda`:

```python
class Tienda(Base):
    # ...
    logo_url = Column(String)
    color_primario = Column(String)
    mensaje_bienvenida = Column(String)
    # etc
```

En el frontend, cuando se detecta la tienda (por subdominio/dominio), pide estos datos al backend y adapta el branding dinámicamente.

---

## 8. Tips y buenas prácticas

- Usa SIEMPRE el filtro `tienda_id` en tus queries para evitar fugas de datos.
- Si tu app crece, podrías separar la BD por tienda (pero solo si realmente lo necesitas, añade complejidad).
- Ofrece dominios personalizados para tiendas premium.
- Valida bien la autenticación para que ningún usuario administre datos ajenos.

---

## 9. Recursos útiles

- [FastAPI docs](https://fastapi.tiangolo.com/)
- [Starlette middleware](https://www.starlette.io/middleware/)
- [Ejemplo multi-tenant en SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/examples.html#horizontal-sharding)
- [Arquitectura multi-tenant SaaS (artículo)](https://martinfowler.com/bliki/MultiTenant.html)

---

¿Listo para escalar SOUP?\
Si quieres ejemplos más avanzados, código de auth, o cómo estructurar el frontend react para branding dinámico, pídelo y lo armo en detalle.

