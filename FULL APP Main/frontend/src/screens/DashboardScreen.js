// frontend/src/screens/DashboardScreen.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import Breadcrumbs from '../components/Breadcrumbs';

const DashboardScreen = () => {
  const [stats, setStats] = useState({
    ventasHoy: 0,
    ingresosHoy: '$0.00',
    productosEnStock: 0,
    totalNegocios: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Simular carga de datos del dashboard
        setTimeout(() => {
          setStats({
            ventasHoy: 12,
            ingresosHoy: '$1,250.00',
            productosEnStock: 45,
            totalNegocios: 3
          });
          setLoading(false);
        }, 1000);
        
      } catch (err) {
        console.error('Error cargando datos del dashboard:', err);
        setError('Error al cargar los datos del dashboard');
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  // Datos de resumen con información real
  const resumen = [
    { 
      label: 'Ventas Hoy', 
      value: stats.ventasHoy, 
      icon: '💸', 
      color: 'bg-green-100 text-green-700' 
    },
    { 
      label: 'Ingresos Hoy', 
      value: stats.ingresosHoy, 
      icon: '📈', 
      color: 'bg-blue-100 text-blue-700' 
    },
    { 
      label: 'Productos en Stock', 
      value: stats.productosEnStock, 
      icon: '📦', 
      color: 'bg-yellow-100 text-yellow-700' 
    },
    { 
      label: 'Negocios', 
      value: stats.totalNegocios, 
      icon: '🏪', 
      color: 'bg-purple-100 text-purple-700' 
    },
  ];

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Cargando datos del dashboard...</p>
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
        <button 
          onClick={() => window.location.reload()} 
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          Reintentar
        </button>
      </Layout>
    );
  }

  return (
    <Layout>
      <Breadcrumbs items={[
        { label: 'Dashboard' }
      ]} />
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>
      {/* Cards de resumen */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        {resumen.map((item, idx) => (
          <div key={idx} className={`rounded-2xl shadow-md p-6 flex items-center gap-4 ${item.color}`}>
            <span className="text-3xl">{item.icon}</span>
            <div>
              <div className="text-2xl font-bold">{item.value}</div>
              <div className="text-gray-600 text-sm font-medium">{item.label}</div>
            </div>
          </div>
        ))}
      </div>
      {/* Acciones rápidas */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white rounded-2xl shadow-lg p-8 flex flex-col gap-4">
          <h2 className="text-xl font-bold text-gray-900 mb-2">Acciones Rápidas</h2>
          <Link to="/dashboard/products/new" className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg py-3 px-6 font-semibold text-center">Crear Producto</Link>
          <Link to="/dashboard/insumos/new" className="bg-green-600 hover:bg-green-700 text-white rounded-lg py-3 px-6 font-semibold text-center">Agregar Insumo</Link>
          <Link to="/dashboard/businesses/new" className="bg-purple-600 hover:bg-purple-700 text-white rounded-lg py-3 px-6 font-semibold text-center">Nuevo Negocio</Link>
          <Link to="/dashboard/pos" className="bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg py-3 px-6 font-semibold text-center">Ir al POS</Link>
        </div>
        {/* Panel de bienvenida o ayuda */}
        <div className="bg-white rounded-2xl shadow-lg p-8 flex flex-col gap-4 justify-center items-center">
          <h2 className="text-xl font-bold text-gray-900 mb-2">¡Bienvenido a SOUP!</h2>
          <p className="text-gray-600 text-center">Gestiona tu negocio, productos, ventas e insumos desde un solo lugar. Usa las acciones rápidas para comenzar.</p>
          <div className="w-40 h-40 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full flex items-center justify-center mt-4">
            <span className="text-6xl">🏪</span>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default DashboardScreen;
