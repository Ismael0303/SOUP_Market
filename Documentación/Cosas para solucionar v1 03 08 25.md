

# RESUMEN DE SUGERENCIAS Y RECOMENDACIONES - SOUP Emprendimientos

**Fecha:** 10 de Julio de 2025

---

## 1.  Revisión Detallada del Sistema de Ventas (`POSScreen.js`, `crud/venta.py`, `frontend/src/screens/SalesHistoryScreen.js`, `crud/product.py`)

### **1.1. `POSScreen.js`**

*   **Objetivo:** Asegurar que el flujo de ventas en el punto de venta se implemente correctamente y que los cálculos sean precisos.

    *   **Puntos Clave para Revisar:**
        1.  **Agregar productos al carrito (`addToCart(product)`):**
            *   **Sugerencia:** Considerar mostrar una confirmación visual al usuario cuando se agrega un producto.
                *   **Prioridad:** Media
                *   **Urgencia:** No urgente. Mejora la UX, pero no es crítico para el funcionamiento básico.
        2.  **Actualizar cantidades en el carrito (`updateQty(id, qty)`):**
            *   **Sugerencia:** Asegurarse de que el stock del producto sea actualizado *antes* de permitir que se agregue.
                *   **Prioridad:** Alta
                *   **Urgencia:** Urgente. Evita vender productos que no están disponibles.
        3.  **Función para Finalizar la Venta (`finalizarVenta()`):**
            *   **Sugerencia:** Implementar **Transacciones de Firestore** para asegurar la atomicidad de la operación (venta y actualización de stock).
                *   **Prioridad:** Alta
                *   **Urgencia:** Urgente. Evita inconsistencias en los datos.
            *   **Sugerencia:** Validar el stock *antes* de guardar la venta.
                *   **Prioridad:** Alta
                *   **Urgencia:** Urgente.  Evita vender productos que no están disponibles.
            *   **Sugerencia:** Considerar agregar un modal para confirmar la venta.
                *   **Prioridad:** Media
                *   **Urgencia:** No urgente. Mejora la UX, pero no es crítico.
            *   **Sugerencia:** Considerar agregar la posibilidad de agregar información del cliente.
                *   **Prioridad:** Baja
                *   **Urgencia:** No urgente.
        4.  **Categorías:** Evaluar si la lógica de las categorías es suficiente o si se requiere un buscador para mejorar la usabilidad.
                *   **Prioridad:** Media
                *   **Urgencia:** No urgente.
        5.  **Búsqueda:** Asegurar que la búsqueda sea eficiente.
                *   **Prioridad:** Media
                *   **Urgencia:** No urgente, pero deseable si se tienen muchos productos.
        6.  **Breadcrumbs:** Integrar los componentes de Breadcrumbs para mejorar la navegación.
            *   **Prioridad:** Baja
            *   **Urgencia:** No urgente.

    *   **Entregable:**
        *   Código fuente de `POSScreen.js`.

### **1.2.  `crud/venta.py`**

*   **Objetivo:** Garantizar que la lógica de creación de ventas, cálculo de totales y actualización de stock sea precisa y segura.

    *   **Puntos Clave para Revisar:**
        *   La función `create_venta()` es crítica.
        *   Verificar que se utilicen transacciones de base de datos.
            *   **Prioridad:** Alta
            *   **Urgencia:** Urgente.
        *   Verificar que se actualice el stock de productos correctamente.
            *   **Prioridad:** Alta
            *   **Urgencia:** Urgente.

    *   **Entregable:**
        *   Código fuente de `crud/venta.py`.

### **1.3.  `frontend/src/screens/SalesHistoryScreen.js`**

*   **Objetivo:** Asegurar que el historial de ventas se muestre correctamente y que los informes funcionen como se espera.

    *   **Puntos Clave para Revisar:**
        *   Verificar la conexión a la base de datos (Firestore).
            *   **Prioridad:** Alta
            *   **Urgencia:** Urgente.
        *   Verificar que se muestren correctamente las ventas del usuario.
            *   **Prioridad:** Alta
            *   **Urgencia:** Urgente.
        *   Verificar que la descarga de informes en formato CSV funcione.
            *   **Prioridad:** Media
            *   **Urgencia:** No urgente, pero deseable para el usuario.

    *   **Entregable:**
        *   Código fuente de `frontend/src/screens/SalesHistoryScreen.js`.

### **1.4. `crud/product.py`**

*   **Objetivo:** Asegurar que el stock de los productos se actualice correctamente.

    *   **Puntos Clave para Revisar:**
        *   La función `record_sale()` y `update_product_stock()` son críticas.
        *   Verificar que se actualice el stock de los productos cuando se registra una venta.
            *   **Prioridad:** Alta
            *   **Urgencia:** Urgente.

    *   **Entregable:**
        *   Código fuente de `crud/product.py`.

### **1.5.  Tests**

*   **Objetivo:** Validar que las funcionalidades del sistema de ventas funcionan correctamente.

    *   **Acción:**
        *   Ejecutar el script de pruebas (`test_sales_system.py`).
        *   Analizar los resultados de las pruebas.
            *   **Prioridad:** Alta
            *   **Urgencia:** Urgente.
    *   **Entregable:**
        *   Resultados de la ejecución del script `test_sales_system.py`.

## 2.  Integración de Roles y Permisos (`auth_router.py`, y aplicación en todos los endpoints)

*   **Objetivo:** Restringir el acceso a las funcionalidades del POS, el historial de ventas y los informes según el rol del usuario.

    *   **Puntos Clave:**
        *   Los roles se definen en el modelo `UserRole`.
        *   Usar decoradores (como `@app.get("/.../", dependencies=[Depends(get_current_user)])`) y, dentro de las funciones de las rutas, verificar el rol del usuario autenticado.
            *   **Prioridad:** Alta
            *   **Urgencia:** Urgente.

    *   **Implementación:**
        1.  **Identificar los Endpoints:** Identificar qué endpoints de la API requieren autenticación y autorización.
        2.  **Implementar Decoradores de Autorización:** Usar los roles definidos en el modelo `UserRole` para proteger los endpoints.

    *   **Ejemplo:**
        ```python
        from fastapi import Depends, HTTPException, status
        from app.dependencies import get_current_user
        from app.models import Usuario, UserRole

        @app.get("/products/", dependencies=[Depends(get_current_user)])
        async def read_products(current_user: Usuario = Depends(get_current_user)):
            if current_user.rol not in (UserRole.MANAGER, UserRole.ADMIN, UserRole.TRABAJADOR_ATENCION):  # Ejemplo de autorización basada en rol
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para acceder a este recurso")
            # ... el resto de la lógica ...
        ```

    *   **Entregable:**
        *   Código fuente de los endpoints de FastAPI que acceden a los CRUD.

## 3.  Continuar con el Capítulo 1 del Roadmap (Funcionalidades Específicas de la Panadería Ñiam)

*   **Objetivo:** Añadir funcionalidades específicas para la panadería Ñiam, como la gestión de insumos, la asociación de insumos a productos y el cálculo de costos.

    *   **Tareas:**
        1.  **Gestión de Insumos (Tareas 2.1, 2.2, 2.3 del Roadmap):**
            *   Refactorizar/Crear el modelo `ProductoInsumo`.
                *   **Prioridad:** Alta
                *   **Urgencia:** Urgente.  Base para el cálculo de costos.
            *   Revisar la implementación de `_sync_product_insumos` para que sea eficiente y robusta.
                *   **Prioridad:** Media
                *   **Urgencia:** No urgente, pero conveniente.
        2.  **Implementar el cálculo de COGS y precios sugeridos.** Asegurarse de que la lógica sea precisa.
                *   **Prioridad:** Alta
                *   **Urgencia:** Urgente.  Funcionalidad clave de la panadería.
        3.  **Implementar la Pantalla de Punto de Venta (POS) en el Frontend:**
            *   Crear `frontend/src/screens/SalePointScreen.js`.
                *   **Prioridad:** Alta
                *   **Urgencia:** Urgente.
            *   Integrar la lógica para seleccionar productos, ajustar cantidades y registrar ventas.
                *   **Prioridad:** Alta
                *   **Urgencia:** Urgente.
            *   Añadir la ruta en `frontend/src/App.js`.
                *   **Prioridad:** Alta
                *   **Urgencia:** Urgente.
        4.  **Añadir Campo `stock_terminado` al Modelo `Producto` en Backend:**
            *   Modificar `backend/app/models.py`.
                *   **Prioridad:** Alta
                *   **Urgencia:** Urgente.
            *   Crear migración para añadir este campo.
                *   **Prioridad:** Alta
                *   **Urgencia:** Urgente.
            *   Actualizar `backend/app/schemas.py` y `backend/app/crud/product.py` para manejar este campo.
                *   **Prioridad:** Alta
                *   **Urgencia:** Urgente.
        5.  **Implementar Lógica de Descuento de Stock de Productos Terminados y de Insumos al Vender:**
            *   Modificar `backend/app/crud/product.py` para que la función de registro de venta (o una nueva función) descuente `stock_terminado` del producto y `cantidad_disponible` de los insumos asociados.
                *   **Prioridad:** Alta
                *   **Urgencia:** Urgente.
        6.  **Actualizar `ManageProductsScreen.js` para mostrar `COGS`, `Precio Sugerido`, `Margen Real` y `stock_terminado`:**
            *   Mejorar la visualización en la lista de productos del emprendedor.
                *   **Prioridad:** Media
                *   **Urgencia:** No Urgente, pero deseable.

    *   **Entregable:**
        *   Código actualizado y funcionando de todos los módulos mencionados.

---

**Notas Adicionales:**

*   **Mantenimiento:**
    *   Documentar cualquier cambio o corrección en el `HISTORIAL_DE_BUGS.md`.
        *   **Prioridad:** Media
        *   **Urgencia:** No urgente.
    *   Mantener el código limpio y consistente.
        *   **Prioridad:** Media
        *   **Urgencia:** No urgente.
*   **Testing:**
    *   Ejecutar pruebas después de cada cambio.
        *   **Prioridad:** Alta
        *   **Urgencia:** Urgente.
    *   Asegurarse de que las pruebas cubran todos los casos de uso.
        *   **Prioridad:** Alta
        *   **Urgencia:** Urgente.
*   **Revisión de Código:**
    *   Realizar revisiones de código entre los miembros del equipo.
        *   **Prioridad:** Media
        *   **Urgencia:** No urgente, pero es una buena práctica.
---

Este documento proporciona una guía completa de las tareas pendientes y de los próximos pasos a seguir para el desarrollo de SOUP Emprendimientos.
```

**Resumen de prioridades y urgencia:**

*   **Alta y Urgente:** Implementación de transacciones, validación de stock, autenticación/autorización, revisión de la creación de ventas y actualizaciones de stock, migración de datos, visualización de stock en la lista de productos, y los tests.
*   **Alta y No Urgente:** Implementación de los campos de precios y la actualización del módulo de gestión de productos.
*   **Media y No Urgente:** La mayoría de las mejoras de la interfaz de usuario (UX), la generación de informes CSV, el uso de breadcrumbs, y las revisiones de código.
*   **Baja y No Urgente:** La información adicional del cliente en la venta.

---

**1.  Tareas que *Debes* Implementar *Antes* de la Migración:**

*   **Cálculos Precisos y Consistencia:**

    *   **Transacciones en `finalizarVenta()`:**  *Absolutamente necesario*. Asegura la integridad de las ventas. Si fallan las transacciones, no se debe crear la venta, ni modificar el stock. **Urgente**.
    *   **Validación del Stock en `finalizarVenta()`:**  *Absolutamente necesario*. Evita vender lo que no hay.  **Urgente**.
    *   **Verificación de Autenticación y Autorización:** Implementar la autenticación y autorización en los endpoints.  Esto es clave para la seguridad y el cumplimiento del Roadmap.  **Urgente**.

*   **Las Funcionalidades que Vas a Usar en el PMV de Shuup:**

    *   Si vas a usar el POS en Shuup, cualquier problema en la gestión de ventas (ej., si no se registra correctamente, si no actualiza el stock, si los precios son incorrectos, etc.) *debe* ser resuelto antes de migrar, de lo contrario, el PMV de Shuup tampoco funcionará.

**2.  Tareas que Podrías Posponer (pero con Cuidado) *Si* No las Necesitas en el PMV de Shuup:**

*   **Mejoras de la Interfaz de Usuario (UX):**

    *   Si el PMV de Shuup se enfoca en las funcionalidades centrales (ventas, gestión de productos), puedes posponer las mejoras de UX hasta después de la migración, porque no son críticos para el lanzamiento.

*   **Visualización del Stock en la Lista de Productos:**

    *   Si la administración de stock se va a realizar principalmente en Shuup, puedes posponer esta tarea.

*   **Añadir la información del cliente.**
*   **Añadir una mejor lógica de categorías o buscador.**
*   **Utilizar Breadcrumbs**

**3. Razones para Resolver los Problemas en SOUP *Antes* de la Migración (Aunque no sean Críticos para el PMV de Shuup):**

*   **Facilitar la Migración:** Un código base más limpio, consistente y bien probado facilita la migración.
*   **Evitar el Retrabajo:**  Si no resuelves estos problemas ahora, es probable que tengas que resolverlos en Shuup, o en una etapa posterior.
*   **Asegurar la Calidad de los Datos:** Si migras datos incorrectos o incompletos, tendrás problemas en Shuup.
*   **Reducir Riesgos:**  Un sistema más robusto y estable es menos propenso a errores durante la migración.

**4. Conclusión:**

*   **Prioriza:** Resolver los problemas de cálculos, consistencia y seguridad.
*   **Planifica con Cuidado:** Si decides posponer algo, asegúrate de documentarlo y de tener un plan para abordarlo después de la migración.

---

### Recomendaciones Específicas

Dada la estrategia de *migración progresiva* y que el PMV de Shuup seguramente se enfocará en la funcionalidad de ventas, sugiero que te centres en:

1.  **Implementar las Transacciones en `finalizarVenta()`**.
2.  **Implementar la validación del stock en  `finalizarVenta()`**.
3.  **Implementar la autenticación y autorización**.
4.  **Ejecutar los tests y ver que pasen todas las pruebas.**
5.  **Revisar y validar la consistencia de precios y stock.**

Una vez que tengas estas implementaciones, estarás en una posición mucho mejor para migrar a Shuup, porque tendrás una base estable y funcional.
