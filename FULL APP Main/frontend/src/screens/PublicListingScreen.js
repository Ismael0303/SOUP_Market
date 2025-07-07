// frontend/src/screens/PublicListingScreen.js
import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button.jsx';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card.jsx';
import { getPublicBusinesses, getPublicProducts } from '../api/publicApi'; // Asumimos que crearemos publicApi.js

const PublicListingScreen = () => {
  const [businesses, setBusinesses] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Función para cargar todos los negocios y productos públicos
  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [businessesData, productsData] = await Promise.all([
        getPublicBusinesses(),
        getPublicProducts()
      ]);
      setBusinesses(businessesData);
      setProducts(productsData);
    } catch (err) {
      console.error("Error al cargar listados públicos:", err);
      setError(err.message || "No se pudieron cargar los listados públicos.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-gray-800 dark:text-gray-200">Cargando listado público...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-red-500 text-center">{error}</p>
        <Button onClick={fetchData} className="ml-4">Reintentar Carga</Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 max-w-6xl mt-8">
      <Card className="rounded-xl shadow-lg p-6 space-y-8">
        <CardHeader className="text-center">
          <CardTitle className="text-4xl font-bold">Explora Emprendimientos y Productos</CardTitle>
          <CardDescription className="text-lg text-gray-600 dark:text-gray-400">
            Descubre una variedad de negocios y productos/servicios ofrecidos por emprendedores.
          </CardDescription>
          <div className="mt-4 flex justify-center space-x-4">
            <Link to="/login">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white">Iniciar Sesión</Button>
            </Link>
            <Link to="/register">
              <Button variant="outline">Registrarse</Button>
            </Link>
          </div>
        </CardHeader>
        <CardContent className="space-y-8">
          {/* Sección de Negocios */}
          <section>
            <h2 className="text-3xl font-semibold mb-6 text-center">Negocios Destacados</h2>
            {businesses.length === 0 ? (
              <p className="text-center text-gray-500">No hay negocios disponibles públicamente en este momento.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {businesses.map((business) => (
                  <Card key={business.id} className="rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
                    <CardHeader className="p-4 pb-2">
                      <CardTitle className="text-xl font-semibold truncate">
                        {business.nombre}
                      </CardTitle>
                      <CardDescription className="text-sm text-gray-500">
                        Rubro: {business.rubro}
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="p-4 pt-0">
                      {business.fotos_urls && business.fotos_urls.length > 0 && (
                        <img
                          src={business.fotos_urls[0]}
                          alt={business.nombre}
                          className="w-full h-40 object-cover rounded-md mb-3"
                          onError={(e) => { e.target.onerror = null; e.target.src="https://placehold.co/600x400/cccccc/000000?text=No+Image"; }}
                        />
                      )}
                      <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-3 mb-3">
                        {business.descripcion || 'Sin descripción disponible.'}
                      </p>
                      <Link to={`/public/businesses/${business.id}`}> {/* Ruta para ver detalle del negocio */}
                        <Button className="w-full bg-purple-600 hover:bg-purple-700 text-white">Ver Negocio</Button>
                      </Link>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </section>

          {/* Sección de Productos y Servicios */}
          <section className="mt-10">
            <h2 className="text-3xl font-semibold mb-6 text-center">Productos y Servicios</h2>
            {products.length === 0 ? (
              <p className="text-center text-gray-500">No hay productos o servicios disponibles públicamente en este momento.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {products.map((product) => (
                  <Card key={product.id} className="rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
                    <CardHeader className="p-4 pb-2">
                      <CardTitle className="text-xl font-semibold truncate">
                        {product.nombre}
                      </CardTitle>
                      <CardDescription className="text-sm text-gray-500">
                        Tipo: {product.tipo_producto.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase())}
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="p-4 pt-0">
                      {product.fotos_urls && product.fotos_urls.length > 0 && (
                        <img
                          src={product.fotos_urls[0]}
                          alt={product.nombre}
                          className="w-full h-40 object-cover rounded-md mb-3"
                          onError={(e) => { e.target.onerror = null; e.target.src="https://placehold.co/600x400/cccccc/000000?text=No+Image"; }}
                        />
                      )}
                      <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-3 mb-3">
                        {product.descripcion || 'Sin descripción disponible.'}
                      </p>
                      <Link to={`/public/products/${product.id}`}> {/* Ruta para ver detalle del producto */}
                        <Button className="w-full bg-purple-600 hover:bg-purple-700 text-white">Ver Producto</Button>
                      </Link>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </section>
        </CardContent>
      </Card>
    </div>
  );
};

export default PublicListingScreen;
