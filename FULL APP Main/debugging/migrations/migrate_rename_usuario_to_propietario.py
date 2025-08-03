import psycopg2

# Configuración de conexión
conn = psycopg2.connect(
    dbname="soup_app_db",
    user="soupuser",
    password="souppass",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

try:
    # 1. Verificar si existe usuario_id y no existe propietario_id
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'productos' 
        AND column_name IN ('usuario_id', 'propietario_id')
    """)
    
    columns = [row[0] for row in cur.fetchall()]
    print(f"Columnas encontradas: {columns}")
    
    if 'usuario_id' in columns and 'propietario_id' not in columns:
        # 2. Renombrar usuario_id a propietario_id
        cur.execute("""
            ALTER TABLE productos 
            RENAME COLUMN usuario_id TO propietario_id
        """)
        print("✅ Columna usuario_id renombrada a propietario_id")
        
        # 3. Verificar que el cambio se aplicó
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'productos' 
            AND column_name = 'propietario_id'
        """)
        
        if cur.fetchone():
            print("✅ Verificación exitosa: propietario_id existe")
        else:
            print("❌ Error: propietario_id no se creó correctamente")
            
    elif 'propietario_id' in columns:
        print("✅ La columna ya se llama propietario_id")
    else:
        print("❌ Error: No se encontró usuario_id para renombrar")
    
    conn.commit()
    
except Exception as e:
    print(f"❌ Error durante la migración: {e}")
    conn.rollback()
finally:
    cur.close()
    conn.close()

print("Migración completada.") 