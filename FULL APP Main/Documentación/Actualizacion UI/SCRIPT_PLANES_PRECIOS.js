// SCRIPT_PLANES_PRECIOS.js
// Implementación de pantalla de planes de precios según mockup Gemini

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { 
  Check, 
  X, 
  DollarSign, 
  TrendingUp, 
  Calculator, 
  ShoppingCart,
  Users,
  Settings,
  BarChart3,
  Clock,
  Shield,
  Zap
} from 'lucide-react';

const PricingPlansScreen = () => {
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [billingCycle, setBillingCycle] = useState('monthly'); // 'monthly' or 'yearly'

  const plans = [
    {
      id: 'emprendedor-pro',
      name: 'Emprendedor PRO',
      description: 'Ideal para microemprendimientos con productos y servicios.',
      price: {
        monthly: 29999,
        yearly: 269990 // 10% descuento anual
      },
      features: [
        {
          text: 'Gestión completa de insumos y productos',
          included: true,
          icon: ShoppingCart
        },
        {
          text: 'Cálculo automático de COGS y margen',
          included: true,
          icon: Calculator
        },
        {
          text: 'Automatización de ventas y facturación electrónica',
          included: true,
          icon: TrendingUp
        },
        {
          text: 'Límites generosos en operaciones e ítems de inventario',
          included: true,
          icon: BarChart3
        },
        {
          text: 'Soporte prioritario',
          included: true,
          icon: Users
        },
        {
          text: 'Reportes avanzados y analytics',
          included: true,
          icon: BarChart3
        },
        {
          text: 'Integración con pasarelas de pago',
          included: true,
          icon: DollarSign
        },
        {
          text: 'Backup automático de datos',
          included: true,
          icon: Shield
        }
      ],
      popular: true,
      color: 'blue'
    },
    {
      id: 'freelancer-pro',
      name: 'Freelancer PRO',
      description: 'Perfecto para profesionales independientes y consultores.',
      price: {
        monthly: 24999,
        yearly: 224990 // 10% descuento anual
      },
      features: [
        {
          text: 'Gestión de proyectos y seguimiento de horas',
          included: true,
          icon: Clock
        },
        {
          text: 'Facturación simplificada (incluye opciones en USD)',
          included: true,
          icon: DollarSign
        },
        {
          text: 'CRM básico para seguimiento de clientes',
          included: true,
          icon: Users
        },
        {
          text: 'Reportes de ingresos y gastos',
          included: true,
          icon: BarChart3
        },
        {
          text: 'Plantillas de contratos personalizables',
          included: true,
          icon: Settings
        },
        {
          text: 'Integración con calendarios',
          included: true,
          icon: Clock
        },
        {
          text: 'Soporte por email',
          included: true,
          icon: Users
        },
        {
          text: 'Backup semanal',
          included: false,
          icon: Shield
        }
      ],
      popular: false,
      color: 'gray'
    }
  ];

  const hiddenCosts = [
    {
      title: 'Pérdida de Tiempo',
      description: 'Horas dedicadas a tareas administrativas que podrías usar para crecer.',
      icon: Clock
    },
    {
      title: 'Errores Humanos',
      description: 'Datos inexactos que comprometen tus decisiones financieras.',
      icon: X
    },
    {
      title: 'Oportunidades Perdidas',
      description: 'Sin visibilidad en tiempo real, te pierdes de optimizar tu negocio.',
      icon: TrendingUp
    }
  ];

  const faqs = [
    {
      question: '¿Puedo cambiar de plan en cualquier momento?',
      answer: 'Sí, puedes cambiar de plan en cualquier momento. Los cambios se aplicarán en el próximo ciclo de facturación.'
    },
    {
      question: '¿Hay un período de prueba gratuito?',
      answer: 'Ofrecemos 14 días de prueba gratuita para que puedas evaluar si SOUP Market es la solución adecuada para tu negocio.'
    },
    {
      question: '¿Qué métodos de pago aceptan?',
      answer: 'Aceptamos tarjetas de crédito/débito, transferencias bancarias y Mercado Pago. Todos los pagos son procesados de forma segura.'
    },
    {
      question: '¿Puedo cancelar mi suscripción?',
      answer: 'Sí, puedes cancelar tu suscripción en cualquier momento desde tu panel de control. No hay penalizaciones por cancelación.'
    },
    {
      question: '¿Ofrecen soporte técnico?',
      answer: 'Sí, ofrecemos soporte técnico por email y chat en vivo durante horarios de atención. Los planes PRO incluyen soporte prioritario.'
    }
  ];

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-AR', { 
      style: 'currency', 
      currency: 'ARS', 
      minimumFractionDigits: 0 
    }).format(amount);
  };

  const getCurrentPrice = (plan) => {
    return billingCycle === 'yearly' ? plan.price.yearly : plan.price.monthly;
  };

  const getMonthlyPrice = (plan) => {
    if (billingCycle === 'yearly') {
      return plan.price.yearly / 12;
    }
    return plan.price.monthly;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header Section */}
      <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-16 rounded-b-3xl shadow-lg">
        <div className="max-w-4xl mx-auto text-center px-6">
          <h1 className="text-5xl md:text-6xl font-bold mb-4 leading-tight">
            Planes de Precios de SOUP Market
          </h1>
          <p className="text-xl md:text-2xl mb-8 opacity-90">
            Soluciones de gestión inteligentes para microemprendedores y freelancers en Argentina.
          </p>
          <a href="#planes" className="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold text-lg transform transition-transform duration-300 hover:scale-105">
            Ver Planes Ahora
          </a>
        </div>
      </header>

      {/* Hidden Costs Section */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-8 text-gray-800">
              ¿Cansado de los "Costos Ocultos" de la Gestión Manual?
            </h2>
            <p className="text-lg text-gray-600 mb-12 max-w-3xl mx-auto">
              Las hojas de cálculo y los métodos manuales parecen "gratuitos" al principio, pero te cuestan tiempo valioso, errores costosos y oportunidades perdidas. SOUP Market transforma tu gestión, liberando tu potencial.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {hiddenCosts.map((cost, index) => (
              <Card key={index} className="p-6 text-center border-0 shadow-lg">
                <cost.icon className="w-12 h-12 mx-auto mb-4 text-red-500" />
                <h3 className="text-2xl font-semibold mb-4 text-gray-700">{cost.title}</h3>
                <p className="text-gray-600">{cost.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Plans Section */}
      <section id="planes" className="py-16 bg-gray-50">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4 text-gray-800">Nuestros Planes, Diseñados para Ti</h2>
            <p className="text-lg text-gray-600 mb-8">
              Elige el plan que mejor se adapte a tus necesidades
            </p>
            
            {/* Billing Toggle */}
            <div className="flex items-center justify-center gap-4 mb-8">
              <span className={`text-sm ${billingCycle === 'monthly' ? 'text-blue-600 font-semibold' : 'text-gray-500'}`}>
                Mensual
              </span>
              <button
                onClick={() => setBillingCycle(billingCycle === 'monthly' ? 'yearly' : 'monthly')}
                className="relative inline-flex h-6 w-11 items-center rounded-full bg-blue-600 transition-colors"
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    billingCycle === 'yearly' ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
              <span className={`text-sm ${billingCycle === 'yearly' ? 'text-blue-600 font-semibold' : 'text-gray-500'}`}>
                Anual
                {billingCycle === 'yearly' && (
                  <span className="ml-1 bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                    -10%
                  </span>
                )}
              </span>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
            {plans.map((plan) => (
              <Card 
                key={plan.id} 
                className={`relative p-8 border-2 ${
                  plan.popular 
                    ? 'border-blue-600 shadow-xl scale-105' 
                    : 'border-gray-300 shadow-lg'
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-blue-600 text-white px-4 py-2 rounded-full text-sm font-semibold">
                      Más Popular
                    </span>
                  </div>
                )}

                <div className="text-center mb-8">
                  <h3 className={`text-3xl font-bold mb-2 ${
                    plan.popular ? 'text-blue-600' : 'text-gray-800'
                  }`}>
                    {plan.name}
                  </h3>
                  <p className="text-lg text-gray-600 mb-4">{plan.description}</p>
                  
                  <div className="text-5xl font-extrabold text-gray-900 mb-2">
                    {formatCurrency(getCurrentPrice(plan))}
                    {billingCycle === 'yearly' && (
                      <span className="text-2xl font-medium text-gray-500">/año</span>
                    )}
                    {billingCycle === 'monthly' && (
                      <span className="text-2xl font-medium text-gray-500">/mes</span>
                    )}
                  </div>
                  
                  {billingCycle === 'yearly' && (
                    <p className="text-sm text-gray-500">
                      {formatCurrency(getMonthlyPrice(plan))} por mes (facturado anualmente)
                    </p>
                  )}
                  
                  <p className="text-sm text-gray-500 mt-2">
                    Precio sin IVA. Descuento del 10% con pago anual.
                  </p>
                </div>

                <ul className="space-y-4 mb-8">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-start">
                      {feature.included ? (
                        <Check className="w-6 h-6 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                      ) : (
                        <X className="w-6 h-6 text-red-500 mr-3 mt-0.5 flex-shrink-0" />
                      )}
                      <span className={`${feature.included ? 'text-gray-700' : 'text-gray-400 line-through'}`}>
                        {feature.text}
                      </span>
                    </li>
                  ))}
                </ul>

                <Button 
                  className={`w-full py-3 text-lg font-semibold ${
                    plan.popular 
                      ? 'bg-blue-600 hover:bg-blue-700 text-white' 
                      : 'bg-gray-600 hover:bg-gray-700 text-white'
                  }`}
                  onClick={() => setSelectedPlan(plan.id)}
                >
                  Comenzar con {plan.name}
                </Button>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-6">
          <h2 className="text-4xl font-bold text-center mb-12 text-gray-800">
            Preguntas Frecuentes
          </h2>
          
          <div className="space-y-6">
            {faqs.map((faq, index) => (
              <Card key={index} className="border-0 shadow-sm">
                <CardContent className="p-6">
                  <details className="group">
                    <summary className="flex justify-between items-center cursor-pointer font-semibold text-lg text-gray-800">
                      {faq.question}
                      <span className="text-blue-600 group-open:rotate-180 transition-transform">
                        ▼
                      </span>
                    </summary>
                    <p className="mt-4 text-gray-600 leading-relaxed">
                      {faq.answer}
                    </p>
                  </details>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-blue-600 to-blue-800 text-white">
        <div className="max-w-4xl mx-auto text-center px-6">
          <h2 className="text-4xl font-bold mb-4">
            ¿Listo para Transformar tu Negocio?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Únete a miles de emprendedores que ya confían en SOUP Market
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register">
              <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-100">
                Comenzar Prueba Gratuita
              </Button>
            </Link>
            <Link to="/contact">
              <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-blue-600">
                Contactar Ventas
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-12">
        <div className="max-w-6xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-2xl font-bold text-blue-400 mb-4">SOUP Market</h3>
              <p className="text-gray-300">
                Simplificando la gestión de microemprendimientos en Argentina.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Producto</h4>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-white">Características</a></li>
                <li><a href="#" className="hover:text-white">Precios</a></li>
                <li><a href="#" className="hover:text-white">Integraciones</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Soporte</h4>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-white">Centro de Ayuda</a></li>
                <li><a href="#" className="hover:text-white">Contacto</a></li>
                <li><a href="#" className="hover:text-white">Documentación</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Empresa</h4>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-white">Acerca de</a></li>
                <li><a href="#" className="hover:text-white">Blog</a></li>
                <li><a href="#" className="hover:text-white">Carreras</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-300">
            <p>&copy; 2025 SOUP Market. Todos los derechos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default PricingPlansScreen; 