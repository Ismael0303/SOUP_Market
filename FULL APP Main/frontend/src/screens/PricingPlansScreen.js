// PricingPlansScreen.js - Implementación según mockups Gemini
import React from 'react';

const plans = [
  {
    name: 'Emprendedor PRO',
    price: 'AR$ 2.990/mes',
    features: [
      'Ventas ilimitadas',
      'Gestión avanzada de productos',
      'Soporte prioritario',
      'Reportes y estadísticas',
    ],
    cta: 'Comenzar ahora',
  },
  {
    name: 'Freelancer PRO',
    price: 'AR$ 1.490/mes',
    features: [
      'Hasta 100 ventas/mes',
      'Gestión básica de productos',
      'Soporte estándar',
      'Acceso a marketplace',
    ],
    cta: 'Probar gratis',
  },
];

const PricingPlansScreen = () => (
  <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-8">
    <h1 className="text-4xl font-bold text-blue-700 mb-8">Planes de Precios</h1>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-4xl">
      {plans.map((plan, idx) => (
        <div key={idx} className="bg-white rounded-2xl shadow-lg p-8 flex flex-col items-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h2>
          <div className="text-3xl font-extrabold text-blue-600 mb-4">{plan.price}</div>
          <ul className="mb-6 space-y-2">
            {plan.features.map((f, i) => <li key={i} className="text-gray-700">• {f}</li>)}
          </ul>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors">{plan.cta}</button>
        </div>
      ))}
    </div>
  </div>
);

export default PricingPlansScreen; 