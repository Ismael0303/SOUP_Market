// Hook personalizado para gestión de plugins
import { useState, useEffect, useCallback } from 'react';

export const usePlugins = () => {
  const [plugins, setPlugins] = useState([]);
  const [activePlugins, setActivePlugins] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Cargar plugins disponibles
  const loadPlugins = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Aquí harías la llamada a la API para obtener plugins
      // Por ahora usamos datos de ejemplo
      const mockPlugins = [
        {
          id: 'panaderia',
          name: 'Plugin Panadería',
          description: 'Funcionalidades específicas para panaderías',
          version: '1.0.0',
          author: 'SOUP Team',
          category: 'Negocio',
          price: 0,
          isActive: false,
          features: [
            'Gestión de stock de productos terminados',
            'Cálculo automático de costos',
            'Reportes de rentabilidad',
            'Sistema de ventas optimizado'
          ]
        },
        {
          id: 'discografica',
          name: 'Plugin Discográfica',
          description: 'Herramientas para estudios de grabación',
          version: '1.0.0',
          author: 'SOUP Team',
          category: 'Servicios',
          price: 0,
          isActive: false,
          features: [
            'Gestión de sesiones de grabación',
            'Control de equipamiento',
            'Facturación por hora',
            'Agenda de reservas'
          ]
        },
        {
          id: 'freelancer',
          name: 'Plugin Freelancer',
          description: 'Herramientas para trabajadores independientes',
          version: '1.0.0',
          author: 'SOUP Team',
          category: 'Servicios',
          price: 0,
          isActive: false,
          features: [
            'Gestión de proyectos',
            'Facturación por proyecto',
            'Control de tiempo',
            'Portfolio de trabajos'
          ]
        }
      ];
      
      setPlugins(mockPlugins);
      
      // Cargar plugins activos del usuario
      const userActivePlugins = mockPlugins.filter(p => p.isActive);
      setActivePlugins(userActivePlugins);
      
    } catch (err) {
      setError('Error al cargar plugins: ' + err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  // Activar plugin
  const activatePlugin = useCallback(async (pluginId) => {
    try {
      // Aquí harías la llamada a la API para activar el plugin
      setPlugins(prev => 
        prev.map(plugin => 
          plugin.id === pluginId 
            ? { ...plugin, isActive: true }
            : plugin
        )
      );
      
      const pluginToActivate = plugins.find(p => p.id === pluginId);
      if (pluginToActivate) {
        setActivePlugins(prev => [...prev, pluginToActivate]);
      }
      
      return true;
    } catch (err) {
      setError('Error al activar plugin: ' + err.message);
      return false;
    }
  }, [plugins]);

  // Desactivar plugin
  const deactivatePlugin = useCallback(async (pluginId) => {
    try {
      // Aquí harías la llamada a la API para desactivar el plugin
      setPlugins(prev => 
        prev.map(plugin => 
          plugin.id === pluginId 
            ? { ...plugin, isActive: false }
            : plugin
        )
      );
      
      setActivePlugins(prev => prev.filter(p => p.id !== pluginId));
      
      return true;
    } catch (err) {
      setError('Error al desactivar plugin: ' + err.message);
      return false;
    }
  }, []);

  // Instalar plugin
  const installPlugin = useCallback(async (pluginId) => {
    try {
      // Aquí harías la llamada a la API para instalar el plugin
      const plugin = plugins.find(p => p.id === pluginId);
      if (plugin) {
        // Simular instalación
        await new Promise(resolve => setTimeout(resolve, 1000));
        return true;
      }
      return false;
    } catch (err) {
      setError('Error al instalar plugin: ' + err.message);
      return false;
    }
  }, [plugins]);

  // Obtener plugin por ID
  const getPluginById = useCallback((pluginId) => {
    return plugins.find(p => p.id === pluginId);
  }, [plugins]);

  // Verificar si un plugin está activo
  const isPluginActive = useCallback((pluginId) => {
    return activePlugins.some(p => p.id === pluginId);
  }, [activePlugins]);

  // Obtener plugins por categoría
  const getPluginsByCategory = useCallback((category) => {
    return plugins.filter(p => p.category === category);
  }, [plugins]);

  // Cargar plugins al montar el componente
  useEffect(() => {
    loadPlugins();
  }, [loadPlugins]);

  return {
    // Estado
    plugins,
    activePlugins,
    loading,
    error,
    
    // Acciones
    loadPlugins,
    activatePlugin,
    deactivatePlugin,
    installPlugin,
    
    // Utilidades
    getPluginById,
    isPluginActive,
    getPluginsByCategory
  };
}; 