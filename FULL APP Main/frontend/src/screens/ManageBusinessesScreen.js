// frontend/src/screens/ManageBusinessesScreen.js
import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button.jsx';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card.jsx';
import { getMyBusinesses, deleteBusiness } from '../api/businessApi';
import Layout from '../components/Layout';

const ManageBusinessesScreen = () => {
  const [businesses, setBusinesses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingId, setDeletingId] = useState(null);

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
  }, [fetchBusinesses]);

  // Función para manejar la eliminación de un negocio
  const handleDelete = async (businessId) => {
    if (window.confirm("¿Estás seguro de que quieres eliminar este negocio? Esta acción no se puede deshacer.")) {
      setDeletingId(businessId);
      try {
        await deleteBusiness(businessId);
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
      <Layout>
        <div className="flex justify-center items-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Cargando negocios...</p>
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
        <Button onClick={fetchBusinesses} className="bg-blue-600 hover:bg-blue-700 text-white">
          Reintentar Carga
        </Button>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Gestionar Negocios</h1>
          <Link to="/dashboard/businesses/new">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white">
              Crear Nuevo Negocio
            </Button>
          </Link>
        </div>

        <p className="text-gray-600">
          Aquí puedes ver, crear, editar y eliminar tus negocios.
        </p>

        {businesses.length === 0 ? (
          <div className="bg-white rounded-xl shadow-lg p-8 text-center">
            <div className="text-gray-500 mb-4">
              <span className="text-4xl">🏪</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              No tienes negocios registrados
            </h3>
            <p className="text-gray-600 mb-4">
              Comienza creando tu primer negocio
            </p>
            <Link to="/dashboard/businesses/new">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                Crear Primer Negocio
              </Button>
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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
                      src={business.fotos_urls[0]}
                      alt={business.nombre}
                      className="w-full h-32 object-cover rounded-md mb-3"
                      onError={(e) => { 
                        e.target.onerror = null; 
                        e.target.src="https://placehold.co/600x400/cccccc/000000?text=No+Image"; 
                      }}
                    />
                  )}
                  <p className="text-sm text-gray-700 line-clamp-2 mb-3">
                    {business.descripcion || 'Sin descripción.'}
                  </p>
                  
                  {/* Información adicional del negocio */}
                  <div className="mb-3">
                    <span className="text-xs font-medium px-2 py-1 rounded-full bg-blue-100 text-blue-800">
                      {business.tipo_negocio || 'Sin tipo'}
                    </span>
                  </div>
                  
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
      </div>
    </Layout>
  );
};

export default ManageBusinessesScreen;
