# Historial de cambios impulsados por Codex

Los siguientes commits incluyen la palabra "codex" en su mensaje:

- **7d50eaa** (2025-08-04): Use public API in listing screen  
  - *Áreas*: backend (models, schemas), frontend (PublicListingScreen)  
  - *Motivo*: reemplazar datos mock por llamadas reales a la API.

- **5606961** (2025-08-04): Integrate carrito API for POS and update venta payload  
  - *Áreas*: backend (venta_router), frontend (ventaApi, POSScreen)  
  - *Motivo*: sustituir CartContext con endpoints reales.

- **b35f844** (2025-08-04): Use public API in business landing  
  - *Áreas*: frontend (BusinessLandingScreen)  
  - *Motivo*: quitar carga de datos mock y consumir API pública.

- **2143953** (2025-08-04): feat: connect product creation to API  
  - *Áreas*: frontend (CreateProductScreen)  
  - *Motivo*: enlazar el formulario de creación con la API.

- **9aaf416** (2025-08-03): test: cover MessageBox empty message handling and type classes  
  - *Áreas*: frontend/tests  
  - *Motivo*: asegurar manejo correcto de mensajes vacíos y clases según tipo.

- **2f72c1f** (2025-08-03): Fix notification clearing by tracking IDs  
  - *Áreas*: frontend (utils/notifications)  
  - *Motivo*: limpiar notificaciones usando IDs para evitar persistencia.

- **4b1ffa4** (2025-08-03): fix: usar sesión como unidad de venta  
  - *Áreas*: frontend (CreateProductScreen)  
  - *Motivo*: ajustar arreglo de unidades a sesión.

- **27871e0** (2025-08-03): fix: replace deprecated query.get usage  
  - *Áreas*: backend (crud), tests  
  - *Motivo*: corregir bug crítico por uso de query.get obsoleto.

### Resumen de áreas
- **Backend**: se ajustaron modelos y routers para soportar nuevas llamadas a la API y corregir consultas obsoletas.
- **Frontend**: se reemplazó el uso de datos mock por peticiones reales, se mejoró la gestión de notificaciones y se cubrieron componentes con pruebas.
- **Documentación**: no se registraron cambios en estos commits.

