// frontend/src/screens/SalesHistoryScreen.js
import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';

const SalesHistoryScreen = () => {
    const [sales, setSales] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [startDate, setStartDate] = useState(''); // Formato 'YYYY-MM-DD'
    const [endDate, setEndDate] = useState(''); // Formato 'YYYY-MM-DD'
    const [reportData, setReportData] = useState([]);
    const [loadingReport, setLoadingReport] = useState(false);

    // Función para mostrar notificaciones
    const showNotification = (message, type) => {
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

    // Cargar ventas al montar el componente
    useEffect(() => {
        const loadSales = async () => {
            try {
                setLoading(true);
                // Por ahora usamos datos simulados, pero aquí iría la llamada real a la API
                const mockSales = [
                    {
                        id: 1,
                        fecha: '2025-07-10',
                        total: 150.00,
                        productos: [
                            { nombre: 'Pan Francés', cantidad: 2, precio: 25.00 },
                            { nombre: 'Croissant', cantidad: 1, precio: 100.00 }
                        ],
                        metodo_pago: 'Efectivo',
                        estado: 'Completada'
                    },
                    {
                        id: 2,
                        fecha: '2025-07-09',
                        total: 75.50,
                        productos: [
                            { nombre: 'Pan Integral', cantidad: 1, precio: 30.00 },
                            { nombre: 'Galletas', cantidad: 1, precio: 45.50 }
                        ],
                        metodo_pago: 'Tarjeta',
                        estado: 'Completada'
                    }
                ];
                
                setSales(mockSales);
                setError(null);
            } catch (err) {
                setError('Error al cargar las ventas');
                showNotification('Error al cargar las ventas', 'error');
            } finally {
                setLoading(false);
            }
        };

        loadSales();
    }, []);

    const generateReport = async () => {
        if (!startDate || !endDate) {
            showNotification('Por favor selecciona fechas de inicio y fin', 'error');
            return;
        }

        try {
            setLoadingReport(true);
            
            // Aquí iría la llamada real a la API
            const mockReport = {
                ventas: sales.filter(sale => 
                    sale.fecha >= startDate && sale.fecha <= endDate
                ),
                totalVentas: sales.filter(sale => 
                    sale.fecha >= startDate && sale.fecha <= endDate
                ).length,
                promedioVenta: 112.75,
                productosMasVendidos: [
                    { nombre: 'Pan Francés', cantidad: 5 },
                    { nombre: 'Croissant', cantidad: 3 },
                    { nombre: 'Pan Integral', cantidad: 2 }
                ]
            };
            
            setReportData(mockReport);
            showNotification('Reporte generado exitosamente', 'success');
        } catch (err) {
            showNotification('Error al generar el reporte', 'error');
        } finally {
            setLoadingReport(false);
        }
    };

    const exportToCSV = () => {
        if (reportData.ventas && reportData.ventas.length > 0) {
            const csvContent = [
                ['Fecha', 'Total', 'Método de Pago', 'Estado'],
                ...reportData.ventas.map(sale => [
                    sale.fecha,
                    sale.total,
                    sale.metodo_pago,
                    sale.estado
                ])
            ].map(row => row.join(',')).join('\n');

            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `ventas_${startDate}_${endDate}.csv`;
            a.click();
            window.URL.revokeObjectURL(url);
            
            showNotification('Reporte exportado exitosamente', 'success');
        }
    };

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('es-AR', {
            style: 'currency',
            currency: 'ARS'
        }).format(amount);
    };

    if (loading) {
        return (
            <Layout>
                <div className="flex items-center justify-center h-64">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                </div>
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="p-6">
                <div className="mb-6">
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">Historial de Ventas</h1>
                    <p className="text-gray-600">Gestiona y analiza todas las ventas de tu negocio</p>
                </div>

                {/* Filtros y Generación de Reportes */}
                <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                    <h2 className="text-xl font-semibold mb-4">Generar Reporte</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Fecha de Inicio
                            </label>
                            <input
                                type="date"
                                value={startDate}
                                onChange={(e) => setStartDate(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Fecha de Fin
                            </label>
                            <input
                                type="date"
                                value={endDate}
                                onChange={(e) => setEndDate(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>
                        <div className="flex items-end">
                            <button
                                onClick={generateReport}
                                disabled={loadingReport}
                                className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {loadingReport ? 'Generando...' : 'Generar Reporte'}
                            </button>
                        </div>
                    </div>
                    
                    {reportData.ventas && reportData.ventas.length > 0 && (
                        <div className="flex gap-2">
                            <button
                                onClick={exportToCSV}
                                className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
                            >
                                Exportar CSV
                            </button>
                        </div>
                    )}
                </div>

                {/* Estadísticas del Reporte */}
                {reportData.ventas && reportData.ventas.length > 0 && (
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                        <div className="bg-white rounded-lg shadow-md p-4">
                            <h3 className="text-sm font-medium text-gray-500">Total Ventas</h3>
                            <p className="text-2xl font-bold text-gray-900">{reportData.totalVentas}</p>
                        </div>
                        <div className="bg-white rounded-lg shadow-md p-4">
                            <h3 className="text-sm font-medium text-gray-500">Promedio por Venta</h3>
                            <p className="text-2xl font-bold text-gray-900">
                                {formatCurrency(reportData.promedioVenta)}
                            </p>
                        </div>
                        <div className="bg-white rounded-lg shadow-md p-4">
                            <h3 className="text-sm font-medium text-gray-500">Total Ingresos</h3>
                            <p className="text-2xl font-bold text-gray-900">
                                {formatCurrency(reportData.ventas.reduce((sum, sale) => sum + sale.total, 0))}
                            </p>
                        </div>
                        <div className="bg-white rounded-lg shadow-md p-4">
                            <h3 className="text-sm font-medium text-gray-500">Período</h3>
                            <p className="text-lg font-semibold text-gray-900">
                                {startDate} - {endDate}
                            </p>
                        </div>
                    </div>
                )}

                {/* Lista de Ventas */}
                <div className="bg-white rounded-lg shadow-md">
                    <div className="p-6 border-b border-gray-200">
                        <h2 className="text-xl font-semibold">Ventas Recientes</h2>
                    </div>
                    
                    {error && (
                        <div className="p-4 bg-red-50 border border-red-200 rounded-md">
                            <p className="text-red-600">{error}</p>
                        </div>
                    )}

                    {sales.length === 0 ? (
                        <div className="p-8 text-center">
                            <p className="text-gray-500">No hay ventas registradas</p>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Fecha
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Productos
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Total
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Método de Pago
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Estado
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {sales.map((sale) => (
                                        <tr key={sale.id} className="hover:bg-gray-50">
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                                {new Date(sale.fecha).toLocaleDateString('es-AR')}
                                            </td>
                                            <td className="px-6 py-4 text-sm text-gray-900">
                                                <ul className="list-disc list-inside">
                                                    {sale.productos.map((producto, index) => (
                                                        <li key={index}>
                                                            {producto.cantidad}x {producto.nombre}
                                                        </li>
                                                    ))}
                                                </ul>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                                {formatCurrency(sale.total)}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                                {sale.metodo_pago}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                                    sale.estado === 'Completada' 
                                                        ? 'bg-green-100 text-green-800' 
                                                        : 'bg-yellow-100 text-yellow-800'
                                                }`}>
                                                    {sale.estado}
                                                </span>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>
        </Layout>
    );
};

export default SalesHistoryScreen; 