# 🗺️ ROADMAP DEFINITIVO DE SOUP MARKET (MVP)

> **ACTUALIZACIÓN IMPORTANTE (Agosto 2025):**
> 
> Se ha decidido migrar la lógica de marketplace y gestión de productos/negocios a Shuup (ERP open source). El backend FastAPI actuará como gateway/orquestador y el frontend React se adaptará para consumir los nuevos endpoints. Esto implica cambios en la arquitectura, mapeo de modelos y migración de datos. Ver detalles en `Documentación/Migracion Shuup/`.
> 
> **Implicancias:**
> - Varias funcionalidades de backend (CRUD de productos, negocios, encargos, reviews, etc.) pasarán a gestionarse vía la API de Shuup.
> - El sistema de autenticación y lógica de insumos/productos propios de SOUP se mantendrá solo donde Shuup no cubra la funcionalidad.
> - El cronograma y los capítulos de este roadmap han sido adaptados para reflejar la nueva arquitectura.

---

## OBJETIVOS OBSOLETOS Y SUSTITUCIONES POR MIGRACIÓN A SHUUP

| Objetivo/Tarea Obsoleta (SOUP Nativo) | Nuevo Objetivo (Con Shuup) |
|---------------------------------------|----------------------------|
| Modelos y migraciones de BD para: Producto, Negocio, Encargo, Review, Publicidad, etc. | Mapeo y migración de datos a modelos equivalentes de Shuup. |
| CRUD de productos, negocios, encargos, reviews, publicidad en FastAPI | Integración de FastAPI como gateway a la API de Shuup para estas entidades. |
| Routers y lógica de negocio propia para marketplace en FastAPI | Adaptación de endpoints FastAPI para orquestar y transformar datos entre frontend y Shuup. |
| Migraciones y scripts de actualización de BD para entidades marketplace | Scripts de migración de datos y sincronización con Shuup. |
| Implementación de lógica de marketplace (stock, ventas, pedidos, reviews, etc.) en SOUP | Uso de lógica y flujos nativos de Shuup para marketplace, ventas, pedidos, reviews, etc. |
| Desarrollo de paneles de administración propios para marketplace | Adaptación de UI/UX para consumir y mostrar datos provenientes de Shuup. |
| Pruebas unitarias/integración de lógica CRUD marketplace en SOUP | Pruebas de integración y validación de la comunicación FastAPI ↔ Shuup ↔ Frontend. |

> **Nota:** La gestión de insumos, recetas y lógica específica de panadería se mantiene en SOUP si Shuup no cubre esa funcionalidad.

---

## 📋 ÍNDICE

1. [Funcionalidades Completadas a la Fecha](#1-funcionalidades-completadas-a-la-fecha)
2. [Arquitectura de Software Ya Implementada](#2-arquitectura-de-software-ya-implementada)
3. [Nuevas Funcionalidades a Implementar (Por Capítulos)](#3-nuevas-funcionalidades-a-implementar-por-capítulos)
4. [Arquitectura General del MVP Completo](#4-arquitectura-general-del-mvp-completo)
5. [Cronograma de Desarrollo](#5-cronograma-de-desarrollo)

---

## 1. FUNCIONALIDADES COMPLETADAS A LA FECHA

Hemos establecido una base sólida para la aplicación, cubriendo la gestión esencial para usuarios y emprendedores, y un listado público.

### **Capítulo 1: Gestión de Usuarios y Negocios**

#### **Backend:**
- ✅ Modelos Usuario y Negocio
- ✅ Esquemas Pydantic para registro, login, perfil y CRUD de negocios
- ✅ Lógica CRUD para usuarios y negocios
- ✅ Routers para autenticación, perfil de usuario y negocios

#### **Frontend:**
- ✅ Pantallas: LoginScreen, RegisterScreen, DashboardScreen, ProfileScreen
- ✅ Pantallas: ManageBusinessesScreen, CreateBusinessScreen, EditBusinessScreen
- ✅ Integración con API de autenticación y negocios

#### **Funcionalidad:**
- ✅ Registro y login de usuarios
- ✅ Edición de perfil
- ✅ Creación, listado, edición y eliminación de negocios por parte de usuarios microemprendimiento o freelancer

### **Capítulo 2: Gestión de Productos y Servicios**

#### **Backend:**
- ✅ Modelo Producto
- ✅ Esquemas Pydantic para CRUD de productos
- ✅ Lógica CRUD para productos (incluyendo asociación opcional a Negocio)
- ✅ Router para productos

#### **Frontend:**
- ✅ Pantallas: ManageProductsScreen, CreateProductScreen, EditProductScreen
- ✅ Integración con API de productos
- ✅ Selección de tipo de producto y asociación a negocio

#### **Funcionalidad:**
- ✅ Creación, listado, edición y eliminación de productos/servicios por parte de usuarios microemprendimiento o freelancer

### **Capítulo 3: Listado Público y Búsqueda Básica**

#### **Backend:**
- ✅ Esquema UserPublicResponse
- ✅ Funciones CRUD para obtener todos los negocios y productos
- ✅ Router público (/public) para exponer negocios, productos y perfiles de usuario sin autenticación

#### **Frontend:**
- ✅ PublicListingScreen como página de inicio (/)
- ✅ Consumo de APIs públicas para mostrar listados de negocios y productos
- ✅ Botones de login/registro en la página pública

#### **Funcionalidad:**
- ✅ Acceso público a un listado de todos los negocios y productos
- ✅ Visualización de perfiles de usuario públicos (información no sensible)

---

## 2. ARQUITECTURA DE SOFTWARE YA IMPLEMENTADA

La arquitectura actual está diseñada para ser modular, escalable y mantenible, siguiendo las mejores prácticas para aplicaciones web modernas.

### **Backend (FastAPI - Python):**

#### **Tecnologías:**
- ✅ **Framework:** FastAPI (asíncrono, alto rendimiento)
- ✅ **Base de Datos:** PostgreSQL
- ✅ **ORM:** SQLAlchemy (declarative models)
- ✅ **Validación/Serialización:** Pydantic (para esquemas de datos)
- ✅ **Autenticación:** JWT (JSON Web Tokens) gestionado con python-jose y passlib

#### **Estructura de Archivos:**
```
backend/app/
├── main.py              # Punto de entrada, configuración CORS, inclusión de routers
├── database.py          # Configuración de conexión a BD y sesión
├── models.py            # Definición de modelos de BD (tablas)
├── schemas.py           # Esquemas de validación y respuesta (Pydantic)
├── dependencies.py      # Funciones de inyección de dependencias
├── crud/                # Lógica CRUD por entidad
│   ├── user.py
│   ├── business.py
│   └── product.py
└── routers/             # Endpoints API por sección
    ├── auth_router.py
    ├── user_router.py
    ├── business_router.py
    ├── product_router.py
    └── public_router.py
```

### **Frontend (React - JavaScript):**

#### **Tecnologías:**
- ✅ **Framework:** React.js
- ✅ **Routing:** React Router DOM
- ✅ **Estilos:** Tailwind CSS + Shadcn UI
- ✅ **Gestión de Estado:** React Context API (para autenticación)
- ✅ **Comunicación con API:** fetch API nativa con funciones de ayuda

#### **Estructura de Archivos:**
```
frontend/src/
├── App.js               # Configuración principal de rutas
├── context/
│   └── AuthContext.js   # Contexto global para autenticación
├── api/                 # Funciones para interactuar con backend
│   ├── authApi.js
│   ├── userApi.js
│   ├── businessApi.js
│   ├── productApi.js
│   └── publicApi.js
├── components/ui/       # Componentes UI de Shadcn
└── screens/            # Componentes de pantalla
    ├── LoginScreen.js
    ├── RegisterScreen.js
    ├── DashboardScreen.js
    ├── ProfileScreen.js
    ├── ManageBusinessesScreen.js
    ├── CreateBusinessScreen.js
    ├── EditBusinessScreen.js
    ├── ManageProductsScreen.js
    ├── CreateProductScreen.js
    ├── EditProductScreen.js
    └── PublicListingScreen.js
```

---

## 3. NUEVAS FUNCIONALIDADES A IMPLEMENTAR (POR CAPÍTULOS)

> **NOTA:** A partir de la migración a Shuup, las siguientes funcionalidades se implementarán adaptando el frontend y backend para interactuar con Shuup. Las tareas de CRUD y lógica de negocio que ahora dependen de Shuup están marcadas como [MIGRACIÓN SHUUP].

### **Capítulo ACTUAL: Workflow Interno y Gestión de Ventas en Local (Panadería Ñiam)**

#### **Descripción General:**
Implementar las funcionalidades clave para que un negocio físico (ej. Panadería Ñiam) pueda usar SOUP como su sistema principal de gestión de ventas en el local, inventario y producción, reemplazando a Excel.

#### **Roles y Funcionalidades Clave:**

**1. 🗣️ Trabajador de Atención al Cliente (Punto de Venta Principal):**
- **Registro de Ventas en Local:** Nueva pantalla POS (`SalePointScreen.js`) para seleccionar productos, ajustar cantidades y registrar ventas
- **Consulta de Inventario:** Actualización de `ManageProductsScreen.js` para mostrar stock terminado
- **Gestión de Pedidos Online:** Módulo futuro para encargos

**2. 👨‍🍳 Cocinero / Productor:**
- **Gestión de Insumos:** Uso de pantallas existentes (`ManageInsumosScreen`, `CreateInsumoScreen`, `EditInsumoScreen`)
- **Gestión de Productos:** Uso de pantallas existentes con cálculo de COGS y márgenes
- **Definir Recetas:** Asociación de insumos a productos (ya implementado)

**3. 📊 Dueños / Managers:**
- **Visión General:** Actualización de `DashboardScreen.js` y `ManageBusinessesScreen.js`
- **Análisis de Rentabilidad:** Visualización de COGS, precios y márgenes en `ManageProductsScreen.js`

**4. 🚶 Cliente:**
- **Compra en Local:** Gestionado por el trabajador de atención al cliente
- **Exploración Online:** Uso de pantallas públicas existentes

#### **Tareas de Backend:**
- **models.py:** Añadir campo `stock_terminado` al modelo Producto
- **crud/product.py:** Implementar función `record_sale` para descuento de inventario
- **routers/product_router.py:** Nuevo endpoint `POST /products/{product_id}/record_sale`
- **Migración de BD:** Añadir campo `stock_terminado` a tabla productos

#### **Tareas de Frontend:**
- **screens/SalePointScreen.js:** Crear nueva pantalla de punto de venta
- **api/productApi.js:** Añadir función `recordSale`
- **App.js:** Añadir ruta `/dashboard/pos`
- **ManageProductsScreen.js:** Actualizar para mostrar stock terminado y métricas financieras

#### **Próximos Pasos Prioritarios:**
1. Implementar pantalla de punto de venta (POS)
2. Añadir campo `stock_terminado` al modelo Producto
3. Implementar lógica de descuento de stock al vender
4. Actualizar visualización de productos con métricas financieras

---

### **Capítulo 4: Gestión de Insumos y Cálculo de Costos (Completado)**

#### **Descripción UI/UX:**
- **Dashboard:** Nuevo botón "Gestionar Insumos" para emprendedores
- **ManageInsumosScreen:** Tabla/lista de insumos del usuario con botones "Crear Insumo", "Editar" y "Eliminar"
- **CreateInsumoScreen/EditInsumoScreen:** Formulario con campos para nombre, cantidad disponible, unidad de medida, costo unitario de compra
- **CreateProductScreen/EditProductScreen:**
  - Sección "Insumos del Producto" con botón "Añadir Insumo"
  - Modal/sección expandible para seleccionar insumo existente y especificar cantidad necesaria
  - Visualización dinámica del COGS y Precio Sugerido

#### **Tareas de Backend:**
- **models.py:**
  - Crear modelo Insumo (id, nombre, cantidad_disponible, unidad_medida_compra, costo_unitario_compra, usuario_id, fecha_creacion, fecha_actualizacion)
  - Crear modelo ProductoInsumo (tabla de asociación id, producto_id, insumo_id, cantidad_necesaria)
  - Modificar modelo Producto para incluir relaciones con ProductoInsumo y campos cogs y precio_sugerido
- **schemas.py:**
  - Definir InsumoCreate, InsumoUpdate, InsumoResponse
  - Definir ProductoInsumoCreate, ProductoInsumoResponse
  - Modificar ProductoCreate, ProductoUpdate, ProductoResponse para manejar lista de ProductoInsumoCreate/Response
- **crud/insumo.py:** Implementar CRUD para Insumo
- **crud/product.py:**
  - Añadir lógica para crear/actualizar ProductoInsumo al crear/actualizar productos
  - Implementar cálculo de cogs y precio_sugerido basado en insumos asociados y sus costos
- **routers/insumo_router.py:** Crear router con endpoints protegidos para CRUD de insumos
- **main.py:** Incluir insumo_router

#### **Tareas de Frontend:**
- **api/insumoApi.js:** Crear funciones para interactuar con endpoints de insumos
- **screens/ManageInsumosScreen.js:** Crear componente para listar insumos
- **screens/CreateInsumoScreen.js:** Crear componente para formulario de creación de insumos
- **screens/EditInsumoScreen.js:** Crear componente para formulario de edición de insumos
- **screens/CreateProductScreen.js/EditProductScreen.js:** Modificar para integrar selección de insumos, cantidad necesaria, y mostrar COGS/Precio Sugerido
- **App.js:** Añadir rutas para pantallas de insumos
- **screens/DashboardScreen.js:** Añadir botón "Gestionar Insumos"

### **Capítulo 5: Gestión de Encargos (Pedidos)**

#### **Descripción UI/UX:**
- **Dashboard:** Botón "Ver Encargos"
- **ManageEncargosScreen:** Lista de encargos con estados (Pendiente de pago, En producción, Listo para envío, Completado, Cancelado). Botones para ver detalles, actualizar estado
- **CreateEncargoScreen:** Formulario para registrar nuevo encargo (seleccionar cliente, producto, cantidad, precio total, fecha estimada de entrega, notas, dirección de envío)
- **EncargoDetailScreen:** Vista detallada del encargo, con historial de estados y opciones para actualizarlo
- **Integración WhatsApp (PMV):**
  - En EncargoDetailScreen, opciones para enviar notificaciones de estado por WhatsApp al cliente
  - En pantallas de detalle de Producto/Negocio (públicas), botón "Compartir por WhatsApp"

#### **Tareas de Backend:**
- **models.py:**
  - Modelo Encargo (id, cliente_id, producto_id, cantidad, precio_total, fecha_encargo, fecha_entrega_estimada, estado, notas, direccion_envio, progreso_envio, usuario_id)
  - Relaciones con Usuario (gestor) y Producto
- **schemas.py:** Definir EncargoCreate, EncargoUpdate, EncargoResponse
- **crud/encargo.py:** Implementar CRUD para Encargo
- **routers/encargo_router.py:** Crear router con endpoints protegidos para CRUD de encargos
- **Integración WhatsApp (Backend):**
  - Configuración para almacenar credenciales de WhatsApp Business API
  - Lógica para interactuar con API de WhatsApp Business para enviar mensajes de plantilla
  - Integrar llamadas a esta lógica en funciones CRUD de Encargo (al cambiar de estado)

#### **Tareas de Frontend:**
- **api/encargoApi.js:** Crear funciones para interactuar con endpoints de encargos
- **screens/ManageEncargosScreen.js:** Crear componente para listar encargos
- **screens/CreateEncargoScreen.js:** Crear componente para formulario de creación de encargos
- **screens/EncargoDetailScreen.js:** Crear componente para ver y editar detalles de encargo, incluyendo cambio de estado
- **Integración WhatsApp (Frontend):**
  - Botones para enviar notificaciones de WhatsApp en EncargoDetailScreen
  - Botones "Compartir por WhatsApp" en PublicListingScreen y futuras pantallas de detalle público
- **App.js:** Añadir rutas para pantallas de encargos
- **screens/DashboardScreen.js:** Añadir botón "Ver Encargos"

### **Capítulo 6: Reseñas y Calificaciones**

#### **Descripción UI/UX:**
- **EncargoDetailScreen:** Después de encargo "Completado", botón "Dejar Reseña" que lleve a formulario
- **CreateReviewScreen:** Campo para calificación (estrellas 1-5) y comentario
- **Pantallas de Detalle Público (Negocio/Producto):** Mostrar rating_promedio y reviews_count

#### **Tareas de Backend:**
- **models.py:** Modelo Review (id, encargo_id, rating, comentario, fecha_review, usuario_id)
- **schemas.py:** Definir ReviewCreate, ReviewResponse
- **crud/review.py:** Implementar CRUD para Review
- **crud/negocio.py/crud/product.py:** Lógica para actualizar rating_promedio y reviews_totales/reviews_count al crear nueva reseña
- **routers/review_router.py:** Crear router con endpoints protegidos para creación de reseñas

#### **Tareas de Frontend:**
- **api/reviewApi.js:** Crear funciones para interactuar con endpoints de reseñas
- **screens/EncargoDetailScreen.js:** Añadir botón "Dejar Reseña" condicional
- **screens/CreateReviewScreen.js:** Crear componente para formulario de reseña
- **Pantallas de Detalle Público (futuras):** Mostrar rating_promedio y reviews_count
- **App.js:** Añadir rutas para pantallas de reseña

### **Capítulo 7: Publicidad y Monetización**

#### **Descripción UI/UX:**
- **Dashboard:** Botón "Gestionar Publicidad" (para usuarios Premium)
- **ManageAdsScreen:** Lista de anuncios del usuario, con estado (activo/inactivo), visualizaciones, clics. Botones para crear, editar, pausar/activar
- **CreateAdScreen/EditAdScreen:** Formulario para seleccionar negocio o producto a publicitar, tipo de publicidad, fechas de inicio/fin, costo
- **Pantallas Públicas:** Espacios designados para mostrar anuncios (ej. "Anuncios Destacados")

#### **Tareas de Backend:**
- **models.py:** Modelo Publicidad (id, item_publicitado_id, tipo_publicidad, fecha_inicio, fecha_fin, costo, usuario_id, estado, visualizaciones, clics, conversiones, fecha_creacion, fecha_actualizacion)
- **schemas.py:** Definir PublicidadCreate, PublicidadUpdate, PublicidadResponse
- **crud/publicidad.py:** Implementar CRUD para Publicidad
- **Lógica de Tracking:** Implementar lógica para registrar visualizaciones y clics en anuncios
- **routers/publicidad_router.py:** Crear router con endpoints protegidos para gestión de publicidad
- **routers/public_router.py:** Añadir endpoints públicos para obtener anuncios activos

#### **Tareas de Frontend:**
- **api/publicidadApi.js:** Crear funciones para interactuar con endpoints de publicidad
- **screens/ManageAdsScreen.js:** Crear componente para gestionar anuncios
- **screens/CreateAdScreen.js/EditAdScreen.js:** Crear componentes para formularios de anuncios
- **screens/PublicListingScreen.js/Pantallas de Detalle Público:** Integrar componentes para mostrar anuncios
- **App.js:** Añadir rutas para pantallas de publicidad
- **screens/DashboardScreen.js:** Añadir botón "Gestionar Publicidad"

### **Capítulo 8: Integración de IA (SOUP Flow AI - Primeros Pasos)**

#### **Descripción UI/UX:**
- **Dashboard/Panel de Control:** Sección "Asistente SOUP AI" con campo de texto para preguntas o botón para generar sugerencias
- **Generación de Descripciones:** En CreateProductScreen/EditProductScreen, botón "Generar Descripción con IA" que use nombre del producto y tipo para generar texto
- **Generación de Mensajes WhatsApp:** En EncargoDetailScreen, botón "Sugerir Mensaje WhatsApp" que genere borrador basado en estado del encargo

#### **Tareas de Backend:**
- **services/ai_service.py:** Nuevo módulo para encapsular lógica de llamadas a Gemini API
- **Endpoints de IA:** Nuevos endpoints en routers existentes o nuevo ai_router para:
  - POST /ai/generate-description (para productos/servicios)
  - POST /ai/suggest-whatsapp-message (para encargos)
  - POST /ai/chat (para chatbot básico)
- **Integración:** Utilizar Gemini API (gemini-2.0-flash para texto) para generar contenido

#### **Tareas de Frontend:**
- **api/aiApi.js:** Crear funciones para interactuar con nuevos endpoints de IA
- **screens/CreateProductScreen.js/EditProductScreen.js:** Añadir botón y lógica para generar descripciones
- **screens/EncargoDetailScreen.js:** Añadir botón y lógica para sugerir mensajes de WhatsApp
- **screens/DashboardScreen.js:** Posiblemente campo de texto para chatbot básico o área de sugerencias

### **Capítulo 9: Notificaciones y Mensajería (Consolidación)**

#### **Descripción UI/UX:**
- **Dashboard:** Icono de campana para notificaciones
- **Panel de Notificaciones:** Modal o página para ver lista de notificaciones (ej. "Tarea de proyecto actualizada", "Nuevo encargo", "Reseña recibida")
- **Mensajería Básica:** Hilo de comentarios o chat simple dentro de vista de proyecto

#### **Tareas de Backend:**
- **models.py:** Modelo Notificacion (id, usuario_id, tipo, contenido, leida, fecha)
- **schemas.py:** Definir esquemas para Notificacion
- **crud/notification.py:** Implementar CRUD para notificaciones
- **Disparadores de Notificaciones:** Modificar lógica CRUD en otros módulos para crear notificaciones
- **routers/notification_router.py:** Crear router para obtener y marcar notificaciones como leídas
- **Consolidación WhatsApp:** Asegurar que lógica de WhatsApp del Capítulo 5 esté bien encapsulada y sea reutilizable

#### **Tareas de Frontend:**
- **api/notificationApi.js:** Crear funciones para interactuar con endpoints de notificaciones
- **Componente de Notificaciones:** Componente reutilizable para mostrar icono de campana con contador y panel de notificaciones
- **screens/DashboardScreen.js:** Integrar componente de notificaciones
- **screens/ProjectDetailScreen.js (futuro):** Implementar hilo de comentarios/chat

### **Capítulo 10: Búsqueda Avanzada y Filtrado (Público)**

#### **Descripción UI/UX:**
- **PublicListingScreen:** Añadir barra de búsqueda con autocompletado y filtros (por rubro, tipo de producto, ubicación, rango de precios, rating)
- **Resultados de Búsqueda:** Mostrar resultados de forma clara y paginada

#### **Tareas de Backend:**
- **routers/public_router.py:** Modificar endpoints GET /public/businesses y GET /public/products para aceptar parámetros de consulta para búsqueda y filtrado
- **crud/business.py/crud/product.py:** Modificar funciones get_all_businesses y get_all_products para aplicar filtros y lógica de búsqueda

#### **Tareas de Frontend:**
- **screens/PublicListingScreen.js:** Implementar barra de búsqueda y controles de filtro
- **Lógica de Estado:** Gestionar estado de filtros y consulta de búsqueda
- **Actualización de API:** Modificar llamadas a publicApi.js para incluir parámetros de búsqueda y filtro

### **Capítulo 11: Refinamiento de Roles de Usuario y Permisos**

#### **Descripción UI/UX:**
- **Registro:** Asegurar que selección de tipo_tier sea clara
- **Dashboard/Navegación:** Asegurar que botones y enlaces solo sean visibles para roles de usuario adecuados (ej. "Gestionar Publicidad" solo para Premium)
- **Mensajes de Error:** Mostrar mensajes claros si usuario intenta acceder a funcionalidad sin permisos adecuados

#### **Tareas de Backend:**
- **dependencies.py:** Crear funciones de dependencia para verificar roles (ej. require_microemprendedor_or_freelancer)
- **Routers:** Aplicar estas dependencias a endpoints API para asegurar que solo roles autorizados puedan acceder a ciertas funcionalidades
- **Lógica de Negocio:** Refinar cualquier lógica de negocio que dependa del tipo_tier del usuario

#### **Tareas de Frontend:**
- **Componentes de Navegación/Botones:** Implementar lógica condicional para renderizar elementos de UI basados en user.tipo_tier del AuthContext
- **Manejo de Errores:** Mostrar mensajes amigables al usuario si intenta acceder a rutas no autorizadas

### **Capítulo 12: Despliegue y Consideraciones de Escalabilidad**

#### **Descripción UI/UX:** N/A (principalmente tareas de infraestructura)

#### **Tareas de Backend:**
- **Contenedorización:** Crear Dockerfile para aplicación FastAPI
- **Configuración de Producción:** Variables de entorno para base de datos, JWT secrets, etc.
- **Optimización:** Considerar Gunicorn/Uvicorn workers

#### **Tareas de Frontend:**
- **Optimización de Build:** npm run build
- **Configuración de Producción:** Variables de entorno para URL del backend

#### **Consideraciones Generales:**
- **Base de Datos:** Optimización de consultas, índices
- **Seguridad:** Hardening de la API, protección contra ataques comunes
- **Monitoring:** Herramientas básicas de monitoreo de rendimiento y errores

### **Capítulo 13: SOUP Projects (Gestión Colaborativa Simple)**

#### **Descripción UI/UX:**
- **EncargoDetailScreen/ProductDetailScreen:** Opción "Crear Proyecto Colaborativo" o "Invitar Colaboradores"
- **ProjectDetailScreen:**
  - Vista de detalles del proyecto (descripción, plazos)
  - Lista de "Tareas" con checkboxes de estado (Pendiente, En Proceso, Completada)
  - Sección de "Notas" o "Comentarios" con feed cronológico
  - Botón "Invitar Colaborador" (para propietario del proyecto)
- **Correo Electrónico:** Plantilla de email para invitaciones a colaboradores

#### **Tareas de Backend:**
- **models.py:**
  - Modelo Project (id, encargo_id (opcional), owner_id, name, description, status, due_date)
  - Modelo Task (id, project_id, description, assigned_to_user_id, status)
  - Modelo ProjectCollaborator (project_id, user_id, role)
  - Modelo ProjectNote (id, project_id, user_id, content, timestamp)
- **schemas.py:** Definir esquemas para Project, Task, ProjectCollaborator, ProjectNote
- **crud/project.py:** Implementar CRUD para Project, Task, ProjectCollaborator, ProjectNote
- **Lógica de Invitación:** Generación de tokens de invitación, envío de emails
- **routers/project_router.py:** Crear router con endpoints protegidos para gestión de proyectos

#### **Tareas de Frontend:**
- **api/projectApi.js:** Crear funciones para interactuar con endpoints de proyectos
- **screens/EncargoDetailScreen.js/ProductDetailScreen.js:** Añadir botón "Crear Proyecto"
- **screens/ProjectDetailScreen.js:** Crear componente para vista de proyecto (tareas, notas, invitación)
- **App.js:** Añadir rutas para pantallas de proyectos
- **screens/DashboardScreen.js:** Añadir botón "Mis Proyectos"

### **Capítulo 14: Historias de Negocio y Contenido Multimedia**

#### **Descripción UI/UX:**
- **Dashboard/Panel de Negocio:** Botón "Añadir Historia" o sección "Mis Actualizaciones"
- **CreateStoryScreen:** Campo de texto corto, botón para subir única foto
- **Perfil Público del Negocio:** Nueva sección "Historias" o "Novedades" con feed cronológico de tarjetas de historias (foto + texto corto)

#### **Tareas de Backend:**
- **models.py:** Modelo Story (id, business_id, user_id, text_content, image_url, location_text (opcional), timestamp, is_public)
- **schemas.py:** Definir esquemas para Story
- **crud/story.py:** Implementar CRUD para Story
- **Servicio de Almacenamiento de Archivos:** Integración con servicio de almacenamiento en la nube (ej. Google Cloud Storage, Firebase Storage) para subir y gestionar imágenes
- **routers/story_router.py:** Crear router con endpoints protegidos para gestión de historias
- **routers/public_router.py:** Añadir endpoint público para obtener historias de un negocio

#### **Tareas de Frontend:**
- **api/storyApi.js:** Crear funciones para interactuar con endpoints de historias
- **screens/CreateStoryScreen.js:** Crear componente para formulario de creación de historias, incluyendo subida de imagen
- **screens/BusinessDetailScreen.js (futura):** Integrar componente para mostrar feed de historias
- **App.js:** Añadir rutas para pantallas de historias
- **screens/DashboardScreen.js:** Añadir botón "Mis Historias"

---

## 4. ARQUITECTURA GENERAL DEL MVP COMPLETO

El MVP completo de SOUP Emprendimientos se construirá sobre una arquitectura de microservicios lógicos (aunque implementados en una única aplicación por simplicidad inicial) con una separación clara de responsabilidades entre el frontend y el backend.

### **Frontend:**
- **Tecnologías:** React.js, React Router DOM, Tailwind CSS, Shadcn UI
- **Propósito:** Interfaz de usuario interactiva y responsiva para emprendedores y clientes
- **Despliegue:** Idealmente en servicio de hosting de frontend como Vercel o Netlify

### **Backend:**
- **Tecnologías:** FastAPI (Python), PostgreSQL, SQLAlchemy, Pydantic, JWT
- **Propósito:** API RESTful para lógica de negocio, gestión de datos y comunicación con base de datos
- **Despliegue:** En servidor virtual privado (VPS) o servicio PaaS como Render, Heroku, o Google Cloud Run

### **Base de Datos:**
- **Tecnología:** PostgreSQL
- **Propósito:** Almacenamiento persistente de todos los datos de la aplicación
- **Despliegue:** Puede ser autohospedada en el mismo VPS que el backend o como servicio de base de datos gestionado (ej. AWS RDS, DigitalOcean Managed Databases)

### **Servicios Externos (Futuros/Opcionales):**
- **Almacenamiento de Archivos:** Google Cloud Storage, AWS S3, Firebase Storage (para imágenes de productos/historias)
- **Servicio de Email:** SendGrid, Mailgun (para invitaciones, notificaciones)
- **API de WhatsApp Business:** Para notificaciones y mensajería
- **Modelos de IA:** Gemini API (para generación de texto, análisis)

### **Valor del MVP:**
El valor de este MVP radica en proporcionar una herramienta integral para microemprendedores y freelancers que les permita:

- **Profesionalizar su presencia online:** Con perfiles públicos, listados de productos/servicios
- **Optimizar la gestión interna:** Control de negocios, productos, insumos, costos y encargos
- **Mejorar la comunicación con clientes:** A través de notificaciones y futuras integraciones
- **Obtener insights:** Con cálculos de costos y futuras analíticas
- **Reducir la fricción:** Al centralizar herramientas que usualmente están dispersas

Para los clientes, el valor es un directorio curado y transparente donde pueden encontrar proveedores de confianza con historial de producción y reseñas.

Este MVP establece una base sólida para futuras expansiones hacia un ecosistema completo de emprendimiento, con potencial para monetización a través de planes premium y publicidad.

---

## 5. CRONOGRAMA DE DESARROLLO

**Objetivo: MVP Online a Finales de Septiembre 2025**

Este cronograma es una estimación ambiciosa pero alcanzable, asumiendo un desarrollo enfocado. Se basa en el 7 de julio de 2025 como fecha de inicio.

### **Semana 1 (Jul 07 - Jul 13):**
**Capítulo 4: Gestión de Insumos y Cálculo de Costos (Backend completo)**
- Modelos Insumo, ProductoInsumo y modificación de Producto
- Esquemas Pydantic para Insumos y ProductoInsumo, modificación de esquemas de Producto
- CRUD para Insumos
- Modificación CRUD de Productos (cálculo COGS/Precio Sugerido, manejo ProductoInsumo)
- Routers para Insumos
- Integración en main.py
- **Deadline:** Backend de Capítulo 4 operativo y probado en Swagger UI

### **Semana 2 (Jul 14 - Jul 20):**
**Capítulo 4: Gestión de Insumos y Cálculo de Costos (Frontend completo)**
- API Services para Insumos
- Pantallas ManageInsumosScreen, CreateInsumoScreen, EditInsumoScreen
- Integración de Insumos en CreateProductScreen y EditProductScreen (UI para añadir/gestionar insumos, mostrar COGS/Precio Sugerido)
- Actualización de Rutas y Navegación (App.js, DashboardScreen.js)
- **Deadline:** Frontend de Capítulo 4 operativo y probado

### **Semana 3 (Jul 21 - Jul 27):**
**Capítulo 5: Gestión de Encargos (Backend completo)**
- Modelo Encargo
- Esquemas Pydantic para Encargos
- CRUD para Encargos
- Routers para Encargos
- Integración en main.py
- **Deadline:** Backend de Capítulo 5 operativo y probado en Swagger UI

### **Semana 4 (Jul 28 - Ago 03):**
**Capítulo 5: Gestión de Encargos (Frontend completo)**
- API Services para Encargos
- Pantallas ManageEncargosScreen, CreateEncargoScreen, EncargoDetailScreen
- Actualización de Rutas y Navegación
- Capítulo 3: Actualización Frontend (Botones Compartir WhatsApp)
- Añadir botones "Compartir por WhatsApp" en PublicListingScreen (tarjetas)
- **Deadline:** Frontend de Capítulo 5 operativo y probado

### **Semana 5 (Ago 04 - Ago 10):**
**Capítulo 6: Reseñas y Calificaciones (Backend y Frontend)**
- Modelos, esquemas, CRUD, routers para Review
- Lógica para actualizar ratings en Negocios/Productos
- API Services y Pantallas de Frontend para reseñas
- **Deadline:** Reseñas funcionales

### **Semana 6 (Ago 11 - Ago 17):**
**Capítulo 7: Publicidad y Monetización (Backend y Frontend)**
- Modelos, esquemas, CRUD, routers para Publicidad
- Lógica de tracking (visualizaciones/clics)
- API Services y Pantallas de Frontend para gestión de publicidad
- Integración de anuncios en PublicListingScreen
- **Deadline:** Publicidad básica operativa

### **Semana 7 (Ago 18 - Ago 24):**
**Capítulo 14: Historias de Negocio y Contenido Multimedia (Backend y Frontend)**
- Modelos, esquemas, CRUD, routers para Story
- Configuración de almacenamiento de archivos (simulada o con servicio real si se decide)
- API Services y Pantallas de Frontend para crear/listar historias
- Integración de historias en futura pantalla de detalle público de Negocio
- **Deadline:** Historias de negocio funcionales

### **Semana 8 (Ago 25 - Ago 31):**
**Capítulo 13: SOUP Projects (Gestión Colaborativa Simple - Backend)**
- Modelos Project, Task, ProjectCollaborator, ProjectNote
- Esquemas, CRUD, routers
- Lógica de invitación por email (simulada o con servicio real)
- **Deadline:** Backend de Proyectos operativo

### **Semana 9 (Sep 01 - Sep 07):**
**Capítulo 13: SOUP Projects (Gestión Colaborativa Simple - Frontend)**
- API Services y Pantallas de Frontend para Proyectos (creación, detalle, tareas, notas)
- Integración en EncargoDetailScreen
- **Deadline:** Proyectos colaborativos básicos funcionales

### **Semana 10 (Sep 08 - Sep 14):**
**Capítulo 8: Integración de IA (Primeros Pasos - Backend y Frontend)**
- Integración Gemini API para generación de descripciones de productos y sugerencia de mensajes WhatsApp
- UI para estas funcionalidades en pantallas de producto y encargo
**Capítulo 9: Notificaciones y Mensajería (Backend - Consolidación WhatsApp)**
- Modelo Notificacion
- Disparadores de notificaciones
- Consolidación de lógica de envío de WhatsApp
- **Deadline:** Funcionalidades de IA y Notificaciones Backend operativas

### **Semana 11 (Sep 15 - Sep 21):**
**Capítulo 9: Notificaciones y Mensajería (Frontend)**
- API Services y Componente de Notificaciones (campana, panel)
- Integración en DashboardScreen
**Capítulo 10: Búsqueda Avanzada y Filtrado (Backend y Frontend)**
- Modificación de endpoints públicos para aceptar filtros
- Implementación de UI de búsqueda y filtros en PublicListingScreen
- **Deadline:** Notificaciones y Búsqueda Avanzada funcionales

### **Semana 12 (Sep 22 - Sep 30):**
**Capítulo 11: Refinamiento de Roles de Usuario y Permisos (Backend y Frontend)**
- Implementación de dependencias de roles en el backend
- Ajustes de visibilidad de UI basados en roles
**Capítulo 12: Despliegue y Consideraciones de Escalabilidad**
- Dockerización (si aplica)
- Configuración de variables de entorno para producción
- Despliegue inicial del MVP en entorno público
**Revisión General y Bug Fixing:** Pruebas finales, corrección de errores, ajustes menores de UI/UX
- **Deadline: MVP Online a finales de Septiembre 2025**

---

## 📝 NOTAS IMPORTANTES

Este roadmap es un plan de alto nivel. Durante el desarrollo, pueden surgir desafíos inesperados que requieran ajustar las estimaciones. La clave será la comunicación constante y la priorización.

### **Factores de Riesgo:**
- Integración con APIs externas (WhatsApp, IA)
- Configuración de servicios de almacenamiento
- Optimización de rendimiento para producción
- Testing exhaustivo de todas las funcionalidades

### **Estrategias de Mitigación:**
- Desarrollo incremental con testing continuo
- Prototipos rápidos para integraciones complejas
- Documentación detallada de cada capítulo
- Revisión semanal del progreso

---

**Última actualización:** 7 de Julio de 2025  
**Versión del documento:** 1.0  
**Mantenedor:** Equipo SOUP Emprendimientos 

---

## NUEVA SECCIÓN: PLAN DE MIGRACIÓN A SHUUP

Ver `Documentación/Migracion Shuup/PLANTILLA_PLAN_MIGRACION.md` para el plan detallado de migración, mapeo de modelos y registro de decisiones técnicas.

--- 