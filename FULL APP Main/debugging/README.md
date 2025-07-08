# 🐛 CARPETA DE DEBUGGING - SOUP Emprendimientos

Esta carpeta contiene todos los archivos de debugging, testing y migración del proyecto SOUP Emprendimientos.

## 📁 Estructura de Carpetas

```
debugging/
├── scripts/           # Scripts de debugging y corrección de datos
├── migrations/        # Scripts de migración de base de datos
├── tests/            # Scripts de testing de endpoints y funcionalidades
├── HISTORIAL_DE_BUGS.md  # Historial completo de bugs y soluciones
└── README.md         # Este archivo
```

## 🔧 Scripts de Debugging (`scripts/`)

### **debug_business_data.py**
- **Propósito:** Verificar y mostrar datos de negocios en la base de datos
- **Uso:** `python debug_business_data.py`
- **Descripción:** Lista todos los negocios con sus campos principales

### **fix_product_data.py**
- **Propósito:** Corregir datos inválidos en productos
- **Uso:** `python fix_product_data.py`
- **Descripción:** Asigna precios válidos y negocio_id a productos con datos corruptos

### **check_enum_status.py**
- **Propósito:** Verificar el estado de los enums en la base de datos
- **Uso:** `python check_enum_status.py`
- **Descripción:** Muestra los valores actuales de business_type y product_type

### **recreate_enum.py**
- **Propósito:** Recrear enums con valores correctos
- **Uso:** `python recreate_enum.py`
- **Descripción:** Elimina y recrea los tipos enum con valores estándar

### **fix_enum_cache.py**
- **Propósito:** Limpiar cache de SQLAlchemy para enums
- **Uso:** `python fix_enum_cache.py`
- **Descripción:** Fuerza la recarga de metadatos de enums

## 🗄️ Migraciones (`migrations/`)

### **create_tables.py**
- **Propósito:** Crear todas las tablas de la base de datos
- **Uso:** `python create_tables.py`
- **Descripción:** Script inicial para crear la estructura de BD

### **migrate_to_new_models.py**
- **Propósito:** Migrar a nuevos modelos de datos
- **Uso:** `python migrate_to_new_models.py`
- **Descripción:** Actualiza la estructura de tablas existentes

### **migrate_add_tipo_negocio.py**
- **Propósito:** Agregar campo tipo_negocio a tabla negocios
- **Uso:** `python migrate_add_tipo_negocio.py`
- **Descripción:** Añade el enum business_type a la tabla

### **migrate_add_business_fields.py**
- **Propósito:** Agregar campos adicionales a negocios
- **Uso:** `python migrate_add_business_fields.py`
- **Descripción:** Añade rubro, localizacion_geografica y fotos_urls

### **migrate_add_product_fields.py**
- **Propósito:** Agregar campos adicionales a productos
- **Uso:** `python migrate_add_product_fields.py`
- **Descripción:** Añade campos de cálculo de precios

## 🧪 Tests (`tests/`)

### **test_register.py**
- **Propósito:** Probar el endpoint de registro de usuarios
- **Uso:** `python test_register.py`
- **Descripción:** Verifica el proceso de registro y validación

### **test_product_query.py**
- **Propósito:** Probar consultas de productos
- **Uso:** `python test_product_query.py`
- **Descripción:** Verifica queries complejas de productos

### **test_businesses_endpoint.py**
- **Propósito:** Probar endpoint de negocios
- **Uso:** `python test_businesses_endpoint.py`
- **Descripción:** Verifica respuestas del endpoint /businesses/me

### **test_products_endpoint.py**
- **Propósito:** Probar endpoint de productos
- **Uso:** `python test_products_endpoint.py`
- **Descripción:** Verifica respuestas del endpoint /products/me

### **test_simple_endpoint.py**
- **Propósito:** Probar endpoints básicos
- **Uso:** `python test_simple_endpoint.py`
- **Descripción:** Verifica endpoints públicos y autenticación

### **test_product_calculations.py**
- **Propósito:** Probar cálculos de productos
- **Uso:** `python test_product_calculations.py`
- **Descripción:** Verifica lógica de cálculo de precios y márgenes

## 🚀 Cómo Usar

### **Ejecutar Scripts de Debugging**
```bash
cd debugging/scripts
python nombre_del_script.py
```

### **Ejecutar Migraciones**
```bash
cd debugging/migrations
python nombre_migracion.py
```

### **Ejecutar Tests**
```bash
cd debugging/tests
python nombre_test.py
```

## ⚠️ Notas Importantes

1. **Siempre hacer backup** de la base de datos antes de ejecutar migraciones
2. **Verificar el entorno** - asegurarse de que las variables de entorno estén configuradas
3. **Revisar logs** - los scripts generan logs detallados para debugging
4. **Consultar el historial** - ver `HISTORIAL_DE_BUGS.md` para problemas conocidos

## 🔍 Debugging Automático

Para debugging automático basado en el historial:

1. **Identificar el problema** en `HISTORIAL_DE_BUGS.md`
2. **Encontrar la solución** correspondiente
3. **Ejecutar el script** de corrección apropiado
4. **Verificar la solución** con los tests correspondientes

## 📝 Mantenimiento

- **Actualizar el historial** cuando se encuentren nuevos bugs
- **Documentar nuevos scripts** en este README
- **Mantener versiones** de scripts importantes
- **Limpiar scripts obsoletos** periódicamente

---

**Última actualización:** 7 de Julio de 2025  
**Organización:** Scripts organizados por categoría 