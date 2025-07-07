// frontend/src/screens/EditProductScreen.js
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { getProductById, updateProduct } from '../api/productApi'; // Importar funciones API de producto
import { getMyBusinesses } from '../api/businessApi'; // Para obtener la lista de negocios
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card.jsx';
import { Label } from '../components/ui/label.jsx';
import { Input } from '../components/ui/input.jsx';
import { Textarea } from '../components/ui/textarea.jsx';
import { Button } from '../components/ui/button.jsx';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../components/ui/select.jsx';

const EditProductScreen = () => {
  const { id } = useParams(); // Obtiene el ID del producto de la URL
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    tipo_producto: '',
    fotos_urls: [''],
    stock: '',
    unidad_medida: '',
    atributos_especificos: '', // JSON string
    negocio_id: '',
    precio_sugerido: '',
    margen_ganancia_porcentaje: '',
  });
  const [loading, setLoading] = useState(true); // Estado de carga inicial para obtener datos
  const [submitting, setSubmitting] = useState(false); // Estado de carga para el envío del formulario
  const [error, setError] = useState(null);
  const [businesses, setBusinesses] = useState([]); // Para la lista de negocios del usuario

  // Cargar datos del producto y negocios al montar el componente
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // Cargar negocios primero
        const userBusinesses = await getMyBusinesses();
        setBusinesses(userBusinesses);

        // Cargar datos del producto
        const productData = await getProductById(id);
        setFormData({
          nombre: productData.nombre || '',
          descripcion: productData.descripcion || '',
          tipo_producto: productData.tipo_producto || '',
          fotos_urls: productData.fotos_urls && productData.fotos_urls.length > 0
            ? productData.fotos_urls
            : [''],
          stock: productData.stock !== null ? productData.stock.toString() : '',
          unidad_medida: productData.unidad_medida || '',
          atributos_especificos: productData.atributos_especificos ? JSON.stringify(productData.atributos_especificos, null, 2) : '',
          negocio_id: productData.negocio_id || 'none', // Preseleccionar el negocio si existe
          precio_sugerido: productData.precio_sugerido !== null ? productData.precio_sugerido.toString() : '',
          margen_ganancia_porcentaje: productData.margen_ganancia_porcentaje !== null ? productData.margen_ganancia_porcentaje.toString() : '',
        });
        setError(null);
      } catch (err) {
        console.error("Error al cargar datos:", err);
        setError(err.message || "No se pudo cargar la información del producto/servicio.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]); // Dependencia del ID para recargar si cambia

  // Maneja cambios en los campos del formulario
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  // Maneja cambios en el Select de tipo_producto
  const handleSelectChange = (value) => {
    setFormData((prevData) => ({
      ...prevData,
      tipo_producto: value,
      // Limpiar stock si el tipo de producto cambia y no es físico
      ...(value !== 'bien_fisico' && { stock: '' }),
    }));
  };

  // Maneja cambios en los campos de fotos_urls (para múltiples inputs)
  const handlePhotoUrlChange = (index, e) => {
    const newFotosUrls = [...formData.fotos_urls];
    newFotosUrls[index] = e.target.value;
    setFormData((prevData) => ({
      ...prevData,
      fotos_urls: newFotosUrls,
    }));
  };

  // Añade un nuevo campo de URL de foto
  const addPhotoUrlField = () => {
    setFormData((prevData) => ({
      ...prevData,
      fotos_urls: [...prevData.fotos_urls, ''],
    }));
  };

  // Elimina un campo de URL de foto
  const removePhotoUrlField = (index) => {
    const newFotosUrls = formData.fotos_urls.filter((_, i) => i !== index);
    setFormData((prevData) => ({
      ...prevData,
      fotos_urls: newFotosUrls,
    }));
  };

  // Maneja el envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    // Filtrar URLs vacías y convertir stock/precio/margen a número
    const payload = {
      ...formData,
      fotos_urls: formData.fotos_urls.filter(url => url.trim() !== ''),
      stock: formData.stock ? parseInt(formData.stock, 10) : null,
      precio_sugerido: formData.precio_sugerido ? parseFloat(formData.precio_sugerido) : null,
      margen_ganancia_porcentaje: formData.margen_ganancia_porcentaje ? parseFloat(formData.margen_ganancia_porcentaje) : null,
      // Convertir atributos_especificos a objeto JSON si no está vacío
      atributos_especificos: formData.atributos_especificos ? JSON.parse(formData.atributos_especificos) : null,
      // Si negocio_id es una cadena vacía, enviarlo como null
      negocio_id: formData.negocio_id === "none" ? null : formData.negocio_id,
    };

    try {
      await updateProduct(id, payload);
      alert('Producto/Servicio actualizado exitosamente!'); // Usar alert temporalmente
      navigate('/dashboard/products'); // Redirige a la lista de productos
    } catch (err) {
      console.error("Error al actualizar producto/servicio:", err);
      setError(err.message || "Error al actualizar el producto/servicio. Inténtalo de nuevo.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-gray-800 dark:text-gray-200">Cargando datos del producto/servicio...</p>
      </div>
    );
  }

  if (error && !loading) {
    return (
      <div className="flex flex-col justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-red-500 text-center mb-4">{error}</p>
        <Button onClick={() => navigate('/dashboard/products')}>Volver a Productos</Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 max-w-2xl mt-8">
      <Card className="rounded-xl shadow-lg p-6 space-y-6">
        <CardHeader>
          <CardTitle className="text-3xl font-bold text-center">Editar Producto/Servicio</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="nombre">Nombre del Producto/Servicio</Label>
              <Input
                id="nombre"
                name="nombre"
                value={formData.nombre}
                onChange={handleChange}
                required
              />
            </div>
            <div>
              <Label htmlFor="tipo_producto">Tipo de Producto/Servicio</Label>
              <Select name="tipo_producto" value={formData.tipo_producto} onValueChange={handleSelectChange} required>
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona el tipo" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="servicio_por_hora">Servicio por Hora</SelectItem>
                  <SelectItem value="servicio_por_proyecto">Servicio por Proyecto</SelectItem>
                  <SelectItem value="bien_fisico">Bien Físico</SelectItem>
                  <SelectItem value="bien_digital">Bien Digital</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="descripcion">Descripción (Opcional)</Label>
              <Textarea
                id="descripcion"
                name="descripcion"
                value={formData.descripcion}
                onChange={handleChange}
                rows="4"
              />
            </div>
            
            {/* Campos condicionales basados en tipo_producto */}
            {formData.tipo_producto === 'bien_fisico' && (
              <div>
                <Label htmlFor="stock">Stock (Sólo para Bien Físico)</Label>
                <Input
                  id="stock"
                  name="stock"
                  type="number"
                  value={formData.stock}
                  onChange={handleChange}
                  min="0"
                />
              </div>
            )}

            {formData.tipo_producto !== '' && (
              <div>
                <Label htmlFor="unidad_medida">Unidad de Medida (Ej: unidad, hora, proyecto, GB)</Label>
                <Input
                  id="unidad_medida"
                  name="unidad_medida"
                  value={formData.unidad_medida}
                  onChange={handleChange}
                />
              </div>
            )}

            <div>
              <Label htmlFor="precio_sugerido">Precio Sugerido (Opcional)</Label>
              <Input
                id="precio_sugerido"
                name="precio_sugerido"
                type="number"
                step="0.01"
                value={formData.precio_sugerido}
                onChange={handleChange}
                min="0"
              />
            </div>

            <div>
              <Label htmlFor="margen_ganancia_porcentaje">Margen de Ganancia (%) (Opcional)</Label>
              <Input
                id="margen_ganancia_porcentaje"
                name="margen_ganancia_porcentaje"
                type="number"
                step="0.01"
                value={formData.margen_ganancia_porcentaje}
                onChange={handleChange}
                min="0"
                max="100"
              />
            </div>

            <div>
              <Label htmlFor="negocio_id">Asociar a un Negocio (Opcional)</Label>
              <Select
                name="negocio_id"
                value={formData.negocio_id}
                onValueChange={(value) => setFormData(prev => ({ ...prev, negocio_id: value }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona un negocio" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">Ninguno</SelectItem> {/* Opción para no asociar */}
                  {businesses.map(business => (
                    <SelectItem key={business.id} value={business.id}>
                      {business.nombre}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {businesses.length === 0 && (
                <p className="text-sm text-gray-500 mt-1">No tienes negocios creados. Puedes crear uno <Link to="/dashboard/businesses/new" className="text-blue-500 hover:underline">aquí</Link>.</p>
              )}
            </div>

            <div>
              <Label htmlFor="atributos_especificos">Atributos Específicos (JSON, Opcional)</Label>
              <Textarea
                id="atributos_especificos"
                name="atributos_especificos"
                value={formData.atributos_especificos}
                onChange={handleChange}
                rows="4"
                placeholder='Ej: {"color": "rojo", "material": "madera"}'
              />
              <p className="text-sm text-gray-500 mt-1">Introduce un objeto JSON válido (ej. {'{"key": "value"}'}).</p>
            </div>

            {/* Campos para fotos_urls */}
            <div>
              <Label>URLs de Fotos (Opcional)</Label>
              {formData.fotos_urls.map((url, index) => (
                <div key={index} className="flex items-center space-x-2 mb-2">
                  <Input
                    type="url"
                    placeholder={`URL de Foto ${index + 1}`}
                    value={url}
                    onChange={(e) => handlePhotoUrlChange(index, e)}
                  />
                  {(formData.fotos_urls.length > 1 || url.trim() !== '') && (
                    <Button
                      type="button"
                      variant="destructive"
                      onClick={() => removePhotoUrlField(index)}
                      className="shrink-0"
                    >
                      Eliminar
                    </Button>
                  )}
                </div>
              ))}
              <Button type="button" variant="outline" onClick={addPhotoUrlField} className="mt-2 w-full">
                Añadir otra URL de Foto
              </Button>
            </div>

            {error && <p className="text-red-500 text-sm mt-2">{error}</p>}

            <Button type="submit" className="w-full" disabled={submitting}>
              {submitting ? 'Actualizando...' : 'Actualizar Producto/Servicio'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default EditProductScreen;
