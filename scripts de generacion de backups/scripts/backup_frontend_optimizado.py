#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Backup Optimizado para Frontend - SOUP Emprendimientos
Excluye archivos que se pueden regenerar automáticamente
"""

import os
import sys
import shutil
import datetime
from pathlib import Path

def crear_backup_optimizado():
    """Crea un backup optimizado del frontend excluyendo archivos regenerables"""
    
    # Directorio raíz del proyecto
    root_dir = Path.cwd()
    frontend_dir = root_dir / "frontend"
    
    # Verificar que existe el directorio frontend
    if not frontend_dir.exists():
        print("❌ Error: No se encontró el directorio frontend")
        return False
    
    # Crear nombre del backup con timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"frontend_backup_optimizado_{timestamp}"
    backup_dir = root_dir / backup_name
    
    # Archivos y carpetas a EXCLUIR (se pueden regenerar)
    exclusiones = [
        "node_modules/",
        ".git/",
        "build/",
        "dist/",
        ".cache/",
        "coverage/",
        ".nyc_output/",
        "*.log",
        "*.tmp",
        "*.temp",
        ".DS_Store",
        "Thumbs.db",
        ".env.local",
        ".env.development.local",
        ".env.test.local",
        ".env.production.local"
    ]
    
    print(f"🚀 Creando backup optimizado: {backup_name}")
    print("=" * 50)
    
    try:
        # Crear directorio de backup
        backup_dir.mkdir(exist_ok=True)
        
        # Función para verificar si un archivo debe ser excluido
        def debe_excluir(ruta):
            ruta_str = str(ruta.relative_to(frontend_dir))
            for exclusion in exclusiones:
                if exclusion.endswith('/'):
                    # Es una carpeta
                    if ruta_str.startswith(exclusion[:-1]):
                        return True
                elif exclusion.startswith('*'):
                    # Es un patrón de archivo
                    if ruta.name.endswith(exclusion[1:]):
                        return True
                else:
                    # Es un archivo específico
                    if ruta_str == exclusion:
                        return True
            return False
        
        # Contadores
        archivos_copiados = 0
        archivos_excluidos = 0
        carpetas_excluidas = 0
        
        # Copiar archivos recursivamente
        for item in frontend_dir.rglob('*'):
            if item.is_file():
                # Calcular ruta relativa
                ruta_relativa = item.relative_to(frontend_dir)
                destino = backup_dir / ruta_relativa
                
                # Verificar si debe ser excluido
                if debe_excluir(item):
                    archivos_excluidos += 1
                    continue
                
                # Crear directorio padre si no existe
                destino.parent.mkdir(parents=True, exist_ok=True)
                
                # Copiar archivo
                shutil.copy2(item, destino)
                archivos_copiados += 1
                
                if archivos_copiados % 100 == 0:
                    print(f"  📁 Copiados: {archivos_copiados} archivos...")
            
            elif item.is_dir():
                # Verificar si la carpeta debe ser excluida
                if debe_excluir(item):
                    carpetas_excluidas += 1
                    continue
        
        # Crear archivo de información del backup
        info_backup = {
            "fecha_creacion": datetime.datetime.now().isoformat(),
            "directorio_origen": str(frontend_dir),
            "directorio_backup": str(backup_dir),
            "estadisticas": {
                "archivos_copiados": archivos_copiados,
                "archivos_excluidos": archivos_excluidos,
                "carpetas_excluidas": carpetas_excluidas
            },
            "exclusiones": exclusiones,
            "notas": [
                "Este backup excluye archivos que se pueden regenerar automáticamente",
                "Para restaurar: copiar contenido y ejecutar 'npm install'",
                "node_modules se regenerará automáticamente con npm install"
            ]
        }
        
        # Guardar información del backup
        import json
        with open(backup_dir / "backup_info.json", "w", encoding="utf-8") as f:
            json.dump(info_backup, f, indent=2, ensure_ascii=False)
        
        # Crear script de restauración
        script_restauracion = f"""#!/bin/bash
# Script de Restauración - {backup_name}
# Generado automáticamente el {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

echo "🔄 Restaurando backup: {backup_name}"

# Verificar que estamos en el directorio correcto
if [ ! -f "package.json" ]; then
    echo "❌ Error: No se encontró package.json. Asegúrate de estar en el directorio frontend"
    exit 1
fi

# Hacer backup del estado actual (opcional)
if [ -d "src" ]; then
    echo "📦 Creando backup del estado actual..."
    mkdir -p ../frontend_backup_antes_restauracion_$(date +%Y%m%d_%H%M%S)
    cp -r src ../frontend_backup_antes_restauracion_$(date +%Y%m%d_%H%M%S)/
    cp package.json ../frontend_backup_antes_restauracion_$(date +%Y%m%d_%H%M%S)/
fi

# Restaurar archivos
echo "📁 Restaurando archivos..."
cp -r ../{backup_name}/src ./
cp ../{backup_name}/package.json ./
cp ../{backup_name}/package-lock.json ./
cp ../{backup_name}/tailwind.config.js ./
cp ../{backup_name}/postcss.config.js ./
cp ../{backup_name}/jsconfig.json ./
cp ../{backup_name}/components.json ./

# Regenerar dependencias
echo "📦 Regenerando node_modules..."
npm install

echo "✅ Restauración completada exitosamente!"
echo "💡 Ejecuta 'npm start' para iniciar el servidor de desarrollo"
"""
        
        with open(backup_dir / "restaurar_backup.sh", "w", encoding="utf-8") as f:
            f.write(script_restauracion)
        
        # Hacer el script ejecutable (en sistemas Unix)
        try:
            os.chmod(backup_dir / "restaurar_backup.sh", 0o755)
        except:
            pass  # En Windows no es necesario
        
        print(f"\n✅ Backup optimizado completado exitosamente!")
        print(f"📁 Ubicación: {backup_dir}")
        print(f"📊 Estadísticas:")
        print(f"   • Archivos copiados: {archivos_copiados}")
        print(f"   • Archivos excluidos: {archivos_excluidos}")
        print(f"   • Carpetas excluidas: {carpetas_excluidas}")
        print(f"   • Tamaño del backup: {calcular_tamaño(backup_dir)}")
        
        print(f"\n💡 Para restaurar este backup:")
        print(f"   1. Navegar al directorio frontend")
        print(f"   2. Ejecutar: bash ../{backup_name}/restaurar_backup.sh")
        print(f"   3. O copiar manualmente los archivos y ejecutar 'npm install'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el backup: {e}")
        return False

def calcular_tamaño(directorio):
    """Calcula el tamaño total de un directorio"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directorio):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    
    # Convertir a formato legible
    for unit in ['B', 'KB', 'MB', 'GB']:
        if total_size < 1024.0:
            return f"{total_size:.1f} {unit}"
        total_size /= 1024.0
    return f"{total_size:.1f} TB"

def main():
    """Función principal"""
    print("🔧 Script de Backup Optimizado - SOUP Emprendimientos")
    print("=" * 60)
    
    if crear_backup_optimizado():
        print("\n🎉 Backup completado exitosamente!")
        sys.exit(0)
    else:
        print("\n❌ Error en el backup")
        sys.exit(1)

if __name__ == "__main__":
    main() 