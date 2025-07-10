// frontend/src/screens/EditBusinessScreen.js
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getBusinessById, updateBusiness } from '../api/businessApi'; // Importar funciones API
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card.jsx';
import { Label } from '../components/ui/label.jsx';
import { Input } from '../components/ui/input.jsx';
import { Textarea } from '../components/ui/textarea.jsx';
import { Button } from '../components/ui/button.jsx';

const EditBusinessScreen = () => {
  const { id } = useParams(); // Obtiene el ID del negocio de la URL
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    nombre: '',
    rubro: '',
    descripcion: '',
    localizacion_geografica: '',
    fotos_urls: [''],
  });
  const [loading, setLoading] = useState(true); // Estado de carga inicial para obtener datos
  const [submitting, setSubmitting] = useState(false); // Estado de carga para el envío del formulario
  const [error, setError] = useState(null);

  // useEffect para cargar los datos del negocio cuando el componente se monta
  useEffect(() => {
    const fetchBusiness = async () => {
      try {
        setLoading(true);
        const businessData = await getBusinessById(id);
        setFormData({
          nombre: businessData.nombre || '',
          rubro: businessData.rubro || '',
          descripcion: businessData.descripcion || '',
          localizacion_geografica: businessData.localizacion_geografica || '',
          // Asegúrate de que fotos_urls sea un array, incluso si está vacío o nulo
          fotos_urls: businessData.fotos_urls && businessData.fotos_urls.length > 0
            ? businessData.fotos_urls
            : [''], // Inicializa con un campo vacío si no hay URLs
        });
        setError(null);
      } catch (err) {
        console.error("Error al cargar el negocio:", err);
        setError(err.message || "No se pudo cargar la información del negocio.");
      } finally {
        setLoading(false);
      }
    };

    fetchBusiness();
  }, [id]); // Dependencia del ID para recargar si cambia

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
    setSubmitting(true);
    setError(null);

    // Filtra las URLs vacías antes de enviar
    const filteredFotosUrls = formData.fotos_urls.filter(url => url.trim() !== '');

    try {
      await updateBusiness(id, { ...formData, fotos_urls: filteredFotosUrls });
      navigate('/dashboard/businesses'); // Redirige a la lista de negocios
    } catch (err) {
      console.error("Error al actualizar negocio:", err);
      setError(err.message || "Error al actualizar el negocio. Inténtalo de nuevo.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-gray-800 dark:text-gray-200">Cargando datos del negocio...</p>
      </div>
    );
  }

  if (error && !loading) { // Muestra el error si no está cargando
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-red-500 text-center">{error}</p>
        <Button onClick={() => navigate('/dashboard/businesses')} className="ml-4">Volver a Negocios</Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 max-w-2xl mt-8">
      <Card className="rounded-xl shadow-lg p-6 space-y-6">
        <CardHeader>
          <CardTitle className="text-3xl font-bold text-center">Editar Negocio</CardTitle>
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
                  {/* Solo permite eliminar si hay más de un campo o si el campo actual no está vacío */}
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
              {submitting ? 'Actualizando...' : 'Actualizar Negocio'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default EditBusinessScreen;
