// frontend/src/api/ventaApi.js

const API_BASE_URL = 'http://localhost:8000';

// Función para mostrar notificaciones
const showNotification = (message, type = 'info') => {
  const notificationDiv = document.createElement('div');
  notificationDiv.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
    type === 'success' ? 'bg-green-500 text-white' :
    type === 'error' ? 'bg-red-500 text-white' :
    'bg-blue-500 text-white'
  }`;
  notificationDiv.textContent = message;
  document.body.appendChild(notificationDiv);
  
  setTimeout(() => {
    document.body.removeChild(notificationDiv);
  }, 3000);
};

/**
 * Obtiene las ventas de un negocio específico
 * @param {number} negocioId - ID del negocio
 * @returns {Promise<Array>} Lista de ventas
 */
export const getVentasByNegocio = async (negocioId) => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/ventas/negocio/${negocioId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error('Error al obtener ventas');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    showNotification('Error al obtener ventas', 'error');
    return [];
  }
};

/**
 * Crea una nueva venta
 * @param {Object} ventaData - Datos de la venta
 * @returns {Promise<Object>} Resultado de la operación
 */
export const createVenta = async (ventaData) => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/ventas/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(ventaData)
    });

    if (!response.ok) {
      throw new Error('Error al crear venta');
    }

    const data = await response.json();
    showNotification('Venta creada exitosamente', 'success');
    return data;
  } catch (error) {
    console.error('Error:', error);
    showNotification('Error al crear venta', 'error');
    throw error;
  }
};

// ------- Endpoints de carrito de compras -------

export const createCarrito = async (carritoData) => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/ventas/carrito/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(carritoData)
    });

    if (!response.ok) {
      throw new Error('Error al crear carrito');
    }

    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    showNotification('Error al crear carrito', 'error');
    throw error;
  }
};

export const getCarrito = async (carritoId) => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/ventas/carrito/${carritoId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error('Error al obtener carrito');
    }

    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    showNotification('Error al obtener carrito', 'error');
    throw error;
  }
};

export const addItemToCarrito = async (carritoId, itemData) => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/ventas/carrito/${carritoId}/items/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(itemData)
    });

    if (!response.ok) {
      throw new Error('Error al agregar item al carrito');
    }

    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    showNotification('Error al agregar item al carrito', 'error');
    throw error;
  }
};

export const removeItemFromCarrito = async (carritoId, itemId) => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/ventas/carrito/${carritoId}/items/${itemId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error('Error al eliminar item del carrito');
    }

    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    showNotification('Error al eliminar item del carrito', 'error');
    throw error;
  }
};

export const clearCarrito = async (carritoId) => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/ventas/carrito/${carritoId}/limpiar`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error('Error al limpiar carrito');
    }

    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    showNotification('Error al limpiar carrito', 'error');
    throw error;
  }
};

/**
 * Obtiene estadísticas del dashboard
 * @returns {Promise<Object>} Estadísticas
 */
export const getDashboardStats = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/ventas/dashboard-stats`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error('Error al obtener estadísticas');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    return {
      totalVentas: 0,
      ventasHoy: 0,
      ventasSemana: 0,
      ventasMes: 0,
      promedioVenta: 0
    };
  }
};

/**
 * Obtiene análisis de ventas por período
 * @param {string} startDate - Fecha de inicio (YYYY-MM-DD)
 * @param {string} endDate - Fecha de fin (YYYY-MM-DD)
 * @returns {Promise<Object>} Análisis de ventas
 */
export const getAnalisisVentas = async (startDate, endDate) => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/ventas/analisis?start_date=${startDate}&end_date=${endDate}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error('Error al obtener análisis');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    showNotification('Error al obtener análisis de ventas', 'error');
    return {
      ventas: [],
      totalVentas: 0,
      promedioVenta: 0,
      productosMasVendidos: []
    };
  }
};

/**
 * Obtiene alertas de stock bajo
 * @returns {Promise<Array>} Lista de productos con stock bajo
 */
export const getAlertasStock = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/productos/alertas-stock`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error('Error al obtener alertas');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    return [];
  }
};

/**
 * Obtiene productos por vencer
 * @returns {Promise<Array>} Lista de productos por vencer
 */
export const getProductosPorVencer = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/productos/por-vencer`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error('Error al obtener productos por vencer');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    return [];
  }
};

export default {
  getVentasByNegocio,
  createVenta,
  createCarrito,
  getCarrito,
  addItemToCarrito,
  removeItemFromCarrito,
  clearCarrito,
  getDashboardStats,
  getAnalisisVentas,
  getAlertasStock,
  getProductosPorVencer
};