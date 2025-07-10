#!/usr/bin/env python3
"""
Script para actualizar el frontend con funcionalidades del sistema POS
Autor: Asistente AI
Fecha: 8 de Julio de 2025
"""

import os
import shutil
from datetime import datetime

# Configuración de rutas
FRONTEND_DIR = "../../frontend"
BACKUP_DIR = "backups/frontend_pos_backup"

def create_backup():
    """Crear backup del frontend actual"""
    print("📦 CREANDO BACKUP DEL FRONTEND")
    print("=" * 40)
    
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{BACKUP_DIR}/frontend_backup_{timestamp}"
    
    try:
        shutil.copytree(FRONTEND_DIR, backup_path)
        print(f"✅ Backup creado en: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Error creando backup: {e}")
        return False

def update_product_api():
    """Actualizar productApi.js con funcionalidades POS"""
    print("\n🔄 ACTUALIZANDO PRODUCT API")
    print("=" * 40)
    
    api_file = f"{FRONTEND_DIR}/src/api/productApi.js"
    
    # Nuevas funciones para el sistema POS
    pos_functions = '''
/**
 * Actualiza el stock terminado de un producto (funcionalidad POS).
 * @param {string} productId - El UUID del producto.
 * @param {number} stockTerminado - La nueva cantidad de stock terminado.
 * @returns {Promise<Object>} El objeto del producto actualizado.
 */
export const updateProductStock = async (productId, stockTerminado) => {
  const token = getAuthToken();
  if (!token) throw new Error('No autenticado. Por favor, inicia sesión.');

  const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ stock_terminado: stockTerminado }),
  });
  return handleResponse(response);
};

/**
 * Obtiene productos con información de stock para el sistema POS.
 * @returns {Promise<Array<Object>>} Lista de productos con stock.
 */
export const getProductsWithStock = async () => {
  const token = getAuthToken();
  if (!token) throw new Error('No autenticado. Por favor, inicia sesión.');

  const response = await fetch(`${API_BASE_URL}/products/me`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });
  return handleResponse(response);
};

/**
 * Verifica si un producto tiene stock disponible.
 * @param {Object} product - El objeto del producto.
 * @returns {boolean} True si tiene stock disponible.
 */
export const hasStockAvailable = (product) => {
  return product.stock_terminado && product.stock_terminado > 0;
};

/**
 * Obtiene el estado del stock de un producto.
 * @param {Object} product - El objeto del producto.
 * @returns {string} Estado del stock ('disponible', 'bajo', 'agotado').
 */
export const getStockStatus = (product) => {
  if (!product.stock_terminado || product.stock_terminado <= 0) {
    return 'agotado';
  } else if (product.stock_terminado <= 10) {
    return 'bajo';
  } else {
    return 'disponible';
  }
};
'''
    
    try:
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar la línea antes de la exportación por defecto
        if '// Exportar todas las funciones' in content:
            # Insertar las nuevas funciones antes de la exportación
            content = content.replace(
                '// Exportar todas las funciones como un objeto por defecto para compatibilidad',
                pos_functions + '\n// Exportar todas las funciones como un objeto por defecto para compatibilidad'
            )
            
            # Actualizar la exportación por defecto
            content = content.replace(
                'const productApi = {',
                'const productApi = {\n  updateProductStock,\n  getProductsWithStock,\n  hasStockAvailable,\n  getStockStatus,'
            )
            
            with open(api_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ productApi.js actualizado con funcionalidades POS")
            return True
        else:
            print("❌ No se pudo encontrar el patrón de exportación en productApi.js")
            return False
            
    except Exception as e:
        print(f"❌ Error actualizando productApi.js: {e}")
        return False

def create_pos_screen():
    """Crear pantalla del sistema POS"""
    print("\n🖥️ CREANDO PANTALLA DEL SISTEMA POS")
    print("=" * 40)
    
    pos_screen_file = f"{FRONTEND_DIR}/src/screens/POSScreen.js"
    
    pos_screen_content = '''import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProductsWithStock, updateProductStock, hasStockAvailable, getStockStatus } from '../api/productApi';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';

const POSScreen = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [cart, setCart] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const productsData = await getProductsWithStock();
      setProducts(productsData);
    } catch (err) {
      setError('Error cargando productos: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleProductSelect = (product) => {
    setSelectedProduct(product);
    setQuantity(1);
  };

  const addToCart = () => {
    if (!selectedProduct) return;

    const availableStock = selectedProduct.stock_terminado || 0;
    if (quantity > availableStock) {
      setError(`Solo hay ${availableStock} unidades disponibles`);
      return;
    }

    const cartItem = {
      id: selectedProduct.id,
      nombre: selectedProduct.nombre,
      precio: selectedProduct.precio,
      quantity: quantity,
      stock_terminado: availableStock
    };

    setCart([...cart, cartItem]);
    setSelectedProduct(null);
    setQuantity(1);
    setError(null);
  };

  const removeFromCart = (index) => {
    setCart(cart.filter((_, i) => i !== index));
  };

  const updateStock = async (productId, newStock) => {
    try {
      await updateProductStock(productId, newStock);
      await loadProducts(); // Recargar productos
      setError(null);
    } catch (err) {
      setError('Error actualizando stock: ' + err.message);
    }
  };

  const getTotalCart = () => {
    return cart.reduce((total, item) => total + (item.precio * item.quantity), 0);
  };

  const processSale = async () => {
    if (cart.length === 0) {
      setError('El carrito está vacío');
      return;
    }

    try {
      // Procesar venta - actualizar stock de todos los productos
      for (const item of cart) {
        const product = products.find(p => p.id === item.id);
        if (product) {
          const newStock = product.stock_terminado - item.quantity;
          await updateStock(item.id, newStock);
        }
      }

      // Limpiar carrito después de la venta
      setCart([]);
      setError(null);
      alert('Venta procesada exitosamente');
    } catch (err) {
      setError('Error procesando venta: ' + err.message);
    }
  };

  const getStockStatusColor = (status) => {
    switch (status) {
      case 'disponible': return 'text-green-600';
      case 'bajo': return 'text-yellow-600';
      case 'agotado': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto p-6">
        <div className="text-center">Cargando productos...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Sistema POS - Panadería Ñiam</h1>
        <Button onClick={() => navigate('/dashboard')} variant="outline">
          Volver al Dashboard
        </Button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Lista de Productos */}
        <div className="lg:col-span-2">
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Productos Disponibles</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {products.map((product) => (
                <div
                  key={product.id}
                  className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                    selectedProduct?.id === product.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => handleProductSelect(product)}
                >
                  <h3 className="font-semibold">{product.nombre}</h3>
                  <p className="text-gray-600 text-sm">{product.descripcion}</p>
                  <div className="flex justify-between items-center mt-2">
                    <span className="font-bold text-lg">${product.precio}</span>
                    <span className={`text-sm font-medium ${getStockStatusColor(getStockStatus(product))}`}>
                      Stock: {product.stock_terminado || 0}
                    </span>
                  </div>
                  {!hasStockAvailable(product) && (
                    <div className="text-red-600 text-sm mt-1">Agotado</div>
                  )}
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Panel de Venta */}
        <div className="lg:col-span-1">
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Venta</h2>
            
            {selectedProduct && (
              <div className="mb-4 p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold">{selectedProduct.nombre}</h3>
                <p className="text-gray-600">${selectedProduct.precio}</p>
                <div className="mt-2">
                  <Label htmlFor="quantity">Cantidad:</Label>
                  <Input
                    id="quantity"
                    type="number"
                    min="1"
                    max={selectedProduct.stock_terminado || 0}
                    value={quantity}
                    onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
                    className="mt-1"
                  />
                </div>
                <Button onClick={addToCart} className="w-full mt-2">
                  Agregar al Carrito
                </Button>
              </div>
            )}

            {/* Carrito */}
            <div className="mb-4">
              <h3 className="font-semibold mb-2">Carrito</h3>
              {cart.length === 0 ? (
                <p className="text-gray-500 text-sm">Carrito vacío</p>
              ) : (
                <div className="space-y-2">
                  {cart.map((item, index) => (
                    <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                      <div>
                        <div className="font-medium">{item.nombre}</div>
                        <div className="text-sm text-gray-600">
                          {item.quantity} x ${item.precio}
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="font-semibold">${item.precio * item.quantity}</span>
                        <Button
                          onClick={() => removeFromCart(index)}
                          variant="outline"
                          size="sm"
                        >
                          ×
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Total y Procesar Venta */}
            {cart.length > 0 && (
              <div className="border-t pt-4">
                <div className="flex justify-between items-center mb-4">
                  <span className="text-lg font-semibold">Total:</span>
                  <span className="text-2xl font-bold">${getTotalCart().toFixed(2)}</span>
                </div>
                <Button onClick={processSale} className="w-full" size="lg">
                  Procesar Venta
                </Button>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};

export default POSScreen;
'''
    
    try:
        with open(pos_screen_file, 'w', encoding='utf-8') as f:
            f.write(pos_screen_content)
        
        print("✅ POSScreen.js creada")
        return True
    except Exception as e:
        print(f"❌ Error creando POSScreen.js: {e}")
        return False

def update_manage_products_screen():
    """Actualizar ManageProductsScreen con funcionalidades de stock"""
    print("\n📝 ACTUALIZANDO MANAGE PRODUCTS SCREEN")
    print("=" * 40)
    
    manage_products_file = f"{FRONTEND_DIR}/src/screens/ManageProductsScreen.js"
    
    try:
        with open(manage_products_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Agregar import para las nuevas funciones
        if 'import { getMyProducts, deleteProduct } from' in content:
            content = content.replace(
                'import { getMyProducts, deleteProduct } from',
                'import { getMyProducts, deleteProduct, updateProductStock, getStockStatus } from'
            )
        
        # Buscar la función que renderiza los productos y agregar información de stock
        if 'products.map((product) => (' in content:
            # Encontrar el patrón de renderizado de productos
            import re
            pattern = r'(products\.map\(\(product\) => \([\s\S]*?\)\))'
            match = re.search(pattern, content)
            
            if match:
                product_render = match.group(1)
                
                # Agregar información de stock al renderizado
                new_product_render = product_render.replace(
                    '<div className="flex justify-between items-center">',
                    '''<div className="flex justify-between items-center">
                    <div className="text-sm">
                      <span className={`font-medium ${getStockStatus(product) === 'agotado' ? 'text-red-600' : 
                                        getStockStatus(product) === 'bajo' ? 'text-yellow-600' : 'text-green-600'}`}>
                        Stock: {product.stock_terminado || 0}
                      </span>
                    </div>'''
                )
                
                content = content.replace(product_render, new_product_render)
        
        # Agregar función para actualizar stock
        if 'const handleDelete = async (productId) => {' in content:
            # Agregar función de actualización de stock antes de handleDelete
            stock_function = '''
  const handleUpdateStock = async (productId, newStock) => {
    try {
      await updateProductStock(productId, newStock);
      loadProducts(); // Recargar productos
    } catch (error) {
      console.error('Error actualizando stock:', error);
      alert('Error actualizando stock: ' + error.message);
    }
  };

'''
            content = content.replace('const handleDelete = async (productId) => {', stock_function + 'const handleDelete = async (productId) => {')
        
        with open(manage_products_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ ManageProductsScreen.js actualizada con funcionalidades de stock")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando ManageProductsScreen.js: {e}")
        return False

def update_app_routes():
    """Actualizar App.js para incluir la ruta del POS"""
    print("\n🛣️ ACTUALIZANDO RUTAS DE LA APLICACIÓN")
    print("=" * 40)
    
    app_file = f"{FRONTEND_DIR}/src/App.js"
    
    try:
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Agregar import del POSScreen
        if 'import ManageProductsScreen from' in content:
            content = content.replace(
                'import ManageProductsScreen from',
                'import ManageProductsScreen from\nimport POSScreen from'
            )
            content = content.replace(
                "from './screens/ManageProductsScreen';",
                "from './screens/ManageProductsScreen';\nimport POSScreen from './screens/POSScreen';"
            )
        
        # Agregar ruta del POS
        if '<Route path="/manage-products" element={<ManageProductsScreen />} />' in content:
            content = content.replace(
                '<Route path="/manage-products" element={<ManageProductsScreen />} />',
                '''<Route path="/manage-products" element={<ManageProductsScreen />} />
            <Route path="/pos" element={<POSScreen />} />'''
            )
        
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ App.js actualizada con ruta del POS")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando App.js: {e}")
        return False

def update_dashboard_screen():
    """Actualizar DashboardScreen para incluir enlace al POS"""
    print("\n🏠 ACTUALIZANDO DASHBOARD SCREEN")
    print("=" * 40)
    
    dashboard_file = f"{FRONTEND_DIR}/src/screens/DashboardScreen.js"
    
    try:
        with open(dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar la sección de navegación y agregar enlace al POS
        if 'Gestionar Productos' in content:
            # Agregar botón del POS después del botón de Gestionar Productos
            pos_button = '''
            <Button
              onClick={() => navigate('/pos')}
              className="w-full mb-4 bg-green-600 hover:bg-green-700"
            >
              🛍️ Sistema POS
            </Button>
'''
            
            # Buscar el patrón del botón de Gestionar Productos
            import re
            pattern = r'(<Button[\s\S]*?Gestionar Productos[\s\S]*?</Button>)'
            match = re.search(pattern, content)
            
            if match:
                manage_products_button = match.group(1)
                content = content.replace(manage_products_button, manage_products_button + pos_button)
        
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ DashboardScreen.js actualizada con enlace al POS")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando DashboardScreen.js: {e}")
        return False

def main():
    """Función principal de actualización del frontend"""
    print("🔄 ACTUALIZACIÓN DEL FRONTEND PARA SISTEMA POS")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Verificar que el directorio frontend existe
    if not os.path.exists(FRONTEND_DIR):
        print("❌ Directorio frontend no encontrado")
        return
    
    # Crear backup
    if not create_backup():
        print("❌ No se pudo crear el backup. Abortando actualización.")
        return
    
    # Ejecutar actualizaciones
    updates = [
        ("Product API", update_product_api),
        ("POS Screen", create_pos_screen),
        ("Manage Products Screen", update_manage_products_screen),
        ("App Routes", update_app_routes),
        ("Dashboard Screen", update_dashboard_screen),
    ]
    
    success_count = 0
    for name, update_func in updates:
        print(f"\n🔄 Actualizando {name}...")
        if update_func():
            success_count += 1
        else:
            print(f"⚠️ Falló la actualización de {name}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE ACTUALIZACIÓN FRONTEND")
    print("=" * 60)
    print(f"✅ Actualizaciones exitosas: {success_count}/{len(updates)}")
    
    if success_count == len(updates):
        print("\n🎉 ¡FRONTEND ACTUALIZADO EXITOSAMENTE!")
        print("✅ El frontend está listo para el sistema POS")
        print("\n📋 Funcionalidades agregadas:")
        print("   • Campo stock_terminado en productos")
        print("   • Pantalla del sistema POS")
        print("   • Gestión de stock en tiempo real")
        print("   • Carrito de compras")
        print("   • Procesamiento de ventas")
        print("   • Navegación integrada")
    else:
        print(f"\n⚠️ {len(updates) - success_count} actualizaciones fallaron")
        print("Revisa los errores arriba y ejecuta manualmente las actualizaciones fallidas")

if __name__ == "__main__":
    main() 