// frontend/src/api/insumoApi.js

import axios from 'axios';
import { getAuthHeaders } from '../utils/auth'; // Asegúrate de que esta ruta sea correcta

const API_BASE_URL = 'http://127.0.0.1:8000'; // O la URL de tu backend si no es localhost

// Función para obtener los headers de autorización
// Esto es crucial para que los endpoints protegidos funcionen
const getHeaders = () => {
    return {
        headers: {
            ...getAuthHeaders()
        }
    };
};

/**
 * Servicio API para la gestión de Insumos.
 * Proporciona funciones para interactuar con los endpoints de insumos del backend.
 */
const insumoApi = {
    /**
     * Crea un nuevo insumo.
     * @param {object} insumoData - Los datos del insumo a crear (nombre, cantidad_disponible, unidad_medida_compra, costo_unitario_compra).
     * @returns {Promise<object>} El insumo creado.
     */
    createInsumo: async (insumoData) => {
        try {
            // CAMBIO: Eliminado '/insumos/'
            const response = await axios.post(`${API_BASE_URL}/insumos`, insumoData, getHeaders());
            return response.data;
        } catch (error) {
            console.error('Error creating insumo:', error.response?.data || error.message);
            throw error;
        }
    },

    /**
     * Obtiene todos los insumos del usuario autenticado.
     * @returns {Promise<Array<object>>} Una lista de insumos.
     */
    getAllMyInsumos: async () => {
        try {
            // CAMBIO: Eliminado '/insumos/'
            const response = await axios.get(`${API_BASE_URL}/insumos/me`, getHeaders());
            return response.data;
        } catch (error) {
            console.error('Error fetching user insumos:', error.response?.data || error.message);
            throw error;
        }
    },

    /**
     * Obtiene los detalles de un insumo específico por su ID.
     * @param {string} insumoId - El ID del insumo.
     * @returns {Promise<object>} Los detalles del insumo.
     */
    getInsumoById: async (insumoId) => {
        try {
            // CAMBIO: Eliminado '/insumos/'
            const response = await axios.get(`${API_BASE_URL}/insumos/${insumoId}`, getHeaders());
            return response.data;
        } catch (error) {
            console.error(`Error fetching insumo with ID ${insumoId}:`, error.response?.data || error.message);
            throw error;
        }
    },

    /**
     * Actualiza un insumo existente.
     * @param {string} insumoId - El ID del insumo a actualizar.
     * @param {object} updateData - Los datos a actualizar del insumo.
     * @returns {Promise<object>} El insumo actualizado.
     */
    updateInsumo: async (insumoId, updateData) => {
        try {
            // CAMBIO: Eliminado '/insumos/'
            const response = await axios.put(`${API_BASE_URL}/insumos/${insumoId}`, updateData, getHeaders());
            return response.data;
        } catch (error) {
            console.error(`Error updating insumo with ID ${insumoId}:`, error.response?.data || error.message);
            throw error;
        }
    },

    /**
     * Elimina un insumo por su ID.
     * @param {string} insumoId - El ID del insumo a eliminar.
     * @returns {Promise<void>}
     */
    deleteInsumo: async (insumoId) => {
        try {
            // CAMBIO: Eliminado '/insumos/'
            await axios.delete(`${API_BASE_URL}/insumos/${insumoId}`, getHeaders());
            console.log(`Insumo with ID ${insumoId} deleted successfully.`);
        } catch (error) {
            console.error(`Error deleting insumo with ID ${insumoId}:`, error.response?.data || error.message);
            throw error;
        }
    }
};

export default insumoApi; 