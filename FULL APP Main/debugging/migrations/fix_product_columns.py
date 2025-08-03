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
    print("🔍 Verificando estado actual de la tabla productos...")
    
    # 1. Verificar si existen ambas columnas
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'productos' 
        AND column_name IN ('usuario_id', 'propietario_id')
    """)
    
    columns = [row[0] for row in cur.fetchall()]
    print(f"Columnas encontradas: {columns}")
    
    if 'usuario_id' in columns and 'propietario_id' in columns:
        print("⚠️  Ambas columnas existen. Copiando datos y eliminando usuario_id...")
        
        # Copiar datos de usuario_id a propietario_id si propietario_id está vacío
        cur.execute("""
            UPDATE productos 
            SET propietario_id = usuario_id 
            WHERE propietario_id IS NULL AND usuario_id IS NOT NULL
        """)
        print("✅ Datos copiados de usuario_id a propietario_id")
        
        # Eliminar la columna usuario_id
        cur.execute("ALTER TABLE productos DROP COLUMN usuario_id")
        print("✅ Columna usuario_id eliminada")
        
    elif 'usuario_id' in columns and 'propietario_id' not in columns:
        print("🔄 Renombrando usuario_id a propietario_id...")
        cur.execute("ALTER TABLE productos RENAME COLUMN usuario_id TO propietario_id")
        print("✅ Columna renombrada exitosamente")
        
    elif 'propietario_id' in columns and 'usuario_id' not in columns:
        print("✅ La tabla ya tiene la estructura correcta")
        
    else:
        print("❌ Error: No se encontraron las columnas esperadas")
    
    # Verificar el resultado final
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'productos' 
        AND column_name = 'propietario_id'
    """)
    
    if cur.fetchone():
        print("✅ Verificación final: propietario_id existe")
    else:
        print("❌ Error: propietario_id no existe después de la migración")
    
    conn.commit()
    
except Exception as e:
    print(f"❌ Error durante la migración: {e}")
    conn.rollback()
finally:
    cur.close()
    conn.close()

print("Migración completada.") 