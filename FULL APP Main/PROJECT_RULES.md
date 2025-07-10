# 📚 REGLAS DEL PROYECTO SOUP EMPRENDIMIENTOS

Este documento define las reglas, convenciones y buenas prácticas para el desarrollo y mantenimiento de SOUP Emprendimientos (Full Stack FastAPI + React).

---

## Índice rápido

- [1. Estructura de Carpetas](#1-estructura-de-carpetas)
- [2. Convenciones de Nombres](#2-convenciones-de-nombres)
- [3. Documentación](#3-documentación)
- [4. Uso de Git](#4-uso-de-git)
- [5. Scripts y Automatizaciones](#5-scripts-y-automatizaciones)
- [6. Estilo de Código](#6-estilo-de-código)
- [7. Testing](#7-testing)
- [8. Buenas Prácticas Generales](#8-buenas-prácticas-generales)
- [9. Convenciones Internas del Proyecto](#9-convenciones-internas-del-proyecto)

---

## 1. Estructura de Carpetas

| Carpeta         | Propósito principal                                      |
|----------------|---------------------------------------------------------|
| backend/       | Código backend (FastAPI, scripts, migraciones, tests)    |
| frontend/      | Código frontend (React, componentes, pantallas, estilos) |
| debugging/     | Herramientas, scripts y documentación de soporte         |
| Documentación/ | Documentación técnica y roadmap                          |
| Tutoriales/    | Ejemplos y tutoriales                                    |

Mantén la estructura. Si agregas nuevas carpetas, documenta su propósito.

---

## 2. Convenciones de Nombres

| Contexto           | Ejemplo correcto         | Ejemplo incorrecto      |
|--------------------|-------------------------|-------------------------|
| Python variable    | user_id                 | userId                  |
| Python clase       | UserProfile             | user_profile            |
| JS componente      | ProductCard.jsx         | productcard.jsx         |
| JS función         | fetchData               | fetch_data              |
| Endpoint API       | /api/products/          | /api/Products           |

- **Python:**
  - Variables y funciones: `snake_case`
  - Clases: `CamelCase`
  - Archivos: `snake_case.py`
- **JavaScript/React:**
  - Componentes: `PascalCase.jsx`
  - Funciones/variables: `camelCase`
  - Archivos utilitarios: `camelCase.js`
- **Endpoints API:**
  - Usar inglés, plural y minúsculas: `/api/products/`, `/api/businesses/`

---

## 3. Documentación

- Mantén actualizada la documentación en [`Documentación/DOCUMENTACION_TECNICA.md`](Documentación/DOCUMENTACION_TECNICA.md).
- Usa los formatos exactos requeridos por los scripts automáticos (secciones `## 📋 FUNCIONALIDADES IMPLEMENTADAS` y `## 🔗 ENDPOINTS API`).
- Si modificas endpoints o funcionalidades, actualiza la documentación y ejecuta el script de actualización.
- No dupliques secciones. Si el script falla, revisa y corrige manualmente.
- Consulta el [PROTOCOLO_ACTUALIZACION_DOCUMENTACION.md](debugging/PROTOCOLO_ACTUALIZACION_DOCUMENTACION.md) para el flujo recomendado.

---

## 4. Uso de Git

- Crea ramas para nuevas funcionalidades o fixes: `feature/nombre`, `fix/nombre`.
- Commits claros y descriptivos (en español o inglés, pero sé consistente).
- Antes de hacer push, asegúrate de que la documentación y los tests estén actualizados.
- No subas archivos de entorno, contraseñas ni datos sensibles.

**Ejemplo de commit:**
```
git commit -m "fix: corrige bug en endpoint de productos y actualiza documentación"
```

---

## 5. Scripts y Automatizaciones

- Los scripts de [`debugging/scripts/`](debugging/scripts/) pueden modificar documentación y datos. Úsalos con precaución.
- Antes de ejecutar scripts que modifican archivos, haz un commit previo.
- Si un script requiere un formato específico, respétalo (ver sección 3).

**Ejemplo de uso seguro:**
```
git add .
git commit -m "backup antes de actualizar documentación"
python debugging/scripts/actualizar_documentacion.py
```

---

## 6. Estilo de Código

- **Python:** Usa `black` o `autopep8` para formatear.
- **JavaScript/React:** Usa `prettier` y/o `eslint`.
- Mantén el código limpio, con comentarios útiles y sin código muerto.

**Ejemplo de formateo:**
```
black backend/app/
prettier --write frontend/src/
```

---

## 7. Testing

- Los tests están en [`debugging/tests/`](debugging/tests/) (backend).
- Agrega tests para nuevas funcionalidades o fixes.
- Corre los tests antes de hacer push.

**Ejemplo de ejecución de tests:**
```
pytest debugging/tests/
```

---

## 8. Buenas Prácticas Generales

- Si tienes dudas sobre una convención, revisa este archivo o pregunta antes de decidir.
- Documenta cualquier cambio estructural relevante.
- Facilita el onboarding: deja instrucciones claras para nuevos colaboradores.
- Usa comentarios útiles y claros, evita comentarios obvios o redundantes.

---

## 9. Convenciones Internas del Proyecto

Este proyecto sigue convenciones internas detalladas en la sección ["📏 CONVENCIONES Y ESTÁNDARES"](Documentación/DOCUMENTACION_TECNICA.md#convenciones-y-estándares) de la documentación técnica. A continuación, se resumen los puntos clave:

### Nomenclatura
- **Backend:**
  - Modelos: PascalCase (Usuario, Negocio)
  - Schemas: PascalCase con sufijo (UsuarioCreate, NegocioResponse)
  - Funciones/variables: snake_case
  - Constantes: UPPER_SNAKE_CASE
  - Enums: PascalCase
- **Frontend:**
  - Componentes: PascalCase (LoginScreen)
  - Funciones/variables: camelCase
  - Constantes: UPPER_SNAKE_CASE

### Estructura de archivos
- Backend: modelos y schemas separados, routers y crud organizados por entidad.
- Frontend: componentes y pantallas en carpetas dedicadas, utilidades y contextos separados.

### Validaciones y buenas prácticas
- Campos requeridos: nombre (no vacío), email (válido), precio (>0), cantidades (>=0).
- Manejo de errores: usar HTTPException en backend y try/catch en frontend.
- Siempre validar datos antes de guardar en BD.
- Usar migraciones para cambios estructurales.
- Mantener consistencia en nombres y tipos.
- Documentar cambios relevantes.
- Probar endpoints tras modificaciones.

**Para detalles y ejemplos actualizados, consulta siempre la sección completa en la documentación técnica.**

---

**Actualiza este archivo si cambian las reglas o la estructura del proyecto.** 