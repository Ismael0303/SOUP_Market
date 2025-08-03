import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    'dbname': 'soup_app_db',
    'user': 'soupuser',
    'password': 'souppass',  # Contraseña actualizada
    'host': 'localhost',
    'port': 5432,
}

def main():
    print('Conectando a la base de datos...')
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cur = conn.cursor()

    # Eliminar la columna usuario_id si existe
    print('Eliminando columna usuario_id de negocios (si existe)...')
    cur.execute('''
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='negocios' AND column_name='usuario_id'
            ) THEN
                ALTER TABLE negocios DROP COLUMN usuario_id;
            END IF;
        END$$;
    ''')
    print('Columna usuario_id eliminada (si existía).')

    # Verificar que propietario_id es NOT NULL
    print('Verificando que propietario_id es NOT NULL...')
    cur.execute('''
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='negocios' AND column_name='propietario_id'
            ) THEN
                ALTER TABLE negocios ALTER COLUMN propietario_id SET NOT NULL;
            END IF;
        END$$;
    ''')
    print('propietario_id es NOT NULL.')

    cur.close()
    conn.close()
    print('Script completado.')

if __name__ == '__main__':
    main() 