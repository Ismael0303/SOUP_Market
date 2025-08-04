import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getPublicBusinessById, getPublicProducts } from '../api/publicApi';

const BusinessLandingScreen = () => {
  const { businessId } = useParams();
  const [business, setBusiness] = useState(null);
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const businessData = await getPublicBusinessById(businessId);
        const allProducts = await getPublicProducts();
        const productsData = allProducts.filter(
          (product) => String(product.negocio_id) === String(businessId)
        );

        setBusiness(businessData);
        setProducts(productsData);
      } catch (err) {
        console.error('Error al cargar datos del negocio:', err);
        setError('No se pudieron cargar los datos del negocio. Inténtalo de nuevo más tarde.');
        setBusiness(null);
        setProducts([]);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [businessId]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex justify-center items-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando negocio...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex justify-center items-center">
        <div className="text-center">
          <p className="text-red-600 text-lg mb-4">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Volver al Marketplace
          </button>
        </div>
      </div>
    );
  }

  if (!business) {
    return (
      <div className="min-h-screen bg-gray-50 flex justify-center items-center">
        <div className="text-center">
          <p className="text-red-600 text-lg mb-4">Negocio no encontrado</p>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Volver al Marketplace
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <button
            onClick={() => navigate('/')}
            className="text-blue-600 hover:text-blue-700 font-semibold"
          >
            ← Volver al Marketplace
          </button>
          <div className="text-2xl font-bold text-blue-600">SOUP Market</div>
          <div className="w-20"></div> {/* Espaciador */}
        </div>
      </header>

      {/* Contenido principal */}
      <div className="max-w-6xl mx-auto p-6">
        {/* Información del negocio */}
        <div className="bg-white rounded-xl shadow-sm p-8 mb-8">
          <div className="flex flex-col lg:flex-row gap-8">
            <div className="lg:w-1/3">
              <img
                src={business.fotos_urls[0]}
                alt={business.nombre}
                className="w-full h-64 object-cover rounded-lg"
                onError={(e) => {
                  e.target.src = 'https://via.placeholder.com/400x300?text=Negocio';
                }}
              />
            </div>
            <div className="lg:w-2/3">
              <div className="flex items-center gap-4 mb-4">
                <h1 className="text-4xl font-bold text-gray-900">{business.nombre}</h1>
                <span className="bg-yellow-400 text-yellow-900 px-3 py-1 rounded-full text-sm font-semibold">
                  ⭐ {business.rating}
                </span>
              </div>
              <p className="text-gray-600 text-lg mb-4">{business.descripcion}</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
                <div>
                  <strong>Dirección:</strong> {business.direccion}
                </div>
                <div>
                  <strong>Teléfono:</strong> {business.telefono}
                </div>
                <div>
                  <strong>Horarios:</strong> {business.horarios}
                </div>
                <div>
                  <strong>Categoría:</strong> {business.tipo_negocio?.replace(/_/g, ' ')}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Catálogo de productos */}
        <div className="bg-white rounded-xl shadow-sm p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Catálogo de Productos</h2>
          
          {products.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-600 text-lg">
                Este negocio aún no tiene productos disponibles.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {products.map(product => (
                <div key={product.id} className="bg-gray-50 rounded-xl p-6 hover:shadow-md transition-shadow">
                  <h3 className="text-xl font-bold text-gray-900 mb-2">{product.nombre}</h3>
                  <p className="text-gray-600 mb-4">{product.descripcion}</p>
                  <div className="flex justify-between items-center">
                    <span className="text-2xl font-bold text-blue-600">
                      ${product.precio_venta.toFixed(2)}
                    </span>
                    <span className="text-sm text-gray-500">
                      {product.stock_terminado > 0 ? `${product.stock_terminado} disponibles` : 'Agotado'}
                    </span>
                  </div>
                  <button 
                    className="w-full mt-4 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
                    disabled={product.stock_terminado <= 0}
                  >
                    {product.stock_terminado > 0 ? 'Agregar al Carrito' : 'Agotado'}
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default BusinessLandingScreen;
