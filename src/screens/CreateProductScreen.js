// CreateProductScreen.js - Actualizado según mockups Gemini
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
  Search,
  ArrowLeft,
  Save,
  AlertCircle,
  CheckCircle
} from 'lucide-react';
import { showSuccess, showError, showInfo } from '../utils/notifications';

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

  // Categorías predefinidas
  const categories = [
    'Panadería', 'Bebidas', 'Fiambres', 'Lácteos', 'Limpieza', 'Snacks',
    'Servicios', 'Otros'
  ];

  // Tipos de producto
  const productTypes = [
    'producto_fisico', 'servicio', 'digital'
  ];

  // Unidades de venta
  const units = [
    'unidad', 'kg', 'litro', 'metro', 'hora', 'sesion'
  ];

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
          showError('Error cargando datos iniciales');
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
      showSuccess('Producto creado exitosamente');

      setTimeout(() => {
        navigate('/dashboard/products');
      }, 2000);
    } catch (err) {
      console.error('Error al crear producto:', err);
      const errorMessage = err.response?.data?.detail || 'Error al crear el producto/servicio. Por favor, verifica los datos.';
      setError(errorMessage);
      showError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-AR', { 
      style: 'currency', 
      currency: 'ARS', 
      minimumFractionDigits: 2 
    }).format(amount);
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
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/dashboard/products')}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-5 h-5 text-gray-600" />
            </button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Crear Producto/Servicio</h1>
              <p className="text-gray-600">Agrega un nuevo producto o servicio a tu catálogo</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Package className="w-6 h-6 text-blue-600" />
            <span className="text-sm text-gray-600">Nuevo Producto</span>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Formulario Principal */}
          <div className="lg:col-span-2 space-y-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Información Básica */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Package className="w-5 h-5" />
                    <span>Información Básica</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="nombre">Nombre del Producto *</Label>
                      <Input
                        id="nombre"
                        name="nombre"
                        value={formData.nombre}
                        onChange={handleChange}
                        placeholder="Ej: Pan de Molde Integral"
                        required
                        className="mt-1"
                      />
                    </div>
                    <div>
                      <Label htmlFor="categoria">Categoría</Label>
                      <Select
                        value={formData.categoria}
                        onValueChange={(value) => setFormData({...formData, categoria: value})}
                      >
                        <SelectTrigger className="mt-1">
                          <SelectValue placeholder="Selecciona una categoría" />
                        </SelectTrigger>
                        <SelectContent>
                          {categories.map(category => (
                            <SelectItem key={category} value={category}>
                              {category}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="descripcion">Descripción</Label>
                    <Textarea
                      id="descripcion"
                      name="descripcion"
                      value={formData.descripcion}
                      onChange={handleChange}
                      placeholder="Describe tu producto o servicio..."
                      rows={3}
                      className="mt-1"
                    />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <Label htmlFor="tipo_producto">Tipo de Producto *</Label>
                      <Select
                        value={formData.tipo_producto}
                        onValueChange={(value) => setFormData({...formData, tipo_producto: value})}
                      >
                        <SelectTrigger className="mt-1">
                          <SelectValue placeholder="Selecciona el tipo" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="producto_fisico">Producto Físico</SelectItem>
                          <SelectItem value="servicio">Servicio</SelectItem>
                          <SelectItem value="digital">Producto Digital</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label htmlFor="unidad_venta">Unidad de Venta</Label>
                      <Select
                        value={formData.unidad_venta}
                        onValueChange={(value) => setFormData({...formData, unidad_venta: value})}
                      >
                        <SelectTrigger className="mt-1">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {units.map(unit => (
                            <SelectItem key={unit} value={unit}>
                              {unit.charAt(0).toUpperCase() + unit.slice(1)}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label htmlFor="negocio_id">Negocio *</Label>
                      <Select
                        value={formData.negocio_id}
                        onValueChange={(value) => setFormData({...formData, negocio_id: value})}
                      >
                        <SelectTrigger className="mt-1">
                          <SelectValue placeholder="Selecciona tu negocio" />
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
                </CardContent>
              </Card>

              {/* Precios y Costos */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <DollarSign className="w-5 h-5" />
                    <span>Precios y Costos</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="precio">Precio de Costo *</Label>
                      <Input
                        id="precio"
                        name="precio"
                        type="number"
                        step="0.01"
                        value={formData.precio}
                        onChange={handleChange}
                        placeholder="0.00"
                        required
                        className="mt-1"
                      />
                    </div>
                    <div>
                      <Label htmlFor="precio_venta">Precio de Venta</Label>
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
                  </div>

                  <div>
                    <Label htmlFor="margen_ganancia_sugerido">Margen de Ganancia Sugerido (%)</Label>
                    <Input
                      id="margen_ganancia_sugerido"
                      name="margen_ganancia_sugerido"
                      type="number"
                      step="0.1"
                      value={formData.margen_ganancia_sugerido}
                      onChange={handleChange}
                      placeholder="30"
                      className="mt-1"
                    />
                  </div>
                </CardContent>
              </Card>

              {/* Stock e Inventario */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <BarChart3 className="w-5 h-5" />
                    <span>Stock e Inventario</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="stock_terminado">Stock Actual</Label>
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
                      <Label htmlFor="stock_minimo">Stock Mínimo</Label>
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
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="flex items-center space-x-2">
                      <input
                        id="es_perecedero"
                        name="es_perecedero"
                        type="checkbox"
                        checked={formData.es_perecedero}
                        onChange={handleChange}
                        className="rounded"
                      />
                      <Label htmlFor="es_perecedero">Es Perecedero</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <input
                        id="requiere_refrigeracion"
                        name="requiere_refrigeracion"
                        type="checkbox"
                        checked={formData.requiere_refrigeracion}
                        onChange={handleChange}
                        className="rounded"
                      />
                      <Label htmlFor="requiere_refrigeracion">Requiere Refrigeración</Label>
                    </div>
                  </div>

                  {formData.es_perecedero && (
                    <div>
                      <Label htmlFor="tiempo_vida_util">Tiempo de Vida Útil (días)</Label>
                      <Input
                        id="tiempo_vida_util"
                        name="tiempo_vida_util"
                        type="number"
                        value={formData.tiempo_vida_util}
                        onChange={handleChange}
                        placeholder="7"
                        className="mt-1"
                      />
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Insumos */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <ShoppingCart className="w-5 h-5" />
                    <span>Insumos Necesarios</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {selectedInsumos.map((item, index) => (
                    <div key={index} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                      <div className="flex-1">
                        <Select
                          value={item.insumo_id}
                          onValueChange={(value) => handleInsumoChange(index, 'insumo_id', value)}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Selecciona un insumo" />
                          </SelectTrigger>
                          <SelectContent>
                            {availableInsumos.map(insumo => (
                              <SelectItem key={insumo.id} value={insumo.id}>
                                {insumo.nombre} - {formatCurrency(insumo.costo_unitario_compra)}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="w-32">
                        <Input
                          type="number"
                          step="0.01"
                          placeholder="Cantidad"
                          value={item.cantidad_necesaria}
                          onChange={(e) => handleInsumoChange(index, 'cantidad_necesaria', e.target.value)}
                        />
                      </div>
                      <button
                        type="button"
                        onClick={() => handleRemoveInsumo(index)}
                        className="p-2 text-red-500 hover:text-red-700"
                      >
                        <MinusCircle className="w-5 h-5" />
                      </button>
                    </div>
                  ))}
                  
                  <Button
                    type="button"
                    onClick={handleAddInsumo}
                    variant="outline"
                    className="w-full"
                  >
                    <PlusCircle className="w-4 h-4 mr-2" />
                    Agregar Insumo
                  </Button>
                </CardContent>
              </Card>

              {/* Botones de Acción */}
              <div className="flex justify-end space-x-4">
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
                  {isSubmitting ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Creando...
                    </>
                  ) : (
                    <>
                      <Save className="w-4 h-4 mr-2" />
                      Crear Producto
                    </>
                  )}
                </Button>
              </div>
            </form>
          </div>

          {/* Panel Lateral - Cálculos y Preview */}
          <div className="space-y-6">
            {/* Resumen de Cálculos */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Calculator className="w-5 h-5" />
                  <span>Resumen de Cálculos</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {calculatedInfo.cogs !== null && (
                  <div className="p-3 bg-blue-50 rounded-lg">
                    <div className="text-sm text-blue-600 font-medium">Costo Total (COGS)</div>
                    <div className="text-lg font-bold text-blue-700">
                      {formatCurrency(calculatedInfo.cogs)}
                    </div>
                  </div>
                )}

                {calculatedInfo.precio_sugerido !== null && (
                  <div className="p-3 bg-green-50 rounded-lg">
                    <div className="text-sm text-green-600 font-medium">Precio Sugerido</div>
                    <div className="text-lg font-bold text-green-700">
                      {formatCurrency(calculatedInfo.precio_sugerido)}
                    </div>
                  </div>
                )}

                {calculatedInfo.margen_ganancia_real !== null && (
                  <div className="p-3 bg-purple-50 rounded-lg">
                    <div className="text-sm text-purple-600 font-medium">Margen Real</div>
                    <div className="text-lg font-bold text-purple-700">
                      {calculatedInfo.margen_ganancia_real.toFixed(1)}%
                    </div>
                  </div>
                )}

                {!calculatedInfo.cogs && (
                  <div className="text-center py-4 text-gray-500">
                    <Calculator className="w-8 h-8 mx-auto mb-2 text-gray-300" />
                    <p className="text-sm">Agrega insumos para ver los cálculos</p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Validaciones */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <CheckCircle className="w-5 h-5" />
                  <span>Validaciones</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className={`flex items-center space-x-2 text-sm ${
                  formData.nombre ? 'text-green-600' : 'text-gray-400'
                }`}>
                  {formData.nombre ? <CheckCircle className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
                  <span>Nombre del producto</span>
                </div>
                <div className={`flex items-center space-x-2 text-sm ${
                  formData.tipo_producto ? 'text-green-600' : 'text-gray-400'
                }`}>
                  {formData.tipo_producto ? <CheckCircle className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
                  <span>Tipo de producto</span>
                </div>
                <div className={`flex items-center space-x-2 text-sm ${
                  formData.negocio_id ? 'text-green-600' : 'text-gray-400'
                }`}>
                  {formData.negocio_id ? <CheckCircle className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
                  <span>Negocio seleccionado</span>
                </div>
                <div className={`flex items-center space-x-2 text-sm ${
                  formData.precio ? 'text-green-600' : 'text-gray-400'
                }`}>
                  {formData.precio ? <CheckCircle className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
                  <span>Precio de costo</span>
                </div>
              </CardContent>
            </Card>

            {/* Mensajes de Estado */}
            {error && (
              <Card className="border-red-200 bg-red-50">
                <CardContent className="pt-6">
                  <div className="flex items-center space-x-2 text-red-600">
                    <AlertCircle className="w-5 h-5" />
                    <span className="font-medium">Error</span>
                  </div>
                  <p className="text-red-600 text-sm mt-2">{error}</p>
                </CardContent>
              </Card>
            )}

            {successMessage && (
              <Card className="border-green-200 bg-green-50">
                <CardContent className="pt-6">
                  <div className="flex items-center space-x-2 text-green-600">
                    <CheckCircle className="w-5 h-5" />
                    <span className="font-medium">Éxito</span>
                  </div>
                  <p className="text-green-600 text-sm mt-2">{successMessage}</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateProductScreen; 