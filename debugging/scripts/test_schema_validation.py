#!/usr/bin/env python3
"""
Script para probar la validación de datos de producto
"""

import json
from uuid import UUID

def test_data_structure():
    """Probar estructura de datos para producto"""
    print("🧪 TESTING DATA STRUCTURE")
    print("=" * 40)
    
    # Datos de prueba
    test_data = {
        "nombre": "Test Product",
        "descripcion": "Product for testing",
        "precio": 10.0,
        "tipo_producto": "PHYSICAL_GOOD",
        "negocio_id": "15144d71-502c-422c-99f5-afe94e28101f",
        "precio_venta": 15.0,
        "margen_ganancia_sugerido": 50.0,
        "stock_terminado": 100.0
    }
    
    print("📋 Datos de prueba:")
    for key, value in test_data.items():
        print(f"  {key}: {value} ({type(value).__name__})")
    
    # Validar UUID
    try:
        negocio_uuid = UUID(test_data["negocio_id"])
        print(f"✅ UUID válido: {negocio_uuid}")
    except ValueError as e:
        print(f"❌ UUID inválido: {e}")
        return
    
    # Validar tipos de datos
    print("\n🔍 Validación de tipos:")
    
    # Validar nombre (string no vacío)
    if isinstance(test_data["nombre"], str) and len(test_data["nombre"]) > 0:
        print("✅ nombre: válido")
    else:
        print("❌ nombre: debe ser string no vacío")
    
    # Validar precio (float positivo)
    if isinstance(test_data["precio"], (int, float)) and test_data["precio"] > 0:
        print("✅ precio: válido")
    else:
        print("❌ precio: debe ser número positivo")
    
    # Validar tipo_producto (enum válido)
    valid_types = ["PHYSICAL_GOOD", "SERVICE_BY_HOUR", "SERVICE_BY_PROJECT", "DIGITAL_GOOD"]
    if test_data["tipo_producto"] in valid_types:
        print("✅ tipo_producto: válido")
    else:
        print(f"❌ tipo_producto: debe ser uno de {valid_types}")
    
    # Validar precio_venta (float no negativo o None)
    if test_data["precio_venta"] is None or (isinstance(test_data["precio_venta"], (int, float)) and test_data["precio_venta"] >= 0):
        print("✅ precio_venta: válido")
    else:
        print("❌ precio_venta: debe ser número no negativo o None")
    
    # Validar margen_ganancia_sugerido (float no negativo o None)
    if test_data["margen_ganancia_sugerido"] is None or (isinstance(test_data["margen_ganancia_sugerido"], (int, float)) and test_data["margen_ganancia_sugerido"] >= 0):
        print("✅ margen_ganancia_sugerido: válido")
    else:
        print("❌ margen_ganancia_sugerido: debe ser número no negativo o None")
    
    # Validar stock_terminado (float o None)
    if test_data["stock_terminado"] is None or isinstance(test_data["stock_terminado"], (int, float)):
        print("✅ stock_terminado: válido")
    else:
        print("❌ stock_terminado: debe ser número o None")
    
    print("\n📤 JSON para envío:")
    print(json.dumps(test_data, indent=2))

if __name__ == "__main__":
    test_data_structure() 