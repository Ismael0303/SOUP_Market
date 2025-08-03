import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { NotificationProvider } from './context/NotificationContext';
import './index.css'; // Importa los estilos de Tailwind CSS
import App from './App';
// import reportWebVitals from './reportWebVitals'; // ELIMINAR O COMENTAR ESTA LÍNEA

// Crea la raíz de React para renderizar la aplicación
const root = ReactDOM.createRoot(document.getElementById('root'));
// Renderiza el componente principal <App /> dentro del modo estricto de React
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <NotificationProvider>
        <AuthProvider>
          <App />
        </AuthProvider>
      </NotificationProvider>
    </BrowserRouter>
  </React.StrictMode>
);

// ELIMINAR O COMENTAR ESTE BLOQUE
// Mide el rendimiento de la aplicación
// Puedes pasar una función para registrar los resultados (ej., reportWebVitals(console.log))
// o enviarlos a un endpoint de análisis.
// reportWebVitals();
