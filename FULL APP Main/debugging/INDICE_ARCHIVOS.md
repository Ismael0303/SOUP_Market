# 📋 ÍNDICE DE ARCHIVOS - Debugging

## 🔧 Scripts de Debugging (`scripts/`)

| Archivo | Propósito | Estado | Última Modificación |
|---------|-----------|--------|-------------------|
| `debug_business_data.py` | Verificar datos de negocios | ✅ Activo | 7/7/2025 |
| `fix_product_data.py` | Corregir datos corruptos de productos | ✅ Activo | 7/7/2025 |
| `check_enum_status.py` | Verificar estado de enums | ✅ Activo | 7/7/2025 |
| `recreate_enum.py` | Recrear enums con valores correctos | ✅ Activo | 7/7/2025 |
| `fix_enum_cache.py` | Limpiar cache de SQLAlchemy | ✅ Activo | 7/7/2025 |
| `debug_token.py` | Debugging de tokens JWT | ✅ Activo | 7/7/2025 |
| `debug_api_endpoints.py` | Debugging de endpoints API | ✅ Activo | 7/7/2025 |
| `debug_database.py` | Debugging de base de datos | ✅ Activo | 7/7/2025 |

## 🗄️ Migraciones (`migrations/`)

| Archivo | Propósito | Estado | Orden de Ejecución |
|---------|-----------|--------|-------------------|
| `create_tables.py` | Crear estructura inicial de BD | ✅ Ejecutado | 1º |
| `migrate_to_new_models.py` | Migrar a nuevos modelos | ✅ Ejecutado | 2º |
| `migrate_add_tipo_negocio.py` | Agregar enum business_type | ✅ Ejecutado | 3º |
| `migrate_add_business_fields.py` | Agregar campos adicionales a negocios | ✅ Ejecutado | 4º |
| `migrate_add_product_fields.py` | Agregar campos de cálculo a productos | ✅ Ejecutado | 5º |

## 🧪 Tests (`tests/`)

| Archivo | Propósito | Estado | Endpoint Testeado |
|---------|-----------|--------|------------------|
| `test_register.py` | Probar registro de usuarios | ✅ Funcional | POST /users/register |
| `test_product_query.py` | Probar consultas complejas | ✅ Funcional | Queries SQL |
| `test_businesses_endpoint.py` | Probar endpoint de negocios | ✅ Funcional | GET /businesses/me |
| `test_products_endpoint.py` | Probar endpoint de productos | ✅ Funcional | GET /products/me |
| `test_simple_endpoint.py` | Probar endpoints básicos | ✅ Funcional | Endpoints públicos |
| `test_product_calculations.py` | Probar cálculos de precios | ✅ Funcional | Lógica de negocio |

## 📚 Documentación

| Archivo | Propósito | Estado |
|---------|-----------|--------|
| `HISTORIAL_DE_BUGS.md` | Historial completo de bugs y soluciones | ✅ Actualizado |
| `README.md` | Guía de uso de la carpeta debugging | ✅ Actualizado |
| `INDICE_ARCHIVOS.md` | Este archivo de índice | ✅ Nuevo |

## 🔍 Búsqueda Rápida por Problema

### **Problemas de Enums**
- `check_enum_status.py` - Verificar estado
- `recreate_enum.py` - Recrear enums
- `fix_enum_cache.py` - Limpiar cache

### **Problemas de Datos**
- `debug_business_data.py` - Verificar negocios
- `fix_product_data.py` - Corregir productos
- `debug_database.py` - Debugging general de BD

### **Problemas de Autenticación**
- `debug_token.py` - Debugging de tokens JWT
- `test_register.py` - Probar registro
- `test_simple_endpoint.py` - Probar login

### **Problemas de API**
- `debug_api_endpoints.py` - Debugging de endpoints
- `test_businesses_endpoint.py` - Negocios
- `test_products_endpoint.py` - Productos

### **Problemas de Endpoints**
- `test_businesses_endpoint.py` - Negocios
- `test_products_endpoint.py` - Productos

### **Problemas de Base de Datos**
- `create_tables.py` - Crear estructura
- `migrate_to_new_models.py` - Migrar modelos

## 🚀 Comandos de Ejecución Rápida

### **Debugging General**
```bash
# Verificar estado de enums
python debugging/scripts/check_enum_status.py

# Verificar datos de negocios
python debugging/scripts/debug_business_data.py

# Corregir datos corruptos
python debugging/scripts/fix_product_data.py
```

### **Tests Rápidos**
```bash
# Probar registro
python debugging/tests/test_register.py

# Probar endpoints públicos
python debugging/tests/test_simple_endpoint.py

# Probar cálculos
python debugging/tests/test_product_calculations.py
```

### **Migraciones (Solo si es necesario)**
```bash
# Crear tablas (solo primera vez)
python debugging/migrations/create_tables.py

# Agregar campos a negocios
python debugging/migrations/migrate_add_business_fields.py
```

## ⚠️ Archivos Críticos

### **No Eliminar**
- `HISTORIAL_DE_BUGS.md` - Contiene soluciones históricas
- `create_tables.py` - Script de inicialización
- `fix_product_data.py` - Corrección de datos críticos

### **Usar con Precaución**
- `recreate_enum.py` - Modifica estructura de BD
- `migrate_to_new_models.py` - Cambios estructurales

### **Para Testing**
- Todos los archivos en `tests/` - Seguros de ejecutar
- `debug_business_data.py` - Solo lectura

## 📝 Notas de Mantenimiento

- **Actualizar este índice** cuando se agreguen nuevos archivos
- **Marcar archivos obsoletos** con ❌ en lugar de ✅
- **Documentar cambios** en el historial de bugs
- **Mantener orden cronológico** en las migraciones

---

**Última actualización:** 7 de Julio de 2025  
**Total de archivos:** 19 archivos organizados  
**Estado:** ✅ Completamente organizado 