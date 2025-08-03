# Roadmap Simplificado de Migración a Shuup

## Objetivo
Migrar el marketplace de SOUP a Shuup, manteniendo la lógica propia solo donde sea necesario. Plazo estimado: 2 meses.

---

## Fase 0: Preparación (1-2 días)
- [ ] Realiza un backup completo de la base de datos PostgreSQL.
- [ ] Crea una nueva rama en Git para la migración.
- [ ] Lee la documentación de Shuup y revisa los modelos principales.

**Instrucción:**
- Usa el comando `pg_dump` para el backup.
- Rama sugerida: `feature/shuup-migration`.

---

## Fase 1: Instalación y Prototipo (1 semana)
- [ ] Instala Shuup usando Docker Compose.
- [ ] Asegúrate de que Shuup y su base de datos funcionen localmente.
- [ ] Crea un endpoint de prueba en FastAPI que consulte productos desde Shuup.
- [ ] Muestra esos productos en una pantalla de React.

**Instrucción:**
- Usa la documentación oficial de Shuup para la instalación.
- Prueba la conexión entre FastAPI y Shuup antes de avanzar.

---

## Fase 2: Mapeo y Migración de Datos (1 semana)
- [ ] Documenta cómo se mapean tus modelos actuales a los de Shuup.
- [ ] Escribe scripts para migrar usuarios, negocios y productos a Shuup.
- [ ] Valida que los datos migrados se ven correctamente en Shuup.

**Instrucción:**
- Usa la plantilla de mapeo en esta carpeta.
- Haz pruebas con pocos registros antes de migrar todo.

---

## Fase 3: Adaptación del Backend (1 semana)
- [ ] Modifica los endpoints de FastAPI para que usen Shuup en vez de la base de datos local para productos, negocios, encargos, etc.
- [ ] Mantén la autenticación y lógica de insumos en FastAPI si Shuup no lo cubre.
- [ ] Prueba todos los endpoints adaptados.

**Instrucción:**
- Comenta claramente en el código qué endpoints ahora usan Shuup.

---

## Fase 4: Adaptación del Frontend (1 semana)
- [ ] Modifica las funciones API en React para consumir los nuevos endpoints del backend.
- [ ] Asegúrate de que las pantallas principales (listados, creación, edición) funcionen con los datos de Shuup.
- [ ] Implementa el selector de idioma y archivos de traducción si es necesario.

**Instrucción:**
- Prueba cada pantalla después de cada cambio.

---

## Fase 5: Validación y Lanzamiento Beta (1 semana)
- [ ] Haz pruebas funcionales completas (crear, editar, listar, comprar, etc.).
- [ ] Pide feedback a usuarios clave.
- [ ] Prepara un plan de rollback por si algo falla.
- [ ] Lanza la beta y documenta el proceso.

**Instrucción:**
- Usa la plantilla de checklist y registro de avance en esta carpeta.

---

## Consejos
- Documenta cada decisión y problema en los archivos de esta carpeta.
- Si algo no funciona, vuelve a la última versión estable.
- Prioriza lo esencial para la beta, deja extras para después.

---

**¡Sigue este roadmap y marca cada tarea al completarla!** 