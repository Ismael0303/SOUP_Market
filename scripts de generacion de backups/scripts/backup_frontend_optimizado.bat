@echo off
REM Script de Backup Optimizado para Frontend - SOUP Emprendimientos (Windows)
REM Excluye archivos que se pueden regenerar automáticamente

setlocal enabledelayedexpansion

echo 🔧 Script de Backup Optimizado - SOUP Emprendimientos
echo ============================================================

REM Obtener fecha y hora para el nombre del backup
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%%MM%%DD%_%HH%%Min%%Sec%"

set "backup_name=frontend_backup_optimizado_%timestamp%"
set "frontend_dir=frontend"
set "backup_dir=..\%backup_name%"

echo 🚀 Creando backup optimizado: %backup_name%
echo ================================================

REM Verificar que existe el directorio frontend
if not exist "%frontend_dir%" (
    echo ❌ Error: No se encontró el directorio frontend
    exit /b 1
)

REM Crear directorio de backup
if not exist "%backup_dir%" mkdir "%backup_dir%"

REM Contadores
set "archivos_copiados=0"
set "archivos_excluidos=0"

echo 📁 Copiando archivos del frontend...

REM Copiar archivos principales (excluyendo node_modules)
if exist "%frontend_dir%\src" (
    echo   Copiando src...
    xcopy "%frontend_dir%\src" "%backup_dir%\src" /E /I /Y >nul
    for /r "%frontend_dir%\src" %%f in (*) do set /a archivos_copiados+=1
)

REM Copiar archivos de configuración
if exist "%frontend_dir%\package.json" (
    copy "%frontend_dir%\package.json" "%backup_dir%\" >nul
    set /a archivos_copiados+=1
)

if exist "%frontend_dir%\package-lock.json" (
    copy "%frontend_dir%\package-lock.json" "%backup_dir%\" >nul
    set /a archivos_copiados+=1
)

if exist "%frontend_dir%\tailwind.config.js" (
    copy "%frontend_dir%\tailwind.config.js" "%backup_dir%\" >nul
    set /a archivos_copiados+=1
)

if exist "%frontend_dir%\postcss.config.js" (
    copy "%frontend_dir%\postcss.config.js" "%backup_dir%\" >nul
    set /a archivos_copiados+=1
)

if exist "%frontend_dir%\jsconfig.json" (
    copy "%frontend_dir%\jsconfig.json" "%backup_dir%\" >nul
    set /a archivos_copiados+=1
)

if exist "%frontend_dir%\components.json" (
    copy "%frontend_dir%\components.json" "%backup_dir%\" >nul
    set /a archivos_copiados+=1
)

REM Copiar carpeta public
if exist "%frontend_dir%\public" (
    echo   Copiando public...
    xcopy "%frontend_dir%\public" "%backup_dir%\public" /E /I /Y >nul
    for /r "%frontend_dir%\public" %%f in (*) do set /a archivos_copiados+=1
)

REM Crear archivo de información del backup
echo {> "%backup_dir%\backup_info.json"
echo   "fecha_creacion": "%YYYY%-%MM%-%DD%T%HH%:%Min%:%Sec%",>> "%backup_dir%\backup_info.json"
echo   "directorio_origen": "%cd%\%frontend_dir%",>> "%backup_dir%\backup_info.json"
echo   "directorio_backup": "%cd%\%backup_dir%",>> "%backup_dir%\backup_info.json"
echo   "estadisticas": {>> "%backup_dir%\backup_info.json"
echo     "archivos_copiados": %archivos_copiados%,>> "%backup_dir%\backup_info.json"
echo     "archivos_excluidos": %archivos_excluidos%,>> "%backup_dir%\backup_info.json"
echo     "carpetas_excluidas": 1>> "%backup_dir%\backup_info.json"
echo   },>> "%backup_dir%\backup_info.json"
echo   "exclusiones": [>> "%backup_dir%\backup_info.json"
echo     "node_modules/",>> "%backup_dir%\backup_info.json"
echo     ".git/",>> "%backup_dir%\backup_info.json"
echo     "build/",>> "%backup_dir%\backup_info.json"
echo     "dist/",>> "%backup_dir%\backup_info.json"
echo     "*.log",>> "%backup_dir%\backup_info.json"
echo     "*.tmp">> "%backup_dir%\backup_info.json"
echo   ],>> "%backup_dir%\backup_info.json"
echo   "notas": [>> "%backup_dir%\backup_info.json"
echo     "Este backup excluye archivos que se pueden regenerar automáticamente",>> "%backup_dir%\backup_info.json"
echo     "Para restaurar: copiar contenido y ejecutar 'npm install'",>> "%backup_dir%\backup_info.json"
echo     "node_modules se regenerará automáticamente con npm install">> "%backup_dir%\backup_info.json"
echo   ]>> "%backup_dir%\backup_info.json"
echo }>> "%backup_dir%\backup_info.json"

REM Crear script de restauración para Windows
echo @echo off > "%backup_dir%\restaurar_backup.bat"
echo REM Script de Restauración - %backup_name% >> "%backup_dir%\restaurar_backup.bat"
echo REM Generado automáticamente el %date% %time% >> "%backup_dir%\restaurar_backup.bat"
echo. >> "%backup_dir%\restaurar_backup.bat"
echo echo 🔄 Restaurando backup: %backup_name% >> "%backup_dir%\restaurar_backup.bat"
echo. >> "%backup_dir%\restaurar_backup.bat"
echo REM Verificar que estamos en el directorio correcto >> "%backup_dir%\restaurar_backup.bat"
echo if not exist "package.json" ( >> "%backup_dir%\restaurar_backup.bat"
echo   echo ❌ Error: No se encontró package.json. Asegúrate de estar en el directorio frontend >> "%backup_dir%\restaurar_backup.bat"
echo   exit /b 1 >> "%backup_dir%\restaurar_backup.bat"
echo ) >> "%backup_dir%\restaurar_backup.bat"
echo. >> "%backup_dir%\restaurar_backup.bat"
echo REM Hacer backup del estado actual ^(opcional^) >> "%backup_dir%\restaurar_backup.bat"
echo if exist "src" ( >> "%backup_dir%\restaurar_backup.bat"
echo   echo 📦 Creando backup del estado actual... >> "%backup_dir%\restaurar_backup.bat"
echo   mkdir "..\frontend_backup_antes_restauracion_%timestamp%" >> "%backup_dir%\restaurar_backup.bat"
echo   xcopy "src" "..\frontend_backup_antes_restauracion_%timestamp%\src" /E /I /Y >> "%backup_dir%\restaurar_backup.bat"
echo   copy "package.json" "..\frontend_backup_antes_restauracion_%timestamp%\" >> "%backup_dir%\restaurar_backup.bat"
echo ) >> "%backup_dir%\restaurar_backup.bat"
echo. >> "%backup_dir%\restaurar_backup.bat"
echo REM Restaurar archivos >> "%backup_dir%\restaurar_backup.bat"
echo echo 📁 Restaurando archivos... >> "%backup_dir%\restaurar_backup.bat"
echo xcopy "..\%backup_name%\src" "src" /E /I /Y >> "%backup_dir%\restaurar_backup.bat"
echo copy "..\%backup_name%\package.json" "." >> "%backup_dir%\restaurar_backup.bat"
echo copy "..\%backup_name%\package-lock.json" "." >> "%backup_dir%\restaurar_backup.bat"
echo copy "..\%backup_name%\tailwind.config.js" "." >> "%backup_dir%\restaurar_backup.bat"
echo copy "..\%backup_name%\postcss.config.js" "." >> "%backup_dir%\restaurar_backup.bat"
echo copy "..\%backup_name%\jsconfig.json" "." >> "%backup_dir%\restaurar_backup.bat"
echo copy "..\%backup_name%\components.json" "." >> "%backup_dir%\restaurar_backup.bat"
echo xcopy "..\%backup_name%\public" "public" /E /I /Y >> "%backup_dir%\restaurar_backup.bat"
echo. >> "%backup_dir%\restaurar_backup.bat"
echo REM Regenerar dependencias >> "%backup_dir%\restaurar_backup.bat"
echo echo 📦 Regenerando node_modules... >> "%backup_dir%\restaurar_backup.bat"
echo npm install >> "%backup_dir%\restaurar_backup.bat"
echo. >> "%backup_dir%\restaurar_backup.bat"
echo echo ✅ Restauración completada exitosamente! >> "%backup_dir%\restaurar_backup.bat"
echo echo 💡 Ejecuta 'npm start' para iniciar el servidor de desarrollo >> "%backup_dir%\restaurar_backup.bat"

echo.
echo ✅ Backup optimizado completado exitosamente!
echo 📁 Ubicación: %backup_dir%
echo 📊 Estadísticas:
echo    • Archivos copiados: %archivos_copiados%
echo    • Archivos excluidos: %archivos_excluidos%
echo    • Carpetas excluidas: 1 ^(node_modules^)
echo.
echo 💡 Para restaurar este backup:
echo    1. Navegar al directorio frontend
echo    2. Ejecutar: ..\%backup_name%\restaurar_backup.bat
echo    3. O copiar manualmente los archivos y ejecutar 'npm install'
echo.
echo 🎉 Backup completado exitosamente!

endlocal 