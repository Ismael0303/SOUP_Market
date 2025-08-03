# backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings # Importar la instancia de configuración

# Obtener la URL de la base de datos desde las configuraciones
DATABASE_URL = settings.DATABASE_URL

# Crear el motor de la base de datos
# El parámetro 'echo' se establece en settings.DEBUG para mostrar las consultas SQL solo en modo depuración.
engine = create_engine(DATABASE_URL, echo=settings.DEBUG)

# Crear una sesión local de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos de SQLAlchemy
Base = declarative_base()

# Función de utilidad para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
