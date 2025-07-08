// frontend/src/screens/PublicListingScreen.js

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import publicApi from '../api/publicApi'; // Asumiendo que tienes un publicApi para obtener listados
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { DollarSign, TrendingUp, Calculator, Building2, Package } from 'lucide-react'; // Iconos para mejor UX

const PublicListingScreen = () => {
  const [businesses, setBusinesses] = useState([]);
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPublicData = async () => {
      try {
        setIsLoading(true);
        const fetchedBusinesses = await publicApi.getPublicBusinesses();
        const fetchedProducts = await publicApi.getPublicProducts();
        setBusinesses(fetchedBusinesses);
        setProducts(fetchedProducts);
      } catch (err) {
        console.error('Error al cargar listados públicos:', err);
        setError('No se pudieron cargar los listados públicos. Inténtalo de nuevo más tarde.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchPublicData();
  }, []);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-gray-800 dark:text-gray-200">Cargando listados públicos...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-red-600 text-center">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-4 sm:p-6 lg:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Explora Emprendimientos y Productos</h1>
          <p className="text-lg text-gray-600 dark:text-gray-400 mb-6">
            Descubre una variedad de negocios y productos/servicios ofrecidos por emprendedores
          </p>
          <div className="flex justify-center space-x-4">
            <Link to="/login">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                Iniciar Sesión
              </Button>
            </Link>
            <Link to="/register">
              <Button variant="outline">
                Registrarse
              </Button>
            </Link>
          </div>
        </div>

        {/* Sección de Negocios */}
        <section className="mb-16">
          <div className="flex items-center mb-8">
            <Building2 className="w-8 h-8 mr-3 text-blue-600" />
            <h2 className="text-3xl font-semibold">Negocios Destacados</h2>
          </div>
          
          {businesses.length === 0 ? (
            <div className="text-center py-12">
              <Building2 className="w-16 h-16 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-600 dark:text-gray-400 text-lg">
                No hay negocios destacados disponibles en este momento.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {businesses.map((business) => (
                <Card key={business.id} className="bg-white dark:bg-gray-800 shadow-lg rounded-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-xl font-bold flex items-center">
                      <Building2 className="w-5 h-5 mr-2 text-blue-600" />
                      {business.nombre}
                    </CardTitle>
                    <p className="text-sm text-gray-500 dark:text-gray-400 capitalize">
                      {business.tipo_negocio?.replace(/_/g, ' ') || business.rubro}
                    </p>
                  </CardHeader>
                  <CardContent>
                    {business.fotos_urls && business.fotos_urls.length > 0 && (
                      <img
                        src={business.fotos_urls[0]}
                        alt={business.nombre}
                        className="w-full h-48 object-cover rounded-md mb-4"
                        onError={(e) => {
                          e.target.onerror = null;
                          e.target.src = "https://placehold.co/600x400/cccccc/000000?text=Sin+Imagen";
                        }}
                      />
                    )}
                    <p className="text-gray-700 dark:text-gray-300 mb-4 line-clamp-3">
                      {business.descripcion || 'Sin descripción disponible.'}
                    </p>
                    <Link to={`/public/businesses/${business.id}/products`}>
                      <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white">
                        Ver Productos
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </section>

        {/* Sección de Productos/Servicios */}
        <section>
          <div className="flex items-center mb-8">
            <Package className="w-8 h-8 mr-3 text-green-600" />
            <h2 className="text-3xl font-semibold">Productos y Servicios</h2>
          </div>
          
          {products.length === 0 ? (
            <div className="text-center py-12">
              <Package className="w-16 h-16 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-600 dark:text-gray-400 text-lg">
                No hay productos o servicios disponibles en este momento.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {products.map((product) => (
                <Card key={product.id} className="bg-white dark:bg-gray-800 shadow-lg rounded-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-xl font-bold flex items-center">
                      <Package className="w-5 h-5 mr-2 text-green-600" />
                      {product.nombre}
                    </CardTitle>
                    <p className="text-sm text-gray-500 dark:text-gray-400 capitalize">
                      {product.tipo_producto?.replace(/_/g, ' ')}
                    </p>
                  </CardHeader>
                  <CardContent>
                    {product.fotos_urls && product.fotos_urls.length > 0 && (
                      <img
                        src={product.fotos_urls[0]}
                        alt={product.nombre}
                        className="w-full h-48 object-cover rounded-md mb-4"
                        onError={(e) => {
                          e.target.onerror = null;
                          e.target.src = "https://placehold.co/600x400/cccccc/000000?text=Sin+Imagen";
                        }}
                      />
                    )}
                    <p className="text-gray-700 dark:text-gray-300 mb-4 line-clamp-3">
                      {product.descripcion || 'Sin descripción disponible.'}
                    </p>
                    
                    {/* Información de Precios */}
                    <div className="space-y-2 mb-4">
                      {/* Precio de Venta */}
                      {product.precio_venta !== null && product.precio_venta !== undefined ? (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600 dark:text-gray-400">Precio de Venta:</span>
                          <span className="text-lg font-bold text-green-600 dark:text-green-400 flex items-center">
                            <DollarSign className="w-4 h-4 mr-1" />
                            {product.precio_venta.toFixed(2)}
                          </span>
                        </div>
                      ) : (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600 dark:text-gray-400">Precio:</span>
                          <span className="text-sm text-gray-500 dark:text-gray-400">
                            No especificado
                          </span>
                        </div>
                      )}

                      {/* Información de Costos (si está disponible) */}
                      {product.cogs !== null && product.cogs !== undefined && (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600 dark:text-gray-400">Costo de Producción:</span>
                          <span className="text-sm text-blue-600 dark:text-blue-400 flex items-center">
                            <Calculator className="w-3 h-3 mr-1" />
                            ${product.cogs.toFixed(2)}
                          </span>
                        </div>
                      )}

                      {/* Margen de Ganancia Real (si está disponible) */}
                      {product.margen_ganancia_real !== null && product.margen_ganancia_real !== undefined && (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600 dark:text-gray-400">Margen de Ganancia:</span>
                          <span className={`text-sm font-medium flex items-center ${
                            product.margen_ganancia_real >= 0 
                              ? 'text-green-600 dark:text-green-400' 
                              : 'text-red-600 dark:text-red-400'
                          }`}>
                            <TrendingUp className="w-3 h-3 mr-1" />
                            {product.margen_ganancia_real.toFixed(1)}%
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Botón para ver detalles */}
                    <Link to={`/public/products/${product.id}`}>
                      <Button className="w-full bg-green-600 hover:bg-green-700 text-white">
                        Ver Detalles
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default PublicListingScreen;
