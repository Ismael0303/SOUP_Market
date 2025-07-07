// frontend/src/screens/CreateProductScreen.js
import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { createProduct } from '../api/productApi'; // Importar la función API
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
} from '../components/ui/select.jsx'; // Para el Select de tipo_producto

const CreateProductScreen = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    tipo_producto: '', // Se establecerá con el Select
    fotos_urls: [''],
    stock: '', // Solo para bienes físicos
    unidad_medida: '',
    atributos_especificos: '', // JSON string
    negocio_id: '', // UUID del negocio asociado
    precio_sugerido: '',
    margen_ganancia_porcentaje: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [businesses, setBusinesses] = useState([]); // Para la lista de negocios del usuario

  // Cargar negocios del usuario para el Select de negocio_id
  useEffect(() => {
    const fetchBusinesses = async () => {
      try {
        const userBusinesses = await getMyBusinesses();
        setBusinesses(userBusinesses);
      } catch (err) {
        console.error("Error al cargar negocios para el select:", err);
        // No bloqueamos la creación si no se pueden cargar los negocios
      }
    };
    fetchBusinesses();
  }, []);

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
      // Limpiar stock/unidad_medida si el tipo de producto cambia
      ...(value !== 'bien_fisico' && { stock: '' }),
      ...(value === 'bien_fisico' && { unidad_medida: '' }), // Unidad de medida es más flexible, pero puede limpiarse si no aplica
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
    setLoading(true);
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
     // Si negocio_id es "none", enviarlo como null
      negocio_id: formData.negocio_id === "none" ? null : formData.negocio_id, // <--- CAMBIO AQUÍ
    };
    
    try {
      await createProduct(payload);
      alert('Producto/Servicio creado exitosamente!'); // Usar alert temporalmente
      navigate('/dashboard/products'); // Redirige a la lista de productos
    } catch (err) {
      console.error("Error al crear producto/servicio:", err);
      setError(err.message || "Error al crear el producto/servicio. Inténtalo de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-2xl mt-8">
      <Card className="rounded-xl shadow-lg p-6 space-y-6">
        <CardHeader>
          <CardTitle className="text-3xl font-bold text-center">Crear Nuevo Producto/Servicio</CardTitle>
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

            {formData.tipo_producto !== '' && ( // Mostrar si se ha seleccionado un tipo
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

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Creando...' : 'Crear Producto/Servicio'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default CreateProductScreen;
