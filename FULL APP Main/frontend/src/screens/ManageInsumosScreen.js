// frontend/src/screens/ManageInsumosScreen.js

import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import insumoApi from '../api/insumoApi'; // Importa el servicio API de insumos
import { useAuth } from '../context/AuthContext'; // Para obtener el estado de autenticación
import { Button } from '../components/ui/button'; // Componente de botón de Shadcn
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card'; // Componentes de tarjeta de Shadcn
import Layout from '../components/Layout';

const ManageInsumosScreen = () => {
  const { isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();
  const [insumos, setInsumos] = useState([]);
  const [isLoadingInsumos, setIsLoadingInsumos] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Redirigir si no está autenticado y la carga ha terminado
    if (!loading && !isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, loading, navigate]);

  useEffect(() => {
    const fetchInsumos = async () => {
      if (isAuthenticated) {
        try {
          setIsLoadingInsumos(true);
          const data = await insumoApi.getAllMyInsumos();
          setInsumos(data);
        } catch (err) {
          console.error('Error al cargar insumos:', err);
          setError('No se pudieron cargar los insumos. Inténtalo de nuevo más tarde.');
        } finally {
          setIsLoadingInsumos(false);
        }
      }
    };

    fetchInsumos();
  }, [isAuthenticated]); // Dependencia para recargar si el estado de autenticación cambia

  const handleDeleteInsumo = async (insumoId) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este insumo?')) {
      try {
        await insumoApi.deleteInsumo(insumoId);
        // Actualizar la lista de insumos después de la eliminación
        setInsumos(insumos.filter(insumo => insumo.id !== insumoId));
      } catch (err) {
        console.error('Error al eliminar insumo:', err);
        setError('No se pudo eliminar el insumo. Por favor, inténtalo de nuevo.');
      }
    }
  };

  if (loading || !isAuthenticated) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Cargando...</p>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Gestión de Insumos</h1>
          <Link to="/dashboard/insumos/new">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md shadow-md transition duration-300 ease-in-out">
              Crear Nuevo Insumo
            </Button>
          </Link>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
            <strong className="font-bold">Error:</strong>
            <span className="block sm:inline"> {error}</span>
          </div>
        )}

        {isLoadingInsumos ? (
          <p className="text-center">Cargando insumos...</p>
        ) : insumos.length === 0 ? (
          <div className="bg-white rounded-xl shadow-lg p-8 text-center">
            <div className="text-gray-500 mb-4">
              <span className="text-4xl">🧾</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              No tienes insumos registrados
            </h3>
            <p className="text-gray-600 mb-4">
              Comienza creando tu primer insumo
            </p>
            <Link to="/dashboard/insumos/new">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                Crear Primer Insumo
              </Button>
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {insumos.map((insumo) => (
              <Card key={insumo.id} className="bg-white dark:bg-gray-800 shadow-lg rounded-lg overflow-hidden">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-lg font-medium">{insumo.nombre}</CardTitle>
                  <span className="text-sm text-gray-500 dark:text-gray-400">ID: {insumo.id.substring(0, 8)}...</span>
                </CardHeader>
                <CardContent className="p-6 pt-0">
                  <p className="text-sm text-gray-700 dark:text-gray-300 mb-2">
                    Cantidad Disponible: <span className="font-semibold">{insumo.cantidad_disponible} {insumo.unidad_medida_compra}</span>
                  </p>
                  <p className="text-sm text-gray-700 dark:text-gray-300 mb-4">
                    Costo Unitario: <span className="font-semibold">${insumo.costo_unitario_compra.toFixed(2)} / {insumo.unidad_medida_compra}</span>
                  </p>
                  <div className="flex space-x-2">
                    <Link to={`/dashboard/insumos/edit/${insumo.id}`}>
                      <Button variant="outline" className="text-blue-600 border-blue-600 hover:bg-blue-50 dark:hover:bg-gray-700">
                        Editar
                      </Button>
                    </Link>
                    <Button
                      variant="destructive"
                      onClick={() => handleDeleteInsumo(insumo.id)}
                      className="bg-red-600 hover:bg-red-700 text-white"
                    >
                      Eliminar
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

export default ManageInsumosScreen; 