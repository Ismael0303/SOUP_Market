// frontend/src/screens/CreateInsumoScreen.js

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import insumoApi from '../api/insumoApi';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import Breadcrumbs from '../components/Breadcrumbs';
import { useNotification } from '../context/NotificationContext';

const CreateInsumoScreen = () => {
  const { isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    nombre: '',
    cantidad_disponible: '',
    unidad_medida_compra: '',
    costo_unitario_compra: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const { showNotification } = useNotification();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, loading, navigate]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const validate = () => {
    let isValid = true;
    if (!formData.nombre) {
      setError('El nombre del insumo es obligatorio.');
      isValid = false;
    } else {
      setError(null);
    }
    if (!formData.cantidad_disponible) {
      setError('La cantidad disponible es obligatoria.');
      isValid = false;
    } else {
      setError(null);
    }
    if (!formData.unidad_medida_compra) {
      setError('La unidad de medida de compra es obligatoria.');
      isValid = false;
    } else {
      setError(null);
    }
    if (!formData.costo_unitario_compra) {
      setError('El costo unitario de compra es obligatorio.');
      isValid = false;
    } else {
      setError(null);
    }
    return isValid;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) {
      showNotification('Por favor corrige los errores del formulario.', 'error');
      return;
    }
    setIsSubmitting(true);
    setError(null);
    setSuccessMessage(null);

    try {
      // Convertir valores numéricos a tipo correcto
      const dataToSend = {
        ...formData,
        cantidad_disponible: parseFloat(formData.cantidad_disponible),
        costo_unitario_compra: parseFloat(formData.costo_unitario_compra),
      };

      await insumoApi.createInsumo(dataToSend);
      setSuccessMessage('Insumo creado exitosamente!');
      showNotification('Insumo creado correctamente', 'success');
      // Opcional: Redirigir a la lista de insumos después de un breve retraso
      setTimeout(() => {
        navigate('/dashboard/insumos');
      }, 2000);
    } catch (err) {
      console.error('Error al crear insumo:', err);
      const errorMessage = err.response?.data?.detail || 'Error al crear el insumo. Por favor, verifica los datos.';
      setError(errorMessage);
      showNotification(errorMessage, 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading || !isAuthenticated) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-gray-800 dark:text-gray-200">Cargando...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex bg-gray-100">
      {/* Sidebar de navegación */}
      <main className="flex-1 max-w-4xl mx-auto w-full p-4 sm:p-8">
        <Breadcrumbs items={[
          { label: 'Dashboard', to: '/dashboard' },
          { label: 'Insumos', to: '/dashboard/insumos' },
          { label: 'Crear Insumo' }
        ]} />
        <Card className="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-center">Crear Nuevo Insumo</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="nombre">Nombre del Insumo</Label>
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
                <Label htmlFor="cantidad_disponible">Cantidad Disponible</Label>
                <Input
                  id="cantidad_disponible"
                  name="cantidad_disponible"
                  type="number"
                  step="0.01"
                  value={formData.cantidad_disponible}
                  onChange={handleChange}
                  required
                  className="mt-1"
                />
              </div>
              <div>
                <Label htmlFor="unidad_medida_compra">Unidad de Medida de Compra</Label>
                <Input
                  id="unidad_medida_compra"
                  name="unidad_medida_compra"
                  type="text"
                  value={formData.unidad_medida_compra}
                  onChange={handleChange}
                  required
                  className="mt-1"
                />
              </div>
              <div>
                <Label htmlFor="costo_unitario_compra">Costo Unitario de Compra</Label>
                <Input
                  id="costo_unitario_compra"
                  name="costo_unitario_compra"
                  type="number"
                  step="0.01"
                  value={formData.costo_unitario_compra}
                  onChange={handleChange}
                  required
                  className="mt-1"
                />
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
                {isSubmitting ? 'Creando...' : 'Crear Insumo'}
              </Button>
              <Button
                type="button"
                onClick={() => navigate('/dashboard/insumos')}
                variant="outline"
                className="w-full mt-2 text-gray-600 border-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:border-gray-300 dark:hover:bg-gray-700"
              >
                Cancelar
              </Button>
            </form>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default CreateInsumoScreen; 