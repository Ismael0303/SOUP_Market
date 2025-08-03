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
    # Verificar todas las columnas de la tabla productos
    cur.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'productos'
        ORDER BY ordinal_position
    """)
    
    columns = cur.fetchall()
    print("📋 Columnas actuales de la tabla productos:")
    print("=" * 60)
    
    for col in columns:
        print(f"  {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
    
    # Verificar específicamente usuario_id y propietario_id
    cur.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns 
        WHERE table_name = 'productos' 
        AND column_name IN ('usuario_id', 'propietario_id')
    """)
    
    user_cols = cur.fetchall()
    print("\n🔍 Columnas de usuario/propietario:")
    for col in user_cols:
        print(f"  {col[0]}: {col[1]} (nullable: {col[2]})")
    
    # Verificar si hay datos en ambas columnas
    if len(user_cols) == 2:
        cur.execute("SELECT COUNT(*) FROM productos WHERE usuario_id IS NOT NULL")
        usuario_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM productos WHERE propietario_id IS NOT NULL")
        propietario_count = cur.fetchone()[0]
        
        print(f"\n📊 Datos en columnas:")
        print(f"  usuario_id con datos: {usuario_count}")
        print(f"  propietario_id con datos: {propietario_count}")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    cur.close()
    conn.close() 