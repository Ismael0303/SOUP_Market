// Sistema global de notificaciones
import React from 'react';
import { createRoot } from 'react-dom/client';

// Componente de notificación individual
const Notification = ({ message, type, onClose, duration = 5000 }) => {
  React.useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(onClose, duration);
      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  const baseClasses = "fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg min-w-80 max-w-md transform transition-all duration-300";
  
  const typeClasses = {
    success: "bg-green-100 border border-green-400 text-green-700",
    error: "bg-red-100 border border-red-400 text-red-700",
    info: "bg-blue-100 border border-blue-400 text-blue-700",
    warning: "bg-yellow-100 border border-yellow-400 text-yellow-700"
  };

  return (
    <div className={`${baseClasses} ${typeClasses[type]}`}>
      <div className="flex items-center justify-between">
        <span className="font-medium">{message}</span>
        <button
          onClick={onClose}
          className="ml-4 text-current hover:opacity-70 text-lg font-bold"
        >
          ×
        </button>
      </div>
    </div>
  );
};

// Contenedor de notificaciones
const NotificationContainer = () => {
  const [notifications, setNotifications] = React.useState([]);

  const addNotification = (message, type = 'info', duration = 5000) => {
    const id = Date.now() + Math.random();
    const newNotification = { id, message, type, duration };

    setNotifications(prev => [...prev, newNotification]);
    if (!window.notificationIds) {
      window.notificationIds = new Set();
    }
    window.notificationIds.add(id);

    return id;
  };

  const removeNotification = (id) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
    if (window.notificationIds) {
      window.notificationIds.delete(id);
    }
  };

  // Exponer métodos globalmente
  window.showNotification = addNotification;
  window.removeNotification = removeNotification;

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {notifications.map(notification => (
        <Notification
          key={notification.id}
          message={notification.message}
          type={notification.type}
          duration={notification.duration}
          onClose={() => removeNotification(notification.id)}
        />
      ))}
    </div>
  );
};

// Inicializar el sistema de notificaciones
let notificationRoot = null;

export const initializeNotifications = () => {
  // Crear contenedor para notificaciones
  const container = document.createElement('div');
  container.id = 'notification-container';
  document.body.appendChild(container);

  // Inicializar almacenamiento de IDs
  window.notificationIds = new Set();

  // Renderizar el componente
  notificationRoot = createRoot(container);
  notificationRoot.render(<NotificationContainer />);
};

// Funciones de conveniencia
export const showSuccess = (message, duration = 5000) => {
  if (window.showNotification) {
    return window.showNotification(message, 'success', duration);
  }
};

export const showError = (message, duration = 5000) => {
  if (window.showNotification) {
    return window.showNotification(message, 'error', duration);
  }
};

export const showInfo = (message, duration = 5000) => {
  if (window.showNotification) {
    return window.showNotification(message, 'info', duration);
  }
};

export const showWarning = (message, duration = 5000) => {
  if (window.showNotification) {
    return window.showNotification(message, 'warning', duration);
  }
};

// Limpiar notificaciones
export const clearNotifications = () => {
  if (window.notificationIds && window.removeNotification) {
    [...window.notificationIds].forEach(id => window.removeNotification(id));
    window.notificationIds.clear();
  }
};