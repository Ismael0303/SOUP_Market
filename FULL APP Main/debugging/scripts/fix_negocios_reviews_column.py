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

    # Eliminar la columna reviews_totales si existe
    print('Eliminando columna reviews_totales (si existe)...')
    cur.execute('''
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='negocios' AND column_name='reviews_totales'
            ) THEN
                ALTER TABLE negocios DROP COLUMN reviews_totales;
            END IF;
        END$$;
    ''')
    print('Columna reviews_totales eliminada (si existía).')

    # Asegurar que las columnas correctas sean NULLABLE
    for col in ['calificacion_promedio', 'total_calificaciones', 'ventas_completadas']:
        print(f'Haciendo {col} NULLABLE...')
        cur.execute(f'''
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='negocios' AND column_name='{col}'
                ) THEN
                    ALTER TABLE negocios ALTER COLUMN {col} DROP NOT NULL;
                END IF;
            END$$;
        ''')
        print(f'Columna {col} ahora acepta NULL.')

    cur.close()
    conn.close()
    print('Script completado.')

if __name__ == '__main__':
    main() 