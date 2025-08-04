@echo off
REM Backup ligero de la base de datos SOUP (PostgreSQL)
REM Excluye tablas de logs, sesiones y datos temporales

REM Configura tus variables de conexión
set PGUSER=soupuser
set PGDATABASE=soup_app_db
set PGHOST=localhost
set PGPORT=5432
REM set PGPASSWORD=tu_password (mejor usar el archivo .pgpass para seguridad)

REM Obtener fecha en formato YYYY-MM-DD usando PowerShell
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set FECHA=%%i
set BACKUP_NAME=backup_SOUP_DB_%FECHA%.sql

REM Excluir tablas innecesarias (ajusta los nombres según tu modelo)
set EXCLUDE_TABLES=--exclude-table=logs --exclude-table=sessions --exclude-table=temp_data

REM Ejecutar el backup (requiere que pg_dump esté en el PATH)
pg_dump -U %PGUSER% -d %PGDATABASE% -h %PGHOST% -p %PGPORT% %EXCLUDE_TABLES% > %BACKUP_NAME%

@echo Backup ligero de base de datos completado: %BACKUP_NAME% 