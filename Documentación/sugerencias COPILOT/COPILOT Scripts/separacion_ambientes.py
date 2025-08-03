# Script: Separación de ambientes y configuración por entorno

"""
Este script muestra cómo adaptar la carga de configuración para soportar múltiples ambientes (.env.dev, .env.prod, .env.test).
Coloca este fragmento en tu archivo de configuración principal (por ejemplo, backend/app/core/config.py).
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f".env.{os.getenv('ENV', 'dev')}", extra="ignore")
    # ...otros campos de configuración...

settings = Settings()

# Ahora puedes cambiar de ambiente con la variable de entorno ENV (dev, prod, test)
# Ejemplo: ENV=prod uvicorn app.main:app
