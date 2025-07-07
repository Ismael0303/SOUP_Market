import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext'; // Asegúrate de que AuthProvider y useAuth existan

// Importa tus pantallas existentes
import LoginScreen from './screens/AuthScreens/LoginScreen'; // Ajusta si tu ruta es diferente
import RegisterScreen from './screens/AuthScreens/RegisterScreen'; // Ajusta si tu ruta es diferente
import DashboardScreen from './screens/DashboardScreen';
import ProfileScreen from './screens/ProfileScreen';

// Importa las pantallas para la gestión de negocios (Capítulo 1)
import ManageBusinessesScreen from './screens/ManageBusinessesScreen';
import CreateBusinessScreen from './screens/CreateBusinessScreen';
import EditBusinessScreen from './screens/EditBusinessScreen';

// Importa las nuevas pantallas para la gestión de productos/servicios (Capítulo 2)
import ManageProductsScreen from './screens/ManageProductsScreen';
import CreateProductScreen from './screens/CreateProductScreen';
import EditProductScreen from './screens/EditProductScreen';

// Importa la nueva pantalla para el listado público (Capítulo 3)
import PublicListingScreen from './screens/PublicListingScreen'; // <--- NUEVA IMPORTACIÓN


// Componente de ruta protegida
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth(); // Mantén 'loading' si lo usas en AuthContext

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-gray-800 dark:text-gray-200">Cargando...</p>
      </div>
    );
  }

  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="min-h-screen bg-background text-foreground font-sans">
          <Routes>
            {/* Ruta raíz pública */}
            <Route path="/" element={<PublicListingScreen />} /> {/* <--- CAMBIO AQUÍ */}

            {/* Rutas de autenticación */}
            <Route path="/login" element={<LoginScreen />} />
            <Route path="/register" element={<RegisterScreen />} />

            {/* Rutas protegidas */}
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <DashboardScreen />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfileScreen />
                </ProtectedRoute>
              }
            />

            {/* Rutas Protegidas para Gestión de Negocios (Capítulo 1) */}
            <Route
              path="/dashboard/businesses"
              element={
                <ProtectedRoute>
                  <ManageBusinessesScreen />
                </ProtectedRoute>
              }
            />
            <Route
              path="/dashboard/businesses/new"
              element={
                <ProtectedRoute>
                  <CreateBusinessScreen />
                </ProtectedRoute>
              }
            />
            <Route
              path="/dashboard/businesses/edit/:id"
              element={
                <ProtectedRoute>
                  <EditBusinessScreen />
                </ProtectedRoute>
              }
            />

            {/* Rutas Protegidas para Gestión de Productos/Servicios (Capítulo 2) */}
            <Route
              path="/dashboard/products"
              element={
                <ProtectedRoute>
                  <ManageProductsScreen />
                </ProtectedRoute>
              }
            />
            <Route
              path="/dashboard/products/new"
              element={
                <ProtectedRoute>
                  <CreateProductScreen />
                </ProtectedRoute>
              }
            />
            <Route
              path="/dashboard/products/edit/:id"
              element={
                <ProtectedRoute>
                  <EditProductScreen />
                </ProtectedRoute>
              }
            />

            {/* Rutas Públicas para Detalles (Capítulo 3 - Futuro) */}
            {/* Estas rutas se implementarán en la siguiente fase para mostrar detalles de items públicos */}
            <Route path="/public/businesses/:id" element={<PublicListingScreen />} /> {/* Placeholder por ahora */}
            <Route path="/public/products/:id" element={<PublicListingScreen />} /> {/* Placeholder por ahora */}
            <Route path="/public/users/:id" element={<PublicListingScreen />} /> {/* Placeholder por ahora */}


            {/* Catch-all route for undefined paths */}
            <Route path="*" element={<Navigate to="/" replace />} /> {/* Redirige a la raíz pública */}
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
