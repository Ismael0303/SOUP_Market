// frontend/src/api/productApi.js

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
 * Crea un nuevo producto o servicio.
 * @param {Object} productData - Datos del producto/servicio a crear.
 * @returns {Promise<Object>} El objeto del producto/servicio creado.
 */
export const createProduct = async (productData) => {
  const token = getAuthToken();
  if (!token) throw new Error('No autenticado. Por favor, inicia sesión.');

  const response = await fetch(`${API_BASE_URL}/products/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`, // Envía el token JWT en el encabezado
    },
    body: JSON.stringify(productData),
  });
  return handleResponse(response);
};

/**
 * Obtiene todos los productos/servicios del usuario autenticado.
 * @returns {Promise<Array<Object>>} Una lista de los productos/servicios del usuario.
 */
export const getMyProducts = async () => {
  const token = getAuthToken();
  if (!token) throw new Error('No autenticado. Por favor, inicia sesión.');

  const response = await fetch(`${API_BASE_URL}/products/me`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });
  return handleResponse(response);
};

/**
 * Obtiene los detalles de un producto/servicio específico del usuario autenticado.
 * @param {string} productId - El UUID del producto/servicio.
 * @returns {Promise<Object>} Los detalles del producto/servicio.
 */
export const getProductById = async (productId) => {
  const token = getAuthToken();
  if (!token) throw new Error('No autenticado. Por favor, inicia sesión.');

  const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });
  return handleResponse(response);
};

/**
 * Actualiza un producto/servicio existente del usuario autenticado.
 * @param {string} productId - El UUID del producto/servicio a actualizar.
 * @param {Object} updateData - Los campos a actualizar del producto/servicio.
 * @returns {Promise<Object>} El objeto del producto/servicio actualizado.
 */
export const updateProduct = async (productId, updateData) => {
  const token = getAuthToken();
  if (!token) throw new Error('No autenticado. Por favor, inicia sesión.');

  const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
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
 * Elimina un producto/servicio existente del usuario autenticado.
 * @param {string} productId - El UUID del producto/servicio a eliminar.
 * @returns {Promise<Object>} Un mensaje de éxito.
 */
export const deleteProduct = async (productId) => {
  const token = getAuthToken();
  if (!token) throw new Error('No autenticado. Por favor, inicia sesión.');

  const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
    method: 'DELETE',
    headers: {
      'Accept': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });
  return handleResponse(response);
};

// Exportar todas las funciones como un objeto por defecto para compatibilidad
const productApi = {
  createProduct,
  getMyProducts,
  getProductById,
  updateProduct,
  deleteProduct,
};

export default productApi;
