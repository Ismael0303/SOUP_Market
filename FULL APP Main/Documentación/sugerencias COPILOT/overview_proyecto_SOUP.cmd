@echo off
setlocal enabledelayedexpansion
REM Script: overview_proyecto_SOUP.cmd
REM Muestra un dashboard con esquema arbóreo, conteo de archivos y funciones usando PowerShell para el conteo

REM Definir ruta de log
set "LOGDIR=C:\Users\Ismael\Desktop\PROYECTO SOHA\SOUP\SOUP Emprendimientos\Informes\Informes Copilot"
if not exist "%LOGDIR%" mkdir "%LOGDIR%"
set "LOGFILE=%LOGDIR%\overview_proyecto_SOUP_resultado.txt"

REM Cambia a la carpeta raíz del proyecto
cd /d "%~dp0..\..\..\\"

REM Inicializar log
(echo --- DASHBOARD - OVERVIEW PROYECTO SOUP ---
echo Fecha: %date% %time%
) > "%LOGFILE%"

REM Conteo de archivos por extensión y función (INICIO)
echo.>>"%LOGFILE%"
echo [Conteo de archivos por tipo y función - INICIO]>>"%LOGFILE%"
echo ----------------------------------------------- >>"%LOGFILE%"
powershell -ExecutionPolicy Bypass -File "Documentación\sugerencias COPILOT\conteo_archivos.ps1" >> "%LOGFILE%"

REM Esquema arbóreo de la arquitectura (completo, scrolleable)
echo.>>"%LOGFILE%"
echo [Esquema arbóreo de carpetas y archivos]>>"%LOGFILE%"
echo ---------------------------------------->>"%LOGFILE%"
tree /F /A >> "%LOGFILE%"

REM Fechas de última modificación (10 archivos más recientes)
echo.>>"%LOGFILE%"
echo [Últimas modificaciones]>>"%LOGFILE%"
echo ------------------------>>"%LOGFILE%"
(for /f "delims=" %%a in ('dir /s /b /o-d *.*') do (
    echo %%~ta %%a
)) | more +10 >> "%LOGFILE%"

REM Versión de git (si existe)
echo.>>"%LOGFILE%"
echo [Información de Git]>>"%LOGFILE%"
echo -------------------->>"%LOGFILE%"
if exist .git (
    git --version >> "%LOGFILE%"
    git log -1 --pretty=format:"Último commit: %h %ad %s" --date=short >> "%LOGFILE%"
    git status -s >> "%LOGFILE%"
) else (
    echo No se encontró repositorio Git en esta carpeta.>>"%LOGFILE%"
)

REM Conteo de archivos por extensión y función (FINAL)
echo.>>"%LOGFILE%"
echo [Conteo de archivos por tipo y función - FINAL]>>"%LOGFILE%"
echo --------------------------------------------- >>"%LOGFILE%"
powershell -ExecutionPolicy Bypass -File "Documentación\sugerencias COPILOT\conteo_archivos.ps1" >> "%LOGFILE%"

echo.>>"%LOGFILE%"
echo =====================================================>>"%LOGFILE%"
echo              FIN DEL DASHBOARD>>"%LOGFILE%"
echo =====================================================>>"%LOGFILE%"

echo. & echo --- & echo El resultado del dashboard se guardó en: %LOGFILE%
pause
