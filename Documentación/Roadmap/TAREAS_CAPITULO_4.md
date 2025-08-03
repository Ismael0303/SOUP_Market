# 📋 TAREAS DETALLADAS - CAPÍTULO 4: GESTIÓN DE INSUMOS

**Capítulo:** 4 - Gestión de Insumos y Cálculo de Costos  
**Duración:** 2 semanas (Jul 07 - Jul 20, 2025)  
**Prioridad:** ALTA - Próximo en desarrollo  
**Estado:** ⏳ PENDIENTE

---

## 🎯 **OBJETIVO DEL CAPÍTULO**

Implementar un sistema completo de gestión de insumos que permita a los emprendedores:
- Registrar y gestionar sus insumos (materias primas, materiales)
- Asociar insumos a productos específicos
- Calcular automáticamente el Costo de Bienes Vendidos (COGS)
- Generar precios sugeridos basados en márgenes de ganancia

---

## 📊 **ESTRUCTURA DE DATOS**

### **Nuevos Modelos:**

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

#### **ProductoInsumo (Tabla de Asociación)**
```python
class ProductoInsumo(Base):
    __tablename__ = "producto_insumos"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    producto_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)
    insumo_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("insumos.id"), nullable=False)
    cantidad_necesaria: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Relaciones
    producto: Mapped["Producto"] = relationship("Producto", back_populates="insumos_asociados")
    insumo: Mapped["Insumo"] = relationship("Insumo", back_populates="productos_asociados")
```

#### **Modificaciones al Modelo Producto**
```python
class Producto(Base):
    # ... campos existentes ...
    
    # Nuevos campos calculados
    cogs: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    precio_sugerido: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Nueva relación
    insumos_asociados: Mapped[List["ProductoInsumo"]] = relationship("ProductoInsumo", back_populates="producto", cascade="all, delete-orphan")
```

---

## 🔧 **TAREAS DE BACKEND (SEMANA 1)**

### **Día 1-2: Modelos y Esquemas**

#### **Tarea 1.1: Crear Modelos**
- [ ] Crear modelo `Insumo` en `backend/app/models.py`
- [ ] Crear modelo `ProductoInsumo` en `backend/app/models.py`
- [ ] Modificar modelo `Producto` para incluir nuevos campos y relaciones
- [ ] Crear modelo `Usuario` para incluir relación con insumos

#### **Tarea 1.2: Crear Esquemas Pydantic**
- [ ] Crear `InsumoBase`, `InsumoCreate`, `InsumoUpdate`, `InsumoResponse` en `backend/app/schemas.py`
- [ ] Crear `ProductoInsumoBase`, `ProductoInsumoCreate`, `ProductoInsumoResponse` en `backend/app/schemas.py`
- [ ] Modificar esquemas de `Producto` para incluir lista de insumos asociados

#### **Tarea 1.3: Migración de Base de Datos**
- [ ] Crear script de migración para nuevas tablas
- [ ] Ejecutar migración en base de datos de desarrollo
- [ ] Verificar integridad de datos existentes

### **Día 3-4: CRUD Operations**

#### **Tarea 1.4: Crear CRUD para Insumos**
- [ ] Crear archivo `backend/app/crud/insumo.py`
- [ ] Implementar `create_insumo(db, user_id, insumo: InsumoCreate)`
- [ ] Implementar `get_insumo_by_id(db, insumo_id: UUID)`
- [ ] Implementar `get_insumos_by_user_id(db, user_id: UUID)`
- [ ] Implementar `update_insumo(db, insumo_id: UUID, insumo_update: InsumoUpdate)`
- [ ] Implementar `delete_insumo(db, insumo_id: UUID)`

#### **Tarea 1.5: Modificar CRUD de Productos**
- [ ] Modificar `create_product` para manejar insumos asociados
- [ ] Modificar `update_product` para manejar insumos asociados
- [ ] Implementar función de cálculo de COGS
- [ ] Implementar función de cálculo de precio sugerido

#### **Tarea 1.6: Funciones de Cálculo**
- [ ] Crear función `calculate_cogs(producto_id: UUID, db: Session)`
- [ ] Crear función `calculate_suggested_price(cogs: float, margin_percentage: float)`
- [ ] Integrar cálculos en operaciones CRUD de productos

### **Día 5: Routers y Endpoints**

#### **Tarea 1.7: Crear Router de Insumos**
- [ ] Crear archivo `backend/app/routers/insumo_router.py`
- [ ] Implementar `POST /insumos/` - Crear insumo
- [ ] Implementar `GET /insumos/me` - Listar insumos del usuario
- [ ] Implementar `GET /insumos/{insumo_id}` - Obtener insumo específico
- [ ] Implementar `PUT /insumos/{insumo_id}` - Actualizar insumo
- [ ] Implementar `DELETE /insumos/{insumo_id}` - Eliminar insumo

#### **Tarea 1.8: Modificar Router de Productos**
- [ ] Modificar `POST /products/` para incluir insumos
- [ ] Modificar `PUT /products/{product_id}` para incluir insumos
- [ ] Modificar `GET /products/{product_id}` para incluir insumos asociados

#### **Tarea 1.9: Integración en Main**
- [ ] Incluir `insumo_router` en `backend/app/main.py`
- [ ] Verificar que todos los endpoints estén registrados correctamente

### **Día 6-7: Testing y Validación**

#### **Tarea 1.10: Testing Backend**
- [ ] Crear tests para CRUD de insumos
- [ ] Crear tests para cálculos de COGS y precio sugerido
- [ ] Crear tests para asociación de insumos con productos
- [ ] Verificar todos los endpoints en Swagger UI

#### **Tarea 1.11: Validación de Datos**
- [ ] Verificar validaciones de esquemas Pydantic
- [ ] Probar casos edge (cantidades negativas, costos cero, etc.)
- [ ] Verificar integridad referencial

---

## 🎨 **TAREAS DE FRONTEND (SEMANA 2)**

### **Día 1-2: API Services**

#### **Tarea 2.1: Crear API Service para Insumos**
- [ ] Crear archivo `frontend/src/api/insumoApi.js`
- [ ] Implementar `createInsumo(insumoData)`
- [ ] Implementar `getMyInsumos()`
- [ ] Implementar `getInsumoById(id)`
- [ ] Implementar `updateInsumo(id, updateData)`
- [ ] Implementar `deleteInsumo(id)`

#### **Tarea 2.2: Modificar API Service de Productos**
- [ ] Modificar `createProduct` para incluir insumos
- [ ] Modificar `updateProduct` para incluir insumos
- [ ] Verificar que `getProductById` incluya insumos asociados

### **Día 3-4: Pantallas de Gestión de Insumos**

#### **Tarea 2.3: Crear ManageInsumosScreen**
- [ ] Crear archivo `frontend/src/screens/ManageInsumosScreen.js`
- [ ] Implementar tabla/lista de insumos
- [ ] Agregar botones "Crear", "Editar", "Eliminar"
- [ ] Implementar confirmación de eliminación
- [ ] Agregar loading states y error handling

#### **Tarea 2.4: Crear CreateInsumoScreen**
- [ ] Crear archivo `frontend/src/screens/CreateInsumoScreen.js`
- [ ] Implementar formulario con campos:
  - Nombre del insumo
  - Cantidad disponible
  - Unidad de medida (select con opciones comunes)
  - Costo unitario de compra
- [ ] Agregar validaciones de formulario
- [ ] Implementar navegación de regreso

#### **Tarea 2.5: Crear EditInsumoScreen**
- [ ] Crear archivo `frontend/src/screens/EditInsumoScreen.js`
- [ ] Cargar datos del insumo existente
- [ ] Implementar formulario de edición
- [ ] Agregar validaciones
- [ ] Implementar navegación

### **Día 5: Integración en Productos**

#### **Tarea 2.6: Modificar CreateProductScreen**
- [ ] Agregar sección "Insumos del Producto"
- [ ] Implementar botón "Añadir Insumo"
- [ ] Crear modal/sección para seleccionar insumo y cantidad
- [ ] Mostrar lista de insumos asociados
- [ ] Mostrar COGS y Precio Sugerido calculados
- [ ] Permitir eliminar insumos asociados

#### **Tarea 2.7: Modificar EditProductScreen**
- [ ] Cargar insumos asociados existentes
- [ ] Implementar funcionalidad de edición de insumos
- [ ] Mostrar COGS y Precio Sugerido actualizados
- [ ] Mantener funcionalidad existente

### **Día 6-7: Navegación y Testing**

#### **Tarea 2.8: Actualizar Navegación**
- [ ] Modificar `frontend/src/App.js` para incluir rutas de insumos
- [ ] Agregar botón "Gestionar Insumos" en `DashboardScreen.js`
- [ ] Verificar navegación entre pantallas
- [ ] Probar rutas protegidas

#### **Tarea 2.9: Testing Frontend**
- [ ] Probar creación de insumos
- [ ] Probar edición de insumos
- [ ] Probar eliminación de insumos
- [ ] Probar asociación con productos
- [ ] Verificar cálculos de COGS y precio sugerido
- [ ] Probar validaciones de formularios

#### **Tarea 2.10: UI/UX Improvements**
- [ ] Verificar responsive design
- [ ] Agregar tooltips explicativos
- [ ] Mejorar mensajes de error
- [ ] Optimizar loading states

---

## 🧮 **LÓGICA DE CÁLCULOS**

### **Cálculo de COGS (Cost of Goods Sold):**
```python
def calculate_cogs(producto_id: UUID, db: Session) -> float:
    """
    Calcula el costo de bienes vendidos basado en los insumos asociados
    """
    producto_insumos = db.query(ProductoInsumo).filter(
        ProductoInsumo.producto_id == producto_id
    ).all()
    
    total_cogs = 0.0
    for pi in producto_insumos:
        insumo = db.query(Insumo).filter(Insumo.id == pi.insumo_id).first()
        if insumo:
            costo_insumo = pi.cantidad_necesaria * insumo.costo_unitario_compra
            total_cogs += costo_insumo
    
    return total_cogs
```

### **Cálculo de Precio Sugerido:**
```python
def calculate_suggested_price(cogs: float, margin_percentage: float = 30.0) -> float:
    """
    Calcula el precio sugerido basado en COGS y margen de ganancia
    """
    if cogs <= 0:
        return 0.0
    
    margin_decimal = margin_percentage / 100.0
    precio_sugerido = cogs / (1 - margin_decimal)
    
    return round(precio_sugerido, 2)
```

---

## 🧪 **CASOS DE PRUEBA**

### **Casos de Prueba para Insumos:**
1. **Crear insumo válido** - Debe guardarse correctamente
2. **Crear insumo con datos inválidos** - Debe mostrar errores de validación
3. **Editar insumo existente** - Debe actualizar datos correctamente
4. **Eliminar insumo sin productos asociados** - Debe eliminarse
5. **Eliminar insumo con productos asociados** - Debe mostrar error o eliminar en cascada

### **Casos de Prueba para Cálculos:**
1. **Producto sin insumos** - COGS = 0, Precio Sugerido = 0
2. **Producto con un insumo** - Cálculo directo
3. **Producto con múltiples insumos** - Suma de todos los costos
4. **Insumo con costo cero** - No debe afectar cálculo
5. **Cantidad necesaria cero** - No debe afectar cálculo

### **Casos de Prueba para UI:**
1. **Navegación completa** - Todas las pantallas accesibles
2. **Formularios** - Validaciones funcionando
3. **Cálculos en tiempo real** - COGS y precio sugerido se actualizan
4. **Responsive design** - Funciona en móviles
5. **Error handling** - Mensajes claros de error

---

## ✅ **CRITERIOS DE ACEPTACIÓN**

### **Backend:**
- [ ] Todos los endpoints funcionan correctamente
- [ ] Cálculos de COGS son precisos
- [ ] Cálculos de precio sugerido son precisos
- [ ] Validaciones de datos funcionan
- [ ] Integridad referencial se mantiene
- [ ] Tests pasan al 100%

### **Frontend:**
- [ ] Todas las pantallas se renderizan correctamente
- [ ] Formularios validan datos correctamente
- [ ] Cálculos se muestran en tiempo real
- [ ] Navegación funciona sin errores
- [ ] UI es responsive
- [ ] Error handling es claro

### **Integración:**
- [ ] Backend y frontend se comunican correctamente
- [ ] Datos se sincronizan entre pantallas
- [ ] Cálculos se actualizan automáticamente
- [ ] No hay errores de consola
- [ ] Performance es aceptable

---

## 🚨 **RIESGOS Y MITIGACIONES**

### **Riesgos Técnicos:**
- **Complejidad de cálculos** - Implementar tests exhaustivos
- **Performance con muchos insumos** - Implementar paginación si es necesario
- **Precisión de cálculos** - Usar decimales para cálculos financieros

### **Riesgos de UX:**
- **Confusión con unidades** - Agregar tooltips y ejemplos
- **Cálculos no claros** - Mostrar desglose detallado
- **Formularios complejos** - Validación en tiempo real

---

## 📝 **NOTAS DE DESARROLLO**

### **Decisiones Técnicas:**
- Usar `Float` para cantidades y costos (considerar `Decimal` para producción)
- Implementar soft delete para insumos (marcar como inactivo en lugar de eliminar)
- Considerar cache para cálculos frecuentes

### **Mejoras Futuras:**
- Historial de cambios de precios de insumos
- Alertas de stock bajo
- Importación masiva de insumos
- Categorización de insumos

---

**Responsable:** Equipo de Desarrollo  
**Revisor:** Líder Técnico  
**Fecha de Inicio:** 7 de Julio de 2025  
**Fecha de Finalización:** 20 de Julio de 2025 