# Tutorial Profesional de Backup y Restauración de SOUP

> Este procedimiento permite reconstruir completamente el proyecto **SOUP Market** desde 0, incluyendo el código, configuración y base de datos.

---

## 🔹 Estructura de Backup Completo

El backup profesional debe contener:

### 1. **Código fuente completo (sin dependencias generables)**

- Carpeta `FULL APP Main` comprimida en `.zip`
- Incluir: `backend/`, `frontend/`, `Dockerfile`, `README.md`, etc.
- **Excluir automáticamente** carpetas como:
  - `node_modules/`
  - `__pycache__/`
  - `.venv/`, `venv/`
- El criterio es similar a un `.gitignore`: **todo lo que pueda regenerarse automáticamente, se excluye.**

### 2. **Archivo de configuración**

- `.env` (copiar sin subir a GitHub)

### 3. **Dependencias**

- `requirements.txt` para el backend (Python)
- `package.json` para el frontend (React)

### 4. **Base de datos**

- Backup `.sql` completo hecho con `pg_dump`
  ```bash
  pg_dump -U soupuser -d soup_app_db -h localhost -p 5432 > backup_soup_app_db_YYYY-MM-DD.sql
  ```

---

## 🔧 Script de Backup Automático (versión segura)

```bat
@echo off
:: Script de backup profesional de SOUP Market
set FECHA=%date:~10,4%-%date:~3,2%-%date:~0,2%
set BACKUP_DIR=backup_SOUP_%FECHA%
set DESKTOP_DIR=%USERPROFILE%\Desktop\SOUP full backup %FECHA%

:: Configuración de PostgreSQL
set PGUSER=soupuser
set PGDATABASE=soup_app_db
set PGHOST=localhost
set PGPORT=5432
set PGPASSWORD=souppass

echo ========================================
echo    BACKUP PROFESIONAL SOUP MARKET
echo ========================================
echo Fecha: %FECHA%
echo.

:: Crear directorio de backup temporal
mkdir %BACKUP_DIR%

:: Copia de código fuente SIN node_modules, __pycache__ ni venv
echo Copiando código fuente...
robocopy "FULL APP Main" "%BACKUP_DIR%\FULL APP Main" /E /XD node_modules __pycache__ venv .venv

:: Copia de archivos clave
echo Copiando archivos de configuración...
copy .env %BACKUP_DIR%\.env
copy requirements.txt %BACKUP_DIR%\requirements.txt
copy package.json %BACKUP_DIR%\package.json

:: Backup de base de datos (automático con credenciales)
echo Realizando backup de la base de datos...
pg_dump -U %PGUSER% -d %PGDATABASE% -h %PGHOST% -p %PGPORT% > %BACKUP_DIR%\backup_soup_app_db_%FECHA%.sql

:: Comprimir
echo Comprimiendo backup...
powershell Compress-Archive -Path %BACKUP_DIR% -DestinationPath %BACKUP_DIR%.zip

:: Crear carpeta en escritorio y mover backup
echo Moviendo backup al escritorio...
mkdir "%DESKTOP_DIR%"
move %BACKUP_DIR%.zip "%DESKTOP_DIR%\"

:: Limpiar directorio temporal
rmdir /S /Q %BACKUP_DIR%

:: Final
echo.
echo ========================================
echo    BACKUP COMPLETADO EXITOSAMENTE
echo ========================================
echo Backup guardado en: "%DESKTOP_DIR%"
echo Archivo: %BACKUP_DIR%.zip
echo.
pause
```

---

## 🧰 Restaurar un Proyecto desde Cero (versión segura)

1. **Descomprimir el zip** en una carpeta nueva: `SOUP_RESTORE`
2. **Crear base de datos vacía**:

```bash
createdb -U soupuser soup_app_db_restore
```

3. **Restaurar base de datos**:

```bash
psql -U soupuser -d soup_app_db_restore -f backup_soup_app_db_YYYY-MM-DD.sql
```

4. **Copiar `.env` y configurar variables sensibles manualmente.**
5. **Instalar dependencias**:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd frontend && npm install
```

6. **Levantar el backend y frontend**

---

## ⚡ Recomendaciones

- **No restaurar sobre la carpeta de trabajo activa.**
- Validar que la versión de PostgreSQL sea la misma.
- Guardar los backups en la nube (Drive, Dropbox, etc.)
- Documentar cada backup en `Documentación/historial/` con:

```markdown
- Fecha:
- Responsable:
- Archivos:
- Estado: [✓] validado / [ ] pendiente
```

---

## 📖 Recursos Relacionados

- `PLANTILLA_PLAN_MIGRACION.md`
- `PLANTILLA_REGISTRO_MIGRACION.md`
- `PROTOCOLO_ACTUALIZACION_DOCUMENTACION.md`
- `ROADMAP_SIMPLIFICADO_MIGRACION.md`

---

✅ **Este protocolo garantiza que el proyecto pueda reconstruirse completamente en menos de 15 minutos ante una pérdida crítica.**

