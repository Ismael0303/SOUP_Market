# 🥖 Capítulo ÑIAM: Workflow Interno y Gestión de Ventas en Local

**Prioridad:** ALTA  
**Fecha de Inicio Estimada:** Inmediato  
**Objetivo:** Implementar las funcionalidades clave para que un negocio físico (ej. Panadería Ñiam) pueda usar SOUP como su sistema principal de gestión de ventas en el local, inventario y producción, reemplazando a Excel.

---

## 💡 Visión General

"Panadería Ñiam", especializada en Chipá, busca integrar SOUP Market como su sistema de Punto de Venta (POS) interno para registrar transacciones, gestionar inventario en tiempo real y proporcionar análisis financiero. La venta en local físico es la prioridad, con pedidos online como un canal secundario, pero también gestionado por SOUP.

---

## 👥 Roles y Funcionalidades Clave

### 1. 🗣️ Trabajador de Atención al Cliente (Usa SOUP Dashboard - Punto de Venta Principal)

**Funciones Prioritarias:**

#### **Registro de Ventas en Local (SOUP: `ManageProductsScreen` / Nuevo Módulo POS - *Prioridad Alta*)**

**Pseudocódigo de Alto Nivel:**
```javascript
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
```

**Backend:**
```python
# Backend: crud/product.py
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

**Integración al Código Existente (Capítulo 1 - Prioridad Alta):**
- **Frontend:** Se creará una nueva pantalla `SalePointScreen.js` en `frontend/src/screens/`. Se integrará al `App.js` con una nueva ruta protegida (ej., `/dashboard/pos`).
- **Backend:** La lógica de `record_sale` se integrará en `backend/app/crud/product.py` (o en un nuevo CRUD de `Transaccion` si se crea). La reducción de insumos se realizará en esta lógica. Se necesitará un nuevo endpoint en `backend/app/routers/product_router.py` (o un nuevo `sales_router.py`) para `POST /products/{product_id}/record_sale`.

#### **Consulta de Inventario de Productos (SOUP: `ManageProductsScreen`)**

**Pseudocódigo de Alto Nivel:**
```javascript
// Frontend: ManageProductsScreen.js
FUNCION fetchProducts():
    productos = LLAMAR productApi.getAllMyProducts()
    MOSTRAR productos.map(p => p.nombre, p.stock_terminado) // stock_terminado es un campo futuro
```

**Integración al Código Existente (Capítulo 1 - Prioridad Alta):**
- **Frontend:** Ya existe `ManageProductsScreen.js`. Se actualizará para mostrar un campo `stock_terminado` (futuro).
- **Backend:** El modelo `Producto` en `backend/app/models.py` necesitará un campo `stock_terminado: Mapped[Optional[float]] = mapped_column(Float, nullable=True)`. La lógica para actualizar este stock al producir o vender se añadiría en `crud/product.py`.

#### **Recepción y Gestión de Pedidos Online (*Módulo Encargos - Funcionalidad Futura*)**

**Pseudocódigo de Alto Nivel:**
```javascript
// Frontend: ManageOrdersScreen.js (NUEVO - Capítulo posterior)
FUNCION fetchOrders():
    pedidos = LLAMAR orderApi.getAllMyOrders()
    MOSTRAR pedidos.map(p => p.cliente, p.estado, p.productos)

FUNCION updateOrderStatus(orderId, newStatus):
    LLAMAR orderApi.updateOrder(orderId, { estado: newStatus })
    MOSTRAR mensajeExito("Estado actualizado.")
```

**Integración al Código Existente:** Se dejará para un capítulo posterior. Implicaría nuevos modelos (`Pedido`, `ItemPedido`), esquemas, CRUDs y routers.

### 2. 👨‍🍳 Cocinero / Productor de Insumos (Usa SOUP Dashboard)

**Funciones Prioritarias:**

#### **Gestión de Insumos (SOUP: `ManageInsumosScreen`, `CreateInsumoScreen`, `EditInsumoScreen`)**

**Pseudocódigo de Alto Nivel:**
```javascript
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

**Integración al Código Existente:** Estas pantallas ya existen y funcionan. Solo se enfatizará su uso para el workflow.

#### **Gestión de Productos (SOUP: `ManageProductsScreen`, `CreateProductScreen`, `EditProductScreen`)**

**Definir Recetas (Asociación Insumos):**
```javascript
// Frontend: CreateProductScreen.js / EditProductScreen.js
FUNCION handleAddInsumoToProduct(insumoId, cantidadNecesaria):
    // Añadir a selectedInsumos

FUNCION handleSubmitProduct(formData):
    // formData.insumos_asociados contiene [{insumo_id, cantidad_necesaria}]
    // LLAMAR productApi.createProduct(formData) o productApi.updateProduct(productId, formData)
```

**Ver Costos de Producción (COGS):**
```javascript
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

**Ajustar Precios y Márgenes:**
```javascript
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

**Integración al Código Existente:** Ya implementado en backend y frontend.

### 3. 📊 Dueños / Managers (Usa SOUP Dashboard)

**Funciones Prioritarias:**

#### **Visión General del Negocio (SOUP: `DashboardScreen`, `ManageBusinessesScreen`)**

**Pseudocódigo de Alto Nivel:**
```javascript
// Frontend: DashboardScreen.js
FUNCION fetchDashboardData():
    usuario = LLAMAR authApi.getProfile()
    negocios = LLAMAR businessApi.getAllMyBusinesses()
    productos = LLAMAR productApi.getAllMyProducts()
    // Mostrar resumen de ventas_completadas, calificacion_promedio (futuro)
```

**Integración al Código Existente:** `DashboardScreen.js` y `ManageBusinessesScreen.js` ya existen. Se actualizarán para mostrar `ventas_completadas` y `calificacion_promedio` (futuras).

#### **Gestión Financiera (*Módulo de Reportes - Funcionalidad Futura*)**

**Pseudocódigo de Alto Nivel:**
```javascript
// Frontend: ReportsScreen.js (NUEVO - Capítulo posterior)
FUNCION fetchSalesReports(periodo):
    reporte = LLAMAR salesApi.getSalesReport(periodo) // Nueva API de reportes
    MOSTRAR reporte.ingresosTotales, reporte.egresosInsumos, reporte.margenNeto
```

**Integración al Código Existente:** Se dejará para un capítulo posterior. Implicaría nuevos modelos (`Transaccion`, `Reporte`), esquemas, CRUDs y routers.

#### **Análisis de Rentabilidad:**

**Pseudocódigo de Alto Nivel:**
```javascript
// Frontend: ManageProductsScreen.js (para ver por producto)
// O ReportsScreen.js (para ver agregados)
FUNCION displayProfitability(product):
    MOSTRAR product.cogs, product.precio_venta, product.margen_ganancia_real
```

**Integración al Código Existente:** Ya visible en `EditProductScreen.js`. Se extenderá a `ManageProductsScreen.js` en un paso posterior de este capítulo.

### 4. 🚶 Cliente (Interacción Principalmente Física / Opcional Online)

**Funciones Prioritarias:**

#### **Compra en Local Físico:**

**Pseudocódigo de Alto Nivel:**
```javascript
// Proceso físico en el local, registrado por el Trabajador de Atención al Cliente en SOUP.
// No hay interacción directa del cliente con SOUP en este punto para la venta física.
```

**Integración al Código Existente:** Se gestiona indirectamente a través del rol de Atención al Cliente.

#### **Exploración de Productos Online (SOUP: `PublicListingScreen` y `PublicBusinessProductsScreen`)**

**Pseudocódigo de Alto Nivel:**
```javascript
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

**Integración al Código Existente:** Ya implementado en `PublicListingScreen.js` y `PublicBusinessProductsScreen.js`.

---

## 🚀 Próximos Pasos del Capítulo 1 (Prioridad Alta)

### 1. **Implementar la Pantalla de Punto de Venta (POS) en el Frontend:**
- Crear `frontend/src/screens/SalePointScreen.js`.
- Integrar la lógica para seleccionar productos, ajustar cantidades y registrar ventas.
- Añadir la ruta en `frontend/src/App.js`.

### 2. **Añadir Campo `stock_terminado` al Modelo `Producto` en Backend:**
- Modificar `backend/app/models.py`.
- Crear migración para añadir este campo.
- Actualizar `backend/app/schemas.py` y `backend/app/crud/product.py` para manejar este campo.

### 3. **Implementar Lógica de Descuento de Stock de Productos Terminados y de Insumos al Vender:**
- Modificar `backend/app/crud/product.py` para que la función de registro de venta (o una nueva función) descuente `stock_terminado` del producto y `cantidad_disponible` de los insumos asociados.

### 4. **Actualizar `ManageProductsScreen.js` para mostrar `COGS`, `Precio Sugerido`, `Margen Real` y `stock_terminado`:**
- Mejorar la visualización en la lista de productos del emprendedor.

---

## ⏭️ Funciones Avanzadas (Capítulos Posteriores)

Las siguientes funcionalidades son importantes pero se posponen para capítulos futuros del roadmap:

### **Módulo de Encargos/Pedidos Online Completo:**
- Modelos, esquemas, CRUDs y routers para `Pedido` y `ItemPedido`.
- Pantallas de `CreateOrderScreen`, `ManageOrdersScreen`, `OrderDetailsScreen`.
- Notificaciones para clientes y atención al cliente.

### **Módulo de Reportes Financieros Avanzados:**
- Generación de reportes de ingresos, egresos, rentabilidad por períodos.
- Integración con datos de ventas y costos de insumos.

### **Sistema de Calificaciones y Reseñas:**
- Modelos para `Calificacion` y `Reseña`.
- Lógica para calcular `calificacion_promedio` y `total_calificaciones`.
- Interfaz para clientes y visualización en productos/negocios.

### **Asistente de IA (Chatbot) Completo en Frontend:**
- Implementación del componente de chatbot interactivo en `PublicListingScreen`.
- Manejo de la interfaz de usuario para las recomendaciones de la IA.

### **Gestión de Usuarios y Roles (Administración):**
- Interfaz para que los dueños/managers asignen roles a sus empleados.

### **Integración con Pasarelas de Pago:**
- Manejo de pagos electrónicos para pedidos online.

### **Gestión de Cadetes/Logística:**
- Asignación y seguimiento de envíos a domicilio.

---

## 📋 Checklist de Implementación

### **Backend:**
- [ ] Añadir campo `stock_terminado` al modelo Producto en `models.py`
- [ ] Crear migración SQL para añadir campo `stock_terminado`
- [ ] Actualizar esquemas en `schemas.py` para incluir `stock_terminado`
- [ ] Implementar función `record_sale` en `crud/product.py`
- [ ] Crear endpoint `POST /products/{product_id}/record_sale` en `routers/product_router.py`
- [ ] Probar funcionalidad en Swagger UI

### **Frontend:**
- [ ] Crear `SalePointScreen.js` en `frontend/src/screens/`
- [ ] Añadir función `recordSale` en `api/productApi.js`
- [ ] Añadir ruta `/dashboard/pos` en `App.js`
- [ ] Actualizar `ManageProductsScreen.js` para mostrar métricas financieras
- [ ] Probar funcionalidad completa

### **Testing:**
- [ ] Probar registro de ventas y descuento de inventario
- [ ] Verificar cálculo de COGS y márgenes
- [ ] Probar interfaz de punto de venta
- [ ] Validar actualización de stock de insumos

---

**Última actualización:** 8 de Julio de 2025  
**Versión del documento:** 1.0  
**Mantenedor:** Asistente AI 