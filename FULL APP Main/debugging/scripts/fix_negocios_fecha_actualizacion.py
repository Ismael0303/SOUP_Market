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

    # Hacer fecha_actualizacion NULLABLE
    print('Haciendo fecha_actualizacion NULLABLE...')
    cur.execute('''
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='negocios' AND column_name='fecha_actualizacion'
            ) THEN
                ALTER TABLE negocios ALTER COLUMN fecha_actualizacion DROP NOT NULL;
            END IF;
        END$$;
    ''')
    print('Columna fecha_actualizacion ahora acepta NULL.')

    # Asignar valor por defecto now()
    print('Asignando valor por defecto now() a fecha_actualizacion...')
    cur.execute('''
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='negocios' AND column_name='fecha_actualizacion'
            ) THEN
                ALTER TABLE negocios ALTER COLUMN fecha_actualizacion SET DEFAULT now();
            END IF;
        END$$;
    ''')
    print('Columna fecha_actualizacion ahora tiene valor por defecto now().')

    cur.close()
    conn.close()
    print('Script completado.')

if __name__ == '__main__':
    main() 