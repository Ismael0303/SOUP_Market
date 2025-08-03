// src/screens/ProfileScreen.js
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { updateMyProfile, updateMyCv } from '../api/authApi'; // Importar la función de actualización
import {
  Card, CardContent, CardDescription, CardHeader, CardTitle
} from '../components/ui/card.jsx';
import { Button } from '../components/ui/button.jsx';
import { Input } from '../components/ui/input.jsx';
import { Label } from '../components/ui/label.jsx';
import { Textarea } from '../components/ui/textarea.jsx'; // Shadcn Textarea for CV

function ProfileScreen() {
  const { user, loading, error, setUser, setError } = useAuth(); // Obtener user, funciones y el setter de user
  const [nombre, setNombre] = useState('');
  const [localizacion, setLocalizacion] = useState('');
  const [infoContacto, setInfoContacto] = useState({});
  const [cvData, setCvData] = useState({}); // Para el CV del freelancer
  const [isEditing, setIsEditing] = useState(false);
  const [saveLoading, setSaveLoading] = useState(false);

  // Cargar los datos del usuario cuando el componente se monta o el usuario cambia
  useEffect(() => {
    if (user) {
      setNombre(user.nombre || '');
      setLocalizacion(user.localizacion || '');
      setInfoContacto(user.info_contacto || {});
      setCvData(user.curriculum_vitae || {}); // Cargar CV
    }
  }, [user]);

  const handleInfoContactoChange = (key, value) => {
    setInfoContacto(prev => ({ ...prev, [key]: value }));
  };

  const handleCvDataChange = (key, value) => {
    setCvData(prev => ({ ...prev, [key]: value }));
  };

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    setSaveLoading(true);
    setError(null); // Limpiar errores
    try {
      const updatedProfileData = {
        nombre,
        localizacion,
        info_contacto: infoContacto,
      };
      // Aquí el token se obtiene del contexto, que useAuth ya lo maneja internamente
      const updatedUser = await updateMyProfile(localStorage.getItem('token'), updatedProfileData);
      setUser(updatedUser); // Actualizar el usuario en el contexto
      setIsEditing(false); // Salir del modo edición
    } catch (err) {
      setError(err.message || 'Error al guardar el perfil.');
      console.error('Failed to update profile:', err);
    } finally {
      setSaveLoading(false);
    }
  };

  const handleSaveCv = async (e) => {
    e.preventDefault();
    setSaveLoading(true);
    setError(null); // Limpiar errores
    try {
      const updatedUser = await updateMyCv(localStorage.getItem('token'), cvData);
      setUser(updatedUser); // Actualizar el usuario en el contexto
      setIsEditing(false); // Salir del modo edición
    } catch (err) {
      setError(err.message || 'Error al guardar el CV.');
      console.error('Failed to update CV:', err);
    } finally {
      setSaveLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-gray-800 dark:text-gray-200">Cargando perfil...</p>
      </div>
    );
  }

  if (!user) {
    // Esto no debería ocurrir si AuthContext redirige a login, pero es una salvaguarda
    return (
      <div className="flex justify-center items-center h-screen bg-gray-100 dark:bg-gray-900">
        <p className="text-red-600">No se pudo cargar el perfil. Por favor, inicia sesión.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 max-w-2xl mt-8">
      <Card className="rounded-xl shadow-lg p-6 space-y-6">
        <CardHeader>
          <CardTitle className="text-3xl font-bold">Perfil de Usuario</CardTitle>
          <CardDescription className="text-gray-600 dark:text-gray-400">
            Gestiona la información de tu cuenta.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {error && <p className="text-red-600 text-sm text-center">{error}</p>}

          <form onSubmit={handleSaveProfile} className="space-y-4">
            {/* Campos de Perfil General */}
            <div>
              <Label htmlFor="nombre">Nombre</Label>
              <Input
                id="nombre"
                type="text"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                disabled={!isEditing}
                className="mt-1 block w-full rounded-md"
              />
            </div>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={user.email} // Email no editable directamente desde aquí por seguridad
                disabled
                className="mt-1 block w-full rounded-md bg-gray-100 dark:bg-gray-700"
              />
            </div>
            <div>
              <Label htmlFor="localizacion">Localización</Label>
              <Input
                id="localizacion"
                type="text"
                value={localizacion}
                onChange={(e) => setLocalizacion(e.target.value)}
                disabled={!isEditing}
                className="mt-1 block w-full rounded-md"
              />
            </div>

            {/* Información de Contacto */}
            <h3 className="text-xl font-semibold mt-6">Información de Contacto</h3>
            <div>
              <Label htmlFor="telefono">Teléfono</Label>
              <Input
                id="telefono"
                type="text"
                value={infoContacto.telefono || ''}
                onChange={(e) => handleInfoContactoChange('telefono', e.target.value)}
                disabled={!isEditing}
                className="mt-1 block w-full rounded-md"
              />
            </div>
            <div>
              <Label htmlFor="whatsapp">WhatsApp</Label>
              <Input
                id="whatsapp"
                type="text"
                value={infoContacto.whatsapp || ''}
                onChange={(e) => handleInfoContactoChange('whatsapp', e.target.value)}
                disabled={!isEditing}
                className="mt-1 block w-full rounded-md"
              />
            </div>
            <div>
              <Label htmlFor="instagram">Instagram</Label>
              <Input
                id="instagram"
                type="text"
                value={infoContacto.instagram || ''}
                onChange={(e) => handleInfoContactoChange('instagram', e.target.value)}
                disabled={!isEditing}
                className="mt-1 block w-full rounded-md"
              />
            </div>

            {isEditing && (
              <Button type="submit" className="w-full mt-4" disabled={saveLoading}>
                {saveLoading ? 'Guardando perfil...' : 'Guardar Cambios del Perfil'}
              </Button>
            )}
          </form>

          {/* Sección de CV para Freelancers */}
          {user.tipo_tier === 'freelancer' && (
            <>
              <h3 className="text-xl font-semibold mt-6">Curriculum Vitae</h3>
              <form onSubmit={handleSaveCv} className="space-y-4">
                <div>
                  <Label htmlFor="educacion">Educación</Label>
                  <Textarea
                    id="educacion"
                    value={cvData.educacion || ''}
                    onChange={(e) => handleCvDataChange('educacion', e.target.value)}
                    disabled={!isEditing}
                    className="mt-1 block w-full rounded-md min-h-[100px]"
                    placeholder="Ej: Licenciatura en Diseño Gráfico, Universidad X (2015-2019)"
                  />
                </div>
                <div>
                  <Label htmlFor="experiencia_laboral">Experiencia Laboral</Label>
                  <Textarea
                    id="experiencia_laboral"
                    value={cvData.experiencia_laboral || ''}
                    onChange={(e) => handleCvDataChange('experiencia_laboral', e.target.value)}
                    disabled={!isEditing}
                    className="mt-1 block w-full rounded-md min-h-[150px]"
                    placeholder="Ej: Diseñador Senior en Agencia Y (2020-Presente), Freelancer (2019-2020)"
                  />
                </div>
                <div>
                  <Label htmlFor="conocimientos_habilidades">Conocimientos y Habilidades</Label>
                  <Textarea
                    id="conocimientos_habilidades"
                    value={cvData.conocimientos_habilidades || ''}
                    onChange={(e) => handleCvDataChange('conocimientos_habilidades', e.target.value)}
                    disabled={!isEditing}
                    className="mt-1 block w-full rounded-md min-h-[100px]"
                    placeholder="Ej: Photoshop, Illustrator, UI/UX Design, Figma, Comunicación Efectiva, Gestión de Proyectos"
                  />
                </div>
                {isEditing && (
                  <Button type="submit" className="w-full mt-4" disabled={saveLoading}>
                    {saveLoading ? 'Guardando CV...' : 'Guardar Cambios del CV'}
                  </Button>
                )}
              </form>
            </>
          )}

          {/* Botón para activar/desactivar edición */}
          <Button onClick={() => setIsEditing(!isEditing)} className="w-full mt-6 bg-blue-500 hover:bg-blue-600 text-white">
            {isEditing ? 'Cancelar Edición' : 'Editar Perfil'}
          </Button>

          {/* Mostrar tipo de tier */}
          <p className="text-center text-sm text-gray-500 mt-4">
            Tipo de cuenta: <span className="font-semibold">{user.tipo_tier}</span>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

export default ProfileScreen;
