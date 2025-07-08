#!/usr/bin/env python3
"""
Script para verificar los datos de productos, insumos y producto_insumo en la base de datos.
"""
import os
import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))
os.chdir(backend_path)

from app.database import get_db
from sqlalchemy import text

def main():
    db = next(get_db())
    print("=== Productos ===")
    for row in db.execute(text('SELECT id, nombre, precio, tipo_producto, usuario_id, negocio_id, rating_promedio, reviews_count FROM productos')).fetchall():
        print(row)
    print("\n=== Insumos ===")
    for row in db.execute(text('SELECT id, nombre, cantidad_disponible, unidad_medida_compra, usuario_id FROM insumos')).fetchall():
        print(row)
    print("\n=== Producto-Insumo ===")
    for row in db.execute(text('SELECT id, producto_id, insumo_id, cantidad_necesaria FROM producto_insumo')).fetchall():
        print(row)
    db.close()

if __name__ == "__main__":
    main() 