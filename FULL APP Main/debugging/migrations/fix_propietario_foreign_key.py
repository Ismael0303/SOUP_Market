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
    print("🔧 Arreglando clave foránea y restricciones de propietario_id...")
    
    # 1. Verificar si ya existe la clave foránea
    cur.execute("""
        SELECT constraint_name 
        FROM information_schema.table_constraints 
        WHERE table_name = 'productos' 
        AND constraint_name LIKE '%propietario%'
    """)
    
    existing_fk = cur.fetchone()
    
    if not existing_fk:
        # 2. Agregar la clave foránea
        cur.execute("""
            ALTER TABLE productos 
            ADD CONSTRAINT productos_propietario_id_fkey 
            FOREIGN KEY (propietario_id) REFERENCES usuarios(id)
        """)
        print("✅ Clave foránea productos_propietario_id_fkey agregada")
    else:
        print(f"✅ Clave foránea ya existe: {existing_fk[0]}")
    
    # 3. Hacer propietario_id NOT NULL
    cur.execute("""
        ALTER TABLE productos 
        ALTER COLUMN propietario_id SET NOT NULL
    """)
    print("✅ propietario_id ahora es NOT NULL")
    
    # 4. Verificar el resultado
    cur.execute("""
        SELECT column_name, is_nullable
        FROM information_schema.columns 
        WHERE table_name = 'productos' 
        AND column_name = 'propietario_id'
    """)
    
    result = cur.fetchone()
    if result:
        print(f"✅ Verificación: propietario_id es nullable: {result[1]}")
    
    # 5. Verificar claves foráneas
    cur.execute("""
        SELECT constraint_name 
        FROM information_schema.table_constraints 
        WHERE table_name = 'productos' 
        AND constraint_type = 'FOREIGN KEY'
    """)
    
    foreign_keys = [row[0] for row in cur.fetchall()]
    print(f"✅ Claves foráneas en productos: {foreign_keys}")
    
    conn.commit()
    
except Exception as e:
    print(f"❌ Error durante la migración: {e}")
    conn.rollback()
finally:
    cur.close()
    conn.close()

print("Migración completada.") 