@echo off
REM Backup ligero de SOUP (frontend y backend) - solo código fuente y configuración
REM No incluye node_modules, venv, build, dist ni archivos temporales

REM Obtener fecha en formato YYYY-MM-DD usando PowerShell
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set FECHA=%%i
set BACKUP_DIR=backup_SOUP_%FECHA%
set ZIP_NAME=backup_SOUP_%FECHA%.zip

REM Crear carpeta temporal para backup (ignorar error si ya existe)
if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

REM --- FRONTEND ---
if not exist %BACKUP_DIR%\frontend mkdir %BACKUP_DIR%\frontend
xcopy frontend\src %BACKUP_DIR%\frontend\src /E /I /Y >nul
xcopy frontend\public %BACKUP_DIR%\frontend\public /E /I /Y >nul
if exist frontend\package.json copy /Y frontend\package.json %BACKUP_DIR%\frontend\ >nul
if exist frontend\package-lock.json copy /Y frontend\package-lock.json %BACKUP_DIR%\frontend\ >nul
if exist frontend\jsconfig.json copy /Y frontend\jsconfig.json %BACKUP_DIR%\frontend\ >nul
if exist frontend\tailwind.config.js copy /Y frontend\tailwind.config.js %BACKUP_DIR%\frontend\ >nul
if exist frontend\postcss.config.js copy /Y frontend\postcss.config.js %BACKUP_DIR%\frontend\ >nul
if exist frontend\README.md copy /Y frontend\README.md %BACKUP_DIR%\frontend\ >nul

REM --- BACKEND ---
if not exist %BACKUP_DIR%\backend mkdir %BACKUP_DIR%\backend
xcopy backend\app %BACKUP_DIR%\backend\app /E /I /Y >nul
if exist backend\requirements.txt copy /Y backend\requirements.txt %BACKUP_DIR%\backend\ >nul
if exist backend\README.md copy /Y backend\README.md %BACKUP_DIR%\backend\ >nul

REM --- OTROS ARCHIVOS IMPORTANTES ---
if exist PROJECT_RULES.md copy /Y PROJECT_RULES.md %BACKUP_DIR%\ >nul
if exist requirements.txt copy /Y requirements.txt %BACKUP_DIR%\ >nul

REM Comprimir el backup (requiere PowerShell 5+)
powershell -NoProfile -Command "Compress-Archive -Path '%BACKUP_DIR%' -DestinationPath '%ZIP_NAME%'"

REM Eliminar carpeta temporal de backup
rmdir /S /Q %BACKUP_DIR%

@echo Backup ligero completado: %ZIP_NAME% 