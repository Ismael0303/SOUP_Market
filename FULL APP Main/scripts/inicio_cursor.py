#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicio para Cursor - SOUP Emprendimientos
Este script se ejecuta automáticamente cuando Cursor inicia el proyecto
"""

import os
import sys
import json
import datetime
from pathlib import Path

def cargar_contexto_proyecto():
    """Carga el contexto completo del proyecto para Cursor"""
    
    print("🚀 Iniciando Cursor - SOUP Emprendimientos")
    print("=" * 50)
    
    # Información básica del proyecto
    contexto = {
        "proyecto": "SOUP Emprendimientos",
        "descripcion": "Aplicación completa para gestión de negocios",
        "tecnologias": {
            "backend": "FastAPI + PostgreSQL",
            "frontend": "React + Tailwind CSS",
            "plugins": "Sistema modular de plugins"
        },
        "fecha_inicio": datetime.datetime.now().isoformat(),
        "estado_actual": "Desarrollo activo - Fase UI/UX"
    }
    
    return contexto

def verificar_archivos_criticos():
    """Verifica que existan los archivos críticos del proyecto"""
    
    archivos_criticos = [
        ".cursorrules",
        "PROJECT_RULES.md",
        "backend/app/main.py",
        "frontend/src/App.js",
        "Documentación/historial de cursor/README_HISTORIAL.md"
    ]
    
    archivos_faltantes = []
    archivos_encontrados = []
    
    for archivo in archivos_criticos:
        if Path(archivo).exists():
            archivos_encontrados.append(archivo)
        else:
            archivos_faltantes.append(archivo)
    
    return {
        "encontrados": archivos_encontrados,
        "faltantes": archivos_faltantes,
        "completo": len(archivos_faltantes) == 0
    }

def cargar_historial_reciente():
    """Carga el historial de desarrollo más reciente"""
    
    historial_dir = Path("Documentación/historial de cursor")
    if not historial_dir.exists():
        return {"error": "Directorio de historial no encontrado"}
    
    # Buscar la sesión más reciente
    sesiones_dir = historial_dir / "sesiones"
    if not sesiones_dir.exists():
        return {"error": "No hay sesiones registradas"}
    
    sesiones = list(sesiones_dir.glob("sesion_*.md"))
    if not sesiones:
        return {"error": "No se encontraron archivos de sesión"}
    
    # Obtener la sesión más reciente
    sesion_reciente = max(sesiones, key=lambda x: x.stat().st_mtime)
    
    try:
        with open(sesion_reciente, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        return {
            "archivo": sesion_reciente.name,
            "fecha_modificacion": datetime.datetime.fromtimestamp(sesion_reciente.stat().st_mtime).isoformat(),
            "tamaño": len(contenido),
            "resumen": extraer_resumen_sesion(contenido)
        }
    except Exception as e:
        return {"error": f"Error leyendo sesión: {e}"}

def extraer_resumen_sesion(contenido):
    """Extrae un resumen de la sesión del contenido"""
    
    lineas = contenido.split('\n')
    resumen = []
    
    for linea in lineas:
        if linea.startswith('## ') and 'Objetivo' in linea:
            resumen.append(linea)
        elif linea.startswith('### ') and any(palabra in linea for palabra in ['Acciones', 'Decisiones', 'Próximos']):
            resumen.append(linea)
        elif linea.startswith('- **') and len(resumen) < 10:
            resumen.append(linea)
    
    return resumen[:5]  # Solo las primeras 5 líneas relevantes

def determinar_tareas_actuales():
    """Determina las tareas actuales basándose en el estado del proyecto"""
    
    tareas = [
        {
            "prioridad": "ALTA",
            "tarea": "Implementar mejoras de UI/UX del frontend",
            "descripcion": "Actualizar el frontend según los mockups Gemini",
            "fase": "Fase 1 - Componentes Base"
        },
        {
            "prioridad": "ALTA", 
            "tarea": "Actualizar pantalla POS",
            "descripcion": "Rediseñar la pantalla de punto de venta",
            "fase": "Fase 2 - Pantallas Principales"
        },
        {
            "prioridad": "MEDIA",
            "tarea": "Mejorar formularios de productos",
            "descripcion": "Actualizar formularios según mockups",
            "fase": "Fase 2 - Pantallas Principales"
        },
        {
            "prioridad": "MEDIA",
            "tarea": "Rediseñar marketplace público",
            "descripcion": "Mejorar la experiencia del marketplace",
            "fase": "Fase 2 - Pantallas Principales"
        }
    ]
    
    return tareas

def generar_mensaje_bienvenida():
    """Genera el mensaje de bienvenida para Cursor"""
    
    contexto = cargar_contexto_proyecto()
    archivos = verificar_archivos_criticos()
    historial = cargar_historial_reciente()
    tareas = determinar_tareas_actuales()
    
    mensaje = f"""
🎉 ¡Bienvenido a SOUP Emprendimientos!

📋 CONTEXTO DEL PROYECTO:
   • Proyecto: {contexto['proyecto']}
   • Descripción: {contexto['descripcion']}
   • Backend: {contexto['tecnologias']['backend']}
   • Frontend: {contexto['tecnologias']['frontend']}
   • Estado: {contexto['estado_actual']}

📁 ARCHIVOS CRÍTICOS:
   • Encontrados: {len(archivos['encontrados'])}
   • Faltantes: {len(archivos['faltantes'])}
   • Estado: {'✅ COMPLETO' if archivos['completo'] else '⚠️ INCOMPLETO'}

📝 HISTORIAL RECIENTE:
"""
    
    if 'error' not in historial:
        mensaje += f"   • Última sesión: {historial['archivo']}\n"
        mensaje += f"   • Fecha: {historial['fecha_modificacion'][:10]}\n"
    else:
        mensaje += f"   • {historial['error']}\n"
    
    mensaje += f"""
🎯 TAREAS PRIORITARIAS:
"""
    
    for tarea in tareas[:3]:  # Solo las 3 más importantes
        mensaje += f"   • [{tarea['prioridad']}] {tarea['tarea']}\n"
    
    mensaje += f"""
💡 RECOMENDACIONES:
   1. Revisar el historial en Documentación/historial de cursor/
   2. Consultar los scripts en Documentación/Actualizacion UI/
   3. Seguir el plan de implementación fase por fase
   4. Mantener actualizado el historial de desarrollo

🚀 ¡Listo para continuar el desarrollo!
"""
    
    return mensaje

def main():
    """Función principal del script de inicio"""
    
    try:
        # Generar mensaje de bienvenida
        mensaje = generar_mensaje_bienvenida()
        print(mensaje)
        
        # Guardar contexto en archivo temporal para Cursor
        contexto_completo = {
            "mensaje_bienvenida": mensaje,
            "fecha_inicio": datetime.datetime.now().isoformat(),
            "archivos_criticos": verificar_archivos_criticos(),
            "historial_reciente": cargar_historial_reciente(),
            "tareas_actuales": determinar_tareas_actuales()
        }
        
        # Guardar en archivo temporal
        with open("cursor_context.json", "w", encoding="utf-8") as f:
            json.dump(contexto_completo, f, indent=2, ensure_ascii=False)
        
        print("✅ Contexto guardado en cursor_context.json")
        print("💡 Cursor puede usar este archivo para entender el estado del proyecto")
        
    except Exception as e:
        print(f"❌ Error en el script de inicio: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 