// frontend/src/api/businessApi.js

// Define la URL base de tu API de backend
// Asegúrate de que esta URL coincida con la dirección donde tu backend FastAPI está corriendo
const API_BASE_URL = 'http://localhost:8000';

// Función auxiliar para manejar respuestas de la API
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json();
    // Lanza un error con el detalle del backend
    throw new Error(errorData.detail || 'Algo salió mal en la solicitud a la API.');
  }
  return response.json();
};

// Función para obtener el token de autenticación del localStorage
// Esto es crucial para las rutas protegidas
const getAuthToken = () => {
  return localStorage.getItem('token'); // Asume que el token se guarda con la clave 'token'
};

/**
 * Crea un nuevo negocio.
 * @param {Object} businessData - Datos del negocio a crear (nombre, rubro, descripcion, etc.).
 * @returns {Promise<Object>} El objeto del negocio creado.
 */
export const createBusiness = async (businessData) => {
  const token = getAuthToken();
  if (!token) throw new Error('No autenticado. Por favor, inicia sesión.');

  const response = await fetch(`${API_BASE_URL}/businesses/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`, // Envía el token JWT en el encabezado
    },
    body: JSON.stringify(businessData),
  });
  return handleResponse(response);
};

/**
 * Obtiene todos los negocios del usuario autenticado.
 * @returns {Promise<Array<Object>>} Una lista de los negocios del usuario.
 */
export const getMyBusinesses = async () => {
  const token = getAuthToken();
  if (!token) throw new Error('No autenticado. Por favor, inicia sesión.');

  const response = await fetch(`${API_BASE_URL}/businesses/me`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });
  return handleResponse(response);
};

/**
 * Obtiene los detalles de un negocio específico del usuario autenticado.
 * @param {string} businessId - El UUID del negocio.
 * @returns {Promise<Object>} Los detalles del negocio.
 */
export const getBusinessById = async (businessId) => {
  const token = getAuthToken();
  if (!token) throw new Error('No autenticado. Por favor, inicia sesión.');

  const response = await fetch(`${API_BASE_URL}/businesses/${businessId}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });
  return handleResponse(response);
};

/**
 * Actualiza un negocio existente del usuario autenticado.
 * @param {string} businessId - El UUID del negocio a actualizar.
 * @param {Object} updateData - Los campos a actualizar del negocio.
 * @returns {Promise<Object>} El objeto del negocio actualizado.
 */
export const updateBusiness = async (businessId, updateData) => {
  const token = getAuthToken();
  if (!token) throw new Error('No autenticado. Por favor, inicia sesión.');

  const response = await fetch(`${API_BASE_URL}/businesses/${businessId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(updateData),
  });
  return handleResponse(response);
};

/**
 * Elimina un negocio existente del usuario autenticado.
 * @param {string} businessId - El UUID del negocio a eliminar.
 * @returns {Promise<Object>} Un mensaje de éxito.
 */
export const deleteBusiness = async (businessId) => {
  const token = getAuthToken();
  if (!token) throw new Error('No autenticado. Por favor, inicia sesión.');

  const response = await fetch(`${API_BASE_URL}/businesses/${businessId}`, {
    method: 'DELETE',
    headers: {
      'Accept': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });
  return handleResponse(response);
};

// Exportar todas las funciones como un objeto por defecto para compatibilidad
const businessApi = {
  createBusiness,
  getMyBusinesses,
  getAllMyBusinesses: getMyBusinesses, // Alias para compatibilidad
  getBusinessById,
  updateBusiness,
  deleteBusiness,
};

export default businessApi;
