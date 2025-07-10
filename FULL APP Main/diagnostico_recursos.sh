#!/bin/bash
# Script de diagnóstico de recursos para SOUP Emprendimientos
# Muestra recursos de hardware, requerimientos mínimos y recursos disponibles

# 1. Información de hardware
echo "===== INFORMACIÓN DE HARDWARE ====="
echo "CPU(s):"; nproc || echo "(nproc no disponible)"
echo "Modelo CPU:"; lscpu | grep 'Model name' || echo "(lscpu no disponible)"
echo "RAM total:"; free -h | grep Mem || echo "(free no disponible)"
echo "Espacio en disco (root):"; df -h / | tail -1 || echo "(df no disponible)"
echo "Espacio en disco (directorio actual):"; df -h . | tail -1 || echo "(df no disponible)"
echo

# 2. Recursos mínimos recomendados
cat <<EOF
===== RECURSOS MÍNIMOS RECOMENDADOS =====
- RAM: 4 GB (mínimo), 8 GB (recomendado)
- CPU: 2 núcleos (mínimo), 4 núcleos (recomendado)
- Espacio en disco: 2 GB libres (mínimo)
- Node.js: >= 18.x LTS
- Cursor IDE: >= 2 GB RAM libres para funcionamiento fluido
EOF

echo
# 3. Recursos actualmente disponibles
RAM_TOTAL=$(free -m | awk '/Mem:/ {print $2}')
RAM_LIBRE=$(free -m | awk '/Mem:/ {print $7}')
CPU_CORES=$(nproc 2>/dev/null || echo 1)
DISK_AVAIL=$(df -h . | awk 'NR==2 {print $4}')
NODE_VERSION=$(node -v 2>/dev/null || echo "Node no instalado")

cat <<EOF
===== RECURSOS DISPONIBLES =====
RAM total: ${RAM_TOTAL:-"Desconocido"} MB
RAM libre: ${RAM_LIBRE:-"Desconocido"} MB
CPU núcleos: $CPU_CORES
Espacio libre en disco: $DISK_AVAIL
Versión de Node.js: $NODE_VERSION
EOF

echo
# 4. Procesos relevantes
ps -eo pid,comm,%mem,%cpu --sort=-%mem | head -n 15

echo
# 5. Notas
cat <<EOF
- Si los recursos disponibles son menores a los recomendados, es probable que Cursor, Node o los tests no funcionen correctamente.
- Cierra aplicaciones innecesarias para liberar RAM y CPU.
- Si usas Windows, ejecuta este script en Git Bash, WSL o una terminal compatible con comandos Unix.
EOF 