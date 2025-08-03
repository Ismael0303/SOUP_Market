import psycopg2

DB_CONFIG = {
    'dbname': 'soup_app_db',
    'user': 'soupuser',
    'password': 'souppass',
    'host': 'localhost',
    'port': 5432,
}

def main():
    print('Conectando a la base de datos...')
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cur = conn.cursor()

    # Eliminar la columna rating_promedio si existe
    print('Eliminando columna rating_promedio (si existe)...')
    cur.execute('''
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='negocios' AND column_name='rating_promedio'
            ) THEN
                ALTER TABLE negocios DROP COLUMN rating_promedio;
            END IF;
        END$$;
    ''')
    print('Columna rating_promedio eliminada (si existía).')

    # Hacer calificacion_promedio NULLABLE
    print('Haciendo calificacion_promedio NULLABLE...')
    cur.execute('''
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='negocios' AND column_name='calificacion_promedio'
            ) THEN
                ALTER TABLE negocios ALTER COLUMN calificacion_promedio DROP NOT NULL;
            END IF;
        END$$;
    ''')
    print('Columna calificacion_promedio ahora acepta NULL.')

    cur.close()
    conn.close()
    print('Script completado.')

if __name__ == '__main__':
    main() 