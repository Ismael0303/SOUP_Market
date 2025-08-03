// src/screens/AuthScreens/RegisterScreen.js
import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext'; // Importa el hook de autenticación
import { Link } from 'react-router-dom'; // Para el enlace a login

// Componentes de Shadcn UI (asegúrate de que estén instalados y configurados)
import { Button } from '../../components/ui/button.jsx';
import { Input } from '../../components/ui/input.jsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card.jsx';
import { Label } from '../../components/ui/label.jsx';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select.jsx'; // Para el tipo de Tier

function RegisterScreen() {
  const { register, loading, error, setError } = useAuth(); // Obtener funciones del contexto
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [tipoTier, setTipoTier] = useState('client'); // Estado para el tipo de tier

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Limpiar errores anteriores al intentar registro
    try {
      await register({ nombre, email, password, tipo_tier: tipoTier });
      // La redirección se maneja dentro de AuthContext en caso de éxito
    } catch (err) {
      console.error('Register failed:', err);
      // El error ya se establece en el AuthContext, aquí solo se loguea
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
      <Card className="w-full max-w-md p-6 space-y-4 rounded-xl shadow-lg">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl font-bold">Únete a SOUP Emprendimientos</CardTitle>
          <CardDescription className="text-gray-600 dark:text-gray-400">
            Crea tu cuenta para empezar a gestionar tu negocio.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="nombre">Nombre</Label>
              <Input
                id="nombre"
                type="text"
                placeholder="Tu Nombre"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              />
            </div>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="tu@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              />
            </div>
            <div>
              <Label htmlFor="password">Contraseña</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              />
            </div>
            <div>
              <Label htmlFor="tipoTier">Tipo de Cuenta</Label>
              {/* Utiliza el componente Select de Shadcn UI */}
              <Select value={tipoTier} onValueChange={setTipoTier}>
                <SelectTrigger className="w-full mt-1">
                  <SelectValue placeholder="Selecciona tu tipo de cuenta" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="client">Cliente</SelectItem>
                  <SelectItem value="freelancer">Freelancer</SelectItem>
                  <SelectItem value="microemprendimiento">Microemprendimiento</SelectItem>
                </SelectContent>
              </Select>
            </div>
            {error && (
              <p className="text-red-600 text-sm text-center">{error}</p>
            )}
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Registrando...' : 'Registrarse'}
            </Button>
          </form>
          <div className="mt-4 text-center text-sm">
            ¿Ya tienes una cuenta?{' '}
            <Link to="/login" className="text-blue-600 hover:underline">
              Inicia sesión aquí
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default RegisterScreen;
