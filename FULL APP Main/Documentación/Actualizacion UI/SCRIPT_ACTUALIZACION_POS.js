// SCRIPT_ACTUALIZACION_POS.js
// Actualización de POSScreen.js según mockup Gemini

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProductsWithStock, updateProductStock, hasStockAvailable, getStockStatus } from '../api/productApi';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Search, Clock, User, ShoppingCart, CreditCard, DollarSign } from 'lucide-react';

const POSScreen = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [cart, setCart] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [currentDateTime, setCurrentDateTime] = useState(new Date());
  const [selectedPaymentMethod, setSelectedPaymentMethod] = useState(null);
  const navigate = useNavigate();

  // Categorías con colores del mockup
  const categories = [
    { id: 'panaderia', name: 'Panadería', color: 'bg-blue-500 hover:bg-blue-600' },
    { id: 'bebidas', name: 'Bebidas', color: 'bg-green-500 hover:bg-green-600' },
    { id: 'fiambres', name: 'Fiambres', color: 'bg-yellow-500 hover:bg-yellow-600' },
    { id: 'lacteos', name: 'Lácteos', color: 'bg-red-500 hover:bg-red-600' },
    { id: 'limpieza', name: 'Limpieza', color: 'bg-purple-500 hover:bg-purple-600' },
    { id: 'snacks', name: 'Snacks', color: 'bg-indigo-500 hover:bg-indigo-600' }
  ];

  // Métodos de pago
  const paymentMethods = [
    { id: 'efectivo', name: 'Efectivo', icon: DollarSign },
    { id: 'tarjeta', name: 'Tarjeta', icon: CreditCard },
    { id: 'mercadopago', name: 'Mercado Pago', icon: ShoppingCart },
    { id: 'otros', name: 'Otros Medios', icon: CreditCard }
  ];

  useEffect(() => {
    loadProducts();
    // Actualizar fecha y hora cada minuto
    const timer = setInterval(() => {
      setCurrentDateTime(new Date());
    }, 60000);
    return () => clearInterval(timer);
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

  // Filtrar productos por búsqueda y categoría
  const filteredProducts = products.filter(product => {
    const matchesSearch = product.nombre.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || product.categoria === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const addToCart = (product) => {
    const existingItem = cart.find(item => item.id === product.id);
    
    if (existingItem) {
      setCart(cart.map(item => 
        item.id === product.id 
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      setCart([...cart, { 
        id: product.id, 
        nombre: product.nombre, 
        precio: product.precio, 
        quantity: 1,
        stock_terminado: product.stock_terminado || 0
      }]);
    }
    showMessage(`"${product.nombre}" agregado al carrito.`, 'success');
  };

  const updateCartQuantity = (index, action) => {
    const updatedCart = [...cart];
    if (action === 'increment') {
      updatedCart[index].quantity += 1;
    } else if (action === 'decrement') {
      updatedCart[index].quantity -= 1;
      if (updatedCart[index].quantity <= 0) {
        updatedCart.splice(index, 1);
      }
    }
    setCart(updatedCart);
  };

  const removeFromCart = (index) => {
    const itemName = cart[index].nombre;
    setCart(cart.filter((_, i) => i !== index));
    showMessage(`"${itemName}" eliminado del carrito.`, 'info');
  };

  const clearCart = () => {
    setCart([]);
    setSelectedPaymentMethod(null);
  };

  const showMessage = (message, type) => {
    // Implementar sistema de notificaciones
    console.log(`${type.toUpperCase()}: ${message}`);
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-AR', { 
      style: 'currency', 
      currency: 'ARS', 
      minimumFractionDigits: 2 
    }).format(amount);
  };

  const getSubtotal = () => {
    return cart.reduce((total, item) => total + (item.precio * item.quantity), 0);
  };

  const getTax = () => {
    return getSubtotal() * 0.21; // 21% IVA
  };

  const getTotal = () => {
    return getSubtotal() + getTax();
  };

  const processSale = async () => {
    if (cart.length === 0) {
      showMessage('El carrito está vacío', 'error');
      return;
    }

    if (!selectedPaymentMethod) {
      showMessage('Selecciona un método de pago', 'error');
      return;
    }

    try {
      // Procesar venta - actualizar stock de todos los productos
      for (const item of cart) {
        const product = products.find(p => p.id === item.id);
        if (product) {
          const newStock = product.stock_terminado - item.quantity;
          await updateProductStock(item.id, newStock);
        }
      }

      showMessage('Venta procesada exitosamente', 'success');
      clearCart();
      await loadProducts(); // Recargar productos
    } catch (err) {
      showMessage('Error procesando venta: ' + err.message, 'error');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando productos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-blue-600">Punto de Venta</h1>
          <div className="text-gray-600 text-sm md:text-base flex items-center space-x-4">
            <div className="flex items-center">
              <Clock className="w-4 h-4 mr-2" />
              <span>{currentDateTime.toLocaleDateString('es-AR', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}</span>
            </div>
            <div className="flex items-center">
              <Clock className="w-4 h-4 mr-2" />
              <span>{currentDateTime.toLocaleTimeString('es-AR', { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}</span>
            </div>
            <div className="flex items-center">
              <User className="w-4 h-4 mr-2" />
              <span>Vendedor POS</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex flex-grow p-6 gap-6">
        {/* Left Panel - Products */}
        <section className="flex-1 bg-white rounded-xl shadow-sm p-6">
          {/* Search Bar */}
          <div className="relative mb-6">
            <Input
              type="text"
              placeholder="Buscar producto por nombre o SKU..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4"
            />
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          </div>

          {/* Categories */}
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Categorías</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 mb-6">
            <button
              onClick={() => setSelectedCategory('all')}
              className={`py-2 px-3 rounded-lg text-sm font-medium transition-colors ${
                selectedCategory === 'all' 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Todos
            </button>
            {categories.map(category => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`py-2 px-3 rounded-lg text-sm font-medium transition-colors ${
                  selectedCategory === category.id 
                    ? category.color + ' text-white' 
                    : category.color.replace('bg-', 'bg-gray-200 ').replace('hover:bg-', 'hover:bg-gray-300 ') + 'text-gray-700'
                }`}
              >
                {category.name}
              </button>
            ))}
          </div>

          {/* Products List */}
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Productos</h2>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {filteredProducts.map((product) => (
              <div
                key={product.id}
                className="flex justify-between items-center bg-gray-50 p-4 rounded-lg border border-gray-200 hover:border-gray-300 transition-colors"
              >
                <div>
                  <p className="font-medium text-gray-900">{product.nombre}</p>
                  <p className="text-sm text-gray-500">{formatCurrency(product.precio)}</p>
                  <p className="text-xs text-gray-400">Stock: {product.stock_terminado || 0}</p>
                </div>
                <Button
                  onClick={() => addToCart(product)}
                  disabled={!hasStockAvailable(product)}
                  className="bg-blue-600 hover:bg-blue-700 text-white text-sm py-1 px-3"
                >
                  Agregar
                </Button>
              </div>
            ))}
          </div>
        </section>

        {/* Right Panel - Cart and Payment */}
        <div className="w-full md:w-1/2 lg:w-2/5 xl:w-1/3 space-y-6">
          {/* Cart */}
          <Card className="p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Detalle de Venta</h2>
            <div className="overflow-y-auto max-h-64 mb-6">
              {cart.length === 0 ? (
                <p className="text-center text-gray-500 py-4">El carrito está vacío.</p>
              ) : (
                <table className="w-full text-left">
                  <thead>
                    <tr className="text-gray-600 text-sm border-b pb-2">
                      <th className="w-1/2">Ítem</th>
                      <th className="w-1/5 text-center">Cant.</th>
                      <th className="w-1/5 text-right">P. Unit.</th>
                      <th className="w-1/5 text-right">Subtotal</th>
                      <th className="w-1/12 text-center"></th>
                    </tr>
                  </thead>
                  <tbody>
                    {cart.map((item, index) => (
                      <tr key={index} className="border-b border-gray-100 last:border-b-0">
                        <td className="py-3 pr-2 font-medium">{item.nombre}</td>
                        <td className="py-3 px-2 text-center">
                          <div className="flex items-center justify-center gap-1">
                            <button
                              onClick={() => updateCartQuantity(index, 'decrement')}
                              className="w-6 h-6 rounded-full bg-gray-200 text-gray-700 hover:bg-gray-300 flex items-center justify-center text-sm font-bold"
                            >
                              -
                            </button>
                            <span className="mx-2">{item.quantity}</span>
                            <button
                              onClick={() => updateCartQuantity(index, 'increment')}
                              className="w-6 h-6 rounded-full bg-gray-200 text-gray-700 hover:bg-gray-300 flex items-center justify-center text-sm font-bold"
                            >
                              +
                            </button>
                          </div>
                        </td>
                        <td className="py-3 px-2 text-right text-sm text-gray-600">
                          {formatCurrency(item.precio)}
                        </td>
                        <td className="py-3 pl-2 text-right font-semibold">
                          {formatCurrency(item.precio * item.quantity)}
                        </td>
                        <td className="py-3 pl-2 text-center">
                          <button
                            onClick={() => removeFromCart(index)}
                            className="text-red-500 hover:text-red-700"
                          >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                            </svg>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>

            {/* Totals */}
            <div className="border-t pt-4 text-right space-y-2">
              <p className="text-lg text-gray-700">
                Subtotal: <span className="font-semibold">{formatCurrency(getSubtotal())}</span>
              </p>
              <p className="text-lg text-gray-700">
                Impuestos (IVA): <span className="font-semibold">{formatCurrency(getTax())}</span>
              </p>
              <p className="text-3xl font-bold text-blue-600">
                TOTAL: <span>{formatCurrency(getTotal())}</span>
              </p>
            </div>
          </Card>

          {/* Payment Methods */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">Opciones de Pago</h2>
            <div className="grid grid-cols-2 gap-4 mb-8">
              {paymentMethods.map(method => (
                <button
                  key={method.id}
                  onClick={() => setSelectedPaymentMethod(method.id)}
                  className={`py-3 px-4 rounded-lg font-medium transition-colors ${
                    selectedPaymentMethod === method.id
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {method.name}
                </button>
              ))}
            </div>

            {/* Actions */}
            <h2 className="text-xl font-semibold text-gray-800 mb-6">Acciones de Venta</h2>
            <div className="flex flex-col gap-4">
              <Button
                onClick={clearCart}
                variant="outline"
                className="w-full py-3"
              >
                Cancelar Venta
              </Button>
              <Button
                onClick={processSale}
                disabled={cart.length === 0 || !selectedPaymentMethod}
                className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white"
              >
                Finalizar Venta
              </Button>
            </div>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default POSScreen; 