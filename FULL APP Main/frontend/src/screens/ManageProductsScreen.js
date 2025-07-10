// frontend/src/screens/ManageProductsScreen.js
import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button.jsx';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card.jsx';
import { getMyProducts, deleteProduct, updateProductStock, getStockStatus } from '../api/productApi';
import Layout from '../components/Layout';

const ManageProductsScreen = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingId, setDeletingId] = useState(null);

  // Función para cargar los productos del usuario
  const fetchProducts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getMyProducts();
      setProducts(data);
    } catch (err) {
      console.error("Error al cargar productos:", err);
      setError(err.message || "No se pudieron cargar tus productos o servicios.");
    } finally {
      setLoading(false);
    }
  }, []);

  // Cargar productos al montar el componente
  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  const handleUpdateStock = async (productId, newStock) => {
    try {
      await updateProductStock(productId, newStock);
      fetchProducts();
    } catch (error) {
      console.error('Error actualizando stock:', error);
      alert('Error actualizando stock: ' + error.message);
    }
  };

  const handleDelete = async (productId) => {
    if (window.confirm("¿Estás seguro de que quieres eliminar este producto/servicio? Esta acción no se puede deshacer.")) {
      setDeletingId(productId);
      try {
        await deleteProduct(productId);
        await fetchProducts();
      } catch (err) {
        console.error("Error al eliminar producto:", err);
        setError(err.message || "No se pudo eliminar el producto/servicio.");
      } finally {
        setDeletingId(null);
      }
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Cargando productos...</p>
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
        <Button onClick={fetchProducts} className="bg-blue-600 hover:bg-blue-700 text-white">
          Reintentar Carga
        </Button>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Gestionar Productos y Servicios</h1>
          <Link to="/dashboard/products/new">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white">
              Crear Nuevo Producto/Servicio
            </Button>
          </Link>
        </div>

        <p className="text-gray-600">
          Aquí puedes ver, crear, editar y eliminar tus productos y servicios.
        </p>

        {products.length === 0 ? (
          <div className="bg-white rounded-xl shadow-lg p-8 text-center">
            <div className="text-gray-500 mb-4">
              <span className="text-4xl">📦</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              No tienes productos registrados
            </h3>
            <p className="text-gray-600 mb-4">
              Comienza creando tu primer producto o servicio
            </p>
            <Link to="/dashboard/products/new">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                Crear Primer Producto
              </Button>
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map((product) => (
              <Card key={product.id} className="relative rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
                <CardHeader className="p-4 pb-2">
                  <CardTitle className="text-lg font-semibold truncate">
                    {product.nombre}
                  </CardTitle>
                  <CardDescription className="text-sm text-gray-500">
                    Tipo: {product.tipo_producto?.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase()) || 'Sin tipo'}
                  </CardDescription>
                </CardHeader>
                <CardContent className="p-4 pt-0">
                  {product.fotos_urls && product.fotos_urls.length > 0 && (
                    <img
                      src={product.fotos_urls[0]}
                      alt={product.nombre}
                      className="w-full h-32 object-cover rounded-md mb-3"
                      onError={(e) => { 
                        e.target.onerror = null; 
                        e.target.src="https://placehold.co/600x400/cccccc/000000?text=No+Image"; 
                      }}
                    />
                  )}
                  <p className="text-sm text-gray-700 line-clamp-2 mb-3">
                    {product.descripcion || 'Sin descripción.'}
                  </p>
                  
                  {/* Información de stock */}
                  {product.stock_terminado !== undefined && (
                    <div className="mb-3">
                      <span className={`text-xs font-medium px-2 py-1 rounded-full ${
                        product.stock_terminado > 10 
                          ? 'bg-green-100 text-green-800' 
                          : product.stock_terminado > 0 
                            ? 'bg-yellow-100 text-yellow-800' 
                            : 'bg-red-100 text-red-800'
                      }`}>
                        Stock: {product.stock_terminado} unidades
                      </span>
                    </div>
                  )}
                  
                  <div className="flex justify-between items-center mt-3">
                    {product.id ? (
                      <Link to={`/dashboard/products/edit/${product.id}`}>
                        <Button variant="outline" size="sm">Editar</Button>
                      </Link>
                    ) : (
                      <Button variant="outline" size="sm" disabled>Editar</Button>
                    )}
                    <Button
                      variant="destructive"
                      size="sm"
                      onClick={() => handleDelete(product.id)}
                      disabled={deletingId === product.id || !product.id}
                    >
                      {deletingId === product.id ? 'Eliminando...' : 'Eliminar'}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default ManageProductsScreen;
