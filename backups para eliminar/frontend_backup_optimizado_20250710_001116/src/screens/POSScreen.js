import React, { useState, useEffect } from 'react';
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
