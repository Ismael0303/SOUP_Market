// SCRIPT_ACTUALIZACION_MARKETPLACE.js
// Actualización de PublicListingScreen.js según mockup Gemini

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import publicApi from '../api/publicApi';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { 
  Search, 
  ShoppingCart, 
  User, 
  Package,
  Building2,
  Filter,
  DollarSign
} from 'lucide-react';

const PublicListingScreen = () => {
  const [businesses, setBusinesses] = useState([]);
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [priceRange, setPriceRange] = useState({ min: '', max: '' });
  const [filteredProducts, setFilteredProducts] = useState([]);

  // Categorías del mockup
  const categories = [
    { id: 'all', name: 'Todos los Productos' },
    { id: 'panaderia', name: 'Panadería' },
    { id: 'discograficas', name: 'Discográficas' },
    { id: 'servicios', name: 'Servicios' },
    { id: 'tecnologia', name: 'Tecnología' },
    { id: 'artesania', name: 'Artesanía' },
    { id: 'moda', name: 'Moda' }
  ];

  useEffect(() => {
    const fetchPublicData = async () => {
      try {
        setIsLoading(true);
        const fetchedBusinesses = await publicApi.getPublicBusinesses();
        const fetchedProducts = await publicApi.getPublicProducts();
        setBusinesses(fetchedBusinesses);
        setProducts(fetchedProducts);
        setFilteredProducts(fetchedProducts);
      } catch (err) {
        console.error('Error al cargar listados públicos:', err);
        setError('No se pudieron cargar los listados públicos. Inténtalo de nuevo más tarde.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchPublicData();
  }, []);

  // Filtrar productos
  useEffect(() => {
    let filtered = products;

    // Filtro por búsqueda
    if (searchTerm) {
      filtered = filtered.filter(product =>
        product.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.descripcion?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filtro por categoría
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(product => product.categoria === selectedCategory);
    }

    // Filtro por precio
    if (priceRange.min || priceRange.max) {
      filtered = filtered.filter(product => {
        const price = product.precio_venta || product.precio;
        if (!price) return false;
        
        const minPrice = priceRange.min ? parseFloat(priceRange.min) : 0;
        const maxPrice = priceRange.max ? parseFloat(priceRange.max) : Infinity;
        
        return price >= minPrice && price <= maxPrice;
      });
    }

    setFilteredProducts(filtered);
  }, [products, searchTerm, selectedCategory, priceRange]);

  const handleApplyFilters = () => {
    // Los filtros se aplican automáticamente con useEffect
  };

  const formatCurrency = (amount) => {
    if (!amount) return 'No especificado';
    return new Intl.NumberFormat('es-AR', { 
      style: 'currency', 
      currency: 'ARS', 
      minimumFractionDigits: 2 
    }).format(amount);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando listados públicos...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100">
        <div className="text-center">
          <p className="text-red-600 text-lg">{error}</p>
          <Button onClick={() => window.location.reload()} className="mt-4">
            Reintentar
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-3xl font-bold text-blue-600">SOUP Market</div>
          
          <div className="flex-grow max-w-2xl w-full">
            <div className="relative">
              <Input
                type="text"
                placeholder="Buscar productos..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2"
              />
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <Button variant="ghost" className="flex items-center">
              <ShoppingCart className="w-6 h-6" />
              <span className="ml-1 hidden md:inline">Carrito</span>
            </Button>
            <Button variant="outline" className="flex items-center">
              <User className="w-6 h-6 mr-1" />
              Usuario
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex flex-col md:flex-row flex-grow p-6 gap-8">
        {/* Sidebar Filters */}
        <aside className="w-full md:w-64 bg-white rounded-xl shadow-sm p-6 flex-shrink-0">
          <h3 className="text-xl font-bold text-gray-800 mb-6 flex items-center">
            <Filter className="w-5 h-5 mr-2" />
            Filtros
          </h3>

          {/* Categories */}
          <div className="mb-8">
            <h4 className="text-lg font-semibold text-gray-700 mb-3">Categorías</h4>
            <ul className="space-y-2">
              {categories.map(category => (
                <li key={category.id}>
                  <button
                    onClick={() => setSelectedCategory(category.id)}
                    className={`block w-full text-left p-2 rounded-lg transition-colors ${
                      selectedCategory === category.id
                        ? 'text-blue-600 font-medium bg-blue-50'
                        : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                    }`}
                  >
                    {category.name}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Price Range */}
          <div>
            <h4 className="text-lg font-semibold text-gray-700 mb-3">Rango de Precio (ARS)</h4>
            <div className="flex gap-2 mb-4">
              <Input
                type="number"
                placeholder="Mín."
                value={priceRange.min}
                onChange={(e) => setPriceRange(prev => ({ ...prev, min: e.target.value }))}
                className="w-1/2"
              />
              <Input
                type="number"
                placeholder="Máx."
                value={priceRange.max}
                onChange={(e) => setPriceRange(prev => ({ ...prev, max: e.target.value }))}
                className="w-1/2"
              />
            </div>
            <Button 
              onClick={handleApplyFilters}
              className="w-full bg-gray-600 hover:bg-gray-700"
            >
              Aplicar
            </Button>
          </div>
        </aside>

        {/* Products Grid */}
        <section className="flex-grow">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredProducts.length === 0 ? (
              <div className="col-span-full text-center py-12">
                <Package className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                <p className="text-gray-600 text-lg">
                  No se encontraron productos con los filtros aplicados.
                </p>
              </div>
            ) : (
              filteredProducts.map((product) => (
                <Card key={product.id} className="bg-white shadow-sm rounded-xl overflow-hidden hover:shadow-lg transition-shadow duration-300">
                  {/* Product Image */}
                  <div className="relative">
                    {product.fotos_urls && product.fotos_urls.length > 0 ? (
                      <img
                        src={product.fotos_urls[0]}
                        alt={product.nombre}
                        className="w-full h-48 object-cover"
                        onError={(e) => {
                          e.target.onerror = null;
                          e.target.src = "https://placehold.co/400x250/007bff/ffffff?text=Producto";
                        }}
                      />
                    ) : (
                      <div className="w-full h-48 bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
                        <Package className="w-16 h-16 text-white" />
                      </div>
                    )}
                    
                    {/* Category Badge */}
                    {product.categoria && (
                      <div className="absolute top-2 left-2">
                        <span className="bg-blue-600 text-white text-xs px-2 py-1 rounded-full">
                          {product.categoria}
                        </span>
                      </div>
                    )}
                  </div>

                  <CardContent className="p-4">
                    {/* Product Title */}
                    <h3 className="text-xl font-bold text-gray-900 mb-2 line-clamp-2">
                      {product.nombre}
                    </h3>
                    
                    {/* Business Info */}
                    {product.negocio && (
                      <p className="text-sm text-gray-500 mb-3 flex items-center">
                        <Building2 className="w-4 h-4 mr-1" />
                        {product.negocio.nombre}
                      </p>
                    )}

                    {/* Description */}
                    <p className="text-gray-700 mb-4 line-clamp-3">
                      {product.descripcion || 'Sin descripción disponible.'}
                    </p>

                    {/* Price Information */}
                    <div className="space-y-2 mb-4">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Precio:</span>
                        <span className="text-lg font-bold text-green-600 flex items-center">
                          <DollarSign className="w-4 h-4 mr-1" />
                          {formatCurrency(product.precio_venta || product.precio)}
                        </span>
                      </div>

                      {/* Cost Information (if available) */}
                      {product.cogs && (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">Costo:</span>
                          <span className="text-sm text-blue-600">
                            {formatCurrency(product.cogs)}
                          </span>
                        </div>
                      )}

                      {/* Stock Information */}
                      {product.stock_terminado !== undefined && (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">Stock:</span>
                          <span className={`text-sm font-medium ${
                            product.stock_terminado > 0 ? 'text-green-600' : 'text-red-600'
                          }`}>
                            {product.stock_terminado > 0 ? `${product.stock_terminado} disponibles` : 'Agotado'}
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Action Buttons */}
                    <div className="flex gap-2">
                      <Button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white">
                        Ver Detalles
                      </Button>
                      <Button variant="outline" size="sm">
                        <ShoppingCart className="w-4 h-4" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>

          {/* Results Count */}
          <div className="mt-8 text-center text-gray-600">
            <p>
              Mostrando {filteredProducts.length} de {products.length} productos
              {searchTerm && ` para "${searchTerm}"`}
              {selectedCategory !== 'all' && ` en ${categories.find(c => c.id === selectedCategory)?.name}`}
            </p>
          </div>
        </section>
      </main>

      {/* Call to Action Section */}
      <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-12">
        <div className="max-w-4xl mx-auto text-center px-6">
          <h2 className="text-3xl font-bold mb-4">
            ¿Eres emprendedor? Únete a SOUP Market
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Gestiona tu negocio de manera inteligente y conecta con más clientes
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register">
              <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-100">
                Registrarse Gratis
              </Button>
            </Link>
            <Link to="/login">
              <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-blue-600">
                Iniciar Sesión
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default PublicListingScreen; 