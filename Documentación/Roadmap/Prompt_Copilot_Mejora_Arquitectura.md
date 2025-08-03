# Prompt para Copilot: Mejoras de Arquitectura Backend

Analiza y mejora la arquitectura del backend de este proyecto FastAPI + SQLAlchemy siguiendo estas recomendaciones:

1. **Separación de ambientes**
   - Implementa carga de configuración diferenciada para desarrollo, producción y testing.
   - Usa diferentes archivos `.env` o variables de entorno.

2. **Modularización avanzada**
   - Si algún router o lógica de negocio crece demasiado, divídelo en submódulos o crea una carpeta `services/` para lógica de negocio.

3. **Manejo global de errores**
   - Añade un middleware para manejo uniforme de errores y logging centralizado.
   - Usa logging estructurado (por ejemplo, con `loguru`).

4. **Validación y serialización**
   - Refuerza la validación de datos con Pydantic, incluyendo validaciones personalizadas.

5. **Seguridad**
   - Implementa rate limiting y revisa la protección de endpoints críticos.
   - Asegura autenticación y autorización en endpoints sensibles.

6. **Testing automatizado**
   - Añade tests unitarios y de integración usando `pytest` y `httpx`.

7. **Documentación automática**
   - Añade ejemplos de request/response en los modelos Pydantic para mejorar la documentación Swagger.

8. **Optimización de base de datos**
   - Usa migraciones automáticas (Alembic) y añade índices a campos consultados frecuentemente.

9. **CI/CD y despliegue**
   - Sugiere o implementa un pipeline básico de CI/CD para tests y despliegue automático.

10. **Observabilidad**
    - Añade monitoreo, métricas y health checks.

---

## Script base sugerido

```python
# Ejemplo de middleware de manejo global de errores en FastAPI
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
import logging

app = FastAPI()

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logging.error(f"Unhandled error: {exc}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# Ejemplo de configuración por entorno
import os
from app.core.config import Settings

settings = Settings(_env_file=f".env.{os.getenv('ENV', 'dev')}")
```

---

Sigue estas recomendaciones y aplica los cambios necesarios en el proyecto para mejorar su robustez, mantenibilidad y escalabilidad.
