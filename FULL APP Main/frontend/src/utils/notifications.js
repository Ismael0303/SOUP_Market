// frontend/src/utils/notifications.js
// Utilidades simples de notificaciones para SOUP

export function showSuccess(message) {
  window.alert('✅ Éxito: ' + message);
}

export function showError(message) {
  window.alert('❌ Error: ' + message);
}

export function showInfo(message) {
  window.alert('ℹ️ Info: ' + message);
} 