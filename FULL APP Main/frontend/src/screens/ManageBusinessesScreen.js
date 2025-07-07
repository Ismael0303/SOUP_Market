// frontend/src/screens/ManageBusinessesScreen.js
import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button.jsx';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card.jsx';
import { getMyBusinesses, deleteBusiness } from '../api/businessApi'; // Importar funciones API

const ManageBusinessesScreen = () => {
  const [businesses, setBusinesses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingId, setDeletingId] = useState(null); // Para mostrar estado de eliminación

  // Función para cargar los negocios del usuario
  const fetchBusinesses = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getMyBusinesses();
      setBusinesses(data);
    } catch (err) {
      console.error("Error al cargar negocios:", err);
      setError(err.message || "No se pudieron cargar tus negocios.");
    } finally {
      setLoading(false);
    }
  }, []);

  // Cargar negocios al montar el componente
  useEffect(() => {
    fetchBusinesses();
  }, [fetchBusinesses]); // Dependencia del useCallback

  // Función para manejar la eliminación de un negocio
  const handleDelete = async (businessId) => {
    if (window.confirm("¿Estás seguro de que quieres eliminar este negocio? Esta acción no se puede deshacer.")) {
      setDeletingId(businessId);
      try {
        await deleteBusiness(businessId);
        // Si la eliminación es exitosa, recargar la lista de negocios
        await fetchBusinesses();
      } catch (err) {
        console.error("Error al eliminar negocio:", err);
        setError(err.message || "No se pudo eliminar el negocio.");
      } finally {
        setDeletingId(null);
      }
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-gray-800 dark:text-gray-200">Cargando negocios...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-red-500 text-center">{error}</p>
        <Button onClick={fetchBusinesses} className="ml-4">Reintentar Carga</Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 max-w-4xl mt-8">
      <Card className="rounded-xl shadow-lg p-6 space-y-6">
        <CardHeader>
          <CardTitle className="text-3xl font-bold text-center">Gestionar Negocios</CardTitle>
          <CardDescription className="text-center text-gray-600 dark:text-gray-400">
            Aquí puedes ver, crear, editar y eliminar tus negocios.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex justify-end mb-4">
            <Link to="/dashboard/businesses/new">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white">Crear Nuevo Negocio</Button>
            </Link>
          </div>

          {businesses.length === 0 ? (
            <div className="mt-6 p-4 border rounded-lg text-center text-gray-500 dark:text-gray-400">
              No tienes negocios registrados aún. ¡Crea uno!
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {businesses.map((business) => (
                <Card key={business.id} className="relative rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
                  <CardHeader className="p-4 pb-2">
                    <CardTitle className="text-lg font-semibold truncate">
                      {business.nombre}
                    </CardTitle>
                    <CardDescription className="text-sm text-gray-500">
                      Rubro: {business.rubro}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="p-4 pt-0">
                    {business.fotos_urls && business.fotos_urls.length > 0 && (
                      <img
                        src={business.fotos_urls[0]} // Muestra la primera imagen
                        alt={business.nombre}
                        className="w-full h-32 object-cover rounded-md mb-3"
                        onError={(e) => { e.target.onerror = null; e.target.src="https://placehold.co/600x400/cccccc/000000?text=No+Image"; }}
                      />
                    )}
                    <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2 mb-3">
                      {business.descripcion || 'Sin descripción.'}
                    </p>
                    <div className="flex justify-between items-center mt-3">
                      <Link to={`/dashboard/businesses/edit/${business.id}`}>
                        <Button variant="outline" size="sm">Editar</Button>
                      </Link>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDelete(business.id)}
                        disabled={deletingId === business.id}
                      >
                        {deletingId === business.id ? 'Eliminando...' : 'Eliminar'}
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

export default ManageBusinessesScreen;
