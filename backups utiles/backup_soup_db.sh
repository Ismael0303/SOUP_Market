#!/bin/bash

# Variables de conexión
HOST="localhost"
PORT="5432"
DB_NAME="soup_app_db"
DB_USER="soupuser"
DB_PASSWORD="souppass"

# Fecha para versión del archivo
DATE=$(date +"%Y-%m-%d_%H-%M")

# Nombre del archivo de salida
OUTPUT_FILE="backup_${DB_NAME}_${DATE}.sql"

# Ejecutar respaldo
echo "Generando respaldo de la base de datos $DB_NAME..."
PGPASSWORD="$DB_PASSWORD" pg_dump -U "$DB_USER" -h "$HOST" -p "$PORT" "$DB_NAME" > "$OUTPUT_FILE"

# Verificar éxito
if [ $? -eq 0 ]; then
    echo "Respaldo generado con éxito: $OUTPUT_FILE"
else
    echo "Error al generar el respaldo"
fi
