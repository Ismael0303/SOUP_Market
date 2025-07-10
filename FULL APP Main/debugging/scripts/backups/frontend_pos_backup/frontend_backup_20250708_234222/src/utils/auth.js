// frontend/src/utils/auth.js

/**
 * Obtiene los encabezados de autorización, incluyendo el token JWT del almacenamiento local.
 * @returns {object} Un objeto con los encabezados de autorización.
 */
export const getAuthHeaders = () => {
    const token = localStorage.getItem('token'); // Asume que el token se guarda en localStorage
    if (token) {
        return {
            Authorization: `Bearer ${token}`
        };
    }
    return {};
};

/**
 * Guarda el token JWT en el almacenamiento local.
 * @param {string} token - El token JWT a guardar.
 */
export const setAuthToken = (token) => {
    localStorage.setItem('token', token);
};

/**
 * Elimina el token JWT del almacenamiento local.
 */
export const removeAuthToken = () => {
    localStorage.removeItem('token');
};

/**
 * Verifica si el usuario está autenticado comprobando la existencia de un token.
 * @returns {boolean} True si hay un token, false en caso contrario.
 */
export const isAuthenticated = () => {
    return !!localStorage.getItem('token');
}; 