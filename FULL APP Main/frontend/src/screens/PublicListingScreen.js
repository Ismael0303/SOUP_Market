// frontend/src/screens/PublicListingScreen.js

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import publicApi from '../api/publicApi';

const PublicListingScreen = () => {
  const [businesses, setBusinesses] = useState([]);
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        const [businessesData, productsData] = await Promise.all([
          publicApi.getPublicBusinesses(),
          publicApi.getPublicProducts()
        ]);
        setBusinesses(businessesData);
        setProducts(productsData);
      } catch (err) {
        console.error('Error al cargar datos:', err);
        setError('No se pudieron cargar los datos. Inténtalo de nuevo más tarde.');
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex justify-center items-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando marketplace...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex justify-center items-center">
        <div className="text-center">
          <p className="text-red-600 text-lg">{error}</p>
        </div>
      </div>
    );
  }

  // Filtrado de productos
  const filteredProducts = products.filter(p => {
    const matchesSearch = searchTerm === '' || p.nombre.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || p.categoria === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-3xl font-bold text-blue-600">SOUP Market</div>
          <div className="flex-grow max-w-2xl w-full">
            <div className="relative">
              <input
                type="text"
                placeholder="Buscar productos..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 w-full rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-300"
              />
              <svg className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
          </div>
          <div className="flex items-center gap-4">
            {isAuthenticated ? (
              <button
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                onClick={() => navigate('/dashboard')}
              >
                Mi Dashboard
              </button>
            ) : (
              <button
                className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors"
                onClick={() => navigate('/login')}
              >
                Iniciar Sesión
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Contenido principal */}
      <div className="max-w-7xl mx-auto w-full p-4 sm:p-6 lg:p-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Bienvenido a SOUP Market
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Descubre los mejores negocios y productos locales
          </p>
          <div className="flex justify-center gap-4">
            <button
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
              onClick={() => navigate('/register')}
            >
              Registrarse
            </button>
            <button
              className="bg-gray-200 text-gray-700 px-6 py-3 rounded-lg hover:bg-gray-300 transition-colors"
              onClick={() => navigate('/pricing')}
            >
              Ver Planes
            </button>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar de filtros */}
          <aside className="w-full lg:w-64 bg-white rounded-xl shadow-sm p-6 flex-shrink-0">
            <h3 className="text-xl font-bold text-gray-800 mb-6">Filtros</h3>
            
            {/* Categorías */}
            <div className="mb-8">
              <h4 className="text-lg font-semibold text-gray-700 mb-3">Categorías</h4>
              <ul className="space-y-2">
                <li>
                  <button 
                    onClick={() => setSelectedCategory('all')} 
                    className={`block w-full text-left p-2 rounded-lg transition-colors ${
                      selectedCategory === 'all' ? 'text-blue-600 font-medium bg-blue-50' : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                    }`}
                  >
                    Todas las categorías
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => setSelectedCategory('panaderia')} 
                    className={`block w-full text-left p-2 rounded-lg transition-colors ${
                      selectedCategory === 'panaderia' ? 'text-blue-600 font-medium bg-blue-50' : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                    }`}
                  >
                    Panadería
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => setSelectedCategory('restaurante')} 
                    className={`block w-full text-left p-2 rounded-lg transition-colors ${
                      selectedCategory === 'restaurante' ? 'text-blue-600 font-medium bg-blue-50' : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                    }`}
                  >
                    Restaurante
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => setSelectedCategory('servicios')} 
                    className={`block w-full text-left p-2 rounded-lg transition-colors ${
                      selectedCategory === 'servicios' ? 'text-blue-600 font-medium bg-blue-50' : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                    }`}
                  >
                    Servicios
                  </button>
                </li>
              </ul>
            </div>
          </aside>

          {/* Contenido principal */}
          <div className="flex-1">
            {/* Sección de Negocios */}
            <section className="mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-8">Negocios Destacados</h2>
              
              {businesses.length === 0 ? (
                <div className="text-center py-16 bg-white rounded-xl shadow-sm">
                  <p className="text-gray-600 text-lg">
                    No hay negocios destacados disponibles en este momento.
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {businesses.map((business) => (
                    <div key={business.id} className="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-xl transition-all duration-300">
                      <div className="relative">
                        <img
                          src={business.fotos_urls[0]}
                          alt={business.nombre}
                          className="w-full h-48 object-cover"
                          onError={(e) => {
                            e.target.src = 'https://via.placeholder.com/400x300?text=Negocio';
                          }}
                        />
                        <div className="absolute top-2 right-2 bg-yellow-400 text-yellow-900 px-2 py-1 rounded-full text-sm font-semibold">
                          ⭐ {business.rating}
                        </div>
                      </div>
                      <div className="p-6">
                        <h3 className="text-xl font-bold text-gray-900 mb-2">{business.nombre}</h3>
                        <p className="text-sm text-gray-500 capitalize mb-3">
                          {business.tipo_negocio?.replace(/_/g, ' ') || 'Negocio'}
                        </p>
                        <p className="text-gray-600 mb-4">{business.descripcion}</p>
                        <button
                          className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
                          onClick={() => navigate(`/business/${business.id}`)}
                        >
                          Ver Negocio
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>

            {/* Sección de Productos */}
            <section>
              <h2 className="text-3xl font-bold text-gray-900 mb-8">Productos</h2>
              
              {filteredProducts.length === 0 ? (
                <div className="text-center py-16 bg-white rounded-xl shadow-sm">
                  <p className="text-gray-600 text-lg">
                    No se encontraron productos con los filtros seleccionados.
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredProducts.map((product) => (
                    <div key={product.id} className="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-xl transition-all duration-300">
                      <div className="p-6">
                        <h3 className="text-lg font-bold text-gray-900 mb-2">{product.nombre}</h3>
                        <p className="text-gray-600 mb-3">{product.descripcion}</p>
                        <div className="flex items-center mb-3">
                          {Array.from({ length: 5 }, (_, i) => (
                            <span key={i}>{i < Math.round(product.rating_promedio || 0) ? '⭐' : '☆'}</span>
                          ))}
                          <span className="ml-2 text-sm text-gray-600">({product.reviews_count || 0})</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-2xl font-bold text-blue-600">
                            ${((product.precio_venta ?? product.precio)).toFixed(2)}
                          </span>
                          <button
                            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
                            onClick={() => navigate(`/business/${product.negocio_id}`)}
                          >
                            Ver
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PublicListingScreen;
