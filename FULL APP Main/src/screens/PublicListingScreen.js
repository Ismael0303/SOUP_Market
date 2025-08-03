// PublicListingScreen.js - Actualizado según mockups Gemini
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
  DollarSign,
  Star,
  MapPin,
  Phone,
  Mail,
  ExternalLink,
  Heart,
  Share2
} from 'lucide-react';
import { showInfo } from '../utils/notifications';

const PublicListingScreen = () => {
  const [businesses, setBusinesses] = useState([]);
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [priceRange, setPriceRange] = useState({ min: '', max: '' });
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [viewMode, setViewMode] = useState('products'); // 'products' or 'businesses'

  // Categorías del mockup
  const categories = [
    { id: 'all', name: 'Todos los Productos', color: 'bg-gray-500' },
    { id: 'panaderia', name: 'Panadería', color: 'bg-blue-500' },
    { id: 'discograficas', name: 'Discográficas', color: 'bg-purple-500' },
    { id: 'servicios', name: 'Servicios', color: 'bg-green-500' },
    { id: 'tecnologia', name: 'Tecnología', color: 'bg-indigo-500' },
    { id: 'artesania', name: 'Artesanía', color: 'bg-orange-500' },
    { id: 'moda', name: 'Moda', color: 'bg-pink-500' }
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
        product.descripcion?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.categoria?.toLowerCase().includes(searchTerm.toLowerCase())
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
    showInfo('Filtros aplicados');
  };

  const handleClearFilters = () => {
    setSearchTerm('');
    setSelectedCategory('all');
    setPriceRange({ min: '', max: '' });
    showInfo('Filtros limpiados');
  };

  const formatCurrency = (amount) => {
    if (!amount) return 'No especificado';
    return new Intl.NumberFormat('es-AR', { 
      style: 'currency', 
      currency: 'ARS', 
      minimumFractionDigits: 2 
    }).format(amount);
  };

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating || 0);
    const hasHalfStar = (rating || 0) % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(<Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />);
    }
    
    if (hasHalfStar) {
      stars.push(<Star key="half" className="w-4 h-4 fill-yellow-400 text-yellow-400" />);
    }

    const emptyStars = 5 - Math.ceil(rating || 0);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<Star key={`empty-${i}`} className="w-4 h-4 text-gray-300" />);
    }

    return stars;
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
          <div className="flex items-center space-x-4">
            <div className="text-3xl font-bold text-blue-600">SOUP Market</div>
            <div className="hidden md:flex items-center space-x-2 text-sm text-gray-600">
              <span>•</span>
              <span>Descubre emprendimientos locales</span>
              <span>•</span>
              <span>Apoya el comercio local</span>
            </div>
          </div>
          
          <div className="flex-grow max-w-2xl w-full">
            <div className="relative">
              <Input
                type="text"
                placeholder="Buscar productos, servicios o negocios..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-3 text-lg"
              />
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <Button variant="ghost" className="flex items-center">
              <ShoppingCart className="w-6 h-6" />
              <span className="ml-1 hidden md:inline">Carrito</span>
            </Button>
            <Link to="/login">
              <Button variant="outline" className="flex items-center">
                <User className="w-6 h-6 mr-1" />
                Iniciar Sesión
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex flex-col md:flex-row flex-grow p-6 gap-8">
        {/* Sidebar Filters */}
        <aside className="w-full md:w-80 bg-white rounded-xl shadow-sm p-6 flex-shrink-0">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-gray-800 flex items-center">
              <Filter className="w-5 h-5 mr-2" />
              Filtros
            </h3>
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={handleClearFilters}
              className="text-gray-500 hover:text-gray-700"
            >
              Limpiar
            </Button>
          </div>

          {/* View Mode Toggle */}
          <div className="mb-6">
            <h4 className="text-lg font-semibold text-gray-700 mb-3">Ver</h4>
            <div className="flex space-x-2">
              <Button
                variant={viewMode === 'products' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setViewMode('products')}
                className="flex-1"
              >
                <Package className="w-4 h-4 mr-1" />
                Productos
              </Button>
              <Button
                variant={viewMode === 'businesses' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setViewMode('businesses')}
                className="flex-1"
              >
                <Building2 className="w-4 h-4 mr-1" />
                Negocios
              </Button>
            </div>
          </div>

          {/* Categories */}
          <div className="mb-8">
            <h4 className="text-lg font-semibold text-gray-700 mb-3">Categorías</h4>
            <div className="space-y-2">
              {categories.map(category => (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`block w-full text-left p-3 rounded-lg transition-colors ${
                    selectedCategory === category.id
                      ? 'text-white font-medium shadow-md'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                  style={{
                    backgroundColor: selectedCategory === category.id ? category.color : 'transparent'
                  }}
                >
                  <div className="flex items-center justify-between">
                    <span>{category.name}</span>
                    {selectedCategory === category.id && (
                      <span className="text-white text-sm">
                        {filteredProducts.filter(p => p.categoria === category.id).length}
                      </span>
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Price Range */}
          <div className="mb-6">
            <h4 className="text-lg font-semibold text-gray-700 mb-3">Rango de Precio (ARS)</h4>
            <div className="space-y-3">
              <div>
                <label className="block text-sm text-gray-600 mb-1">Precio mínimo</label>
                <Input
                  type="number"
                  placeholder="0"
                  value={priceRange.min}
                  onChange={(e) => setPriceRange({...priceRange, min: e.target.value})}
                  className="w-full"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">Precio máximo</label>
                <Input
                  type="number"
                  placeholder="10000"
                  value={priceRange.max}
                  onChange={(e) => setPriceRange({...priceRange, max: e.target.value})}
                  className="w-full"
                />
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="bg-blue-50 rounded-lg p-4">
            <h4 className="font-semibold text-blue-800 mb-2">Estadísticas</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-blue-600">Productos:</span>
                <span className="font-medium">{filteredProducts.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-blue-600">Negocios:</span>
                <span className="font-medium">{businesses.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-blue-600">Categorías:</span>
                <span className="font-medium">{categories.length - 1}</span>
              </div>
            </div>
          </div>
        </aside>

        {/* Main Content Area */}
        <div className="flex-1">
          {/* Results Header */}
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                {viewMode === 'products' ? 'Productos' : 'Negocios'} Disponibles
              </h2>
              <p className="text-gray-600">
                {viewMode === 'products' 
                  ? `${filteredProducts.length} productos encontrados`
                  : `${businesses.length} negocios registrados`
                }
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <Button variant="outline" size="sm">
                <Share2 className="w-4 h-4 mr-1" />
                Compartir
              </Button>
            </div>
          </div>

          {/* Products Grid */}
          {viewMode === 'products' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {filteredProducts.map(product => (
                <Card key={product.id} className="hover:shadow-lg transition-shadow duration-200 cursor-pointer">
                  <div className="relative">
                    <div className="w-full h-48 bg-gradient-to-br from-blue-500 to-blue-600 rounded-t-lg flex items-center justify-center">
                      <Package className="w-16 h-16 text-white" />
                    </div>
                    <button className="absolute top-2 right-2 p-2 bg-white rounded-full shadow-md hover:bg-gray-50">
                      <Heart className="w-4 h-4 text-gray-600" />
                    </button>
                  </div>
                  <CardContent className="p-4">
                    <div className="mb-2">
                      <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium text-white ${
                        product.categoria === 'Panadería' ? 'bg-blue-500' :
                        product.categoria === 'Discográficas' ? 'bg-purple-500' :
                        product.categoria === 'Servicios' ? 'bg-green-500' :
                        product.categoria === 'Tecnología' ? 'bg-indigo-500' :
                        product.categoria === 'Artesanía' ? 'bg-orange-500' :
                        product.categoria === 'Moda' ? 'bg-pink-500' : 'bg-gray-500'
                      }`}>
                        {product.categoria || 'Sin categoría'}
                      </span>
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">
                      {product.nombre}
                    </h3>
                    <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                      {product.descripcion || 'Sin descripción disponible'}
                    </p>
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-1">
                        {renderStars(product.rating || 0)}
                        <span className="text-sm text-gray-500">({product.reviews || 0})</span>
                      </div>
                      <span className="text-lg font-bold text-green-600">
                        {formatCurrency(product.precio_venta || product.precio)}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-1 text-sm text-gray-500">
                        <Building2 className="w-4 h-4" />
                        <span>{product.negocio_nombre || 'Negocio'}</span>
                      </div>
                      <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                        <ExternalLink className="w-4 h-4 mr-1" />
                        Ver
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* Businesses Grid */}
          {viewMode === 'businesses' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {businesses.map(business => (
                <Card key={business.id} className="hover:shadow-lg transition-shadow duration-200">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                        <Building2 className="w-8 h-8 text-white" />
                      </div>
                      <button className="p-2 text-gray-400 hover:text-red-500">
                        <Heart className="w-4 h-4" />
                      </button>
                    </div>
                    
                    <h3 className="font-bold text-gray-900 text-lg mb-2">
                      {business.nombre}
                    </h3>
                    
                    <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                      {business.descripcion || 'Sin descripción disponible'}
                    </p>
                    
                    <div className="flex items-center space-x-1 mb-3">
                      {renderStars(business.rating || 0)}
                      <span className="text-sm text-gray-500">({business.reviews || 0} reseñas)</span>
                    </div>
                    
                    <div className="space-y-2 mb-4">
                      {business.direccion && (
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                          <MapPin className="w-4 h-4" />
                          <span>{business.direccion}</span>
                        </div>
                      )}
                      {business.telefono && (
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                          <Phone className="w-4 h-4" />
                          <span>{business.telefono}</span>
                        </div>
                      )}
                      {business.email && (
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                          <Mail className="w-4 h-4" />
                          <span>{business.email}</span>
                        </div>
                      )}
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium text-white ${
                        business.tipo_negocio === 'Panadería' ? 'bg-blue-500' :
                        business.tipo_negocio === 'Discográfica' ? 'bg-purple-500' :
                        business.tipo_negocio === 'Servicios' ? 'bg-green-500' :
                        business.tipo_negocio === 'Tecnología' ? 'bg-indigo-500' :
                        business.tipo_negocio === 'Artesanía' ? 'bg-orange-500' :
                        business.tipo_negocio === 'Moda' ? 'bg-pink-500' : 'bg-gray-500'
                      }`}>
                        {business.tipo_negocio || 'Negocio'}
                      </span>
                      <Button size="sm" variant="outline">
                        <ExternalLink className="w-4 h-4 mr-1" />
                        Ver Negocio
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* Empty State */}
          {filteredProducts.length === 0 && viewMode === 'products' && (
            <div className="text-center py-12">
              <Package className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No se encontraron productos</h3>
              <p className="text-gray-600 mb-4">Intenta ajustar los filtros de búsqueda</p>
              <Button onClick={handleClearFilters} variant="outline">
                Limpiar Filtros
              </Button>
            </div>
          )}

          {businesses.length === 0 && viewMode === 'businesses' && (
            <div className="text-center py-12">
              <Building2 className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No se encontraron negocios</h3>
              <p className="text-gray-600">Pronto habrá más negocios disponibles</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default PublicListingScreen; 