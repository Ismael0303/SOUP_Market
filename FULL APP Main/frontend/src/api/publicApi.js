// frontend/src/api/publicApi.js

// Define the base URL for your backend API
// Ensure this URL matches the address where your FastAPI backend is running
const API_BASE_URL = 'http://localhost:8000';

// Helper function to handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json();
    // Throw an error with the backend detail
    throw new Error(errorData.detail || 'Something went wrong with the API request.');
  }
  return response.json();
};

/**
 * Fetches all publicly available businesses.
 * @returns {Promise<Array<Object>>} A list of all public businesses.
 */
export const getPublicBusinesses = async () => {
  const response = await fetch(`${API_BASE_URL}/public/businesses`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse(response);
};

/**
 * Fetches details of a specific publicly available business by its ID.
 * @param {string} businessId - The UUID of the business.
 * @returns {Promise<Object>} The details of the public business.
 */
export const getPublicBusinessById = async (businessId) => {
  const response = await fetch(`${API_BASE_URL}/public/businesses/${businessId}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse(response);
};

/**
 * Fetches all publicly available products or services.
 * @returns {Promise<Array<Object>>} A list of all public products/services.
 */
export const getPublicProducts = async () => {
  const response = await fetch(`${API_BASE_URL}/public/products`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse(response);
};

/**
 * Fetches details of a specific publicly available product or service by its ID.
 * @param {string} productId - The UUID of the product/service.
 * @returns {Promise<Object>} The details of the public product/service.
 */
export const getPublicProductById = async (productId) => {
  const response = await fetch(`${API_BASE_URL}/public/products/${productId}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse(response);
};

/**
 * Fetches the public profile details of a specific user by their ID.
 * @param {string} userId - The UUID of the user.
 * @returns {Promise<Object>} The public profile details of the user.
 */
export const getPublicUser = async (userId) => {
  const response = await fetch(`${API_BASE_URL}/public/users/${userId}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });
  return handleResponse(response);
};
