# Script: Middleware de manejo global de errores y logging estructurado

"""
Agrega este middleware a tu archivo principal de FastAPI (por ejemplo, backend/app/main.py).
Puedes instalar loguru con: pip install loguru
"""

from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from loguru import logger

app = FastAPI()

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.error(f"Unhandled error: {exc}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# Configura loguru para logging estructurado en toda la app
logger.add("logs/soup_backend.log", rotation="1 week", retention="4 weeks", level="INFO")
