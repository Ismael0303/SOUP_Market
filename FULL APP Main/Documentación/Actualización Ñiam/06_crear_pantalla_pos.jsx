import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { useAuth } from '../context/AuthContext';
import { productApi } from '../api/productApi';

const SalePointScreen = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    
    // Estados principales
    const [productos, setProductos] = useState([]);
    const [productosSeleccionados, setProductosSeleccionados] = useState([]);
    const [totalVenta, setTotalVenta] = useState(0);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    
    // Estados para filtros
    const [filtroNombre, setFiltroNombre] = useState('');
    const [filtroCategoria, setFiltroCategoria] = useState('todos');
    
    // Estados para la venta
    const [metodoPago, setMetodoPago] = useState('efectivo');
    const [notasVenta, setNotasVenta] = useState('');

    useEffect(() => {
        cargarProductos();
    }, []);

    useEffect(() => {
        calcularTotal();
    }, [productosSeleccionados]);

    const cargarProductos = async () => {
        try {
            setLoading(true);
            const data = await productApi.getAllMyProducts();
            // Filtrar solo productos con stock disponible
            const productosConStock = data.filter(p => 
                p.stock_terminado > 0 || p.stock_terminado === null
            );
            setProductos(productosConStock);
        } catch (err) {
            setError('Error al cargar productos: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    const calcularTotal = () => {
        const total = productosSeleccionados.reduce((sum, item) => {
            return sum + (item.precio_venta * item.cantidad);
        }, 0);
        setTotalVenta(total);
    };

    const agregarProducto = (producto) => {
        const existente = productosSeleccionados.find(p => p.id === producto.id);
        
        if (existente) {
            // Si ya existe, aumentar cantidad
            const actualizados = productosSeleccionados.map(p => 
                p.id === producto.id 
                    ? { ...p, cantidad: p.cantidad + 1 }
                    : p
            );
            setProductosSeleccionados(actualizados);
        } else {
            // Si no existe, agregar nuevo
            setProductosSeleccionados([
                ...productosSeleccionados,
                {
                    ...producto,
                    cantidad: 1
                }
            ]);
        }
    };

    const actualizarCantidad = (productoId, nuevaCantidad) => {
        if (nuevaCantidad <= 0) {
            // Si cantidad es 0 o menor, remover del carrito
            setProductosSeleccionados(productosSeleccionados.filter(p => p.id !== productoId));
        } else {
            // Actualizar cantidad
            const actualizados = productosSeleccionados.map(p => 
                p.id === productoId 
                    ? { ...p, cantidad: nuevaCantidad }
                    : p
            );
            setProductosSeleccionados(actualizados);
        }
    };

    const removerProducto = (productoId) => {
        setProductosSeleccionados(productosSeleccionados.filter(p => p.id !== productoId));
    };

    const registrarVenta = async () => {
        if (productosSeleccionados.length === 0) {
            setError('No hay productos seleccionados');
            return;
        }

        try {
            setLoading(true);
            setError('');
            
            // Registrar cada venta individualmente
            const ventasRegistradas = [];
            
            for (const item of productosSeleccionados) {
                const ventaData = {
                    quantity_sold: item.cantidad,
                    precio_unitario: item.precio_venta,
                    total_venta: item.precio_venta * item.cantidad,
                    notas: notasVenta
                };
                
                const resultado = await productApi.recordSale(item.id, ventaData);
                ventasRegistradas.push(resultado);
            }
            
            setSuccess(`Venta registrada exitosamente! Total: $${totalVenta.toFixed(2)}`);
            
            // Limpiar carrito
            setProductosSeleccionados([]);
            setTotalVenta(0);
            setNotasVenta('');
            
            // Recargar productos para actualizar stock
            setTimeout(() => {
                cargarProductos();
            }, 1000);
            
        } catch (err) {
            setError('Error al registrar venta: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    const filtrarProductos = () => {
        return productos.filter(producto => {
            const cumpleNombre = producto.nombre.toLowerCase().includes(filtroNombre.toLowerCase());
            const cumpleCategoria = filtroCategoria === 'todos' || producto.tipo_producto === filtroCategoria;
            return cumpleNombre && cumpleCategoria;
        });
    };

    const productosFiltrados = filtrarProductos();

    return (
        <div className="container mx-auto p-6">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-900">Punto de Venta</h1>
                <Button 
                    onClick={() => navigate('/dashboard')}
                    variant="outline"
                >
                    Volver al Dashboard
                </Button>
            </div>

            {/* Mensajes de estado */}
            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                    {error}
                </div>
            )}
            
            {success && (
                <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
                    {success}
                </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Panel de Productos */}
                <div className="lg:col-span-2">
                    <Card>
                        <CardHeader>
                            <CardTitle>Productos Disponibles</CardTitle>
                            
                            {/* Filtros */}
                            <div className="flex gap-4">
                                <div className="flex-1">
                                    <Label htmlFor="filtro-nombre">Buscar por nombre</Label>
                                    <Input
                                        id="filtro-nombre"
                                        value={filtroNombre}
                                        onChange={(e) => setFiltroNombre(e.target.value)}
                                        placeholder="Buscar productos..."
                                    />
                                </div>
                                <div className="w-48">
                                    <Label htmlFor="filtro-categoria">Categoría</Label>
                                    <Select value={filtroCategoria} onValueChange={setFiltroCategoria}>
                                        <SelectTrigger>
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="todos">Todos</SelectItem>
                                            <SelectItem value="PHYSICAL_GOOD">Producto Físico</SelectItem>
                                            <SelectItem value="DIGITAL_GOOD">Producto Digital</SelectItem>
                                            <SelectItem value="SERVICE_BY_HOUR">Servicio por Hora</SelectItem>
                                            <SelectItem value="SERVICE_BY_PROJECT">Servicio por Proyecto</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>
                        </CardHeader>
                        
                        <CardContent>
                            {loading ? (
                                <div className="text-center py-8">Cargando productos...</div>
                            ) : (
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-96 overflow-y-auto">
                                    {productosFiltrados.map((producto) => (
                                        <Card key={producto.id} className="cursor-pointer hover:shadow-md transition-shadow">
                                            <CardContent className="p-4">
                                                <div className="flex justify-between items-start mb-2">
                                                    <h3 className="font-semibold text-sm">{producto.nombre}</h3>
                                                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                                                        {producto.stock_terminado || '∞'} disponibles
                                                    </span>
                                                </div>
                                                
                                                <p className="text-xs text-gray-600 mb-2">
                                                    {producto.descripcion?.substring(0, 50)}...
                                                </p>
                                                
                                                <div className="flex justify-between items-center">
                                                    <span className="font-bold text-green-600">
                                                        ${producto.precio_venta}
                                                    </span>
                                                    <Button
                                                        size="sm"
                                                        onClick={() => agregarProducto(producto)}
                                                        disabled={producto.stock_terminado === 0}
                                                    >
                                                        Agregar
                                                    </Button>
                                                </div>
                                            </CardContent>
                                        </Card>
                                    ))}
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </div>

                {/* Panel de Venta */}
                <div className="lg:col-span-1">
                    <Card>
                        <CardHeader>
                            <CardTitle>Carrito de Venta</CardTitle>
                        </CardHeader>
                        
                        <CardContent>
                            {/* Productos seleccionados */}
                            <div className="space-y-3 mb-4 max-h-64 overflow-y-auto">
                                {productosSeleccionados.map((item) => (
                                    <div key={item.id} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                                        <div className="flex-1">
                                            <h4 className="font-medium text-sm">{item.nombre}</h4>
                                            <p className="text-xs text-gray-600">${item.precio_venta} c/u</p>
                                        </div>
                                        
                                        <div className="flex items-center gap-2">
                                            <Button
                                                size="sm"
                                                variant="outline"
                                                onClick={() => actualizarCantidad(item.id, item.cantidad - 1)}
                                            >
                                                -
                                            </Button>
                                            
                                            <span className="w-8 text-center text-sm">{item.cantidad}</span>
                                            
                                            <Button
                                                size="sm"
                                                variant="outline"
                                                onClick={() => actualizarCantidad(item.id, item.cantidad + 1)}
                                            >
                                                +
                                            </Button>
                                            
                                            <Button
                                                size="sm"
                                                variant="destructive"
                                                onClick={() => removerProducto(item.id)}
                                            >
                                                ×
                                            </Button>
                                        </div>
                                    </div>
                                ))}
                                
                                {productosSeleccionados.length === 0 && (
                                    <p className="text-center text-gray-500 py-8">
                                        No hay productos seleccionados
                                    </p>
                                )}
                            </div>

                            {/* Total */}
                            <div className="border-t pt-4 mb-4">
                                <div className="flex justify-between items-center text-lg font-bold">
                                    <span>Total:</span>
                                    <span>${totalVenta.toFixed(2)}</span>
                                </div>
                            </div>

                            {/* Método de pago */}
                            <div className="mb-4">
                                <Label htmlFor="metodo-pago">Método de Pago</Label>
                                <Select value={metodoPago} onValueChange={setMetodoPago}>
                                    <SelectTrigger>
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="efectivo">Efectivo</SelectItem>
                                        <SelectItem value="tarjeta">Tarjeta</SelectItem>
                                        <SelectItem value="transferencia">Transferencia</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

                            {/* Notas */}
                            <div className="mb-4">
                                <Label htmlFor="notas">Notas de la venta</Label>
                                <Input
                                    id="notas"
                                    value={notasVenta}
                                    onChange={(e) => setNotasVenta(e.target.value)}
                                    placeholder="Notas adicionales..."
                                />
                            </div>

                            {/* Botón de venta */}
                            <Button
                                onClick={registrarVenta}
                                disabled={loading || productosSeleccionados.length === 0}
                                className="w-full"
                                size="lg"
                            >
                                {loading ? 'Registrando...' : 'Completar Venta'}
                            </Button>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
};

export default SalePointScreen; 