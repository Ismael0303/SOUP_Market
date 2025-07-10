// frontend/src/screens/ManageProductsScreen.js
import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button.jsx';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card.jsx';
import { getMyProducts, deleteProduct, updateProductStock, getStockStatus } from '../api/productApi'; // Importar funciones API

const ManageProductsScreen = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingId, setDeletingId] = useState(null); // Para mostrar estado de eliminación

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
  }, [fetchProducts]); // Dependencia del useCallback

  // Función para manejar la eliminación de un producto
  
  const handleUpdateStock = async (productId, newStock) => {
    try {
      await updateProductStock(productId, newStock);
      fetchProducts(); // Recargar productos
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
        // Si la eliminación es exitosa, recargar la lista de productos
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
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-gray-800 dark:text-gray-200">Cargando productos y servicios...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-red-500 text-center">{error}</p>
        <Button onClick={fetchProducts} className="ml-4">Reintentar Carga</Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 max-w-4xl mt-8">
      <Card className="rounded-xl shadow-lg p-6 space-y-6">
        <CardHeader>
          <CardTitle className="text-3xl font-bold text-center">Gestionar Productos y Servicios</CardTitle>
          <CardDescription className="text-center text-gray-600 dark:text-gray-400">
            Aquí puedes ver, crear, editar y eliminar tus productos y servicios.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex justify-end mb-4">
            <Link to="/dashboard/products/new">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white">Crear Nuevo Producto/Servicio</Button>
            </Link>
          </div>

          {products.length === 0 ? (
            <div className="mt-6 p-4 border rounded-lg text-center text-gray-500 dark:text-gray-400">
              No tienes productos o servicios registrados aún. ¡Crea uno!
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {products.map((product) => (
                <Card key={product.id} className="relative rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
                  <CardHeader className="p-4 pb-2">
                    <CardTitle className="text-lg font-semibold truncate">
                      {product.nombre}
                    </CardTitle>
                    <CardDescription className="text-sm text-gray-500">
                      Tipo: {product.tipo_producto.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase())} {/* Formato legible */}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="p-4 pt-0">
                    {product.fotos_urls && product.fotos_urls.length > 0 && (
                      <img
                        src={product.fotos_urls[0]} // Muestra la primera imagen
                        alt={product.nombre}
                        className="w-full h-32 object-cover rounded-md mb-3"
                        onError={(e) => { e.target.onerror = null; e.target.src="https://placehold.co/600x400/cccccc/000000?text=No+Image"; }}
                      />
                    )}
                    <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2 mb-3">
                      {product.descripcion || 'Sin descripción.'}
                    </p>
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
        </CardContent>
      </Card>
    </div>
  );
};

export default ManageProductsScreen;
