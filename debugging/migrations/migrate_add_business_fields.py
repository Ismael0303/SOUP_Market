# backend/migrate_add_business_fields.py

from sqlalchemy import text
from app.database import engine

def add_business_fields():
    """Agrega campos faltantes a la tabla negocios"""
    with engine.begin() as conn:
        # Verificar si las columnas ya existen
        check_columns_query = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'negocios' 
        AND column_name IN ('rubro', 'localizacion_geografica', 'fotos_urls');
        """
        result = conn.execute(text(check_columns_query))
        existing_columns = [row[0] for row in result.fetchall()]
        print(f"Columnas existentes: {existing_columns}")

        # Agregar columna rubro si no existe
        if 'rubro' not in existing_columns:
            print("Agregando columna 'rubro'...")
            conn.execute(text("ALTER TABLE negocios ADD COLUMN rubro VARCHAR;"))
            print("Columna 'rubro' agregada exitosamente")

        # Agregar columna localizacion_geografica si no existe
        if 'localizacion_geografica' not in existing_columns:
            print("Agregando columna 'localizacion_geografica'...")
            conn.execute(text("ALTER TABLE negocios ADD COLUMN localizacion_geografica VARCHAR;"))
            print("Columna 'localizacion_geografica' agregada exitosamente")

        # Agregar columna fotos_urls si no existe
        if 'fotos_urls' not in existing_columns:
            print("Agregando columna 'fotos_urls'...")
            conn.execute(text("ALTER TABLE negocios ADD COLUMN fotos_urls TEXT[];"))
            print("Columna 'fotos_urls' agregada exitosamente")

        print("Migración completada exitosamente")

if __name__ == "__main__":
    add_business_fields() 