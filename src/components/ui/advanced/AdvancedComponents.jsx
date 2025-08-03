// AdvancedComponents.jsx
// Componentes UI avanzados según mockups Gemini

import React from 'react';
import { cn } from '../../lib/utils';

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
          {onAddToCart && product.stock_terminado > 0 && (
            <button
              onClick={() => onAddToCart(product)}
              className="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg font-medium transition-colors"
            >
              Agregar
            </button>
          )}
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

  const total = items.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);

  return (
    <div className={cn("bg-white rounded-lg shadow-sm", className)}>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-sm font-medium text-gray-700">Producto</th>
              <th className="px-4 py-3 text-center text-sm font-medium text-gray-700">Precio</th>
              <th className="px-4 py-3 text-center text-sm font-medium text-gray-700">Cantidad</th>
              <th className="px-4 py-3 text-center text-sm font-medium text-gray-700">Subtotal</th>
              <th className="px-4 py-3 text-center text-sm font-medium text-gray-700">Acciones</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {items.map((item, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="px-4 py-3">
                  <div className="flex items-center">
                    <img
                      src={item.fotos_urls?.[0] || "https://placehold.co/60x60/007bff/ffffff?text=P"}
                      alt={item.nombre}
                      className="w-12 h-12 rounded-lg object-cover mr-3"
                    />
                    <div>
                      <h4 className="text-sm font-medium text-gray-900">{item.nombre}</h4>
                      <p className="text-xs text-gray-500">{item.categoria}</p>
                    </div>
                  </div>
                </td>
                <td className="px-4 py-3 text-center text-sm text-gray-900">
                  {formatCurrency(item.precio)}
                </td>
                <td className="px-4 py-3 text-center">
                  <div className="flex items-center justify-center space-x-2">
                    <button
                      onClick={() => onUpdateQuantity(index, Math.max(1, item.cantidad - 1))}
                      className="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center"
                    >
                      -
                    </button>
                    <span className="w-12 text-center text-sm font-medium">{item.cantidad}</span>
                    <button
                      onClick={() => onUpdateQuantity(index, item.cantidad + 1)}
                      className="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center"
                    >
                      +
                    </button>
                  </div>
                </td>
                <td className="px-4 py-3 text-center text-sm font-medium text-gray-900">
                  {formatCurrency(item.precio * item.cantidad)}
                </td>
                <td className="px-4 py-3 text-center">
                  <button
                    onClick={() => onRemoveItem(index)}
                    className="text-red-600 hover:text-red-800"
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
      </div>
      
      {/* Total */}
      <div className="border-t border-gray-200 px-4 py-3">
        <div className="flex justify-between items-center">
          <span className="text-lg font-semibold text-gray-900">Total:</span>
          <span className="text-2xl font-bold text-green-600">{formatCurrency(total)}</span>
        </div>
      </div>
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
    <div className={cn("space-y-3", className)}>
      <h4 className="text-lg font-semibold text-gray-700">Método de Pago</h4>
      <div className="space-y-2">
        {methods.map(method => (
          <label key={method.id} className="flex items-center p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
            <input
              type="radio"
              name="payment-method"
              value={method.id}
              checked={selectedMethod === method.id}
              onChange={() => onMethodSelect(method.id)}
              className="mr-3"
            />
            <div className="flex items-center">
              <span className="text-lg mr-2">{method.icon}</span>
              <span className="font-medium">{method.name}</span>
            </div>
          </label>
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
    <nav className={cn("w-64 bg-white shadow-lg h-screen", className)}>
      <div className="p-4">
        <div className="flex items-center mb-6">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center mr-3">
            <span className="text-white font-bold text-lg">S</span>
          </div>
          <h1 className="text-xl font-bold text-gray-900">SOUP</h1>
        </div>
        
        <ul className="space-y-1">
          {items.map(item => (
            <li key={item.id}>
              <button
                onClick={() => onItemClick(item.id)}
                className={cn(
                  "w-full flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                  activeItem === item.id
                    ? "bg-blue-100 text-blue-700"
                    : "text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                )}
              >
                <item.icon className="w-5 h-5 mr-3" />
                {item.name}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
};

// 8. Breadcrumbs Component
export const Breadcrumbs = ({ items, className }) => {
  return (
    <nav className={cn("flex", className)} aria-label="Breadcrumb">
      <ol className="flex items-center space-x-2">
        {items.map((item, index) => (
          <li key={index} className="flex items-center">
            {index > 0 && (
              <svg className="w-4 h-4 text-gray-400 mx-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
              </svg>
            )}
            {item.href ? (
              <a
                href={item.href}
                className="text-sm font-medium text-blue-600 hover:text-blue-800"
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
    sm: "w-4 h-4",
    md: "w-8 h-8",
    lg: "w-12 h-12",
    xl: "w-16 h-16"
  };

  return (
    <div className={cn("flex items-center justify-center", className)}>
      <div className={cn("animate-spin rounded-full border-2 border-gray-300 border-t-blue-600", sizeClasses[size])}></div>
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
      {Icon && (
        <div className="mx-auto w-16 h-16 text-gray-400 mb-4">
          <Icon className="w-full h-full" />
        </div>
      )}
      <h3 className="text-lg font-medium text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-500 mb-6">{description}</p>
      {action && action}
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
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {change !== undefined && (
            <p className={`text-sm font-medium ${
              change >= 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              {change >= 0 ? '+' : ''}{change}% desde el mes pasado
            </p>
          )}
        </div>
        {Icon && (
          <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <Icon className="w-6 h-6 text-blue-600" />
          </div>
        )}
      </div>
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
  const sizeClasses = {
    sm: "max-w-md",
    md: "max-w-lg",
    lg: "max-w-2xl",
    xl: "max-w-4xl"
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 transition-opacity" aria-hidden="true">
          <div className="absolute inset-0 bg-gray-500 opacity-75" onClick={onClose}></div>
        </div>

        <div className={cn("inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:w-full", sizeClasses[size], className)}>
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">{title}</h3>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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