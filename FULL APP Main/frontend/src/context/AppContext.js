// frontend/src/context/AppContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

const AppContext = createContext();

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp debe ser usado dentro de un AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  const [currentSection, setCurrentSection] = useState('dashboard');
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Secciones disponibles en la aplicación
  const sections = {
    dashboard: {
      id: 'dashboard',
      name: 'Dashboard',
      icon: '📊',
      path: '/dashboard',
      component: 'DashboardScreen'
    },
    products: {
      id: 'products',
      name: 'Productos',
      icon: '📦',
      path: '/dashboard/products',
      component: 'ProductsScreen'
    },
    insumos: {
      id: 'insumos',
      name: 'Insumos',
      icon: '🧾',
      path: '/dashboard/insumos',
      component: 'InsumosScreen'
    },
    businesses: {
      id: 'businesses',
      name: 'Negocios',
      icon: '🏪',
      path: '/dashboard/businesses',
      component: 'BusinessesScreen'
    },
    ventas: {
      id: 'ventas',
      name: 'Ventas',
      icon: '💰',
      path: '/dashboard/ventas',
      component: 'SalesHistoryScreen'
    },
    pos: {
      id: 'pos',
      name: 'POS',
      icon: '🛒',
      path: '/pos',
      component: 'POSScreen'
    }
  };

  // Navegar a una sección específica
  const navigateToSection = (sectionId) => {
    if (sections[sectionId]) {
      setCurrentSection(sectionId);
      // Aquí se podría implementar navegación sin recargar la página
      // Por ahora usamos la navegación normal
      window.history.pushState({}, '', sections[sectionId].path);
    }
  };

  // Obtener la sección actual
  const getCurrentSection = () => {
    return sections[currentSection];
  };

  // Obtener todas las secciones
  const getAllSections = () => {
    return Object.values(sections);
  };

  // Verificar si una sección está activa
  const isSectionActive = (sectionId) => {
    return currentSection === sectionId;
  };

  // Cargar datos del usuario al iniciar
  useEffect(() => {
    const loadUserData = () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          // Aquí se podría cargar información del usuario desde la API
          setUser({ token, isAuthenticated: true });
        }
      } catch (error) {
        console.error('Error cargando datos del usuario:', error);
      } finally {
        setLoading(false);
      }
    };

    loadUserData();
  }, []);

  const value = {
    currentSection,
    setCurrentSection,
    user,
    setUser,
    loading,
    sections,
    navigateToSection,
    getCurrentSection,
    getAllSections,
    isSectionActive
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}; 