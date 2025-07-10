import psycopg2

# Configuración de conexión
conn = psycopg2.connect(
    dbname="soup_app_db",
    user="soupuser",
    password="souppass",  # Contraseña de soupuser
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# 1. Actualizar valores nulos existentes
cur.execute("""
UPDATE productos SET rating_promedio = 0.0 WHERE rating_promedio IS NULL;
UPDATE productos SET reviews_count = 0 WHERE reviews_count IS NULL;
""")

# 2. Alterar columnas para poner default y not null
cur.execute("""
ALTER TABLE productos ALTER COLUMN rating_promedio SET DEFAULT 0.0;
ALTER TABLE productos ALTER COLUMN rating_promedio SET NOT NULL;
ALTER TABLE productos ALTER COLUMN reviews_count SET DEFAULT 0;
ALTER TABLE productos ALTER COLUMN reviews_count SET NOT NULL;
""")

conn.commit()
cur.close()
conn.close()

print("Migración aplicada: rating_promedio y reviews_count ahora son NOT NULL y tienen valor por defecto.") 