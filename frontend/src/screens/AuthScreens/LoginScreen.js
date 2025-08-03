// src/screens/AuthScreens/LoginScreen.js
import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext'; // Importa el hook de autenticación
import { Link } from 'react-router-dom'; // Para el enlace a registro

// Componentes de Shadcn UI (asegúrate de que estén instalados y configurados)
// Asumo que estos componentes básicos de UI ya han sido generados por shadcn/ui cli
import { Button } from '../../components/ui/button.jsx'; // Ruta de ejemplo, ajusta si es necesario
import { Input } from '../../components/ui/input.jsx'; // Ruta de ejemplo, ajusta si es necesario
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card.jsx'; // Ruta de ejemplo, ajusta si es necesario
import { Label } from '../../components/ui/label.jsx'; // Ruta de ejemplo, ajusta si es necesario

function LoginScreen() {
  const { login, loading, error, setError } = useAuth(); // Obtener funciones del contexto
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Limpiar errores anteriores al intentar login
    try {
      await login(email, password);
      // La redirección se maneja dentro de AuthContext en caso de éxito
    } catch (err) {
      // El error ya se establece en el AuthContext, aquí solo lo logueamos o lo mostramos si es necesario
      console.error('Login failed:', err);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
      <Card className="w-full max-w-md p-6 space-y-4 rounded-xl shadow-lg">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl font-bold">Bienvenido de nuevo</CardTitle>
          <CardDescription className="text-gray-600 dark:text-gray-400">
            Ingresa tus credenciales para acceder a tu cuenta.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="tu@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
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
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
              />
            </div>
            {error && (
              <p className="text-red-600 text-sm text-center">{error}</p>
            )}
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
            </Button>
          </form>
          <div className="mt-4 text-center text-sm">
            ¿No tienes una cuenta?{' '}
            <Link to="/register" className="text-blue-600 hover:underline">
              Regístrate aquí
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default LoginScreen;
