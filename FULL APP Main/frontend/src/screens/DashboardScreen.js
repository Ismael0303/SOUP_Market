// frontend/src/screens/DashboardScreen.js
import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card.jsx';
import { Button } from '../components/ui/button.jsx';
import { Link } from 'react-router-dom';

function DashboardScreen() {
  const { user, loading, error, logout } = useAuth();

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-gray-800 dark:text-gray-200">Cargando dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-red-600 text-center">Error: {error}. Por favor, <Link to="/login" className="text-blue-600 hover:underline">inicia sesión de nuevo</Link>.</p>
      </div>
    );
  }

  if (!user) {
    // Esto no debería pasar si la lógica de AuthContext redirige a login
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-red-600">No autenticado. Redirigiendo a login...</p>
        <Link to="/login" className="text-blue-600 hover:underline ml-2">Ir a Login</Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 max-w-4xl mt-8">
      <Card className="rounded-xl shadow-lg p-6 space-y-6">
        <CardHeader>
          <CardTitle className="text-4xl font-bold text-center">Dashboard</CardTitle>
          <CardDescription className="text-lg text-gray-600 dark:text-gray-400 text-center">
            Bienvenido, {user.nombre} ({user.email})!
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Sección de perfil rápido */}
            <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg shadow-sm">
              <h3 className="text-xl font-semibold mb-2 text-blue-800 dark:text-blue-200">Tu Perfil</h3>
              <p className="text-gray-700 dark:text-gray-300">
                Tipo de cuenta: <span className="font-medium capitalize">{user.tipo_tier.replace('_', ' ')}</span>
              </p>
              {user.localizacion && <p className="text-gray-700 dark:text-gray-300">Ubicación: {user.localizacion}</p>}
              {user.curriculum_vitae && (
                <p className="text-gray-700 dark:text-gray-300">
                  CV: <span className="font-medium">Disponible</span>
                </p>
              )}
              <Link to="/profile">
                <Button className="mt-3 w-full bg-blue-600 hover:bg-blue-700 text-white">Ver/Editar Perfil</Button>
              </Link>
            </div>

            {/* Sección de Acciones Rápidas */}
            <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg shadow-sm">
              <h3 className="text-xl font-semibold mb-2 text-green-800 dark:text-green-200">Acciones Rápidas</h3>
              <div className="space-y-2">
                {/* Botón para Gestionar Negocios (visible para microemprendimiento y freelancer) */}
                {user.tipo_tier !== 'client' && (
                  <Link to="/dashboard/businesses" className="block">
                    <Button className="w-full bg-green-600 hover:bg-green-700 text-white">Gestionar Negocios</Button>
                  </Link>
                )}
                {/* Botón para Gestionar Productos/Servicios (visible para microemprendimiento y freelancer) */}
                {user.tipo_tier !== 'client' && (
                  <Link to="/dashboard/products" className="block"> {/* Nueva ruta para productos */}
                    <Button className="w-full bg-green-600 hover:bg-green-700 text-white">Gestionar Productos/Servicios</Button>
                  </Link>
                )}
                <Link to="/my-encargos" className="block">
                  <Button className="w-full bg-green-600 hover:bg-green-700 text-white">Ver Encargos</Button>
                </Link>
                <Link to="/my-clients-suppliers" className="block">
                  <Button className="w-full bg-green-600 hover:bg-green-700 text-white">Gestionar Contactos</Button>
                </Link>
                <Link to="/reports" className="block">
                  <Button className="w-full bg-green-600 hover:bg-green-700 text-white">Ver Informes</Button>
                </Link>
              </div>
            </div>
          </div>

          {/* Sección de Novedades o Estadísticas Clave (a futuro) */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md">
            <h3 className="text-2xl font-semibold mb-4 text-text-dark dark:text-text-light">Novedades y Estadísticas</h3>
            <p className="text-gray-700 dark:text-gray-300">
              Aquí se mostrarán tus estadísticas clave, nuevos encargos, y alertas importantes.
              (Funcionalidad futura de la Fase 6).
            </p>
          </div>

          <Button onClick={logout} className="w-full bg-red-600 hover:bg-red-700 text-white mt-8">
            Cerrar Sesión
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

export default DashboardScreen;
