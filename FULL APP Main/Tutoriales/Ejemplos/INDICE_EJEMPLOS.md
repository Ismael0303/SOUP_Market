# 📋 ÍNDICE DE EJEMPLOS Y TEMPLATES - SOUP Emprendimientos

**Fecha:** 8 de Julio de 2025  
**Propósito:** Guía rápida para ejemplos y templates de testing

---

## 🎯 **RESUMEN**

Este directorio contiene ejemplos completos de datos ficticios ("bots") que pueden ser cargados en la base de datos de SOUP para testing, desarrollo y demostraciones.

---

## 📁 **ESTRUCTURA DE ARCHIVOS**

```
Tutoriales/Ejemplos/
├── README_EJEMPLOS.md          # Documentación principal
├── INDICE_EJEMPLOS.md          # Este archivo
└── bots/                       # Archivos JSON de ejemplos
    ├── bot_panadero.json       # Panadería artesanal
    ├── bot_freelancer_disenador.json  # Diseñador gráfico
    └── ... (futuros ejemplos)
```

---

## 🤖 **BOTS DISPONIBLES**

### **1. Bot Panadero** (`bot_panadero.json`)
- **Tipo:** Microemprendimiento - Alimentos
- **Usuario:** panadero@ejemplo.com
- **Negocio:** Panadería Artesanal 'El Horno Mágico'
- **Insumos:** 10 tipos (harinas, levadura, azúcar, etc.)
- **Productos:** 5 productos (panes, facturas, tortas)
- **Características:** Ejemplo completo de negocio de productos físicos

### **2. Bot Freelancer Diseñador** (`bot_freelancer_disenador.json`)
- **Tipo:** Freelancer - Diseño y Tecnología
- **Usuario:** disenador@ejemplo.com
- **Negocio:** Estudio de Diseño 'Pixel Perfect'
- **Insumos:** 10 tipos (licencias, hosting, energía, etc.)
- **Productos:** 6 servicios (logos, branding, web, UX/UI)
- **Características:** Ejemplo de servicios profesionales

---

## 🚀 **CÓMO USAR**

### **Cargar Ejemplos:**
```bash
# Desde la raíz del proyecto
python debugging/scripts/load_examples.py
```

### **Verificar Carga:**
1. Iniciar el backend: `cd backend && python main.py`
2. Iniciar el frontend: `cd frontend && npm start`
3. Navegar a la aplicación y verificar datos

### **Credenciales de Acceso:**
- **Panadero:** panadero@ejemplo.com / passwordSeguro123
- **Diseñador:** disenador@ejemplo.com / passwordSeguro123

---

## 📊 **ESTADÍSTICAS DE DATOS**

### **Bot Panadero:**
- **Insumos:** 10 tipos diferentes
- **Productos:** 5 productos con insumos asociados
- **Cálculos:** COGS y precios sugeridos incluidos
- **Relaciones:** Productos con múltiples insumos

### **Bot Diseñador:**
- **Insumos:** 10 tipos (servicios digitales)
- **Productos:** 6 servicios profesionales
- **Cálculos:** Costos por hora y proyecto
- **Relaciones:** Servicios con insumos de tiempo y recursos

---

## 🔧 **ESTRUCTURA JSON**

Cada archivo JSON contiene:

```json
{
  "usuario": {
    "email": "usuario@ejemplo.com",
    "nombre": "Nombre del Usuario",
    "password_raw": "contraseña",
    "tipo_tier": "microemprendimiento|freelancer|cliente",
    "localizacion": "Ubicación",
    "curriculum_vitae": "Descripción profesional"
  },
  "negocio": {
    "nombre": "Nombre del Negocio",
    "descripcion": "Descripción detallada",
    "tipo_negocio": "PRODUCTOS|SERVICIOS|AMBOS",
    "rubro": "Categoría del negocio",
    "localizacion_geografica": "Ubicación del negocio",
    "fotos_urls": ["url1", "url2"]
  },
  "insumos": [
    {
      "nombre": "Nombre del Insumo",
      "cantidad_disponible": 100.0,
      "unidad_medida_compra": "kg|litro|unidad|etc",
      "costo_unitario_compra": 1.5
    }
  ],
  "productos": [
    {
      "nombre": "Nombre del Producto",
      "descripcion": "Descripción del producto",
      "precio": 10.0,
      "tipo_producto": "PHYSICAL_GOOD|SERVICE_BY_HOUR|SERVICE_BY_PROJECT|DIGITAL_GOOD",
      "precio_venta": 25.0,
      "margen_ganancia_sugerido": 150.0,
      "insumos_asociados": [
        {
          "insumo_nombre": "Nombre del Insumo",
          "cantidad_necesaria": 2.0
        }
      ]
    }
  ]
}
```

---

## 🎨 **CASOS DE USO**

### **Desarrollo:**
- Testing de funcionalidades con datos realistas
- Verificación de cálculos de costos
- Pruebas de relaciones entre entidades

### **Demostraciones:**
- Presentaciones con datos significativos
- Casos de uso realistas
- Ejemplos de diferentes tipos de negocio

### **Documentación:**
- Templates para nuevos usuarios
- Ejemplos de estructura de datos
- Referencias para desarrolladores

---

## 🔄 **AGREGAR NUEVOS BOTS**

Para agregar un nuevo bot:

1. **Crear archivo JSON** en `Tutoriales/Ejemplos/bots/`
2. **Seguir la estructura** definida arriba
3. **Usar datos realistas** para el tipo de negocio
4. **Incluir relaciones** entre insumos y productos
5. **Documentar** en este índice

### **Tipos de Negocio Sugeridos:**
- **Restaurante:** Comida rápida o gourmet
- **Taller:** Mecánico, carpintero, costura
- **Consultoría:** Marketing, finanzas, legal
- **Educación:** Cursos, tutorías, talleres
- **Tecnología:** Desarrollo, soporte, hosting

---

## ⚠️ **NOTAS IMPORTANTES**

### **Seguridad:**
- Las contraseñas en los JSON son solo para testing
- No usar en producción
- Cambiar contraseñas después de cargar

### **Datos:**
- Todos los datos son ficticios
- Usar solo para desarrollo y testing
- No representan casos reales

### **Mantenimiento:**
- Actualizar ejemplos cuando cambie la estructura
- Mantener consistencia entre bots
- Documentar cambios en este índice

---

## 🛠️ **SCRIPT DE CARGA**

El script `load_examples.py` incluye:

- **Validación de datos** antes de cargar
- **Manejo de errores** robusto
- **Verificación de duplicados**
- **Relaciones automáticas** entre entidades
- **Logs detallados** del proceso

### **Características:**
- ✅ Carga usuarios con contraseñas hasheadas
- ✅ Crea negocios asociados a usuarios
- ✅ Carga insumos con costos realistas
- ✅ Crea productos con insumos asociados
- ✅ Calcula COGS y precios sugeridos
- ✅ Maneja errores y duplicados

---

**Última actualización:** 8 de Julio de 2025  
**Responsable:** Equipo de Desarrollo SOUP  
**Estado:** Activo 