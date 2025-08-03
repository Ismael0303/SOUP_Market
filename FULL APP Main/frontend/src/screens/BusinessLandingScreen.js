import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const BusinessLandingScreen = () => {
  const { businessId } = useParams();
  const [business, setBusiness] = useState(null);
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const loadMockData = async () => {
      try {
        setIsLoading(true);
        
        // Datos simulados para demostración
        const mockBusinesses = {
          1: {
            id: 1,
            nombre: 'Panadería Ñiam',
            tipo_negocio: 'panaderia',
            descripcion: 'Los mejores panes artesanales de la ciudad. Especialistas en panes artesanales, facturas y pastelería tradicional.',
            rating: 4.8,
            fotos_urls: ['https://via.placeholder.com/400x300?text=Panaderia'],
            direccion: 'Av. Principal 123, Centro',
            telefono: '+54 11 1234-5678',
            horarios: 'Lunes a Sábado 7:00 - 20:00'
          },
          2: {
            id: 2,
            nombre: 'Restaurante El Buen Sabor',
            tipo_negocio: 'restaurante',
            descripcion: 'Comida casera y tradicional. Los mejores platos de la cocina argentina con ingredientes frescos y de calidad.',
            rating: 4.5,
            fotos_urls: ['https://via.placeholder.com/400x300?text=Restaurante'],
            direccion: 'Calle Comercial 456, Barrio Norte',
            telefono: '+54 11 2345-6789',
            horarios: 'Martes a Domingo 12:00 - 23:00'
          },
          3: {
            id: 3,
            nombre: 'Servicios Técnicos Rápidos',
            tipo_negocio: 'servicios',
            descripcion: 'Reparación y mantenimiento de equipos informáticos. Servicio técnico especializado en computadoras y notebooks.',
            rating: 4.7,
            fotos_urls: ['https://via.placeholder.com/400x300?text=Servicios'],
            direccion: 'Zona Industrial 789, Sector Sur',
            telefono: '+54 11 3456-7890',
            horarios: 'Lunes a Viernes 9:00 - 18:00'
          }
        };

        const mockProducts = {
          1: [
            {
              id: 1,
              nombre: 'Pan Francés',
              descripcion: 'Pan artesanal recién horneado',
              precio_venta: 25.00,
              categoria: 'panaderia',
              stock_terminado: 50
            },
            {
              id: 2,
              nombre: 'Croissant',
              descripcion: 'Croissant de mantequilla',
              precio_venta: 100.00,
              categoria: 'panaderia',
              stock_terminado: 30
            },
            {
              id: 3,
              nombre: 'Facturas',
              descripcion: 'Facturas dulces variadas',
              precio_venta: 80.00,
              categoria: 'panaderia',
              stock_terminado: 25
            }
          ],
          2: [
            {
              id: 4,
              nombre: 'Pizza Margherita',
              descripcion: 'Pizza tradicional italiana',
              precio_venta: 800.00,
              categoria: 'restaurante',
              stock_terminado: 20
            },
            {
              id: 5,
              nombre: 'Milanesa con Papas',
              descripcion: 'Milanesa de ternera con papas fritas',
              precio_venta: 1200.00,
              categoria: 'restaurante',
              stock_terminado: 15
            },
            {
              id: 6,
              nombre: 'Ensalada César',
              descripcion: 'Ensalada fresca con aderezo especial',
              precio_venta: 600.00,
              categoria: 'restaurante',
              stock_terminado: 10
            }
          ],
          3: [
            {
              id: 7,
              nombre: 'Mantenimiento PC',
              descripcion: 'Servicio de mantenimiento preventivo',
              precio_venta: 1500.00,
              categoria: 'servicios',
              stock_terminado: 999
            },
            {
              id: 8,
              nombre: 'Reparación Notebook',
              descripcion: 'Diagnóstico y reparación de notebooks',
              precio_venta: 2500.00,
              categoria: 'servicios',
              stock_terminado: 999
            }
          ]
        };

        const businessData = mockBusinesses[businessId];
        const productsData = mockProducts[businessId] || [];

        if (businessData) {
          setBusiness(businessData);
          setProducts(productsData);
        } else {
          setBusiness(null);
          setProducts([]);
        }
      } catch (err) {
        console.error('Error al cargar datos del negocio:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadMockData();
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