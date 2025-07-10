# debugging/scripts/test_fase2_pos.py

import requests
import json
import sys
import os
from datetime import date, datetime, timedelta

# Configuración
BASE_URL = "http://127.0.0.1:8000"
TEST_EMAIL = "ismaeldimenza@hotmail.com"
TEST_PASSWORD = "ismael38772433"

def test_fase2_pos():
    """Test completo de la Fase 2: Sistema POS mejorado"""
    
    print("🛒 TESTEANDO FASE 2: SISTEMA POS MEJORADO")
    print("=" * 60)
    
    # 1. Login para obtener token
    print("\n1. 🔐 Login para obtener token")
    try:
        login_data = {
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        response = requests.post(f"{BASE_URL}/users/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            print(f"✅ Login exitoso")
            print(f"✅ Token obtenido: {access_token[:20]}...")
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # Headers con token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 2. Obtener negocios del usuario
    print("\n2. 🏪 Obteniendo negocios del usuario")
    try:
        response = requests.get(f"{BASE_URL}/businesses/", headers=headers)
        if response.status_code == 200:
            negocios = response.json()
            if negocios:
                negocio_id = negocios[0]["id"]
                print(f"✅ Negocio encontrado: {negocios[0]['nombre']}")
                print(f"✅ ID del negocio: {negocio_id}")
            else:
                print("❌ No se encontraron negocios")
                return False
        else:
            print(f"❌ Error obteniendo negocios: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 3. Test crear carrito de compras
    print("\n3. 🛒 Test crear carrito de compras")
    try:
        carrito_data = {
            "negocio_id": negocio_id,
            "cliente_id": None,
            "session_id": "test_session_123"
        }
        response = requests.post(f"{BASE_URL}/ventas/carrito/", json=carrito_data, headers=headers)
        if response.status_code == 200:
            carrito = response.json()
            carrito_id = carrito["id"]
            print(f"✅ Carrito creado exitosamente")
            print(f"✅ ID del carrito: {carrito_id}")
        else:
            print(f"❌ Error creando carrito: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 4. Obtener productos para añadir al carrito
    print("\n4. 📦 Obteniendo productos disponibles")
    try:
        response = requests.get(f"{BASE_URL}/products/", headers=headers)
        if response.status_code == 200:
            productos = response.json()
            if productos:
                producto_id = productos[0]["id"]
                print(f"✅ Producto encontrado: {productos[0]['nombre']}")
                print(f"✅ ID del producto: {producto_id}")
            else:
                print("❌ No se encontraron productos")
                return False
        else:
            print(f"❌ Error obteniendo productos: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 5. Test añadir item al carrito
    print("\n5. ➕ Test añadir item al carrito")
    try:
        item_data = {
            "producto_id": producto_id,
            "cantidad": 2.0
        }
        response = requests.post(f"{BASE_URL}/ventas/carrito/{carrito_id}/items/", json=item_data, headers=headers)
        if response.status_code == 200:
            item = response.json()
            print(f"✅ Item añadido al carrito")
            print(f"✅ Cantidad: {item['cantidad']}")
            print(f"✅ Precio unitario: {item['precio_unitario']}")
        else:
            print(f"❌ Error añadiendo item: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 6. Test obtener carrito
    print("\n6. 📋 Test obtener carrito")
    try:
        response = requests.get(f"{BASE_URL}/ventas/carrito/{carrito_id}", headers=headers)
        if response.status_code == 200:
            carrito = response.json()
            print(f"✅ Carrito obtenido")
            print(f"✅ Items en carrito: {len(carrito['items'])}")
            print(f"✅ Total items: {sum(item['cantidad'] for item in carrito['items'])}")
        else:
            print(f"❌ Error obteniendo carrito: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 7. Test finalizar compra (convertir carrito en venta)
    print("\n7. 💰 Test finalizar compra")
    try:
        response = requests.post(
            f"{BASE_URL}/ventas/carrito/{carrito_id}/finalizar",
            params={
                "metodo_pago": "efectivo",
                "descuento": 0.0,
                "impuestos": 0.0,
                "notas": "Test de venta desde carrito"
            },
            headers=headers
        )
        if response.status_code == 200:
            venta = response.json()
            venta_id = venta["id"]
            print(f"✅ Venta creada exitosamente")
            print(f"✅ Número de venta: {venta['numero_venta']}")
            print(f"✅ Total: ${venta['total']}")
            print(f"✅ Estado: {venta['estado']}")
        else:
            print(f"❌ Error finalizando compra: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 8. Test obtener venta
    print("\n8. 📄 Test obtener venta")
    try:
        response = requests.get(f"{BASE_URL}/ventas/{venta_id}", headers=headers)
        if response.status_code == 200:
            venta = response.json()
            print(f"✅ Venta obtenida")
            print(f"✅ Detalles: {len(venta['detalles'])}")
            print(f"✅ Margen ganancia: ${venta.get('margen_ganancia_total', 0)}")
        else:
            print(f"❌ Error obteniendo venta: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 9. Test obtener ventas del negocio
    print("\n9. 📊 Test obtener ventas del negocio")
    try:
        response = requests.get(f"{BASE_URL}/ventas/negocio/{negocio_id}", headers=headers)
        if response.status_code == 200:
            ventas = response.json()
            print(f"✅ Ventas obtenidas")
            print(f"✅ Total de ventas: {len(ventas)}")
        else:
            print(f"❌ Error obteniendo ventas: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 10. Test análisis de ventas
    print("\n10. 📈 Test análisis de ventas")
    try:
        fecha_inicio = (date.today() - timedelta(days=30)).isoformat()
        fecha_fin = date.today().isoformat()
        
        response = requests.get(
            f"{BASE_URL}/ventas/analisis/{negocio_id}",
            params={
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin
            },
            headers=headers
        )
        if response.status_code == 200:
            analisis = response.json()
            print(f"✅ Análisis obtenido")
            print(f"✅ Total ventas: ${analisis.get('total_ventas', 0)}")
            print(f"✅ Productos vendidos: {analisis.get('total_productos_vendidos', 0)}")
            print(f"✅ Margen total: ${analisis.get('margen_ganancia_total', 0)}")
        else:
            print(f"❌ Error obteniendo análisis: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 11. Test alertas de stock
    print("\n11. ⚠️ Test alertas de stock")
    try:
        response = requests.get(f"{BASE_URL}/ventas/alertas/stock/{negocio_id}", headers=headers)
        if response.status_code == 200:
            alertas = response.json()
            print(f"✅ Alertas obtenidas")
            print(f"✅ Total alertas: {alertas.get('total', 0)}")
        else:
            print(f"❌ Error obteniendo alertas: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 12. Test productos por vencer
    print("\n12. 📅 Test productos por vencer")
    try:
        response = requests.get(
            f"{BASE_URL}/ventas/alertas/vencimiento/{negocio_id}",
            params={"dias_limite": 7},
            headers=headers
        )
        if response.status_code == 200:
            productos = response.json()
            print(f"✅ Productos por vencer obtenidos")
            print(f"✅ Total productos: {productos.get('total', 0)}")
        else:
            print(f"❌ Error obteniendo productos por vencer: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 FASE 2 COMPLETADA EXITOSAMENTE")
    print("✅ Sistema POS mejorado funcionando correctamente")
    print("✅ Carrito de compras operativo")
    print("✅ Sistema de ventas completo")
    print("✅ Análisis financiero disponible")
    print("✅ Alertas de stock y vencimiento funcionando")
    return True

if __name__ == "__main__":
    success = test_fase2_pos()
    sys.exit(0 if success else 1) 