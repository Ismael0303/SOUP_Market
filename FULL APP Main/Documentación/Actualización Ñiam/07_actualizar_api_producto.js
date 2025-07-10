// Actualización de la API de Productos para el Capítulo Ñiam
// Archivo: frontend/src/api/productApi.js

// Función para registrar una venta de producto
export const recordSale = async (productId, saleData) => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No hay token de autenticación');
        }

        const response = await fetch(`${API_BASE_URL}/products/${productId}/record_sale`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(saleData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al registrar la venta');
        }

        const data = await response.json();
        return data.venta_info;
    } catch (error) {
        console.error('Error en recordSale:', error);
        throw error;
    }
};

// Función para actualizar el stock de un producto
export const updateProductStock = async (productId, newStock) => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No hay token de autenticación');
        }

        const response = await fetch(`${API_BASE_URL}/products/${productId}/stock`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ new_stock: newStock })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al actualizar stock');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error en updateProductStock:', error);
        throw error;
    }
};

// Función para obtener productos con stock bajo
export const getProductsLowStock = async (threshold = 5.0) => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No hay token de autenticación');
        }

        const response = await fetch(`${API_BASE_URL}/products/low_stock?threshold=${threshold}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al obtener productos con stock bajo');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error en getProductsLowStock:', error);
        throw error;
    }
};

// Función para obtener productos sin stock
export const getProductsOutOfStock = async () => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No hay token de autenticación');
        }

        const response = await fetch(`${API_BASE_URL}/products/out_of_stock`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al obtener productos sin stock');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error en getProductsOutOfStock:', error);
        throw error;
    }
};

// Función para obtener estadísticas de inventario
export const getInventoryStats = async () => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No hay token de autenticación');
        }

        // Obtener todos los productos
        const allProducts = await getAllMyProducts();
        
        // Calcular estadísticas
        const stats = {
            totalProducts: allProducts.length,
            productsWithStock: allProducts.filter(p => p.stock_terminado > 0).length,
            productsLowStock: allProducts.filter(p => p.stock_terminado > 0 && p.stock_terminado <= 5).length,
            productsOutOfStock: allProducts.filter(p => p.stock_terminado === 0 || p.stock_terminado === null).length,
            totalStockValue: allProducts.reduce((sum, p) => {
                return sum + ((p.stock_terminado || 0) * (p.precio_venta || 0));
            }, 0)
        };

        return stats;
    } catch (error) {
        console.error('Error en getInventoryStats:', error);
        throw error;
    }
};

// Función para obtener historial de ventas (simulada para capítulo posterior)
export const getSalesHistory = async (startDate = null, endDate = null) => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No hay token de autenticación');
        }

        let url = `${API_BASE_URL}/sales/history`;
        const params = new URLSearchParams();
        
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        
        if (params.toString()) {
            url += `?${params.toString()}`;
        }

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al obtener historial de ventas');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error en getSalesHistory:', error);
        // Para este capítulo, retornar datos simulados
        return {
            ventas: [],
            total_ventas: 0,
            total_ingresos: 0,
            mensaje: "Historial de ventas no implementado en este capítulo"
        };
    }
};

// Función para generar reporte de ventas (simulada para capítulo posterior)
export const generateSalesReport = async (periodo = 'hoy') => {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No hay token de autenticación');
        }

        const response = await fetch(`${API_BASE_URL}/sales/report?periodo=${periodo}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al generar reporte de ventas');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error en generateSalesReport:', error);
        // Para este capítulo, retornar reporte simulado
        return {
            periodo: periodo,
            total_ventas: 0,
            total_ingresos: 0,
            productos_mas_vendidos: [],
            mensaje: "Reportes de ventas no implementados en este capítulo"
        };
    }
};

// Exportar todas las funciones actualizadas
export const productApi = {
    // Funciones existentes (asumiendo que ya están definidas)
    getAllMyProducts,
    getProductById,
    createProduct,
    updateProduct,
    deleteProduct,
    
    // Nuevas funciones para el Capítulo Ñiam
    recordSale,
    updateProductStock,
    getProductsLowStock,
    getProductsOutOfStock,
    getInventoryStats,
    getSalesHistory,
    generateSalesReport
};

// Nota: Este archivo debe ser integrado con el archivo productApi.js existente
// Las funciones existentes (getAllMyProducts, etc.) deben mantenerse
// Solo se añaden las nuevas funciones para el sistema POS 