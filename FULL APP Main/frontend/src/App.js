import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';

// Importar pantallas
import LoginScreen from './screens/AuthScreens/LoginScreen';
import RegisterScreen from './screens/AuthScreens/RegisterScreen';
import DashboardScreen from './screens/DashboardScreen';
import ProfileScreen from './screens/ProfileScreen';
import ManageProductsScreen from './screens/ManageProductsScreen';
import CreateProductScreen from './screens/CreateProductScreen';
import EditProductScreen from './screens/EditProductScreen';
import ManageInsumosScreen from './screens/ManageInsumosScreen';
import CreateInsumoScreen from './screens/CreateInsumoScreen';
import EditInsumoScreen from './screens/EditInsumoScreen';
import ManageBusinessesScreen from './screens/ManageBusinessesScreen';
import CreateBusinessScreen from './screens/CreateBusinessScreen';
import EditBusinessScreen from './screens/EditBusinessScreen';
import POSScreen from './screens/POSScreen';
import SalesHistoryScreen from './screens/SalesHistoryScreen';
import PublicListingScreen from './screens/PublicListingScreen';
import BusinessLandingScreen from './screens/BusinessLandingScreen';
import PricingPlansScreen from './screens/PricingPlansScreen';

function App() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <Routes>
        {/* Rutas públicas */}
        <Route path="/" element={<PublicListingScreen />} />
        <Route path="/login" element={!isAuthenticated ? <LoginScreen /> : <Navigate to="/dashboard" />} />
        <Route path="/register" element={!isAuthenticated ? <RegisterScreen /> : <Navigate to="/dashboard" />} />
        <Route path="/public/:businessId" element={<PublicListingScreen />} />
        <Route path="/business/:businessId" element={<BusinessLandingScreen />} />
        <Route path="/pricing" element={<PricingPlansScreen />} />
        
        {/* Rutas protegidas */}
        <Route path="/dashboard" element={isAuthenticated ? <DashboardScreen /> : <Navigate to="/login" />} />
        <Route path="/dashboard/profile" element={isAuthenticated ? <ProfileScreen /> : <Navigate to="/login" />} />
        <Route path="/dashboard/products" element={isAuthenticated ? <ManageProductsScreen /> : <Navigate to="/login" />} />
        <Route path="/dashboard/products/new" element={isAuthenticated ? <CreateProductScreen /> : <Navigate to="/login" />} />
        <Route path="/dashboard/products/:id/edit" element={isAuthenticated ? <EditProductScreen /> : <Navigate to="/login" />} />
        <Route path="/dashboard/insumos" element={isAuthenticated ? <ManageInsumosScreen /> : <Navigate to="/login" />} />
        <Route path="/dashboard/insumos/new" element={isAuthenticated ? <CreateInsumoScreen /> : <Navigate to="/login" />} />
        <Route path="/dashboard/insumos/:id/edit" element={isAuthenticated ? <EditInsumoScreen /> : <Navigate to="/login" />} />
        <Route path="/dashboard/businesses" element={isAuthenticated ? <ManageBusinessesScreen /> : <Navigate to="/login" />} />
        <Route path="/dashboard/businesses/new" element={isAuthenticated ? <CreateBusinessScreen /> : <Navigate to="/login" />} />
        <Route path="/dashboard/businesses/:id/edit" element={isAuthenticated ? <EditBusinessScreen /> : <Navigate to="/login" />} />
        <Route path="/dashboard/pos" element={isAuthenticated ? <POSScreen /> : <Navigate to="/login" />} />
        <Route path="/dashboard/sales" element={isAuthenticated ? <SalesHistoryScreen /> : <Navigate to="/login" />} />
        
        {/* Ruta de fallback */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </div>
  );
}

export default App;
