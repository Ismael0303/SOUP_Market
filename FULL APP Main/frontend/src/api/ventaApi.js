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


/**
 * Obtiene análisis de ventas por período
 * @param {string} negocioId - ID del negocio
 * @param {string} startDate - Fecha de inicio (YYYY-MM-DD)
 * @param {string} endDate - Fecha de fin (YYYY-MM-DD)
 * @returns {Promise<Object>} Análisis de ventas
 */
export const getAnalisisVentas = async (negocioId, startDate, endDate) => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(
      `${API_BASE_URL}/ventas/analisis/${negocioId}?fecha_inicio=${startDate}&fecha_fin=${endDate}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );

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
 * @param {string} negocioId - ID del negocio
 * @returns {Promise<Object>} Lista de productos con stock bajo y total
 */
export const getAlertasStock = async (negocioId) => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/ventas/alertas/stock/${negocioId}`, {
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
    return { alertas: [], total: 0 };
  }
};

/**
 * Obtiene productos próximos a vencer
 * @param {string} negocioId - ID del negocio
 * @param {number} diasLimite - Días límite para alerta de vencimiento (opcional)
 * @returns {Promise<Object>} Lista de productos por vencer y total
 */
export const getProductosPorVencer = async (negocioId, diasLimite = 7) => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(
      `${API_BASE_URL}/ventas/alertas/vencimiento/${negocioId}?dias_limite=${diasLimite}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );

    if (!response.ok) {
      throw new Error('Error al obtener productos por vencer');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    return { productos: [], total: 0 };
  }
};

export default {
  getVentasByNegocio,
  createVenta,
  getAnalisisVentas,
  getAlertasStock,
  getProductosPorVencer
};
