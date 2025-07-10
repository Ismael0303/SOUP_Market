#!/bin/bash
# Script de Restauración - frontend_backup_optimizado_20250710_001116
# Generado automáticamente el 2025-07-10 00:11:39

echo "🔄 Restaurando backup: frontend_backup_optimizado_20250710_001116"

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
cp -r ../frontend_backup_optimizado_20250710_001116/src ./
cp ../frontend_backup_optimizado_20250710_001116/package.json ./
cp ../frontend_backup_optimizado_20250710_001116/package-lock.json ./
cp ../frontend_backup_optimizado_20250710_001116/tailwind.config.js ./
cp ../frontend_backup_optimizado_20250710_001116/postcss.config.js ./
cp ../frontend_backup_optimizado_20250710_001116/jsconfig.json ./
cp ../frontend_backup_optimizado_20250710_001116/components.json ./

# Regenerar dependencias
echo "📦 Regenerando node_modules..."
npm install

echo "✅ Restauración completada exitosamente!"
echo "💡 Ejecuta 'npm start' para iniciar el servidor de desarrollo"
