import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

// Importar pantallas de autenticación
import LoginScreen from './screens/AuthScreens/LoginScreen';
import RegisterScreen from './screens/AuthScreens/RegisterScreen';

// Importar pantallas del dashboard
import DashboardScreen from './screens/DashboardScreen';
import ProfileScreen from './screens/ProfileScreen';
import ManageBusinessesScreen from './screens/ManageBusinessesScreen';
import CreateBusinessScreen from './screens/CreateBusinessScreen';
import EditBusinessScreen from './screens/EditBusinessScreen';
import ManageProductsScreen from './screens/ManageProductsScreen';
import POSScreen from './screens/POSScreen';
import CreateProductScreen from './screens/CreateProductScreen';
import EditProductScreen from './screens/EditProductScreen';

// Importar pantallas públicas
import PublicListingScreen from './screens/PublicListingScreen';

// Importar las nuevas pantallas de Insumos
import ManageInsumosScreen from './screens/ManageInsumosScreen';
import CreateInsumoScreen from './screens/CreateInsumoScreen';
import EditInsumoScreen from './screens/EditInsumoScreen';

// Componente de Ruta Privada
const PrivateRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-gray-800 dark:text-gray-200">Cargando...</p>
      </div>
    );
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
};

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          {/* Rutas de autenticación */}
          <Route path="/login" element={<LoginScreen />} />
          <Route path="/register" element={<RegisterScreen />} />

          {/* Rutas públicas */}
          <Route path="/" element={<PublicListingScreen />} />

          {/* Rutas protegidas (requieren autenticación) */}
          <Route path="/dashboard" element={<PrivateRoute><DashboardScreen /></PrivateRoute>} />
          <Route path="/dashboard/profile" element={<PrivateRoute><ProfileScreen /></PrivateRoute>} />

          {/* Rutas de Negocios */}
          <Route path="/dashboard/businesses" element={<PrivateRoute><ManageBusinessesScreen /></PrivateRoute>} />
          <Route path="/dashboard/businesses/new" element={<PrivateRoute><CreateBusinessScreen /></PrivateRoute>} />
          <Route path="/dashboard/businesses/edit/:id" element={<PrivateRoute><EditBusinessScreen /></PrivateRoute>} />

          {/* Rutas de Productos */}
          <Route path="/dashboard/products" element={<PrivateRoute><ManageProductsScreen /></PrivateRoute>} />
          <Route path="/dashboard/products/new" element={<PrivateRoute><CreateProductScreen /></PrivateRoute>} />
          <Route path="/dashboard/products/edit/:productId" element={<PrivateRoute><EditProductScreen /></PrivateRoute>} />

          {/* Ruta del Sistema POS */}
          <Route path="/pos" element={<PrivateRoute><POSScreen /></PrivateRoute>} />

          {/* NUEVAS Rutas de Insumos */}
          <Route path="/dashboard/insumos" element={<PrivateRoute><ManageInsumosScreen /></PrivateRoute>} />
          <Route path="/dashboard/insumos/new" element={<PrivateRoute><CreateInsumoScreen /></PrivateRoute>} />
          <Route path="/dashboard/insumos/edit/:insumoId" element={<PrivateRoute><EditInsumoScreen /></PrivateRoute>} />

          {/* Ruta por defecto para cualquier otra URL no definida */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
};

export default App;
