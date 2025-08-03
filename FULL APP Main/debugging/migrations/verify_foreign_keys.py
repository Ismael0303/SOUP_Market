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
    print("🔍 Verificando claves foráneas de la tabla productos...")
    
    # Verificar claves foráneas
    cur.execute("""
        SELECT 
            tc.constraint_name, 
            tc.table_name, 
            kcu.column_name, 
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name 
        FROM 
            information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY' 
        AND tc.table_name='productos';
    """)
    
    foreign_keys = cur.fetchall()
    print("📋 Claves foráneas encontradas:")
    for fk in foreign_keys:
        print(f"  {fk[0]}: {fk[2]} -> {fk[3]}.{fk[4]}")
    
    # Verificar si las tablas referenciadas existen
    print("\n🔍 Verificando tablas referenciadas...")
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_name IN ('usuarios', 'negocios')")
    tables = [row[0] for row in cur.fetchall()]
    print(f"Tablas encontradas: {tables}")
    
    # Verificar si hay datos en las tablas referenciadas
    if 'usuarios' in tables:
        cur.execute("SELECT COUNT(*) FROM usuarios")
        user_count = cur.fetchone()[0]
        print(f"Usuarios en la base de datos: {user_count}")
    
    if 'negocios' in tables:
        cur.execute("SELECT COUNT(*) FROM negocios")
        business_count = cur.fetchone()[0]
        print(f"Negocios en la base de datos: {business_count}")
    
    # Verificar estructura de la tabla productos
    print("\n📋 Estructura actual de productos:")
    cur.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'productos'
        ORDER BY ordinal_position
    """)
    
    columns = cur.fetchall()
    for col in columns:
        print(f"  {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    cur.close()
    conn.close() 