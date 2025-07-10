#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analizar automáticamente el estado del proyecto SOUP Emprendimientos
Este script es ejecutado por Cursor al iniciar para entender el contexto actual
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any

class AnalizadorProyecto:
    def __init__(self):
        self.root_dir = Path.cwd()
        self.report = {
            "fecha_analisis": datetime.datetime.now().isoformat(),
            "estado_proyecto": {},
            "tareas_prioritarias": [],
            "archivos_criticos": {},
            "historial_reciente": [],
            "recomendaciones": []
        }
    
    def analizar_estructura_proyecto(self) -> Dict[str, Any]:
        """Analiza la estructura general del proyecto"""
        estructura = {
            "backend": self._verificar_backend(),
            "frontend": self._verificar_frontend(),
            "documentacion": self._verificar_documentacion(),
            "scripts": self._verificar_scripts()
        }
        return estructura
    
    def _verificar_backend(self) -> Dict[str, Any]:
        """Verifica el estado del backend"""
        backend_dir = self.root_dir / "backend"
        if not backend_dir.exists():
            return {"existe": False, "estado": "NO ENCONTRADO"}
        
        archivos_criticos = [
            "app/main.py",
            "app/models.py", 
            "app/schemas.py",
            "requirements.txt"
        ]
        
        archivos_encontrados = []
        for archivo in archivos_criticos:
            if (backend_dir / archivo).exists():
                archivos_encontrados.append(archivo)
        
        return {
            "existe": True,
            "archivos_criticos": archivos_encontrados,
            "estado": "COMPLETO" if len(archivos_encontrados) >= 3 else "INCOMPLETO"
        }
    
    def _verificar_frontend(self) -> Dict[str, Any]:
        """Verifica el estado del frontend"""
        frontend_dir = self.root_dir / "frontend"
        if not frontend_dir.exists():
            return {"existe": False, "estado": "NO ENCONTRADO"}
        
        archivos_criticos = [
            "src/App.js",
            "package.json",
            "src/screens/",
            "src/components/"
        ]
        
        archivos_encontrados = []
        for archivo in archivos_criticos:
            if (frontend_dir / archivo).exists():
                archivos_encontrados.append(archivo)
        
        return {
            "existe": True,
            "archivos_criticos": archivos_encontrados,
            "estado": "COMPLETO" if len(archivos_encontrados) >= 3 else "INCOMPLETO"
        }
    
    def _verificar_documentacion(self) -> Dict[str, Any]:
        """Verifica el estado de la documentación"""
        docs_dir = self.root_dir / "Documentación"
        if not docs_dir.exists():
            return {"existe": False, "estado": "NO ENCONTRADO"}
        
        carpetas_importantes = [
            "historial de cursor",
            "Actualizacion UI",
            "Roadmap"
        ]
        
        carpetas_encontradas = []
        for carpeta in carpetas_importantes:
            if (docs_dir / carpeta).exists():
                carpetas_encontradas.append(carpeta)
        
        return {
            "existe": True,
            "carpetas_importantes": carpetas_encontradas,
            "estado": "COMPLETA" if len(carpetas_encontradas) >= 2 else "INCOMPLETA"
        }
    
    def _verificar_scripts(self) -> Dict[str, Any]:
        """Verifica los scripts disponibles"""
        scripts_dir = self.root_dir / "scripts"
        if not scripts_dir.exists():
            return {"existe": False, "estado": "NO ENCONTRADO"}
        
        scripts_importantes = [
            "analizar_estado_proyecto.py",
            "actualizar_documentacion.py",
            "check_db_structure.py"
        ]
        
        scripts_encontrados = []
        for script in scripts_importantes:
            if (scripts_dir / script).exists():
                scripts_encontrados.append(script)
        
        return {
            "existe": True,
            "scripts_importantes": scripts_encontrados,
            "estado": "DISPONIBLE"
        }
    
    def analizar_historial_reciente(self) -> List[Dict[str, Any]]:
        """Analiza el historial de chat más reciente"""
        historial_dir = self.root_dir / "Documentación" / "historial de cursor"
        if not historial_dir.exists():
            return []
        
        sesiones_dir = historial_dir / "sesiones"
        if not sesiones_dir.exists():
            return []
        
        sesiones = []
        for archivo in sesiones_dir.glob("sesion_*.md"):
            try:
                # Extraer fecha del nombre del archivo
                fecha_str = archivo.stem.replace("sesion_", "")
                fecha = datetime.datetime.strptime(fecha_str, "%Y%m%d_%H%M%S")
                
                # Leer contenido básico
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                sesiones.append({
                    "archivo": archivo.name,
                    "fecha": fecha.isoformat(),
                    "tamaño": len(contenido),
                    "lineas": len(contenido.split('\n'))
                })
            except Exception as e:
                print(f"Error leyendo {archivo}: {e}")
        
        # Ordenar por fecha (más reciente primero)
        sesiones.sort(key=lambda x: x["fecha"], reverse=True)
        return sesiones[:5]  # Solo las 5 más recientes
    
    def determinar_tareas_prioritarias(self) -> List[str]:
        """Determina las tareas prioritarias basándose en el análisis"""
        tareas = []
        
        # Verificar estado del frontend
        frontend = self._verificar_frontend()
        if frontend["existe"] and frontend["estado"] == "INCOMPLETO":
            tareas.append("Implementar mejoras de UI/UX del frontend")
        
        # Verificar scripts de actualización
        docs_dir = self.root_dir / "Documentación" / "Actualizacion UI"
        if docs_dir.exists():
            scripts_ui = list(docs_dir.glob("SCRIPT_*.js"))
            if scripts_ui:
                tareas.append("Ejecutar scripts de actualización de UI")
        
        # Verificar historial
        historial_dir = self.root_dir / "Documentación" / "historial de cursor"
        if historial_dir.exists():
            tareas.append("Revisar historial de desarrollo reciente")
        
        # Tareas por defecto
        if not tareas:
            tareas = [
                "Implementar Fase 1: Componentes UI base",
                "Actualizar pantalla POS según mockups Gemini",
                "Mejorar formularios de productos",
                "Rediseñar marketplace público"
            ]
        
        return tareas
    
    def generar_recomendaciones(self) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        recomendaciones = []
        
        # Verificar .cursorrules
        if not (self.root_dir / ".cursorrules").exists():
            recomendaciones.append("Crear archivo .cursorrules para configuración de Cursor")
        
        # Verificar historial
        historial_dir = self.root_dir / "Documentación" / "historial de cursor"
        if not historial_dir.exists():
            recomendaciones.append("Configurar sistema de historial de chat")
        
        # Verificar documentación
        docs_dir = self.root_dir / "Documentación"
        if not docs_dir.exists():
            recomendaciones.append("Crear estructura de documentación")
        
        # Recomendaciones generales
        recomendaciones.extend([
            "Revisar el historial de desarrollo antes de hacer cambios",
            "Seguir el plan de implementación fase por fase",
            "Mantener actualizado el índice de sesiones",
            "Priorizar las mejoras de UI/UX del frontend"
        ])
        
        return recomendaciones
    
    def analizar_completo(self) -> Dict[str, Any]:
        """Realiza el análisis completo del proyecto"""
        print("🔍 Analizando estado del proyecto SOUP Emprendimientos...")
        
        # Análisis de estructura
        self.report["estado_proyecto"] = self.analizar_estructura_proyecto()
        
        # Análisis de historial
        self.report["historial_reciente"] = self.analizar_historial_reciente()
        
        # Tareas prioritarias
        self.report["tareas_prioritarias"] = self.determinar_tareas_prioritarias()
        
        # Recomendaciones
        self.report["recomendaciones"] = self.generar_recomendaciones()
        
        # Archivos críticos
        self.report["archivos_criticos"] = {
            "backend": ["app/main.py", "app/models.py", "app/schemas.py"],
            "frontend": ["src/App.js", "src/screens/", "src/components/"],
            "documentacion": ["Documentación/historial de cursor/", "Documentación/Actualizacion UI/"],
            "configuracion": [".cursorrules", "PROJECT_RULES.md"]
        }
        
        return self.report
    
    def guardar_reporte(self, archivo: str = "reporte_estado_proyecto.json"):
        """Guarda el reporte en un archivo JSON"""
        reporte_path = self.root_dir / archivo
        with open(reporte_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Reporte guardado en: {reporte_path}")
        return reporte_path
    
    def mostrar_resumen(self):
        """Muestra un resumen del análisis en consola"""
        print("\n" + "="*60)
        print("📊 RESUMEN DEL ESTADO DEL PROYECTO")
        print("="*60)
        
        # Estado general
        estado = self.report["estado_proyecto"]
        print(f"\n🏗️  BACKEND: {estado['backend']['estado']}")
        print(f"🎨 FRONTEND: {estado['frontend']['estado']}")
        print(f"📚 DOCUMENTACIÓN: {estado['documentacion']['estado']}")
        print(f"🔧 SCRIPTS: {estado['scripts']['estado']}")
        
        # Tareas prioritarias
        print(f"\n🎯 TAREAS PRIORITARIAS:")
        for i, tarea in enumerate(self.report["tareas_prioritarias"], 1):
            print(f"  {i}. {tarea}")
        
        # Historial reciente
        if self.report["historial_reciente"]:
            print(f"\n📝 HISTORIAL RECIENTE:")
            for sesion in self.report["historial_reciente"][:3]:
                print(f"  • {sesion['archivo']} ({sesion['fecha'][:10]})")
        
        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES:")
        for i, rec in enumerate(self.report["recomendaciones"][:3], 1):
            print(f"  {i}. {rec}")
        
        print("\n" + "="*60)

def main():
    """Función principal del script"""
    analizador = AnalizadorProyecto()
    
    # Realizar análisis completo
    reporte = analizador.analizar_completo()
    
    # Mostrar resumen
    analizador.mostrar_resumen()
    
    # Guardar reporte
    archivo_reporte = analizador.guardar_reporte()
    
    print(f"\n✅ Análisis completado. Reporte guardado en: {archivo_reporte}")
    print("💡 Cursor puede usar este reporte para entender el estado del proyecto")

if __name__ == "__main__":
    main() 