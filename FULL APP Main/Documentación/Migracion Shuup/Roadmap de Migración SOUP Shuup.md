# Roadmap de Migración SOUP → Shuup (IA-Ready)

## **Reglas Generales del Proceso**

1. **Documentación Obligatoria:**  
   - Cada decisión de arquitectura, mapeo de modelos y cambio relevante debe documentarse en `Documentación/historial de cursor/` y en un archivo de decisiones técnicas.
2. **Commits Atómicos y Descriptivos:**  
   - Cada commit debe abordar una sola tarea y tener un mensaje claro, siguiendo la convención:  
     `feat: [área] breve descripción`  
     `fix: [área] breve descripción`  
     `docs: [área] breve descripción`
3. **Pruebas Automatizadas:**  
   - Todo endpoint nuevo o modificado debe tener pruebas unitarias y de integración.
4. **Backups y Rollback:**  
   - Antes de cada migración de datos o cambio mayor, realizar backup y documentar el procedimiento de rollback.
5. **Convenciones de Código:**  
   - Seguir las reglas de `PROJECT_RULES.md` y comentar en español.
6. **Tareas Desglosadas:**  
   - Cada tarea grande debe dividirse en subtareas pequeñas y ejecutables en menos de 1 día.
7. **Validación Continua:**  
   - Al finalizar cada fase, realizar una demo funcional y documentar los resultados.

---

## **Fases y Tareas**

### **Fase 0: Preparación y Seguridad**
- [ ] Backup completo de la base de datos actual.
- [ ] Crear rama de migración: `feature/shuup-migration`.
- [ ] Documentar el estado inicial del sistema.

**Pseudocódigo:**
```bash
# Backup
pg_dump -U soupuser -d soup_app_db > soup_backup_YYYYMMDD.sql

# Git
git checkout main
git pull origin main
git checkout -b feature/shuup-migration
```

---

### **Fase 1: Prototipo de Integración Shuup**
- [ ] Instalar Shuup con Docker Compose.
- [ ] Crear un endpoint FastAPI que consulte la API de Shuup y devuelva una lista de productos.
- [ ] Adaptar un componente React para mostrar estos productos.

**Pseudocódigo:**
```python
# FastAPI: routers/shuup_gateway.py
@router.get("/shuup/products")
def get_products():
    response = requests.get("http://shuup:8000/api/products/")
    return response.json()
```
```jsx
// React: src/screens/ProductsFromShuup.js
useEffect(() => {
  fetch('/api/shuup/products')
    .then(res => res.json())
    .then(setProducts);
}, []);
```

---

### **Fase 2: Mapeo y Migración de Modelos**
- [ ] Documentar el mapeo de modelos SOUP ↔ Shuup.
- [ ] Crear scripts de migración de datos.
- [ ] Validar integridad de datos migrados.

**Pseudocódigo:**
```python
# Script de migración
for negocio in negocios_soup:
    shop_data = map_negocio_to_shuup(negocio)
    requests.post("http://shuup:8000/api/shops/", json=shop_data)
```
```markdown
# Documentación/mapeo_modelos.md
| SOUP        | Shuup      | Notas                  |
|-------------|------------|------------------------|
| Usuario     | Customer   | tipo_tier: custom attr |
| Negocio     | Shop       | i18n: name, desc       |
| Producto    | Product    | i18n: name, desc       |
```

---

### **Fase 3: Adaptación del Backend (Gateway)**
- [ ] Refactorizar endpoints de negocio/producto para que usen Shuup.
- [ ] Mantener autenticación JWT y sincronización de usuarios.
- [ ] Pruebas de integración.

**Pseudocódigo:**
```python
# FastAPI: routers/product_router.py
@router.post("/products")
def create_product(product: ProductSchema):
    shuup_payload = map_product_to_shuup(product)
    response = requests.post("http://shuup:8000/api/products/", json=shuup_payload)
    return response.json()
```

---

### **Fase 4: Adaptación del Frontend**
- [ ] Modificar clientes API en React para consumir los nuevos endpoints.
- [ ] Implementar i18n con react-i18next.
- [ ] Añadir selector de idioma y archivos de traducción.

**Pseudocódigo:**
```jsx
// src/i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
i18n.use(initReactI18next).init({
  resources: { es: {...}, en: {...} },
  lng: "es",
  fallbackLng: "en",
});
```
```jsx
// src/components/LanguageSwitcher.jsx
<button onClick={() => i18n.changeLanguage('en')}>EN</button>
<button onClick={() => i18n.changeLanguage('es')}>ES</button>
```

---

### **Fase 5: Funcionalidades Avanzadas**
- [ ] Integrar pasarela de pagos (Mercado Pago).
- [ ] Integrar mensajería interna (Matrix).
- [ ] Integrar traducción automática (LibreTranslate).

**Pseudocódigo:**
```python
# FastAPI: crear preferencia de pago Mercado Pago
def crear_preferencia_pago(order):
    payload = {...}
    response = requests.post("https://api.mercadopago.com/checkout/preferences", json=payload)
    return response.json()
```
```jsx
// React: función para traducir texto con LibreTranslate
async function traducir(texto, targetLang) {
  const res = await fetch('http://localhost:5000/translate', {
    method: 'POST',
    body: JSON.stringify({ q: texto, source: 'es', target: targetLang }),
    headers: { 'Content-Type': 'application/json' }
  });
  return (await res.json()).translatedText;
}
```

---

### **Fase 6: Testing y Lanzamiento**
- [ ] Pruebas funcionales y de idioma.
- [ ] Validación con usuarios beta.
- [ ] Documentar el proceso de despliegue y rollback.
- [ ] Lanzamiento beta.

---

## **Convenciones para Agentes de IA**

- **Siempre documentar cada paso en la carpeta `Documentación/historial de cursor/` y actualizar el índice.**
- **Antes de ejecutar scripts de migración o cambios masivos, pedir confirmación y documentar el plan de rollback.**
- **Al crear o modificar endpoints, incluir ejemplos de request/response en la documentación.**
- **Al finalizar cada fase, generar un resumen de avances y lecciones aprendidas.**
- **Usar comentarios en español y explicar la lógica de cada función compleja.**
- **Dividir tareas grandes en subtareas y marcar el estado (pendiente, en progreso, completado) en un archivo de seguimiento.**

---
