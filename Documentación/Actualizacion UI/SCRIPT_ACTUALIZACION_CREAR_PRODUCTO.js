// SCRIPT_ACTUALIZACION_CREAR_PRODUCTO.js
// Actualización de CreateProductScreen.js según mockup Gemini

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import productApi from '../api/productApi';
import insumoApi from '../api/insumoApi';
import businessApi from '../api/businessApi';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Textarea } from '../components/ui/textarea';
import { 
  PlusCircle, 
  MinusCircle, 
  Calculator, 
  DollarSign, 
  TrendingUp,
  Home,
  Package,
  ShoppingCart,
  BarChart3,
  Settings,
  User,
  Search
} from 'lucide-react';

const CreateProductScreen = () => {
  const { isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    precio: '',
    tipo_producto: '',
    negocio_id: '',
    precio_venta: '',
    margen_ganancia_sugerido: '',
    categoria: '',
    stock_terminado: '',
    stock_minimo: '',
    unidad_venta: 'unidad',
    es_perecedero: true,
    tiempo_vida_util: '',
    requiere_refrigeracion: false,
    ingredientes: [],
    alergenos: []
  });

  const [businesses, setBusinesses] = useState([]);
  const [availableInsumos, setAvailableInsumos] = useState([]);
  const [selectedInsumos, setSelectedInsumos] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoadingData, setIsLoadingData] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const [calculatedInfo, setCalculatedInfo] = useState({
    cogs: null,
    precio_sugerido: null,
    margen_ganancia_real: null,
  });

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      navigate('/login');
      return;
    }

    const fetchData = async () => {
      if (isAuthenticated) {
        try {
          setIsLoadingData(true);
          const businessData = await businessApi.getAllMyBusinesses();
          const insumosData = await insumoApi.getAllMyInsumos();
          setBusinesses(businessData);
          setAvailableInsumos(insumosData);
        } catch (err) {
          console.error('Error al cargar datos iniciales:', err);
          setError('No se pudieron cargar los datos iniciales (negocios/insumos).');
        } finally {
          setIsLoadingData(false);
        }
      }
    };

    fetchData();
  }, [isAuthenticated, loading, navigate]);

  useEffect(() => {
    let totalCogs = 0;
    
    selectedInsumos.forEach(item => {
      if (item.insumo_id && item.cantidad_necesaria) {
        const insumo = availableInsumos.find(i => i.id === item.insumo_id);
        if (insumo) {
          totalCogs += parseFloat(item.cantidad_necesaria) * insumo.costo_unitario_compra;
        }
      }
    });

    let precioSugerido = null;
    if (totalCogs > 0 && formData.margen_ganancia_sugerido) {
      const margen = parseFloat(formData.margen_ganancia_sugerido);
      precioSugerido = totalCogs * (1 + margen / 100);
    }

    let margenReal = null;
    if (totalCogs > 0 && formData.precio_venta) {
      const precioVenta = parseFloat(formData.precio_venta);
      margenReal = ((precioVenta - totalCogs) / totalCogs) * 100;
    }

    setCalculatedInfo({
      cogs: totalCogs > 0 ? totalCogs : null,
      precio_sugerido: precioSugerido,
      margen_ganancia_real: margenReal,
    });
  }, [selectedInsumos, availableInsumos, formData.margen_ganancia_sugerido, formData.precio_venta]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleInsumoChange = (index, field, value) => {
    const updatedInsumos = [...selectedInsumos];
    updatedInsumos[index] = {
      ...updatedInsumos[index],
      [field]: value,
    };
    setSelectedInsumos(updatedInsumos);
  };

  const handleAddInsumo = () => {
    setSelectedInsumos((prev) => [...prev, { insumo_id: '', cantidad_necesaria: '' }]);
  };

  const handleRemoveInsumo = (index) => {
    setSelectedInsumos((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const insumosToSend = selectedInsumos
        .filter(item => item.insumo_id && parseFloat(item.cantidad_necesaria) > 0)
        .map(item => ({
          insumo_id: item.insumo_id,
          cantidad_necesaria: parseFloat(item.cantidad_necesaria),
        }));

      const dataToSend = {
        ...formData,
        precio: parseFloat(formData.precio),
        precio_venta: formData.precio_venta ? parseFloat(formData.precio_venta) : null,
        margen_ganancia_sugerido: formData.margen_ganancia_sugerido ? parseFloat(formData.margen_ganancia_sugerido) : null,
        stock_terminado: formData.stock_terminado ? parseFloat(formData.stock_terminado) : 0,
        stock_minimo: formData.stock_minimo ? parseFloat(formData.stock_minimo) : 0,
        tiempo_vida_util: formData.tiempo_vida_util ? parseInt(formData.tiempo_vida_util) : null,
        insumos: insumosToSend,
      };

      const createdProduct = await productApi.createProduct(dataToSend);
      setSuccessMessage('Producto/Servicio creado exitosamente!');

      setTimeout(() => {
        navigate('/dashboard/products');
      }, 2000);
    } catch (err) {
      console.error('Error al crear producto:', err);
      const errorMessage = err.response?.data?.detail || 'Error al crear el producto/servicio. Por favor, verifica los datos.';
      setError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading || !isAuthenticated || isLoadingData) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-white shadow-lg border-r border-gray-200 flex-shrink-0">
        <div className="p-6">
          <div className="text-3xl font-bold text-blue-600 mb-8">SOUP Market</div>
          <nav>
            <ul className="space-y-4">
              <li>
                <a href="/dashboard" className="flex items-center text-blue-600 font-semibold p-3 rounded-lg bg-blue-50">
                  <Home className="w-5 h-5 mr-3" />
                  Dashboard
                </a>
              </li>
              <li>
                <a href="/dashboard/products" className="flex items-center text-gray-700 hover:text-blue-600 p-3 rounded-lg hover:bg-gray-50">
                  <Package className="w-5 h-5 mr-3" />
                  Productos
                </a>
              </li>
              <li>
                <a href="/pos" className="flex items-center text-gray-700 hover:text-blue-600 p-3 rounded-lg hover:bg-gray-50">
                  <ShoppingCart className="w-5 h-5 mr-3" />
                  Ventas
                </a>
              </li>
              <li>
                <a href="/dashboard/insumos" className="flex items-center text-gray-700 hover:text-blue-600 p-3 rounded-lg hover:bg-gray-50">
                  <BarChart3 className="w-5 h-5 mr-3" />
                  Inventario
                </a>
              </li>
              <li>
                <a href="/dashboard/reports" className="flex items-center text-gray-700 hover:text-blue-600 p-3 rounded-lg hover:bg-gray-50">
                  <BarChart3 className="w-5 h-5 mr-3" />
                  Reportes
                </a>
              </li>
              <li>
                <a href="/dashboard/settings" className="flex items-center text-gray-700 hover:text-blue-600 p-3 rounded-lg hover:bg-gray-50">
                  <Settings className="w-5 h-5 mr-3" />
                  Ajustes
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-grow p-8">
        {/* Header */}
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <div>
            <h1 className="text-4xl font-bold text-gray-800 mb-1">Crear Producto</h1>
            <p className="text-sm text-gray-500">Dashboard > Productos > Crear Producto</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="relative">
              <Input
                type="text"
                placeholder="Buscar..."
                className="pl-10 pr-4 py-2 w-full md:w-64"
              />
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>
            <Button variant="outline" className="flex items-center">
              <User className="w-5 h-5 mr-2" />
              Usuario
            </Button>
          </div>
        </header>

        {/* Messages */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {successMessage && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
            {successMessage}
          </div>
        )}

        {/* Form */}
        <Card className="p-8">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-center">Detalles del Producto</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-8">
              {/* Basic Information */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <Label htmlFor="nombre" className="required-label">Nombre del producto</Label>
                  <Input
                    id="nombre"
                    name="nombre"
                    value={formData.nombre}
                    onChange={handleChange}
                    placeholder="Introduce el nombre del producto"
                    className="mt-1"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="tipo_producto" className="required-label">Tipo de producto</Label>
                  <Select name="tipo_producto" value={formData.tipo_producto} onValueChange={(value) => handleChange({ target: { name: 'tipo_producto', value } })}>
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder="Selecciona el tipo" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="PHYSICAL_GOOD">Producto Físico</SelectItem>
                      <SelectItem value="SERVICE_BY_HOUR">Servicio por Hora</SelectItem>
                      <SelectItem value="SERVICE_BY_PROJECT">Servicio por Proyecto</SelectItem>
                      <SelectItem value="DIGITAL_GOOD">Producto Digital</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="categoria">Categoría</Label>
                  <Select name="categoria" value={formData.categoria} onValueChange={(value) => handleChange({ target: { name: 'categoria', value } })}>
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder="Selecciona la categoría" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="pan">Pan</SelectItem>
                      <SelectItem value="pastel">Pastel</SelectItem>
                      <SelectItem value="galleta">Galleta</SelectItem>
                      <SelectItem value="bollo">Bollo</SelectItem>
                      <SelectItem value="tarta">Tarta</SelectItem>
                      <SelectItem value="empanada">Empanada</SelectItem>
                      <SelectItem value="chipa">Chipa</SelectItem>
                      <SelectItem value="otro">Otro</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="negocio_id" className="required-label">Negocio</Label>
                  <Select name="negocio_id" value={formData.negocio_id} onValueChange={(value) => handleChange({ target: { name: 'negocio_id', value } })}>
                    <SelectTrigger className="mt-1">
                      <SelectValue placeholder="Selecciona el negocio" />
                    </SelectTrigger>
                    <SelectContent>
                      {businesses.map(business => (
                        <SelectItem key={business.id} value={business.id}>
                          {business.nombre}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Description */}
              <div>
                <Label htmlFor="descripcion">Descripción</Label>
                <Textarea
                  id="descripcion"
                  name="descripcion"
                  value={formData.descripcion}
                  onChange={handleChange}
                  placeholder="Describe el producto o servicio..."
                  className="mt-1"
                  rows={4}
                />
              </div>

              {/* Pricing Information */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <Label htmlFor="precio" className="required-label">Precio base</Label>
                  <Input
                    id="precio"
                    name="precio"
                    type="number"
                    step="0.01"
                    value={formData.precio}
                    onChange={handleChange}
                    placeholder="0.00"
                    className="mt-1"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="precio_venta">Precio de venta</Label>
                  <Input
                    id="precio_venta"
                    name="precio_venta"
                    type="number"
                    step="0.01"
                    value={formData.precio_venta}
                    onChange={handleChange}
                    placeholder="0.00"
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label htmlFor="margen_ganancia_sugerido">Margen sugerido (%)</Label>
                  <Input
                    id="margen_ganancia_sugerido"
                    name="margen_ganancia_sugerido"
                    type="number"
                    step="0.1"
                    value={formData.margen_ganancia_sugerido}
                    onChange={handleChange}
                    placeholder="0.0"
                    className="mt-1"
                  />
                </div>
              </div>

              {/* Stock Information */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <Label htmlFor="stock_terminado">Stock actual</Label>
                  <Input
                    id="stock_terminado"
                    name="stock_terminado"
                    type="number"
                    step="0.01"
                    value={formData.stock_terminado}
                    onChange={handleChange}
                    placeholder="0"
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label htmlFor="stock_minimo">Stock mínimo</Label>
                  <Input
                    id="stock_minimo"
                    name="stock_minimo"
                    type="number"
                    step="0.01"
                    value={formData.stock_minimo}
                    onChange={handleChange}
                    placeholder="0"
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label htmlFor="unidad_venta">Unidad de venta</Label>
                  <Select name="unidad_venta" value={formData.unidad_venta} onValueChange={(value) => handleChange({ target: { name: 'unidad_venta', value } })}>
                    <SelectTrigger className="mt-1">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="unidad">Unidad</SelectItem>
                      <SelectItem value="kg">Kilogramo</SelectItem>
                      <SelectItem value="docena">Docena</SelectItem>
                      <SelectItem value="litro">Litro</SelectItem>
                      <SelectItem value="metro">Metro</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Product Properties */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="flex items-center space-x-4">
                  <input
                    type="checkbox"
                    id="es_perecedero"
                    name="es_perecedero"
                    checked={formData.es_perecedero}
                    onChange={handleChange}
                    className="rounded"
                  />
                  <Label htmlFor="es_perecedero">Es perecedero</Label>
                </div>
                <div className="flex items-center space-x-4">
                  <input
                    type="checkbox"
                    id="requiere_refrigeracion"
                    name="requiere_refrigeracion"
                    checked={formData.requiere_refrigeracion}
                    onChange={handleChange}
                    className="rounded"
                  />
                  <Label htmlFor="requiere_refrigeracion">Requiere refrigeración</Label>
                </div>
              </div>

              {formData.es_perecedero && (
                <div>
                  <Label htmlFor="tiempo_vida_util">Tiempo de vida útil (días)</Label>
                  <Input
                    id="tiempo_vida_util"
                    name="tiempo_vida_util"
                    type="number"
                    value={formData.tiempo_vida_util}
                    onChange={handleChange}
                    placeholder="0"
                    className="mt-1"
                  />
                </div>
              )}

              {/* Insumos Section */}
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold">Insumos del Producto</h3>
                  <Button type="button" onClick={handleAddInsumo} variant="outline" size="sm">
                    <PlusCircle className="w-4 h-4 mr-2" />
                    Agregar Insumo
                  </Button>
                </div>
                
                {selectedInsumos.map((item, index) => (
                  <div key={index} className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 p-4 bg-gray-50 rounded-lg">
                    <div>
                      <Label>Insumo</Label>
                      <Select
                        value={item.insumo_id}
                        onValueChange={(value) => handleInsumoChange(index, 'insumo_id', value)}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Selecciona insumo" />
                        </SelectTrigger>
                        <SelectContent>
                          {availableInsumos.map(insumo => (
                            <SelectItem key={insumo.id} value={insumo.id}>
                              {insumo.nombre}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label>Cantidad necesaria</Label>
                      <Input
                        type="number"
                        step="0.01"
                        value={item.cantidad_necesaria}
                        onChange={(e) => handleInsumoChange(index, 'cantidad_necesaria', e.target.value)}
                        placeholder="0.00"
                      />
                    </div>
                    <div className="flex items-end">
                      <Button
                        type="button"
                        onClick={() => handleRemoveInsumo(index)}
                        variant="outline"
                        size="sm"
                        className="text-red-600 hover:text-red-700"
                      >
                        <MinusCircle className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>

              {/* Calculated Information */}
              {calculatedInfo.cogs && (
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h3 className="text-lg font-semibold mb-3 flex items-center">
                    <Calculator className="w-5 h-5 mr-2" />
                    Información Calculada
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <Label className="text-sm text-gray-600">COGS (Costo de Producción)</Label>
                      <p className="text-lg font-semibold text-blue-600">
                        ${calculatedInfo.cogs.toFixed(2)}
                      </p>
                    </div>
                    {calculatedInfo.precio_sugerido && (
                      <div>
                        <Label className="text-sm text-gray-600">Precio Sugerido</Label>
                        <p className="text-lg font-semibold text-green-600">
                          ${calculatedInfo.precio_sugerido.toFixed(2)}
                        </p>
                      </div>
                    )}
                    {calculatedInfo.margen_ganancia_real && (
                      <div>
                        <Label className="text-sm text-gray-600">Margen Real</Label>
                        <p className="text-lg font-semibold text-purple-600">
                          {calculatedInfo.margen_ganancia_real.toFixed(1)}%
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Submit Buttons */}
              <div className="flex justify-end space-x-4 pt-6 border-t">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => navigate('/dashboard/products')}
                >
                  Cancelar
                </Button>
                <Button
                  type="submit"
                  disabled={isSubmitting}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  {isSubmitting ? 'Creando...' : 'Crear Producto'}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default CreateProductScreen; 