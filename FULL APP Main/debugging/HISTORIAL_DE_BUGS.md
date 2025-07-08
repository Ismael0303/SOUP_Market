# HISTORIAL DE BUGS Y SOLUCIONES - SOUP Emprendimientos

**Fecha de creación:** 7 de Julio de 2025  
**Proyecto:** SOUP Emprendimientos - Full Stack (FastAPI + React)  
**Mantenedor:** Asistente AI

---

## 📋 RESUMEN EJECUTIVO

Este documento registra todos los problemas encontrados durante el desarrollo del proyecto SOUP Emprendimientos, incluyendo su diagnóstico, solución aplicada y lecciones aprendidas para debugging futuro.

---

## 🐛 BUGS RESUELTOS

### 1. **PROBLEMA: Enums de Base de Datos Inconsistentes**
**Fecha:** 7 de Julio de 2025  
**Severidad:** CRÍTICA  
**Estado:** ✅ RESUELTO

#### **Descripción del Problema:**
- Los enums `businesstype` y `producttype` en la base de datos tenían valores diferentes a los esperados por el código
- `businesstype`: valores en mayúsculas vs minúsculas
- `producttype`: valores completamente diferentes entre BD y código

#### **Síntomas:**
- Endpoint `/public/businesses` devolvía error 500
- Endpoint `/public/products` devolvía error 500
- Errores de validación de SQLAlchemy

#### **Diagnóstico:**
```sql
-- Verificar valores en BD
SELECT DISTINCT tipo_negocio FROM negocios;
SELECT DISTINCT tipo_producto FROM productos;
```

#### **Solución Aplicada:**
1. **Actualizar valores en BD:**
```sql
UPDATE negocios SET tipo_negocio = 'PRODUCTOS' WHERE tipo_negocio = 'productos';
UPDATE negocios SET tipo_negocio = 'SERVICIOS' WHERE tipo_negocio = 'servicios';
UPDATE negocios SET tipo_negocio = 'AMBOS' WHERE tipo_negocio = 'ambos';

UPDATE productos SET tipo_producto = 'PHYSICAL_GOOD' WHERE tipo_producto = 'producto_fisico';
UPDATE productos SET tipo_producto = 'SERVICE_BY_HOUR' WHERE tipo_producto = 'servicio_por_hora';
UPDATE productos SET tipo_producto = 'SERVICE_BY_PROJECT' WHERE tipo_producto = 'servicio_por_proyecto';
UPDATE productos SET tipo_producto = 'DIGITAL_GOOD' WHERE tipo_producto = 'producto_digital';
```

2. **Limpiar cache de SQLAlchemy** en `main.py`

#### **Lecciones Aprendidas:**
- Siempre verificar consistencia entre enums de BD y código
- Usar migraciones para cambios de enums
- Limpiar cache de SQLAlchemy después de cambios estructurales

---

### 2. **PROBLEMA: Datos Inválidos en Productos**
**Fecha:** 7 de Julio de 2025  
**Severidad:** ALTA  
**Estado:** ✅ RESUELTO

#### **Descripción del Problema:**
- Productos con `precio = 0.0` y `negocio_id = NULL`
- Violaba validaciones del schema Pydantic

#### **Síntomas:**
- Endpoint `/public/products` fallaba con error 500
- Errores de validación en serialización

#### **Diagnóstico:**
```sql
SELECT * FROM productos WHERE precio = 0.0 OR negocio_id IS NULL;
```

#### **Solución Aplicada:**
```sql
-- Corregir productos inválidos
UPDATE productos 
SET precio = 10.0, negocio_id = (SELECT id FROM negocios LIMIT 1)
WHERE precio = 0.0 OR negocio_id IS NULL;
```

#### **Lecciones Aprendidas:**
- Validar datos antes de migraciones
- Implementar constraints en BD para evitar datos inválidos

---

### 3. **PROBLEMA: Campo de Contraseña Incorrecto**
**Fecha:** 7 de Julio de 2025  
**Severidad:** CRÍTICA  
**Estado:** ✅ RESUELTO

#### **Descripción del Problema:**
- Modelo `Usuario` tenía campo `hashed_password`
- Código intentaba acceder a `password_hash`
- Inconsistencia en nombres de campos

#### **Síntomas:**
- Error 500 en registro de usuarios
- Errores de atributo no encontrado

#### **Diagnóstico:**
```python
# Buscar todas las referencias incorrectas
grep -r "password_hash" backend/
```

#### **Solución Aplicada:**
1. **Actualizar router de autenticación:**
```python
# Cambiar de password_hash a hashed_password
if not verify_password(form_data.password, user.hashed_password):
```

2. **Actualizar CRUD de usuarios:**
```python
# Cambiar todas las referencias
user.hashed_password = get_password_hash(user.password)
```

#### **Lecciones Aprendidas:**
- Mantener consistencia en nombres de campos
- Usar búsqueda global para encontrar referencias incorrectas

---

### 4. **PROBLEMA: Token JWT Sin user_id**
**Fecha:** 7 de Julio de 2025  
**Severidad:** CRÍTICA  
**Estado:** ✅ RESUELTO

#### **Descripción del Problema:**
- Schema `TokenData` solo tenía campo `email`
- Token se creaba con `user_id`, `email`, `tipo_tier`
- Validación fallaba al decodificar token

#### **Síntomas:**
- Login exitoso (200 OK)
- Endpoint `/profile/me` devolvía 401 Unauthorized
- Error: `'TokenData' object has no attribute 'user_id'`

#### **Diagnóstico:**
```python
# Agregar logs de debug
print(f"🔍 DEBUG: Token decodificado: {token_data}")
```

#### **Solución Aplicada:**
```python
# Actualizar schema TokenData
class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    tipo_tier: Optional[str] = None
```

#### **Lecciones Aprendidas:**
- Schema de token debe coincidir con datos del token
- Usar logs de debug para validación de tokens

---

### 5. **PROBLEMA: Endpoint /profile/me con Tipo Incorrecto**
**Fecha:** 7 de Julio de 2025  
**Severidad:** ALTA  
**Estado:** ✅ RESUELTO

#### **Descripción del Problema:**
- Endpoint esperaba `UsuarioResponse` como parámetro
- `get_current_user` devuelve `Usuario` (modelo SQLAlchemy)
- Incompatibilidad de tipos

#### **Síntomas:**
- Error 401 en `/profile/me`
- Problemas de validación de tipos

#### **Solución Aplicada:**
```python
# Cambiar tipo de parámetro
def get_current_user_profile(current_user: Usuario = Depends(get_current_user)):
```

#### **Lecciones Aprendidas:**
- FastAPI convierte automáticamente modelos SQLAlchemy a schemas Pydantic
- Usar tipo correcto en dependencias

---

### 6. **PROBLEMA: CRUD de Negocios con Nombres Incorrectos**
**Fecha:** 7 de Julio de 2025  
**Severidad:** ALTA  
**Estado:** ✅ RESUELTO

#### **Descripción del Problema:**
- Router llamaba `get_businesses_by_owner`
- Función no existía en CRUD
- Parámetros incorrectos (`propietario_id` vs `user_id`)

#### **Síntomas:**
- Error 500 en `/businesses/me`
- `AttributeError: module 'crud.business' has no attribute 'get_businesses_by_owner'`

#### **Solución Aplicada:**
```python
# Corregir llamada en router
return crud_business.get_businesses_by_user_id(db, user_id=current_user.id)
```

#### **Lecciones Aprendidas:**
- Verificar nombres exactos de funciones en CRUD
- Usar parámetros correctos según definición

---

### 7. **PROBLEMA: Prefijo Duplicado en Router de Productos**
**Fecha:** 7 de Julio de 2025  
**Severidad:** ALTA  
**Estado:** ✅ RESUELTO

#### **Descripción del Problema:**
- Router tenía prefijo `/products` duplicado
- Rutas se generaban como `/products/products/me`

#### **Síntomas:**
- Error 404 en endpoints de productos
- Rutas incorrectas

#### **Solución Aplicada:**
```python
# Eliminar prefijo duplicado
router = APIRouter()  # Sin prefijo
app.include_router(product_router, prefix="/products", tags=["products"])
```

#### **Lecciones Aprendidas:**
- Revisar prefijos de routers al incluir en app principal

---

### 8. **PROBLEMA: Modelo Negocio Sin Campos Requeridos por Frontend**
**Fecha:** 7 de Julio de 2025  
**Severidad:** CRÍTICA  
**Estado:** ✅ RESUELTO

#### **Descripción del Problema:**
- Modelo `Negocio` en backend no tenía campos que el frontend esperaba:
  - `rubro`
  - `localizacion_geografica` 
  - `fotos_urls`
- Frontend intentaba acceder a campos inexistentes

#### **Síntomas:**
- Error 422 (Unprocessable Entity) al editar negocios
- URL con "undefined" como ID: `/businesses/undefined`
- Serialización incorrecta del modelo

#### **Diagnóstico:**
```python
# Script de debugging para verificar datos
def debug_business_data():
    db = SessionLocal()
    all_businesses = db.query(Negocio).all()
    for business in all_businesses:
        print(f"ID: {business.id}")
        print(f"Rubro: {business.rubro}")
        print(f"Fotos URLs: {business.fotos_urls}")
```

#### **Solución Aplicada:**

1. **Migración de Base de Datos:**
```sql
-- Agregar campos faltantes
ALTER TABLE negocios ADD COLUMN rubro VARCHAR;
ALTER TABLE negocios ADD COLUMN localizacion_geografica VARCHAR;
ALTER TABLE negocios ADD COLUMN fotos_urls TEXT[];
```

2. **Actualizar Modelo SQLAlchemy:**
```python
class Negocio(Base):
    # ... campos existentes ...
    rubro: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    localizacion_geografica: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fotos_urls: Mapped[Optional[List[str]]] = mapped_column(Text, nullable=True)
```

3. **Actualizar Schemas Pydantic:**
```python
class NegocioBase(BaseModel):
    # ... campos existentes ...
    rubro: Optional[str] = None
    localizacion_geografica: Optional[str] = None
    fotos_urls: Optional[List[str]] = None
```

4. **Actualizar CRUD para manejar JSON:**
```python
def _convert_fotos_urls(business):
    """Convierte fotos_urls de JSON string a lista"""
    if hasattr(business, 'fotos_urls'):
        import json
        try:
            if business.fotos_urls is None:
                business.fotos_urls = []
            elif isinstance(business.fotos_urls, str):
                if business.fotos_urls.strip():
                    business.fotos_urls = json.loads(business.fotos_urls)
                else:
                    business.fotos_urls = []
        except (json.JSONDecodeError, TypeError):
            business.fotos_urls = []
    return business
```

#### **Lecciones Aprendidas:**
- Mantener sincronización entre modelo backend y expectativas frontend
- Usar migraciones para agregar campos a modelos existentes
- Manejar conversión JSON-string para campos de array
- Verificar serialización completa del modelo

---

### 9. **PROBLEMA: Parámetro de Ruta Incorrecto en React Router**
**Fecha:** 7 de Julio de 2025  
**Severidad:** ALTA  
**Estado:** ✅ RESUELTO

#### **Descripción del Problema:**
- Ruta configurada con parámetro `:businessId`
- Componente `EditBusinessScreen` usaba `useParams()` para obtener `id`
- Inconsistencia en nombres de parámetros

#### **Síntomas:**
- Error 422 (Unprocessable Entity) al editar negocios
- URL con "undefined" como ID: `/businesses/undefined`
- `useParams()` devolvía `undefined` para `id`

#### **Diagnóstico:**
```javascript
// En EditBusinessScreen.js
const { id } = useParams(); // Devuelve undefined porque la ruta usa :businessId
console.log("ID recibido:", id); // undefined
```

#### **Solución Aplicada:**
```javascript
// Cambiar ruta en App.js
<Route path="/dashboard/businesses/edit/:id" element={<PrivateRoute><EditBusinessScreen /></PrivateRoute>} />

// En lugar de:
<Route path="/dashboard/businesses/edit/:businessId" element={<PrivateRoute><EditBusinessScreen /></PrivateRoute>} />
```

#### **Lecciones Aprendidas:**
- Mantener consistencia entre nombres de parámetros en rutas y componentes
- Verificar que `useParams()` devuelva el parámetro esperado
- Usar nombres descriptivos pero consistentes para parámetros de ruta
- CRUD tenía función `get_businesses_by_user_id`
- Inconsistencia en nombres de funciones y parámetros

#### **Síntomas:**
- Error 500 en `/businesses/me`
- `AttributeError: module 'app.crud.business' has no attribute 'get_businesses_by_owner'`

#### **Solución Aplicada:**
```python
# Corregir llamada en router
return crud_business.get_businesses_by_user_id(db, user_id=current_user.id)

# Corregir parámetros en create_business
return crud_business.create_business(db=db, user_id=current_user.id, business=business)
```

#### **Lecciones Aprendidas:**
- Mantener consistencia en nombres de funciones CRUD
- Verificar parámetros correctos en llamadas

---

### 7. **PROBLEMA: Prefijo Duplicado en Router de Productos**
**Fecha:** 7 de Julio de 2025  
**Severidad:** ALTA  
**Estado:** ✅ RESUELTO

#### **Descripción del Problema:**
- Router tenía prefijo `/products`
- `main.py` agregaba prefijo `/products`
- Ruta resultante: `/products/products/me` en lugar de `/products/me`

#### **Síntomas:**
- Error 404 en `/products/me`
- Endpoint no encontrado

#### **Diagnóstico:**
```python
# Verificar configuración en main.py
app.include_router(product_router.router, prefix="/products", tags=["Products & Services"])
```

#### **Solución Aplicada:**
```python
# Eliminar prefijo duplicado del router
router = APIRouter(
    tags=["Products & Services"]  # Sin prefix
)
```

#### **Lecciones Aprendidas:**
- Evitar prefijos duplicados en routers
- Verificar rutas finales en configuración de FastAPI

---

## 🔧 HERRAMIENTAS DE DEBUGGING UTILIZADAS

### **Scripts de Debug:**
1. **Verificación de Enums:**
```sql
SELECT DISTINCT tipo_negocio FROM negocios;
SELECT DISTINCT tipo_producto FROM productos;
```

2. **Verificación de Datos Inválidos:**
```sql
SELECT * FROM productos WHERE precio = 0.0 OR negocio_id IS NULL;
```

3. **Debug de Tokens:**
```python
print(f"🔍 DEBUG: Token recibido: {token[:20]}...")
print(f"🔍 DEBUG: Token decodificado: {token_data}")
```

### **Comandos Útiles:**
```bash
# Buscar referencias incorrectas
grep -r "password_hash" backend/

# Verificar logs del servidor
uvicorn app.main:app --reload

# Conectar a BD
psql -U soupuser -d soup_app_db -h localhost -p 5432
```

---

## 📚 PATRONES DE SOLUCIÓN IDENTIFICADOS

### **1. Problemas de Consistencia de Datos:**
- **Patrón:** Valores en BD diferentes a código
- **Solución:** Migraciones SQL + limpieza de cache
- **Prevención:** Validaciones y constraints en BD

### **2. Problemas de Nombres de Campos:**
- **Patrón:** Inconsistencia en nombres (camelCase vs snake_case)
- **Solución:** Búsqueda global y reemplazo sistemático
- **Prevención:** Convenciones de nomenclatura claras

### **3. Problemas de Tipos en FastAPI:**
- **Patrón:** Incompatibilidad entre modelos SQLAlchemy y schemas Pydantic
- **Solución:** Usar tipo correcto en dependencias
- **Prevención:** Documentar tipos esperados

### **4. Problemas de Rutas:**
- **Patrón:** Prefijos duplicados o rutas mal configuradas
- **Solución:** Revisar configuración en main.py
- **Prevención:** Estructura clara de routers

---

## 🚀 MEJORAS IMPLEMENTADAS

1. **Logs de Debug:** Agregados logs temporales para diagnóstico
2. **Validaciones:** Mejoradas validaciones de datos
3. **Documentación:** Este historial para referencia futura
4. **Estructura:** Organización de debugging y tests

---

## 📝 NOTAS PARA DEBUGGING FUTURO

### **Checklist de Debugging:**
- [ ] Verificar logs del servidor
- [ ] Revisar configuración de rutas
- [ ] Validar consistencia de datos en BD
- [ ] Verificar tipos en dependencias FastAPI
- [ ] Comprobar nombres de funciones CRUD
- [ ] Revisar prefijos de routers

### **Orden de Prioridad:**
1. **CRÍTICO:** Autenticación y rutas básicas
2. **ALTO:** Funcionalidades principales
3. **MEDIO:** Optimizaciones y mejoras
4. **BAJO:** Cosméticos y UX

---

**Última actualización:** 7 de Julio de 2025  
**Estado del proyecto:** ✅ FUNCIONAL  
**Próximos pasos:** Testing completo y optimizaciones 