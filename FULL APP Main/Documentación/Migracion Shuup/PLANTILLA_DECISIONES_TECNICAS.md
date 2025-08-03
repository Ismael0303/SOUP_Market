# Plantilla de Registro de Decisiones Técnicas

## Formato sugerido
- **Fecha:**
- **Responsable:**
- **Descripción de la decisión:**
- **Motivo:**
- **Alternativas consideradas:**
- **Impacto esperado:**
- **Referencias/documentos relacionados:**

---

## Ejemplo
- **Fecha:** 2025-08-02
- **Responsable:** Ismael
- **Descripción:** Se decide mantener la autenticación JWT en FastAPI y sincronizar usuarios con Shuup solo cuando sea necesario.
- **Motivo:** Minimizar cambios en el flujo de login y aprovechar la lógica existente.
- **Alternativas:** Migrar autenticación completamente a Shuup.
- **Impacto:** Menor riesgo de bugs en login, pero requiere lógica de sincronización.
- **Referencias:** historial de cursor, documentación de Shuup. 