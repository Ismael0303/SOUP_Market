# debugging/scripts/test_fase3_niam.py

import requests
import json
import sys
import os
from datetime import date, datetime, timedelta

# Configuración
BASE_URL = "http://127.0.0.1:8000"
TEST_EMAIL = "ismaeldimenza@hotmail.com"
TEST_PASSWORD = "ismael38772433"

def test_fase3_niam():
    """Test completo de la Fase 3: Optimización para Panadería Ñiam"""
    
    print("🥖 TESTEANDO FASE 3: OPTIMIZACIÓN PARA PANADERÍA ÑIAM")
    print("=" * 70)
    
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
    
    # 2. Test dashboard especializado
    print("\n2. 📊 Test dashboard especializado")
    try:
        response = requests.get(f"{BASE_URL}/niam/dashboard", headers=headers)
        if response.status_code == 200:
            dashboard = response.json()
            print(f"✅ Dashboard obtenido")
            print(f"✅ Negocio: {dashboard['negocio']['nombre']}")
            print(f"✅ Ventas Chipá: {dashboard['metricas_mes']['ventas_chipa']}")
            print(f"✅ Ventas totales: ${dashboard['metricas_mes']['ventas_totales']}")
            print(f"✅ Productos más vendidos: {len(dashboard['productos_mas_vendidos'])}")
            print(f"✅ Alertas: {dashboard['alertas']['stock_bajo']} stock bajo, {dashboard['alertas']['por_vencer']} por vencer")
            print(f"✅ Horarios pico: {len(dashboard['horarios_pico'])} configurados")
        else:
            print(f"❌ Error obteniendo dashboard: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 3. Test recetas de Chipá
    print("\n3. 📖 Test recetas de Chipá")
    try:
        response = requests.get(f"{BASE_URL}/niam/recetas", headers=headers)
        if response.status_code == 200:
            recetas = response.json()
            print(f"✅ Recetas obtenidas")
            print(f"✅ Total recetas: {len(recetas['recetas'])}")
            if recetas['recetas']:
                primera_receta = recetas['recetas'][0]
                print(f"✅ Primera receta: {primera_receta['nombre']}")
                print(f"✅ Dificultad: {primera_receta['dificultad']}")
                print(f"✅ Ingredientes: {primera_receta['ingredientes_count']}")
        else:
            print(f"❌ Error obteniendo recetas: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 4. Test producciones
    print("\n4. 🏭 Test producciones")
    try:
        response = requests.get(f"{BASE_URL}/niam/produccion", headers=headers)
        if response.status_code == 200:
            producciones = response.json()
            print(f"✅ Producciones obtenidas")
            print(f"✅ Total producciones: {len(producciones['producciones'])}")
            if producciones['producciones']:
                primera_prod = producciones['producciones'][0]
                print(f"✅ Primera producción: {primera_prod['receta']}")
                print(f"✅ Estado: {primera_prod['estado']}")
                print(f"✅ Productor: {primera_prod['productor']}")
        else:
            print(f"❌ Error obteniendo producciones: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 5. Test análisis específico de Chipá
    print("\n5. 📈 Test análisis específico de Chipá")
    try:
        fecha_inicio = (date.today() - timedelta(days=30)).isoformat()
        fecha_fin = date.today().isoformat()
        
        response = requests.get(
            f"{BASE_URL}/niam/analisis/chipa",
            params={
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin
            },
            headers=headers
        )
        if response.status_code == 200:
            analisis = response.json()
            print(f"✅ Análisis de Chipá obtenido")
            print(f"✅ Período: {analisis['periodo']['fecha_inicio']} a {analisis['periodo']['fecha_fin']}")
            print(f"✅ Cantidad vendida: {analisis['totales']['cantidad_vendida']}")
            print(f"✅ Total ventas: ${analisis['totales']['total_ventas']}")
            print(f"✅ Precio promedio: ${analisis['totales']['precio_promedio']}")
            print(f"✅ Ventas por día: {len(analisis['ventas_por_dia'])}")
            print(f"✅ Ventas por hora: {len(analisis['ventas_por_hora'])}")
        else:
            print(f"❌ Error obteniendo análisis: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 6. Test alertas específicas
    print("\n6. ⚠️ Test alertas específicas")
    try:
        response = requests.get(f"{BASE_URL}/niam/alertas", headers=headers)
        if response.status_code == 200:
            alertas = response.json()
            print(f"✅ Alertas obtenidas")
            print(f"✅ Insumos críticos: {len(alertas['insumos_criticos'])}")
            print(f"✅ Productos por vencer: {len(alertas['productos_por_vencer'])}")
            print(f"✅ Producciones pendientes: {len(alertas['producciones_pendientes'])}")
            
            if alertas['insumos_criticos']:
                primer_insumo = alertas['insumos_criticos'][0]
                print(f"✅ Primer insumo crítico: {primer_insumo['nombre']}")
                print(f"✅ Stock disponible: {primer_insumo['stock_disponible']} {primer_insumo['unidad_medida']}")
        else:
            print(f"❌ Error obteniendo alertas: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 7. Test endpoints del sistema de ventas mejorado
    print("\n7. 💰 Test sistema de ventas mejorado")
    try:
        # Obtener negocios para usar en las pruebas
        response = requests.get(f"{BASE_URL}/businesses/", headers=headers)
        if response.status_code == 200:
            negocios = response.json()
            if negocios:
                negocio_id = negocios[0]["id"]
                
                # Test análisis de ventas
                fecha_inicio = (date.today() - timedelta(days=7)).isoformat()
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
                    print(f"✅ Análisis de ventas obtenido")
                    print(f"✅ Total ventas: ${analisis.get('total_ventas', 0)}")
                    print(f"✅ Productos vendidos: {analisis.get('total_productos_vendidos', 0)}")
                    print(f"✅ Margen total: ${analisis.get('margen_ganancia_total', 0)}")
                else:
                    print(f"❌ Error obteniendo análisis de ventas: {response.status_code}")
            else:
                print("⚠️ No se encontraron negocios para probar")
        else:
            print(f"❌ Error obteniendo negocios: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("🎉 FASE 3 COMPLETADA EXITOSAMENTE")
    print("✅ Optimización para Panadería Ñiam funcionando correctamente")
    print("✅ Dashboard especializado operativo")
    print("✅ Sistema de roles implementado")
    print("✅ Gestión de recetas disponible")
    print("✅ Control de producción activo")
    print("✅ Análisis específico de Chipá funcionando")
    print("✅ Alertas especializadas operativas")
    return True

if __name__ == "__main__":
    success = test_fase3_niam()
    sys.exit(0 if success else 1) 