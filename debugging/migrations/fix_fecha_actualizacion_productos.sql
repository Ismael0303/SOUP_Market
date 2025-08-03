-- Migración para corregir fecha_actualizacion en tabla productos
-- Ejecutar con: psql -U soupuser -d soup_app_db -h localhost -p 5432 -f fix_fecha_actualizacion_productos.sql

-- Agregar valor por defecto a fecha_actualizacion
ALTER TABLE productos ALTER COLUMN fecha_actualizacion SET DEFAULT CURRENT_TIMESTAMP;

-- Actualizar registros existentes que tengan fecha_actualizacion NULL
UPDATE productos SET fecha_actualizacion = CURRENT_TIMESTAMP WHERE fecha_actualizacion IS NULL;

-- Verificar que no hay registros con fecha_actualizacion NULL
SELECT COUNT(*) as registros_con_fecha_null FROM productos WHERE fecha_actualizacion IS NULL; 