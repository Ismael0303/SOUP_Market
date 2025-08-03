# 📚 DOCUMENTACIÓN - EJEMPLOS Y TEMPLATES PARA TESTING

**Fecha:** 8 de Julio de 2025  
**Proyecto:** SOUP Emprendimientos - Full Stack (FastAPI + React)  
**Propósito:** Almacenar datos ficticios de referencia para testing y demostraciones

---

## 📋 ÍNDICE

1. [Visión General](#visión-general)
2. [Estructura del Directorio](#estructura-del-directorio)
3. [Estructura de Archivos de "Bot" (JSON)](#estructura-de-archivos-de-bot-json)
4. [Script de Carga de Ejemplos](#script-de-carga-de-ejemplos)
5. [Modo de Uso](#modo-de-uso)
6. [Beneficios Clave](#beneficios-clave)

---

## 💡 VISIÓN GENERAL

Este módulo introduce un nuevo directorio `Tutoriales/Ejemplos` que contendrá archivos JSON. Cada archivo representará un "bot" o un conjunto de datos ficticios completos (usuario, negocio, insumos, productos) que pueden ser cargados en la base de datos de SOUP.

Estos ejemplos servirán para:

- **Poblar rápidamente la base de datos** con datos realistas para pruebas de desarrollo
- **Proporcionar templates de referencia** para futuros usuarios o desarrolladores que deseen entender la estructura de datos y las relaciones
- **Facilitar demostraciones** de la aplicación con datos preexistentes

---

## 📁 ESTRUCTURA DEL DIRECTORIO

El nuevo directorio se ubicará en la raíz del proyecto, al mismo nivel que `backend/` y `frontend/`:

```
FULL APP Main/
├── backend/
├── frontend/
├── Tutoriales/
│   └── Ejemplos/
│       └── bots/
│           ├── bot_panadero.json
│           ├── bot_freelancer_disenador.json
│           └── ... (otros archivos de bot)
└── debugging/
    └── scripts/
        └── load_examples.py # Script para cargar los ejemplos
```

---

## 📄 ESTRUCTURA DE ARCHIVOS DE "BOT" (JSON)

Cada archivo JSON dentro de `Tutoriales/Ejemplos/bots/` representará un usuario ficticio ("bot") y todos sus datos asociados. La estructura será la siguiente:

```json
{
  "usuario": {
    "email": "panadero@ejemplo.com",
    "nombre": "Panadero Creativo",
    "password_raw": "passwordSeguro123",
    "tipo_tier": "microemprendimiento",
    "localizacion": "Buenos Aires, Argentina",
    "curriculum_vitae": null
  },
  "negocio": {
    "nombre": "Panadería Artesanal 'El Horno Mágico'",
    "descripcion": "Panes de masa madre, facturas y pastelería fina.",
    "tipo_negocio": "PRODUCTOS",
    "rubro": "Alimentos y Bebidas",
    "localizacion_geografica": "CABA, Argentina",
    "fotos_urls": [
      "https://placehold.co/600x400/FFD700/000000?text=Panaderia+El+Horno+Magico"
    ]
  },
  "insumos": [
    {
      "nombre": "Harina de Trigo 000",
      "cantidad_disponible": 50.0,
      "unidad_medida_compra": "kg",
      "costo_unitario_compra": 0.8
    },
    {
      "nombre": "Levadura Fresca",
      "cantidad_disponible": 2.0,
      "unidad_medida_compra": "kg",
      "costo_unitario_compra": 2.5
    },
    {
      "nombre": "Azúcar Blanca",
      "cantidad_disponible": 25.0,
      "unidad_medida_compra": "kg",
      "costo_unitario_compra": 1.2
    }
  ],
  "productos": [
    {
      "nombre": "Pan de Masa Madre Integral",
      "descripcion": "Pan artesanal de masa madre con harina integral.",
      "precio": 3.0,
      "tipo_producto": "PHYSICAL_GOOD",
      "precio_venta": 6.5,
      "margen_ganancia_sugerido": 100.0,
      "insumos_asociados": [
        {
          "insumo_nombre": "Harina de Trigo 000",
          "cantidad_necesaria": 0.5
        },
        {
          "insumo_nombre": "Levadura Fresca",
          "cantidad_necesaria": 0.01
        }
      ]
    },
    {
      "nombre": "Facturas Mixtas x Docena",
      "descripcion": "Surtido de facturas frescas, ideales para el desayuno.",
      "precio": 5.0,
      "tipo_producto": "PHYSICAL_GOOD",
      "precio_venta": 12.0,
      "margen_ganancia_sugerido": 120.0,
      "insumos_asociados": [
        {
          "insumo_nombre": "Harina de Trigo 000",
          "cantidad_necesaria": 0.8
        },
        {
          "insumo_nombre": "Azúcar Blanca",
          "cantidad_necesaria": 0.1
        }
      ]
    }
  ]
}
```

### **Notas sobre la estructura JSON:**

- **`password_raw`**: Se usará para hashear la contraseña al cargar
- **`insumos_asociados` en productos**: Se referenciará por `insumo_nombre` en lugar de `insumo_id` para facilitar la creación del template. El script de carga buscará el `insumo_id` correspondiente después de crear los insumos

---

## 🐍 SCRIPT DE CARGA DE EJEMPLOS

Se creará un script Python llamado `load_examples.py` en `debugging/scripts/`. Este script será responsable de:

1. **Iterar sobre todos los archivos JSON** en `Tutoriales/Ejemplos/bots/`
2. **Leer el contenido** de cada archivo JSON
3. **Utilizar las funciones CRUD** del backend (`create_user`, `create_business`, `create_insumo`, `create_product`) para insertar los datos en la base de datos
4. **Manejar las relaciones**:
   - Asociar el negocio al usuario creado
   - Asociar los insumos al usuario creado
   - Asociar los productos al negocio y usuario creados

**Importante**: Al asociar insumos a productos, el script deberá buscar el `insumo_id` del insumo recién creado basándose en su nombre.

---

## 🚀 MODO DE USO

Para cargar los datos de ejemplo en tu base de datos:

1. **Asegúrate de que tu base de datos PostgreSQL** esté corriendo y accesible
2. **Asegúrate de que el backend** esté configurado para conectarse a la base de datos correcta
3. **Desde la raíz de tu proyecto** (`FULL APP Main/`), ejecuta el script:
   ```bash
   python debugging/scripts/load_examples.py
   ```
4. **El script imprimirá el progreso** y confirmará la carga de cada bot
5. **Una vez cargados**, podrás iniciar el backend y frontend para ver los datos de ejemplo en la aplicación

---

## ✅ BENEFICIOS CLAVE

### **Agilidad en el Desarrollo**
- Configuración de entornos de prueba en segundos
- Datos consistentes y predecibles para testing

### **Demostraciones Robustas**
- Presenta la aplicación con datos significativos y relaciones complejas
- Casos de uso realistas para mostrar funcionalidades

### **Documentación Viva**
- Los archivos JSON sirven como ejemplos prácticos de la estructura de datos
- Templates reutilizables para diferentes tipos de negocio

### **Consistencia**
- Asegura que los datos de prueba sigan un formato predefinido
- Evita errores de configuración manual

### **Facilidad de Extensión**
- Añadir nuevos bots es tan simple como crear un nuevo archivo JSON
- Escalable para diferentes tipos de emprendimientos

---

## 📝 PRÓXIMOS PASOS

1. **Crear archivos JSON de ejemplo** para diferentes tipos de negocios
2. **Desarrollar el script de carga** con manejo de errores robusto
3. **Documentar casos de uso específicos** para cada tipo de bot
4. **Integrar con el sistema de testing** automatizado

---

**Última actualización:** 8 de Julio de 2025  
**Responsable:** Equipo de Desarrollo SOUP  
**Estado:** En Desarrollo 