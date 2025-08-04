// frontend/src/api/reviewApi.js

const API_BASE_URL = 'http://localhost:8000';

const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Error en la solicitud de la API.');
  }
  return response.json();
};

export const createReview = async (token, reviewData) => {
  const response = await fetch(`${API_BASE_URL}/reviews/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(reviewData),
  });
  return handleResponse(response);
};

export const getReviewsByProduct = async (productId) => {
  const response = await fetch(`${API_BASE_URL}/reviews/product/${productId}`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
  });
  return handleResponse(response);
};

const reviewApi = { createReview, getReviewsByProduct };
export default reviewApi;
