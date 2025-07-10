// frontend/src/screens/CreateBusinessScreen.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createBusiness } from '../api/businessApi'; // Importar la función API
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card.jsx';
import { Label } from '../components/ui/label.jsx';
import { Input } from '../components/ui/input.jsx';
import { Textarea } from '../components/ui/textarea.jsx';
import { Button } from '../components/ui/button.jsx';
// Ya no se importa useToast

const CreateBusinessScreen = () => {
  const [formData, setFormData] = useState({
    nombre: '',
    rubro: '',
    descripcion: '',
    tipo_negocio: '', // Añadido campo obligatorio
    localizacion_geografica: '',
    fotos_urls: [''], // Inicializar con un campo vacío para la primera URL
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  // Ya no se inicializa toast

  // Maneja cambios en los campos del formulario
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
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

    // Filtra las URLs vacías antes de enviar
    const filteredFotosUrls = formData.fotos_urls.filter(url => url.trim() !== '');

    // Construir el objeto de negocio con los nombres de campo correctos
    const businessData = {
      nombre: formData.nombre,
      rubro: formData.rubro,
      descripcion: formData.descripcion,
      tipo_negocio: formData.tipo_negocio, // Asegurarse de incluirlo
      localizacion_geografica: formData.localizacion_geografica,
      fotos_urls: filteredFotosUrls.length > 0 ? filteredFotosUrls : undefined // Solo enviar si hay URLs
    };

    try {
      await createBusiness(businessData);
      navigate('/dashboard/businesses'); // Redirige a la lista de negocios
    } catch (err) {
      console.error("Error al crear negocio:", err);
      setError(err.message || "Error al crear el negocio. Inténtalo de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-2xl mt-8">
      <Card className="rounded-xl shadow-lg p-6 space-y-6">
        <CardHeader>
          <CardTitle className="text-3xl font-bold text-center">Crear Nuevo Negocio</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="nombre">Nombre del Negocio</Label>
              <Input
                id="nombre"
                name="nombre"
                value={formData.nombre}
                onChange={handleChange}
                required
              />
            </div>
            <div>
              <Label htmlFor="rubro">Rubro (Ej: Joyería, Diseño Gráfico, Comida)</Label>
              <Input
                id="rubro"
                name="rubro"
                value={formData.rubro}
                onChange={handleChange}
                required
              />
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
            <div>
              <Label htmlFor="tipo_negocio">Tipo de Negocio</Label>
              <select
                id="tipo_negocio"
                name="tipo_negocio"
                value={formData.tipo_negocio}
                onChange={handleChange}
                required
                className="w-full border rounded p-2"
              >
                <option value="">Selecciona una opción</option>
                <option value="PRODUCTOS">Productos</option>
                <option value="SERVICIOS">Servicios</option>
                <option value="AMBOS">Ambos</option>
              </select>
            </div>
            <div>
              <Label htmlFor="localizacion_geografica">Localización Geográfica (Opcional)</Label>
              <Input
                id="localizacion_geografica"
                name="localizacion_geografica"
                value={formData.localizacion_geografica}
                onChange={handleChange}
              />
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
                  {formData.fotos_urls.length > 1 && (
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
              {loading ? 'Creando...' : 'Crear Negocio'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default CreateBusinessScreen;
