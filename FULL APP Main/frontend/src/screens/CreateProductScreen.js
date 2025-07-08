// frontend/src/screens/CreateProductScreen.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import productApi from '../api/productApi';
import insumoApi from '../api/insumoApi';
import businessApi from '../api/businessApi'; // Importar businessApi para obtener negocios
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Textarea } from '../components/ui/textarea';
import { PlusCircle, MinusCircle, Calculator, DollarSign, TrendingUp } from 'lucide-react';

const CreateProductScreen = () => {
  const { isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    precio: '', // Precio base del producto
    tipo_producto: '',
    negocio_id: '',
    precio_venta: '', // Precio de venta final
    margen_ganancia_sugerido: '', // Margen de ganancia sugerido en %
    insumos: [], // Lista de insumos asociados
  });

  const [businesses, setBusinesses] = useState([]);
  const [availableInsumos, setAvailableInsumos] = useState([]);
  const [selectedInsumos, setSelectedInsumos] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoadingData, setIsLoadingData] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  // Estados para mostrar información calculada
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
          // Obtener negocios del usuario
          const businessData = await businessApi.getAllMyBusinesses();
          setBusinesses(businessData);

          // Obtener insumos del usuario
          const insumosData = await insumoApi.getAllMyInsumos();
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

  // Calcular información basada en insumos seleccionados
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
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
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
      // Preparar los insumos para el envío
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
        insumos: insumosToSend,
      };

      console.log("Datos a enviar:", dataToSend);

      const createdProduct = await productApi.createProduct(dataToSend);
      setSuccessMessage('Producto/Servicio creado exitosamente!');
      console.log("Producto creado:", createdProduct);

      // Mostrar información calculada del producto creado
      if (createdProduct) {
        console.log("COGS calculado:", createdProduct.cogs);
        console.log("Precio sugerido:", createdProduct.precio_sugerido);
        console.log("Margen real:", createdProduct.margen_ganancia_real);
      }

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
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-gray-800 dark:text-gray-200">Cargando...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-4 sm:p-6 lg:p-8">
      <div className="max-w-4xl mx-auto">
        <Card className="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-center">Crear Nuevo Producto/Servicio</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Campos básicos del producto */}
              <div>
                <Label htmlFor="nombre">Nombre del Producto/Servicio</Label>
                <Input
                  id="nombre"
                  name="nombre"
                  type="text"
                  value={formData.nombre}
                  onChange={handleChange}
                  required
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="descripcion">Descripción</Label>
                <Textarea
                  id="descripcion"
                  name="descripcion"
                  value={formData.descripcion}
                  onChange={handleChange}
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="precio">Precio Base</Label>
                <Input
                  id="precio"
                  name="precio"
                  type="number"
                  step="0.01"
                  value={formData.precio}
                  onChange={handleChange}
                  required
                  className="mt-1"
                />
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  Precio base del producto o servicio.
                </p>
              </div>

              <div>
                <Label htmlFor="tipo_producto">Tipo de Producto</Label>
                <Select
                  name="tipo_producto"
                  value={formData.tipo_producto}
                  onValueChange={(value) => setFormData((prev) => ({ ...prev, tipo_producto: value }))}
                  required
                >
                  <SelectTrigger className="mt-1">
                    <SelectValue placeholder="Selecciona un tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="producto_fisico">Producto Físico</SelectItem>
                    <SelectItem value="servicio">Servicio</SelectItem>
                    <SelectItem value="producto_digital">Producto Digital</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="negocio_id">Negocio Asociado</Label>
                <Select
                  name="negocio_id"
                  value={formData.negocio_id}
                  onValueChange={(value) => setFormData((prev) => ({ ...prev, negocio_id: value }))}
                  required
                >
                  <SelectTrigger className="mt-1">
                    <SelectValue placeholder="Selecciona un negocio" />
                  </SelectTrigger>
                  <SelectContent>
                    {businesses.map((business) => (
                      <SelectItem key={business.id} value={business.id}>
                        {business.nombre}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Campos de precio y márgenes */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="precio_venta">
                    <DollarSign className="inline w-4 h-4 mr-1" />
                    Precio de Venta Final (Opcional)
                  </Label>
                  <Input
                    id="precio_venta"
                    name="precio_venta"
                    type="number"
                    step="0.01"
                    value={formData.precio_venta}
                    onChange={handleChange}
                    className="mt-1"
                    placeholder="Ej: 150.00"
                  />
                </div>

                <div>
                  <Label htmlFor="margen_ganancia_sugerido">
                    <TrendingUp className="inline w-4 h-4 mr-1" />
                    Margen de Ganancia Sugerido (%) (Opcional)
                  </Label>
                  <Input
                    id="margen_ganancia_sugerido"
                    name="margen_ganancia_sugerido"
                    type="number"
                    step="0.01"
                    value={formData.margen_ganancia_sugerido}
                    onChange={handleChange}
                    className="mt-1"
                    placeholder="Ej: 20"
                  />
                </div>
              </div>

              {/* Información calculada */}
              {(calculatedInfo.cogs !== null || calculatedInfo.precio_sugerido !== null || calculatedInfo.margen_ganancia_real !== null) && (
                <div className="border p-4 rounded-md bg-blue-50 dark:bg-blue-900/20">
                  <h3 className="text-lg font-semibold mb-3 flex items-center">
                    <Calculator className="w-5 h-5 mr-2" />
                    Información Calculada
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {calculatedInfo.cogs !== null && (
                      <div>
                        <Label className="text-sm font-medium">COGS (Costo de Bienes Vendidos)</Label>
                        <p className="text-lg font-bold text-blue-600 dark:text-blue-400">
                          ${calculatedInfo.cogs.toFixed(2)}
                        </p>
                      </div>
                    )}
                    {calculatedInfo.precio_sugerido !== null && (
                      <div>
                        <Label className="text-sm font-medium">Precio Sugerido</Label>
                        <p className="text-lg font-bold text-green-600 dark:text-green-400">
                          ${calculatedInfo.precio_sugerido.toFixed(2)}
                        </p>
                      </div>
                    )}
                    {calculatedInfo.margen_ganancia_real !== null && (
                      <div>
                        <Label className="text-sm font-medium">Margen de Ganancia Real</Label>
                        <p className={`text-lg font-bold ${calculatedInfo.margen_ganancia_real >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                          {calculatedInfo.margen_ganancia_real.toFixed(2)}%
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Sección de Insumos Asociados */}
              <div className="border p-4 rounded-md bg-gray-50 dark:bg-gray-700">
                <h3 className="text-lg font-semibold mb-3">Insumos Asociados</h3>
                {selectedInsumos.map((insumoItem, index) => (
                  <div key={index} className="flex items-end space-x-2 mb-3">
                    <div className="flex-grow">
                      <Label htmlFor={`insumo-${index}`}>Insumo</Label>
                      <Select
                        value={insumoItem.insumo_id}
                        onValueChange={(value) => handleInsumoChange(index, 'insumo_id', value)}
                      >
                        <SelectTrigger id={`insumo-${index}`}>
                          <SelectValue placeholder="Selecciona un insumo" />
                        </SelectTrigger>
                        <SelectContent>
                          {availableInsumos.map((insumo) => (
                            <SelectItem key={insumo.id} value={insumo.id}>
                              {insumo.nombre} ({insumo.unidad_medida_compra}) - ${insumo.costo_unitario_compra}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="w-24">
                      <Label htmlFor={`cantidad-${index}`}>Cantidad</Label>
                      <Input
                        id={`cantidad-${index}`}
                        type="number"
                        step="0.001"
                        value={insumoItem.cantidad_necesaria}
                        onChange={(e) => handleInsumoChange(index, 'cantidad_necesaria', e.target.value)}
                        placeholder="Ej: 1.5"
                      />
                    </div>
                    <Button
                      type="button"
                      variant="destructive"
                      size="icon"
                      onClick={() => handleRemoveInsumo(index)}
                      className="mt-auto"
                    >
                      <MinusCircle className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
                <Button
                  type="button"
                  variant="outline"
                  onClick={handleAddInsumo}
                  className="w-full mt-2 text-blue-600 border-blue-600 hover:bg-blue-50 dark:hover:bg-gray-700"
                >
                  <PlusCircle className="mr-2 h-4 w-4" /> Añadir Insumo
                </Button>
              </div>

              {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                  <strong className="font-bold">Error:</strong>
                  <span className="block sm:inline"> {error}</span>
                </div>
              )}

              {successMessage && (
                <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
                  <strong className="font-bold">Éxito:</strong>
                  <span className="block sm:inline"> {successMessage}</span>
                </div>
              )}

              <Button
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md shadow-md transition duration-300 ease-in-out"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Creando...' : 'Crear Producto/Servicio'}
              </Button>
              
              <Button
                type="button"
                onClick={() => navigate('/dashboard/products')}
                variant="outline"
                className="w-full mt-2 text-gray-600 border-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:border-gray-300 dark:hover:bg-gray-700"
              >
                Cancelar
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default CreateProductScreen;
