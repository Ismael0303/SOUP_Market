// Actualización de ManageProductsScreen para el Capítulo Ñiam
// Archivo: frontend/src/screens/ManageProductsScreen.js

// Añadir las siguientes importaciones si no están presentes:
import { productApi } from '../api/productApi';

// Añadir estados para métricas financieras
const [inventoryStats, setInventoryStats] = useState(null);
const [showFinancialMetrics, setShowFinancialMetrics] = useState(false);

// Añadir función para cargar estadísticas de inventario
const cargarEstadisticasInventario = async () => {
    try {
        const stats = await productApi.getInventoryStats();
        setInventoryStats(stats);
    } catch (error) {
        console.error('Error al cargar estadísticas:', error);
    }
};

// Llamar a esta función en useEffect
useEffect(() => {
    cargarProductos();
    cargarEstadisticasInventario();
}, []);

// Añadir componente de estadísticas de inventario
const InventoryStatsCard = () => {
    if (!inventoryStats) return null;

    return (
        <Card className="mb-6">
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                    Estadísticas de Inventario
                </CardTitle>
            </CardHeader>
            <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{inventoryStats.totalProducts}</div>
                        <div className="text-sm text-gray-600">Total Productos</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">{inventoryStats.productsWithStock}</div>
                        <div className="text-sm text-gray-600">Con Stock</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-yellow-600">{inventoryStats.productsLowStock}</div>
                        <div className="text-sm text-gray-600">Stock Bajo</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-red-600">{inventoryStats.productsOutOfStock}</div>
                        <div className="text-sm text-gray-600">Sin Stock</div>
                    </div>
                </div>
                <div className="mt-4 pt-4 border-t">
                    <div className="text-center">
                        <div className="text-lg font-bold text-green-600">
                            ${inventoryStats.totalStockValue.toFixed(2)}
                        </div>
                        <div className="text-sm text-gray-600">Valor Total en Inventario</div>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
};

// Actualizar la tabla de productos para incluir métricas financieras
const ProductTable = () => {
    return (
        <div className="overflow-x-auto">
            <table className="w-full border-collapse border border-gray-300">
                <thead>
                    <tr className="bg-gray-50">
                        <th className="border border-gray-300 px-4 py-2 text-left">Nombre</th>
                        <th className="border border-gray-300 px-4 py-2 text-left">Descripción</th>
                        <th className="border border-gray-300 px-4 py-2 text-center">Stock</th>
                        <th className="border border-gray-300 px-4 py-2 text-center">Precio Venta</th>
                        {showFinancialMetrics && (
                            <>
                                <th className="border border-gray-300 px-4 py-2 text-center">COGS</th>
                                <th className="border border-gray-300 px-4 py-2 text-center">Margen</th>
                                <th className="border border-gray-300 px-4 py-2 text-center">Rentabilidad</th>
                            </>
                        )}
                        <th className="border border-gray-300 px-4 py-2 text-center">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {productos.map((producto) => (
                        <tr key={producto.id} className="hover:bg-gray-50">
                            <td className="border border-gray-300 px-4 py-2">
                                <div className="font-medium">{producto.nombre}</div>
                                <div className="text-xs text-gray-500">{producto.tipo_producto}</div>
                            </td>
                            <td className="border border-gray-300 px-4 py-2">
                                <div className="text-sm">
                                    {producto.descripcion?.substring(0, 50)}...
                                </div>
                            </td>
                            <td className="border border-gray-300 px-4 py-2 text-center">
                                <div className={`font-bold ${
                                    producto.stock_terminado === 0 ? 'text-red-600' :
                                    producto.stock_terminado <= 5 ? 'text-yellow-600' :
                                    'text-green-600'
                                }`}>
                                    {producto.stock_terminado || '∞'}
                                </div>
                                <div className="text-xs text-gray-500">disponibles</div>
                            </td>
                            <td className="border border-gray-300 px-4 py-2 text-center">
                                <div className="font-bold text-green-600">
                                    ${producto.precio_venta}
                                </div>
                            </td>
                            {showFinancialMetrics && (
                                <>
                                    <td className="border border-gray-300 px-4 py-2 text-center">
                                        <div className="text-sm">
                                            ${producto.cogs || 0}
                                        </div>
                                    </td>
                                    <td className="border border-gray-300 px-4 py-2 text-center">
                                        <div className={`text-sm font-medium ${
                                            producto.margen_ganancia_real > 30 ? 'text-green-600' :
                                            producto.margen_ganancia_real > 15 ? 'text-yellow-600' :
                                            'text-red-600'
                                        }`}>
                                            {producto.margen_ganancia_real?.toFixed(1) || 0}%
                                        </div>
                                    </td>
                                    <td className="border border-gray-300 px-4 py-2 text-center">
                                        <div className="text-sm">
                                            ${((producto.precio_venta - (producto.cogs || 0)) * (producto.stock_terminado || 0)).toFixed(2)}
                                        </div>
                                    </td>
                                </>
                            )}
                            <td className="border border-gray-300 px-4 py-2 text-center">
                                <div className="flex gap-2 justify-center">
                                    <Button
                                        size="sm"
                                        variant="outline"
                                        onClick={() => navigate(`/dashboard/products/edit/${producto.id}`)}
                                    >
                                        Editar
                                    </Button>
                                    <Button
                                        size="sm"
                                        variant="destructive"
                                        onClick={() => handleDeleteProduct(producto.id)}
                                    >
                                        Eliminar
                                    </Button>
                                </div>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

// Añadir botón para mostrar/ocultar métricas financieras
const FinancialMetricsToggle = () => {
    return (
        <div className="mb-4">
            <Button
                variant="outline"
                onClick={() => setShowFinancialMetrics(!showFinancialMetrics)}
                className="flex items-center gap-2"
            >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                {showFinancialMetrics ? 'Ocultar' : 'Mostrar'} Métricas Financieras
            </Button>
        </div>
    );
};

// Actualizar el componente principal para incluir las nuevas funcionalidades
const ManageProductsScreen = () => {
    // ... estados existentes ...
    
    return (
        <div className="container mx-auto p-6">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-900">Mis Productos</h1>
                <div className="flex gap-2">
                    <Button
                        onClick={() => navigate('/dashboard/pos')}
                        className="bg-green-600 hover:bg-green-700"
                    >
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                        </svg>
                        Punto de Venta
                    </Button>
                    <Button onClick={() => navigate('/dashboard/products/create')}>
                        Crear Producto
                    </Button>
                </div>
            </div>

            {/* Estadísticas de inventario */}
            <InventoryStatsCard />

            {/* Toggle de métricas financieras */}
            <FinancialMetricsToggle />

            {/* Tabla de productos */}
            <Card>
                <CardHeader>
                    <CardTitle>Lista de Productos</CardTitle>
                </CardHeader>
                <CardContent>
                    {loading ? (
                        <div className="text-center py-8">Cargando productos...</div>
                    ) : productos.length === 0 ? (
                        <div className="text-center py-8 text-gray-500">
                            No tienes productos creados
                        </div>
                    ) : (
                        <ProductTable />
                    )}
                </CardContent>
            </Card>
        </div>
    );
};

export default ManageProductsScreen; 