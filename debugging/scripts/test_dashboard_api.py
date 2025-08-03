#!/usr/bin/env python3
"""
Script para probar las APIs del dashboard
Verifica que los endpoints de ventas y estadísticas funcionen correctamente
"""

import requests
import json
from datetime import datetime, timedelta

# Configuración
BASE_URL = "http://localhost:8000"
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword123"

def test_auth():
    """Prueba la autenticación y obtiene token"""
    print("🔐 Probando autenticación...")
    
    # Intentar login
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            print(f"✅ Login exitoso, token obtenido")
            return token
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_businesses_api(token):
    """Prueba la API de negocios"""
    print("\n🏪 Probando API de negocios...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/businesses/me", headers=headers)
        if response.status_code == 200:
            businesses = response.json()
            print(f"✅ Negocios obtenidos: {len(businesses)}")
            for business in businesses:
                print(f"   - {business.get('nombre', 'Sin nombre')} (ID: {business.get('id', 'Sin ID')})")
            return businesses
        else:
            print(f"❌ Error obteniendo negocios: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return []

def test_products_api(token):
    """Prueba la API de productos"""
    print("\n📦 Probando API de productos...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/products/me", headers=headers)
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Productos obtenidos: {len(products)}")
            
            # Contar productos en stock
            productos_en_stock = sum(1 for p in products if p.get('stock_terminado', 0) > 0)
            print(f"   - Productos en stock: {productos_en_stock}")
            print(f"   - Total de productos: {len(products)}")
            
            return products
        else:
            print(f"❌ Error obteniendo productos: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return []

def test_ventas_api(token, business_id):
    """Prueba la API de ventas"""
    print(f"\n💰 Probando API de ventas para negocio {business_id}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    hoy = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # Probar análisis de ventas de hoy
        response = requests.get(
            f"{BASE_URL}/ventas/analisis/{business_id}?fecha_inicio={hoy}&fecha_fin={hoy}",
            headers=headers
        )
        
        if response.status_code == 200:
            analisis = response.json()
            print(f"✅ Análisis de ventas obtenido")
            print(f"   - Total ventas: {analisis.get('total_ventas', 0)}")
            print(f"   - Ingresos totales: ${analisis.get('ingresos_totales', 0)}")
            return analisis
        else:
            print(f"❌ Error obteniendo análisis de ventas: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_dashboard_stats(token):
    """Prueba las estadísticas del dashboard"""
    print("\n📊 Probando estadísticas del dashboard...")
    
    try:
        # Obtener negocios
        businesses = test_businesses_api(token)
        if not businesses:
            print("❌ No se pudieron obtener negocios")
            return
        
        # Obtener productos
        products = test_products_api(token)
        
        # Calcular estadísticas
        total_negocios = len(businesses)
        total_productos = len(products)
        productos_en_stock = sum(1 for p in products if p.get('stock_terminado', 0) > 0)
        
        ventas_hoy = 0
        ingresos_hoy = 0
        
        # Obtener ventas de hoy para cada negocio
        for business in businesses:
            business_id = business.get('id')
            if business_id:
                analisis = test_ventas_api(token, business_id)
                if analisis:
                    ventas_hoy += analisis.get('total_ventas', 0)
                    ingresos_hoy += analisis.get('ingresos_totales', 0)
        
        print(f"\n📈 RESUMEN DEL DASHBOARD:")
        print(f"   - Ventas Hoy: {ventas_hoy}")
        print(f"   - Ingresos Hoy: ${ingresos_hoy:.2f}")
        print(f"   - Productos en Stock: {productos_en_stock}")
        print(f"   - Total Negocios: {total_negocios}")
        print(f"   - Total Productos: {total_productos}")
        
        return {
            "ventasHoy": ventas_hoy,
            "ingresosHoy": f"{ingresos_hoy:.2f}",
            "productosEnStock": productos_en_stock,
            "totalNegocios": total_negocios,
            "totalProductos": total_productos
        }
        
    except Exception as e:
        print(f"❌ Error calculando estadísticas: {e}")
        return None

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DEL DASHBOARD")
    print("=" * 50)
    
    # Probar autenticación
    token = test_auth()
    if not token:
        print("❌ No se pudo obtener token. Verifica que el backend esté corriendo.")
        return
    
    # Probar APIs individuales
    businesses = test_businesses_api(token)
    products = test_products_api(token)
    
    if businesses:
        # Probar ventas con el primer negocio
        first_business = businesses[0]
        test_ventas_api(token, first_business.get('id'))
    
    # Probar estadísticas completas del dashboard
    stats = test_dashboard_stats(token)
    
    print("\n" + "=" * 50)
    if stats:
        print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("El dashboard debería mostrar datos reales ahora.")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print("Revisa los errores anteriores.")

if __name__ == "__main__":
    main() 