@echo off
setlocal

REM Configuración
set DB_NAME=soup_app_db
set DB_USER=soupuser
set DB_PASSWORD=souppass
set HOST=localhost
set PORT=5432

REM Obtener fecha y hora
for /f %%i in ('powershell -command "Get-Date -Format yyyy-MM-dd_HH-mm"') do set DATE=%%i

REM Nombre del archivo de salida
set OUTPUT_FILE=backup_%DB_NAME%_%DATE%.sql

REM Ejecutar el respaldo
echo Generando respaldo de la base de datos %DB_NAME%...
set PGPASSWORD=%DB_PASSWORD%
pg_dump -U %DB_USER% -h %HOST% -p %PORT% %DB_NAME% > %OUTPUT_FILE%

REM Verificar éxito
if %ERRORLEVEL% equ 0 (
    echo Respaldo generado con éxito: %OUTPUT_FILE%
) else (
    echo Error al generar el respaldo
)

endlocal
pause
