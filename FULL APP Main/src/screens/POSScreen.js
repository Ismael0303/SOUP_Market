// POSScreen.js - Actualizado según mockups Gemini
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProductsWithStock, updateProductStock } from '../api/productApi';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { 
  Search, 
  Clock, 
  User, 
  ShoppingCart, 
  CreditCard, 
  DollarSign,
  Plus,
  Minus,
  Trash2,
  Package,
  TrendingUp
} from 'lucide-react';
import { showSuccess, showError, showInfo } from '../utils/notifications';

const POSScreen = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [cart, setCart] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [currentDateTime, setCurrentDateTime] = useState(new Date());
  const [selectedPaymentMethod, setSelectedPaymentMethod] = useState(null);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const navigate = useNavigate();

  // Categorías con colores del mockup
  const categories = [
    { id: 'all', name: 'Todos', color: 'bg-gray-500 hover:bg-gray-600' },
    { id: 'panaderia', name: 'Panadería', color: 'bg-blue-500 hover:bg-blue-600' },
    { id: 'bebidas', name: 'Bebidas', color: 'bg-green-500 hover:bg-green-600' },
    { id: 'fiambres', name: 'Fiambres', color: 'bg-yellow-500 hover:bg-yellow-600' },
    { id: 'lacteos', name: 'Lácteos', color: 'bg-red-500 hover:bg-red-600' },
    { id: 'limpieza', name: 'Limpieza', color: 'bg-purple-500 hover:bg-purple-600' },
    { id: 'snacks', name: 'Snacks', color: 'bg-indigo-500 hover:bg-indigo-600' }
  ];

  // Métodos de pago
  const paymentMethods = [
    { id: 'efectivo', name: 'Efectivo', icon: DollarSign, color: 'bg-green-100 text-green-700' },
    { id: 'tarjeta', name: 'Tarjeta', icon: CreditCard, color: 'bg-blue-100 text-blue-700' },
    { id: 'mercadopago', name: 'Mercado Pago', icon: ShoppingCart, color: 'bg-purple-100 text-purple-700' },
    { id: 'transferencia', name: 'Transferencia', icon: CreditCard, color: 'bg-orange-100 text-orange-700' }
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
      showError('Error cargando productos: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Filtrar productos por búsqueda y categoría
  const filteredProducts = products.filter(product => {
    const matchesSearch = product.nombre.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || product.categoria === selectedCategory;
    return matchesSearch && matchesCategory && (product.stock_terminado > 0 || product.stock_terminado === undefined);
  });

  const addToCart = (product) => {
    const existingItem = cart.find(item => item.id === product.id);
    
    if (existingItem) {
      // Verificar stock disponible
      if (product.stock_terminado && existingItem.quantity >= product.stock_terminado) {
        showError('No hay suficiente stock disponible');
        return;
      }
      
      setCart(cart.map(item => 
        item.id === product.id 
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      setCart([...cart, { 
        id: product.id, 
        nombre: product.nombre, 
        precio: product.precio_venta || product.precio, 
        quantity: 1,
        stock_terminado: product.stock_terminado || 0,
        categoria: product.categoria
      }]);
    }
    showSuccess(`"${product.nombre}" agregado al carrito`);
  };

  const updateCartQuantity = (index, action) => {
    const updatedCart = [...cart];
    const item = updatedCart[index];
    
    if (action === 'increment') {
      // Verificar stock disponible
      if (item.stock_terminado && item.quantity >= item.stock_terminado) {
        showError('No hay suficiente stock disponible');
        return;
      }
      item.quantity += 1;
    } else if (action === 'decrement') {
      item.quantity -= 1;
      if (item.quantity <= 0) {
        updatedCart.splice(index, 1);
      }
    }
    setCart(updatedCart);
  };

  const removeFromCart = (index) => {
    const itemName = cart[index].nombre;
    setCart(cart.filter((_, i) => i !== index));
    showInfo(`"${itemName}" eliminado del carrito`);
  };

  const clearCart = () => {
    setCart([]);
    setSelectedPaymentMethod(null);
    setShowPaymentModal(false);
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
      showError('El carrito está vacío');
      return;
    }

    if (!selectedPaymentMethod) {
      showError('Selecciona un método de pago');
      return;
    }

    try {
      // Procesar venta - actualizar stock de todos los productos
      for (const item of cart) {
        const product = products.find(p => p.id === item.id);
        if (product && product.stock_terminado !== undefined) {
          const newStock = product.stock_terminado - item.quantity;
          await updateProductStock(item.id, newStock);
        }
      }

      showSuccess('Venta procesada exitosamente');
      clearCart();
      await loadProducts(); // Recargar productos
    } catch (err) {
      showError('Error procesando venta: ' + err.message);
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
    <div className="min-h-screen flex bg-gray-100">
      {/* Panel Principal - Productos */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-blue-600">Punto de Venta</h1>
              <p className="text-gray-600">Venta rápida y eficiente</p>
            </div>
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
            </div>
          </div>
        </header>

        {/* Barra de Búsqueda */}
        <div className="p-4 bg-white border-b border-gray-200">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <Input
              type="text"
              placeholder="Buscar productos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-3 text-lg"
            />
          </div>
        </div>

        {/* Filtros de Categorías */}
        <div className="p-4 bg-white border-b border-gray-200">
          <div className="flex flex-wrap gap-2">
            {categories.map(category => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-4 py-2 rounded-lg text-white font-medium transition-colors ${category.color} ${
                  selectedCategory === category.id ? 'ring-2 ring-offset-2 ring-blue-300' : ''
                }`}
              >
                {category.name}
              </button>
            ))}
          </div>
        </div>

        {/* Grid de Productos */}
        <div className="flex-1 p-4 overflow-auto">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
            {filteredProducts.map(product => (
              <Card 
                key={product.id} 
                className="cursor-pointer hover:shadow-lg transition-shadow duration-200"
                onClick={() => addToCart(product)}
              >
                <div className="p-4">
                  <div className="w-full h-32 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg mb-3 flex items-center justify-center">
                    <Package className="w-12 h-12 text-white" />
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-1 line-clamp-2">
                    {product.nombre}
                  </h3>
                  <p className="text-sm text-gray-600 mb-2 line-clamp-1">
                    {product.categoria || 'Sin categoría'}
                  </p>
                  <div className="flex justify-between items-center">
                    <span className="text-lg font-bold text-green-600">
                      {formatCurrency(product.precio_venta || product.precio)}
                    </span>
                    {product.stock_terminado !== undefined && (
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        product.stock_terminado > 0 
                          ? 'bg-green-100 text-green-700' 
                          : 'bg-red-100 text-red-700'
                      }`}>
                        {product.stock_terminado > 0 ? `${product.stock_terminado}` : 'Agotado'}
                      </span>
                    )}
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>

      {/* Panel Lateral - Carrito */}
      <div className="w-96 bg-white shadow-lg flex flex-col">
        {/* Header del Carrito */}
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-900">Carrito de Compras</h2>
            <div className="flex items-center space-x-2">
              <ShoppingCart className="w-5 h-5 text-blue-600" />
              <span className="text-sm text-gray-600">{cart.length} items</span>
            </div>
          </div>
        </div>

        {/* Items del Carrito */}
        <div className="flex-1 overflow-auto p-4">
          {cart.length === 0 ? (
            <div className="text-center py-8">
              <ShoppingCart className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">El carrito está vacío</p>
              <p className="text-sm text-gray-400">Agrega productos para comenzar</p>
            </div>
          ) : (
            <div className="space-y-3">
              {cart.map((item, index) => (
                <div key={index} className="bg-gray-50 rounded-lg p-3">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">{item.nombre}</h4>
                      <p className="text-sm text-gray-600">{item.categoria}</p>
                    </div>
                    <button
                      onClick={() => removeFromCart(index)}
                      className="text-red-500 hover:text-red-700"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                  <div className="flex justify-between items-center">
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => updateCartQuantity(index, 'decrement')}
                        className="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center"
                      >
                        <Minus className="w-4 h-4" />
                      </button>
                      <span className="w-12 text-center font-medium">{item.quantity}</span>
                      <button
                        onClick={() => updateCartQuantity(index, 'increment')}
                        className="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center"
                      >
                        <Plus className="w-4 h-4" />
                      </button>
                    </div>
                    <span className="font-semibold text-gray-900">
                      {formatCurrency(item.precio * item.quantity)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Resumen y Métodos de Pago */}
        {cart.length > 0 && (
          <div className="border-t border-gray-200 p-4">
            {/* Métodos de Pago */}
            <div className="mb-4">
              <h3 className="font-semibold text-gray-900 mb-3">Método de Pago</h3>
              <div className="grid grid-cols-2 gap-2">
                {paymentMethods.map(method => (
                  <button
                    key={method.id}
                    onClick={() => setSelectedPaymentMethod(method.id)}
                    className={`p-3 rounded-lg border-2 transition-colors ${
                      selectedPaymentMethod === method.id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center space-x-2">
                      <method.icon className="w-4 h-4" />
                      <span className="text-sm font-medium">{method.name}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Resumen */}
            <div className="space-y-2 mb-4">
              <div className="flex justify-between text-sm">
                <span>Subtotal:</span>
                <span>{formatCurrency(getSubtotal())}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>IVA (21%):</span>
                <span>{formatCurrency(getTax())}</span>
              </div>
              <div className="border-t pt-2">
                <div className="flex justify-between font-bold text-lg">
                  <span>Total:</span>
                  <span className="text-green-600">{formatCurrency(getTotal())}</span>
                </div>
              </div>
            </div>

            {/* Botones de Acción */}
            <div className="space-y-2">
              <Button
                onClick={processSale}
                disabled={!selectedPaymentMethod}
                className="w-full bg-green-600 hover:bg-green-700 text-white py-3"
              >
                <TrendingUp className="w-4 h-4 mr-2" />
                Procesar Venta
              </Button>
              <Button
                onClick={clearCart}
                variant="outline"
                className="w-full"
              >
                Limpiar Carrito
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default POSScreen; 