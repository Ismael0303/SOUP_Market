#!/bin/bash
# Script de Restauración - frontend_backup_optimizado_20250710_000703
# Generado automáticamente el 2025-07-10 00:07:22

echo "🔄 Restaurando backup: frontend_backup_optimizado_20250710_000703"

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
cp -r ../frontend_backup_optimizado_20250710_000703/src ./
cp ../frontend_backup_optimizado_20250710_000703/package.json ./
cp ../frontend_backup_optimizado_20250710_000703/package-lock.json ./
cp ../frontend_backup_optimizado_20250710_000703/tailwind.config.js ./
cp ../frontend_backup_optimizado_20250710_000703/postcss.config.js ./
cp ../frontend_backup_optimizado_20250710_000703/jsconfig.json ./
cp ../frontend_backup_optimizado_20250710_000703/components.json ./

# Regenerar dependencias
echo "📦 Regenerando node_modules..."
npm install

echo "✅ Restauración completada exitosamente!"
echo "💡 Ejecuta 'npm start' para iniciar el servidor de desarrollo"
