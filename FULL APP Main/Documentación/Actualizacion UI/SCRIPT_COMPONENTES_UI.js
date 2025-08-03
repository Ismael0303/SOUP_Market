// SCRIPT_COMPONENTES_UI.js
// Componentes UI faltantes según mockups Gemini

import React from 'react';
import { cn } from '../lib/utils';

// 1. Message Box Component
export const MessageBox = ({ message, type = 'info', onClose, className }) => {
  const baseClasses = "fixed top-4 left-1/2 transform -translate-x-1/2 z-50 p-4 rounded-lg shadow-lg min-w-80 text-center font-medium";
  
  const typeClasses = {
    success: "bg-green-100 border border-green-400 text-green-700",
    error: "bg-red-100 border border-red-400 text-red-700",
    info: "bg-blue-100 border border-blue-400 text-blue-700",
    warning: "bg-yellow-100 border border-yellow-400 text-yellow-700"
  };

  return (
    <div className={cn(baseClasses, typeClasses[type], className)}>
      <div className="flex items-center justify-between">
        <span>{message}</span>
        {onClose && (
          <button
            onClick={onClose}
            className="ml-4 text-current hover:opacity-70"
          >
            ×
          </button>
        )}
      </div>
    </div>
  );
};

// 2. Search Bar Component
export const SearchBar = ({ 
  placeholder = "Buscar...", 
  value, 
  onChange, 
  onSearch,
  className 
}) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch?.(value);
  };

  return (
    <form onSubmit={handleSubmit} className={cn("relative", className)}>
      <input
        type="text"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      />
      <svg 
        className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" 
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </form>
  );
};

// 3. Category Filter Component
export const CategoryFilter = ({ 
  categories, 
  selectedCategory, 
  onCategoryChange, 
  className 
}) => {
  return (
    <div className={cn("space-y-2", className)}>
      <h4 className="text-lg font-semibold text-gray-700 mb-3">Categorías</h4>
      <ul className="space-y-2">
        {categories.map(category => (
          <li key={category.id}>
            <button
              onClick={() => onCategoryChange(category.id)}
              className={cn(
                "block w-full text-left p-2 rounded-lg transition-colors",
                selectedCategory === category.id
                  ? "text-blue-600 font-medium bg-blue-50"
                  : "text-gray-700 hover:text-blue-600 hover:bg-gray-50"
              )}
            >
              {category.name}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

// 4. Product Card Component
export const ProductCard = ({ 
  product, 
  onAddToCart, 
  onViewDetails,
  className 
}) => {
  const formatCurrency = (amount) => {
    if (!amount) return 'No especificado';
    return new Intl.NumberFormat('es-AR', { 
      style: 'currency', 
      currency: 'ARS', 
      minimumFractionDigits: 2 
    }).format(amount);
  };

  return (
    <div className={cn("bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-lg transition-shadow duration-300", className)}>
      {/* Product Image */}
      <div className="relative">
        {product.fotos_urls && product.fotos_urls.length > 0 ? (
          <img
            src={product.fotos_urls[0]}
            alt={product.nombre}
            className="w-full h-48 object-cover"
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = "https://placehold.co/400x250/007bff/ffffff?text=Producto";
            }}
          />
        ) : (
          <div className="w-full h-48 bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
            <svg className="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
          </div>
        )}
        
        {/* Category Badge */}
        {product.categoria && (
          <div className="absolute top-2 left-2">
            <span className="bg-blue-600 text-white text-xs px-2 py-1 rounded-full">
              {product.categoria}
            </span>
          </div>
        )}
      </div>

      {/* Product Info */}
      <div className="p-4">
        <h3 className="text-xl font-bold text-gray-900 mb-2 line-clamp-2">
          {product.nombre}
        </h3>
        
        {/* Business Info */}
        {product.negocio && (
          <p className="text-sm text-gray-500 mb-3 flex items-center">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            {product.negocio.nombre}
          </p>
        )}

        {/* Description */}
        <p className="text-gray-700 mb-4 line-clamp-3">
          {product.descripcion || 'Sin descripción disponible.'}
        </p>

        {/* Price Information */}
        <div className="space-y-2 mb-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Precio:</span>
            <span className="text-lg font-bold text-green-600 flex items-center">
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
              </svg>
              {formatCurrency(product.precio_venta || product.precio)}
            </span>
          </div>

          {/* Stock Information */}
          {product.stock_terminado !== undefined && (
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Stock:</span>
              <span className={`text-sm font-medium ${
                product.stock_terminado > 0 ? 'text-green-600' : 'text-red-600'
              }`}>
                {product.stock_terminado > 0 ? `${product.stock_terminado} disponibles` : 'Agotado'}
              </span>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          <button
            onClick={() => onViewDetails?.(product)}
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors"
          >
            Ver Detalles
          </button>
          <button
            onClick={() => onAddToCart?.(product)}
            className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

// 5. Cart Table Component
export const CartTable = ({ 
  items, 
  onUpdateQuantity, 
  onRemoveItem,
  className 
}) => {
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-AR', { 
      style: 'currency', 
      currency: 'ARS', 
      minimumFractionDigits: 2 
    }).format(amount);
  };

  return (
    <div className={cn("overflow-y-auto", className)}>
      {items.length === 0 ? (
        <p className="text-center text-gray-500 py-4">El carrito está vacío.</p>
      ) : (
        <table className="w-full text-left">
          <thead>
            <tr className="text-gray-600 text-sm border-b pb-2">
              <th className="w-1/2">Ítem</th>
              <th className="w-1/5 text-center">Cant.</th>
              <th className="w-1/5 text-right">P. Unit.</th>
              <th className="w-1/5 text-right">Subtotal</th>
              <th className="w-1/12 text-center"></th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, index) => (
              <tr key={index} className="border-b border-gray-100 last:border-b-0">
                <td className="py-3 pr-2 font-medium">{item.nombre}</td>
                <td className="py-3 px-2 text-center">
                  <div className="flex items-center justify-center gap-1">
                    <button
                      onClick={() => onUpdateQuantity(index, 'decrement')}
                      className="w-6 h-6 rounded-full bg-gray-200 text-gray-700 hover:bg-gray-300 flex items-center justify-center text-sm font-bold transition-colors"
                    >
                      -
                    </button>
                    <span className="mx-2">{item.quantity}</span>
                    <button
                      onClick={() => onUpdateQuantity(index, 'increment')}
                      className="w-6 h-6 rounded-full bg-gray-200 text-gray-700 hover:bg-gray-300 flex items-center justify-center text-sm font-bold transition-colors"
                    >
                      +
                    </button>
                  </div>
                </td>
                <td className="py-3 px-2 text-right text-sm text-gray-600">
                  {formatCurrency(item.precio)}
                </td>
                <td className="py-3 pl-2 text-right font-semibold">
                  {formatCurrency(item.precio * item.quantity)}
                </td>
                <td className="py-3 pl-2 text-center">
                  <button
                    onClick={() => onRemoveItem(index)}
                    className="text-red-500 hover:text-red-700 transition-colors"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

// 6. Payment Methods Component
export const PaymentMethods = ({ 
  methods, 
  selectedMethod, 
  onMethodSelect,
  className 
}) => {
  return (
    <div className={cn("space-y-4", className)}>
      <h2 className="text-xl font-semibold text-gray-800 mb-6">Opciones de Pago</h2>
      <div className="grid grid-cols-2 gap-4">
        {methods.map(method => (
          <button
            key={method.id}
            onClick={() => onMethodSelect(method.id)}
            className={cn(
              "py-3 px-4 rounded-lg font-medium transition-colors",
              selectedMethod === method.id
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-700 hover:bg-gray-300"
            )}
          >
            {method.name}
          </button>
        ))}
      </div>
    </div>
  );
};

// 7. Sidebar Navigation Component
export const SidebarNavigation = ({ 
  items, 
  activeItem, 
  onItemClick,
  className 
}) => {
  return (
    <aside className={cn("w-64 bg-white shadow-lg border-r border-gray-200 flex-shrink-0", className)}>
      <div className="p-6">
        <div className="text-3xl font-bold text-blue-600 mb-8">SOUP Market</div>
        <nav>
          <ul className="space-y-4">
            {items.map(item => (
              <li key={item.id}>
                <button
                  onClick={() => onItemClick(item.id)}
                  className={cn(
                    "flex items-center w-full p-3 rounded-lg transition-colors",
                    activeItem === item.id
                      ? "text-blue-600 font-semibold bg-blue-50"
                      : "text-gray-700 hover:text-blue-600 hover:bg-gray-50"
                  )}
                >
                  <item.icon className="w-5 h-5 mr-3" />
                  {item.name}
                </button>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </aside>
  );
};

// 8. Breadcrumbs Component
export const Breadcrumbs = ({ items, className }) => {
  return (
    <nav className={cn("flex", className)} aria-label="Breadcrumb">
      <ol className="inline-flex items-center space-x-1 md:space-x-3">
        {items.map((item, index) => (
          <li key={index} className="inline-flex items-center">
            {index > 0 && (
              <svg className="w-6 h-6 text-gray-400 mx-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
              </svg>
            )}
            {item.href ? (
              <a
                href={item.href}
                className={cn(
                  "inline-flex items-center text-sm font-medium",
                  index === items.length - 1
                    ? "text-gray-500 cursor-default"
                    : "text-gray-700 hover:text-blue-600"
                )}
              >
                {item.label}
              </a>
            ) : (
              <span className="text-sm font-medium text-gray-500">
                {item.label}
              </span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
};

// 9. Loading Spinner Component
export const LoadingSpinner = ({ size = "md", className }) => {
  const sizeClasses = {
    sm: "h-4 w-4",
    md: "h-8 w-8",
    lg: "h-12 w-12",
    xl: "h-16 w-16"
  };

  return (
    <div className={cn("flex justify-center items-center", className)}>
      <div className={cn("animate-spin rounded-full border-b-2 border-blue-600", sizeClasses[size])}></div>
    </div>
  );
};

// 10. Empty State Component
export const EmptyState = ({ 
  icon: Icon, 
  title, 
  description, 
  action,
  className 
}) => {
  return (
    <div className={cn("text-center py-12", className)}>
      <Icon className="w-16 h-16 mx-auto text-gray-400 mb-4" />
      <h3 className="text-lg font-medium text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 mb-6">{description}</p>
      {action && (
        <button
          onClick={action.onClick}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
        >
          {action.label}
        </button>
      )}
    </div>
  );
};

// 11. Stats Card Component
export const StatsCard = ({ 
  title, 
  value, 
  change, 
  icon: Icon,
  className 
}) => {
  return (
    <div className={cn("bg-white rounded-lg shadow-sm p-6", className)}>
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <Icon className="h-8 w-8 text-gray-400" />
        </div>
        <div className="ml-5 w-0 flex-1">
          <dl>
            <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
            <dd className="text-lg font-medium text-gray-900">{value}</dd>
          </dl>
        </div>
      </div>
      {change && (
        <div className="mt-4">
          <div className={cn(
            "text-sm",
            change > 0 ? "text-green-600" : "text-red-600"
          )}>
            {change > 0 ? "↑" : "↓"} {Math.abs(change)}%
          </div>
        </div>
      )}
    </div>
  );
};

// 12. Modal Component
export const Modal = ({ 
  isOpen, 
  onClose, 
  title, 
  children, 
  size = "md",
  className 
}) => {
  if (!isOpen) return null;

  const sizeClasses = {
    sm: "max-w-md",
    md: "max-w-lg",
    lg: "max-w-2xl",
    xl: "max-w-4xl"
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 transition-opacity" aria-hidden="true">
          <div className="absolute inset-0 bg-gray-500 opacity-75" onClick={onClose}></div>
        </div>

        <div className={cn(
          "inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:w-full",
          sizeClasses[size]
        )}>
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">{title}</h3>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};

// Export all components
export {
  MessageBox,
  SearchBar,
  CategoryFilter,
  ProductCard,
  CartTable,
  PaymentMethods,
  SidebarNavigation,
  Breadcrumbs,
  LoadingSpinner,
  EmptyState,
  StatsCard,
  Modal
}; 