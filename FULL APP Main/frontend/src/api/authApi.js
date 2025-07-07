// src/api/authApi.js
// Archivo para centralizar las llamadas a la API de autenticación del backend.

const API_BASE_URL = 'http://localhost:8000'; // URL base de tu backend FastAPI

/**
 * Registra un nuevo usuario en la API.
 * @param {object} userData - Objeto con los datos del usuario (nombre, email, password, etc.).
 * @returns {Promise<object>} Los datos del usuario registrado.
 * @throws {Error} Si el registro falla (ej., email ya registrado, errores de validación).
 */
export const registerUser = async (userData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/users/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData), // Envía los datos del usuario como JSON
    });

    if (!response.ok) {
      // Si la respuesta no es OK (ej., 400 Bad Request, 409 Conflict),
      // lanza un error con el mensaje de la API.
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Error al registrar usuario.');
    }

    // Devuelve los datos del usuario si el registro es exitoso
    return await response.json();
  } catch (error) {
    console.error('Error en registerUser:', error);
    throw error; // Vuelve a lanzar el error para que sea manejado en el componente
  }
};

/**
 * Inicia sesión para un usuario existente y obtiene un token de acceso.
 * @param {string} email - El email del usuario.
 * @param {string} password - La contraseña del usuario.
 * @returns {Promise<object>} Un objeto con el token de acceso y su tipo.
 * @throws {Error} Si el login falla (ej., credenciales incorrectas).
 */
export const loginUser = async (email, password) => {
  try {
    // Para OAuth2PasswordRequestForm, FastAPI espera los datos como `application/x-www-form-urlencoded`
    // No podemos usar JSON.stringify directamente. Debemos usar URLSearchParams.
    const formBody = new URLSearchParams();
    formBody.append('username', email); // FastAPI espera 'username' para el email
    formBody.append('password', password);

    const response = await fetch(`${API_BASE_URL}/users/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded', // ¡Importante!
      },
      body: formBody.toString(), // Convierte URLSearchParams a string
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Error al iniciar sesión. Verifica tus credenciales.');
    }

    // Devuelve el token de acceso si el login es exitoso
    return await response.json();
  } catch (error) {
    console.error('Error en loginUser:', error);
    throw error;
  }
};

/**
 * Obtiene el perfil del usuario autenticado.
 * @param {string} token - El token de acceso del usuario.
 * @returns {Promise<object>} Los datos del perfil del usuario.
 * @throws {Error} Si el token es inválido o el usuario no está autenticado.
 */
export const getMyProfile = async (token) => {
  try {
    const response = await fetch(`${API_BASE_URL}/profile/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`, // Envía el token en el header de autorización
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Error al obtener el perfil.');
    }

    return await response.json();
  } catch (error) {
    console.error('Error en getMyProfile:', error);
    throw error;
  }
};

/**
 * Actualiza el perfil del usuario autenticado.
 * @param {string} token - El token de acceso del usuario.
 * @param {object} userData - Objeto con los campos a actualizar del perfil (nombre, localizacion, info_contacto, password).
 * @returns {Promise<object>} Los datos del perfil del usuario actualizado.
 * @throws {Error} Si la actualización falla.
 */
export const updateMyProfile = async (token, userData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/profile/me`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(userData), // Envía los datos a actualizar como JSON
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Error al actualizar el perfil.');
    }

    return await response.json();
  } catch (error) {
    console.error('Error en updateMyProfile:', error);
    throw error;
  }
};

/**
 * Actualiza el CV del usuario autenticado (solo para freelancers).
 * @param {string} token - El token de acceso del usuario.
 * @param {object} cvData - Objeto con los datos del CV.
 * @returns {Promise<object>} Los datos del perfil del usuario actualizado con el CV.
 * @throws {Error} Si la actualización falla o el usuario no es freelancer.
 */
export const updateMyCv = async (token, cvData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/profile/me/cv`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(cvData), // Envía los datos del CV como JSON
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Error al actualizar el CV.');
    }

    return await response.json();
  } catch (error) {
    console.error('Error en updateMyCv:', error);
    throw error;
  }
};
