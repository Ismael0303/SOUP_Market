// TODO: Integrar <Breadcrumbs /> y usar notificaciones globales en acciones clave.
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getProductsWithStock } from '../api/productApi';
import { getMyBusinesses } from '../api/businessApi';
import { createVenta, createCarrito, addItemToCarrito, removeItemFromCarrito, getCarrito, clearCarrito } from '../api/ventaApi';
import Layout from '../components/Layout';
import Breadcrumbs from '../components/Breadcrumbs';
import { useNotification } from '../context/NotificationContext';
import { useAuth } from '../context/AuthContext';

const POSScreen = () => {
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [cart, setCart] = useState([]);
  const [carritoId, setCarritoId] = useState(null);
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [clock, setClock] = useState(new Date());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedBusiness, setSelectedBusiness] = useState(null);
  const [businesses, setBusinesses] = useState([]);
  const [selectedPaymentMethod, setSelectedPaymentMethod] = useState('Efectivo');
  const { showNotification } = useNotification();
  const { user } = useAuth();

  const transformCartItems = (items, productsList = products) =>
    items.map(item => {
      const product = productsList.find(p => p.id === item.producto_id) || {};
      return {
        id: item.producto_id,
        itemId: item.id,
        nombre: product.nombre,
        precio: item.precio_unitario,
        qty: item.cantidad,
        stock_terminado: product.stock_terminado || 0
      };
    });

  const fetchCart = async (id) => {
    try {
      const carrito = await getCarrito(id);
      setCart(transformCartItems(carrito.items));
    } catch (err) {
      console.error('Error al obtener carrito:', err);
    }
  };

  useEffect(() => {
    // Reloj en tiempo real
    const interval = setInterval(() => setClock(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const loadPOSData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Cargar negocios del usuario
        const userBusinesses = await getMyBusinesses();
        setBusinesses(userBusinesses);
        
        if (userBusinesses.length > 0) {
          setSelectedBusiness(userBusinesses[0]);

          // Cargar productos con stock
          const productsWithStock = await getProductsWithStock();
          setProducts(productsWithStock);
          
          // Generar categorías únicas de los productos
          const uniqueCategories = [...new Set(productsWithStock.map(p => p.categoria).filter(Boolean))];
          const categoryColors = [
            'bg-blue-600', 'bg-yellow-500', 'bg-green-500', 'bg-pink-500', 
            'bg-purple-500', 'bg-red-500', 'bg-indigo-500', 'bg-gray-400'
          ];
          
          const categoriesList = [
            { id: 'all', name: 'Todos', color: 'bg-gray-600' },
            ...uniqueCategories.map((cat, index) => ({
              id: cat,
              name: cat.charAt(0).toUpperCase() + cat.slice(1),
              color: categoryColors[index % categoryColors.length]
            }))
          ];
          setCategories(categoriesList);
        }
      } catch (err) {
        console.error('Error cargando datos del POS:', err);
        setError('Error al cargar los datos del POS');
      } finally {
        setLoading(false);
      }
    };

    loadPOSData();
  }, []);

  useEffect(() => {
    const initCarrito = async () => {
      if (selectedBusiness) {
        try {
          const nuevoCarrito = await createCarrito({ negocio_id: selectedBusiness.id });
          setCarritoId(nuevoCarrito.id);
          setCart(transformCartItems(nuevoCarrito.items));
        } catch (err) {
          console.error('Error al crear carrito:', err);
          showNotification('Error al iniciar carrito', 'error');
        }
      }
    };

    initCarrito();
  }, [selectedBusiness]);

  const filteredProducts = products.filter(p =>
    (selectedCategory === 'all' || p.categoria === selectedCategory) &&
    (p.nombre.toLowerCase().includes(search.toLowerCase()) || 
     (p.descripcion && p.descripcion.toLowerCase().includes(search.toLowerCase()))) &&
    p.stock_terminado > 0
  );

  const addToCart = async (product) => {
    if (!carritoId) return;
    await addItemToCarrito(carritoId, { producto_id: product.id, cantidad: 1 });
    await fetchCart(carritoId);
  };

  const removeFromCart = async (item) => {
    if (!carritoId) return;
    await removeItemFromCarrito(carritoId, item.itemId);
    await fetchCart(carritoId);
  };

  const updateQty = async (item, qty) => {
    if (!carritoId) return;
    await removeItemFromCarrito(carritoId, item.itemId);
    await addItemToCarrito(carritoId, { producto_id: item.id, cantidad: qty });
    await fetchCart(carritoId);
  };

  const finalizarVenta = async () => {
    if (!user) {
      showNotification('Debes estar autenticado para realizar ventas.', 'error');
      return;
    }

    if (cart.length === 0) {
      showNotification('El carrito está vacío.', 'error');
      return;
    }

    if (!selectedPaymentMethod) {
      showNotification('Por favor selecciona un método de pago.', 'error');
      return;
    }

    try {
      const subtotal = cart.reduce((sum, item) => sum + (item.precio || 0) * item.qty, 0);
      const impuestos = subtotal * 0.21;
      const total = subtotal + impuestos;

      const ventaData = {
        negocio_id: selectedBusiness.id,
        cliente_id: user.id,
        subtotal,
        impuestos,
        total,
        metodo_pago: selectedPaymentMethod,
        detalles: cart.map(item => ({
          producto_id: item.id,
          cantidad: item.qty,
          precio_unitario: item.precio,
          descuento_unitario: 0,
        })),
      };

      await createVenta(ventaData);
      await clearCarrito(carritoId);
      setCart([]);
      showNotification('Venta finalizada exitosamente y registrada.', 'success');

      const updatedProducts = await getProductsWithStock();
      setProducts(updatedProducts);
    } catch (error) {
      console.error('Error al finalizar y registrar la venta:', error);
      showNotification('Error al finalizar la venta. Inténtalo de nuevo.', 'error');
    }
  };


  const total = cart.reduce((sum, item) => sum + (item.precio || 0) * item.qty, 0);

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Cargando POS...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          <strong>Error:</strong> {error}
        </div>
        <button 
          onClick={() => window.location.reload()} 
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          Reintentar
        </button>
      </Layout>
    );
  }

  if (businesses.length === 0) {
    return (
      <Layout>
        <div className="text-center py-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">No tienes negocios configurados</h2>
          <p className="text-gray-600 mb-4">Necesitas crear un negocio antes de usar el POS</p>
          <Link to="/dashboard/businesses/new" className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-semibold">
            Crear Negocio
          </Link>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <Breadcrumbs items={[
        { label: 'Dashboard', to: '/dashboard' },
        { label: 'Ventas', to: '/dashboard/ventas' },
        { label: 'Punto de Venta' }
      ]} />
      {/* Header POS */}
      <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4 flex flex-col md:flex-row items-center justify-between gap-4 mb-6">
        <div className="flex items-center gap-4">
          <span className="text-2xl font-bold text-blue-600">Punto de Venta</span>
          <span className="text-gray-500 text-lg">{clock.toLocaleTimeString()}</span>
        </div>
        <div className="flex-1 max-w-md w-full">
          <input 
            type="text" 
            placeholder="Buscar productos..." 
            value={search} 
            onChange={e => setSearch(e.target.value)} 
            className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-300" 
          />
        </div>
        <div className="flex items-center gap-4">
          {businesses.length > 1 && (
            <select 
              value={selectedBusiness?.id || ''} 
              onChange={(e) => {
                const business = businesses.find(b => b.id === e.target.value);
                setSelectedBusiness(business);
              }}
              className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300"
            >
              {businesses.map(business => (
                <option key={business.id} value={business.id}>
                  {business.nombre}
                </option>
              ))}
            </select>
          )}
          <span className="bg-gray-200 text-gray-700 px-4 py-2 rounded-full font-semibold">
            {selectedBusiness?.nombre || 'Negocio'}
          </span>
        </div>
      </header>

      <div className="flex flex-col md:flex-row gap-8">
        {/* Sidebar de categorías */}
        <aside className="w-full md:w-56 mb-6 md:mb-0">
          <div className="bg-white rounded-xl shadow-sm p-4 flex flex-col gap-4">
            <h3 className="text-lg font-bold text-gray-800 mb-2">Categorías</h3>
            <div className="flex md:flex-col gap-2">
              {categories.map(cat => (
                <button 
                  key={cat.id} 
                  onClick={() => setSelectedCategory(cat.id)} 
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold transition-colors ${
                    selectedCategory === cat.id 
                      ? cat.color + ' text-white' 
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {cat.name}
                </button>
              ))}
            </div>
          </div>
        </aside>

        {/* Panel principal de productos y carrito */}
        <main className="flex-1 flex flex-col gap-8">
          {/* Grid de productos */}
          <section>
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              Productos ({filteredProducts.length} disponibles)
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {filteredProducts.map(product => (
                <div key={product.id} className="bg-white rounded-xl shadow-md p-4 flex flex-col h-full hover:shadow-lg transition-shadow duration-300">
                  <div className="mb-2">
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${
                      categories.find(c => c.id === product.categoria)?.color || 'bg-gray-400'
                    } text-white`}>
                      {categories.find(c => c.id === product.categoria)?.name || 'Otros'}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-gray-900 mb-1 line-clamp-2">
                    {product.nombre}
                  </h3>
                  <p className="text-gray-600 text-sm mb-2 line-clamp-2">
                    {product.descripcion || 'Sin descripción'}
                  </p>
                  <span className="text-green-600 font-bold text-base mb-2">
                    ${(product.precio || 0).toFixed(2)}
                  </span>
                  <span className={`text-xs font-medium mb-2 ${
                    product.stock_terminado > 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {product.stock_terminado > 0 
                      ? `${product.stock_terminado} disponibles` 
                      : 'Agotado'
                    }
                  </span>
                  <button 
                    onClick={() => addToCart(product)} 
                    disabled={product.stock_terminado <= 0}
                    className={`mt-auto py-2 font-semibold rounded-lg ${
                      product.stock_terminado > 0
                        ? 'bg-blue-600 hover:bg-blue-700 text-white'
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }`}
                  >
                    {product.stock_terminado > 0 ? 'Agregar' : 'Agotado'}
                  </button>
                </div>
              ))}
            </div>
          </section>

          {/* Carrito */}
          <section>
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              Carrito ({cart.length} items)
            </h2>
            <div className="bg-white rounded-xl shadow-md p-4 overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead>
                  <tr className="text-gray-700 border-b">
                      <th className="py-2 px-2 text-left">Producto</th>
                      <th className="py-2 px-2">Precio</th>
                      <th className="py-2 px-2">Cantidad</th>
                      <th className="py-2 px-2">Subtotal</th>
                      <th className="py-2 px-2"></th>
                    </tr>
                </thead>
                <tbody>
                  {cart.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="text-center py-4 text-gray-400">
                        El carrito está vacío.
                      </td>
                    </tr>
                  ) : (
                    cart.map(item => (
                      <tr key={item.itemId} className="border-b">
                        <td className="py-2 px-2 font-semibold">{item.nombre}</td>
                        <td className="py-2 px-2">${(item.precio || 0).toFixed(2)}</td>
                        <td className="py-2 px-2">
                          <input 
                            type="number" 
                            min={1} 
                            max={item.stock_terminado}
                            value={item.qty} 
                            onChange={e => updateQty(item, parseInt(e.target.value))}
                            className="w-16 border rounded px-2 py-1" 
                          />
                        </td>
                        <td className="py-2 px-2">
                          ${((item.precio || 0) * item.qty).toFixed(2)}
                        </td>
                        <td className="py-2 px-2">
                          <button 
                            onClick={() => removeFromCart(item)}
                            className="text-red-500 hover:underline"
                          >
                            Eliminar
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
              
              {/* Total y métodos de pago */}
              <div className="flex flex-col md:flex-row items-center justify-between mt-6 gap-4">
                <div className="text-lg font-bold text-gray-900">
                  Total: ${total.toFixed(2)}
                </div>
                <div className="flex gap-2">
                  <button 
                    onClick={() => setSelectedPaymentMethod('Efectivo')}
                    className={`px-6 py-2 rounded-lg font-semibold transition-colors ${
                      selectedPaymentMethod === 'Efectivo'
                        ? 'bg-green-600 text-white'
                        : 'bg-gray-200 hover:bg-gray-300 text-gray-700'
                    }`}
                  >
                    Efectivo
                  </button>
                  <button 
                    onClick={() => setSelectedPaymentMethod('Tarjeta')}
                    className={`px-6 py-2 rounded-lg font-semibold transition-colors ${
                      selectedPaymentMethod === 'Tarjeta'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 hover:bg-gray-300 text-gray-700'
                    }`}
                  >
                    Tarjeta
                  </button>
                  <button 
                    onClick={() => setSelectedPaymentMethod('Mercado Pago')}
                    className={`px-6 py-2 rounded-lg font-semibold transition-colors ${
                      selectedPaymentMethod === 'Mercado Pago'
                        ? 'bg-yellow-500 text-white'
                        : 'bg-gray-200 hover:bg-gray-300 text-gray-700'
                    }`}
                  >
                    Mercado Pago
                  </button>
                </div>
                <div className="flex gap-2">
                  <button 
                    onClick={() => setCart([])}
                    className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-6 py-2 rounded-lg font-semibold"
                  >
                    Cancelar
                  </button>
                  <button 
                    onClick={finalizarVenta}
                    disabled={cart.length === 0}
                    className={`px-6 py-2 rounded-lg font-semibold ${
                      cart.length > 0
                        ? 'bg-blue-600 hover:bg-blue-700 text-white'
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }`}
                  >
                    Finalizar Venta
                  </button>
                </div>
              </div>
            </div>
          </section>
        </main>
      </div>
    </Layout>
  );
};

export default POSScreen;
