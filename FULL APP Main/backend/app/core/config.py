# backend/app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
import os

class Settings(BaseSettings):
    # Configuración del modelo para cargar variables de entorno
    # .env se carga por defecto si existe
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Configuración de la base de datos
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # Configuración de seguridad JWT
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configuración de entorno (para depuración, etc.)
    DEBUG: bool = Field(False, env="DEBUG") # Por defecto False, se puede sobrescribir con DEBUG=True en .env

    # Configuración de WhatsApp Business API (para Capítulo 5/9)
    WHATSAPP_BUSINESS_API_TOKEN: Optional[str] = Field(None, env="WHATSAPP_BUSINESS_API_TOKEN")
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = Field(None, env="WHATSAPP_PHONE_NUMBER_ID")

    # Configuración para servicios de almacenamiento de archivos (para Capítulo 14)
    # Por ejemplo, para Google Cloud Storage:
    GCS_BUCKET_NAME: Optional[str] = Field(None, env="GCS_BUCKET_NAME")
    # GCS_SERVICE_ACCOUNT_INFO: Optional[str] = Field(None, env="GCS_SERVICE_ACCOUNT_INFO") # JSON string

    # Configuración para Gemini AI (para Capítulo 8)
    GEMINI_API_KEY: Optional[str] = Field(None, env="GEMINI_API_KEY")


# Instancia de configuración global
settings = Settings()

# Crear un archivo .env si no existe para facilitar el desarrollo local
# Esto es solo una ayuda para el desarrollador, no se usa en producción
env_file_path = ".env"
if not os.path.exists(env_file_path):
    with open(env_file_path, "w") as f:
        f.write("# Archivo de configuración de entorno para desarrollo local\n")
        f.write("# Copia este archivo y renómbralo a .env en la raíz de tu backend\n")
        f.write("# No lo subas a control de versiones (añadir a .gitignore)\n\n")
        f.write("DATABASE_URL=\"postgresql://user:password@localhost/dbname\"\n")
        f.write("SECRET_KEY=\"tu_super_secreto_jwt_aqui\"\n")
        f.write("DEBUG=True\n\n")
        f.write("# Opcional: Configuración de WhatsApp Business API\n")
        f.write("WHATSAPP_BUSINESS_API_TOKEN=\n")
        f.write("WHATSAPP_PHONE_NUMBER_ID=\n\n")
        f.write("# Opcional: Configuración de Google Cloud Storage\n")
        f.write("GCS_BUCKET_NAME=\n\n")
        f.write("# Opcional: Configuración de Gemini AI\n")
        f.write("GEMINI_API_KEY=\n")
    print(f"Archivo .env de ejemplo creado en {env_file_path}. Por favor, edítalo con tus credenciales reales.")
