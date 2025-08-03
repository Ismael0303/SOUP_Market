// Este archivo configura la aplicación Firebase y exporta las instancias de db y auth.
// Las variables globales __app_id y __initial_auth_token son proporcionadas por el entorno.

import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously, signInWithCustomToken } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

// Asegúrate de que estas variables globales estén disponibles en el entorno de ejecución.
// En un entorno Canvas, suelen ser inyectadas automáticamente.
const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {};
const initialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;

// Inicializa Firebase si la configuración está disponible
let app;
let db;
let auth;

try {
  if (Object.keys(firebaseConfig).length > 0) {
    app = initializeApp(firebaseConfig);
    db = getFirestore(app);
    auth = getAuth(app);

    // Inicia sesión con el token personalizado si está disponible, de lo contrario, de forma anónima.
    // Esto debe hacerse en un contexto asíncrono, por ejemplo, en AuthContext o en el componente raíz.
    // Para evitar errores de "already defined", no lo ejecutaremos aquí directamente.
    // La lógica de autenticación inicial se manejará en AuthContext.js
  } else {
    console.warn("Firebase config not found. Firebase services will not be initialized.");
  }
} catch (error) {
  console.error("Failed to initialize Firebase:", error);
}

export { db, auth, appId, initialAuthToken }; 