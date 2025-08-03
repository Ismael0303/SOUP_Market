# Actualización Marketplace SOUP

## Estructura de la actualización

- `CartContext.js`: Contexto global de carrito para el marketplace
- `CartDrawer.js`: Componente visual para mostrar y gestionar el carrito
- `BusinessLandingScreen.js`: Landing de negocio con catálogo, carrito y recomendaciones IA

## Hoja de ruta de integración

1. Integra `CartContext` en el árbol principal de la app (ej: envolver en App.js o PublicListingScreen.js)
2. Usa `CartDrawer` para mostrar el carrito en el marketplace y en la landing de negocio
3. Actualiza las cards de producto para permitir agregar al carrito
4. Implementa la navegación a `BusinessLandingScreen` desde las cards de negocio
5. Integra y conecta el componente `AIRecommender` en el marketplace y la landing
6. Asegura el filtrado funcional de productos y negocios
7. Haz funcional el botón de login y la gestión de usuario

## Notas
- Todos los archivos de esta actualización están en `Documentación/Actualizacion Marketplace/` para facilitar pruebas y migración.
- Adapta los imports según la estructura final del frontend. 