import sqlalchemy as sa
from sqlalchemy import create_engine, text

# Configuración de conexión (ajusta según tu entorno)
DB_URL = "postgresql+psycopg2://soupuser:soupuser@localhost:5432/soup_app_db"
engine = create_engine(DB_URL)

ALTERS = [
    "ALTER TABLE productos ADD COLUMN IF NOT EXISTS calificacion_promedio FLOAT;",
    "ALTER TABLE productos ADD COLUMN IF NOT EXISTS total_calificaciones INTEGER;",
    "ALTER TABLE productos ADD COLUMN IF NOT EXISTS ventas_completadas INTEGER;",
    "ALTER TABLE negocios ADD COLUMN IF NOT EXISTS calificacion_promedio FLOAT;",
    "ALTER TABLE negocios ADD COLUMN IF NOT EXISTS total_calificaciones INTEGER;",
    "ALTER TABLE negocios ADD COLUMN IF NOT EXISTS ventas_completadas INTEGER;",
]

def migrate():
    with engine.connect() as conn:
        for stmt in ALTERS:
            print(f"Ejecutando: {stmt}")
            conn.execute(text(stmt))
        conn.commit()
    print("Migración completada.")

if __name__ == "__main__":
    migrate() 