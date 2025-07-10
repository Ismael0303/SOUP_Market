// frontend/src/screens/CreateProductScreen.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Breadcrumbs from '../components/Breadcrumbs';
import { useNotification } from '../context/NotificationContext';

const CreateProductScreen = () => {
  const [form, setForm] = useState({
    nombre: '',
    sku: '',
    precio_venta: '',
    costo: '',
    stock: '',
    categoria: '',
    proveedor: '',
    notas: '',
    activo: true,
  });
  const [errors, setErrors] = useState({});
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const { showNotification } = useNotification();

  // Validación simple
  const validate = () => {
    const newErrors = {};
    if (!form.nombre) newErrors.nombre = 'El nombre es obligatorio';
    if (!form.precio_venta) newErrors.precio_venta = 'El precio es obligatorio';
    if (!form.costo) newErrors.costo = 'El costo es obligatorio';
    if (!form.stock) newErrors.stock = 'El stock es obligatorio';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    if (file) {
      const reader = new FileReader();
      reader.onload = (ev) => setImagePreview(ev.target.result);
      reader.readAsDataURL(file);
    } else {
      setImagePreview(null);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) {
      showNotification('Por favor corrige los errores del formulario.', 'error');
      return;
    }
    // Aquí iría la lógica de envío al backend
    showNotification('Producto creado correctamente', 'success');
  };

  return (
    <div className="min-h-screen flex bg-gray-100">
      {/* Sidebar de navegación */}
      <aside className="w-64 bg-white shadow-lg rounded-r-2xl p-6 flex-shrink-0 hidden md:block">
        <div className="text-2xl font-bold text-blue-600 mb-8">SOUP Market</div>
        <nav>
          <ul className="space-y-4">
            <li><Link to="/dashboard" className="text-gray-700 hover:text-blue-600 font-semibold">Dashboard</Link></li>
            <li><Link to="/dashboard/products" className="text-blue-600 font-semibold">Productos</Link></li>
            <li><Link to="/dashboard/insumos" className="text-gray-700 hover:text-blue-600">Insumos</Link></li>
            <li><Link to="/dashboard/businesses" className="text-gray-700 hover:text-blue-600">Negocios</Link></li>
            <li><Link to="/dashboard/ventas" className="text-gray-700 hover:text-blue-600">Ventas</Link></li>
          </ul>
        </nav>
      </aside>
      {/* Contenido principal */}
      <main className="flex-1 max-w-4xl mx-auto w-full p-4 sm:p-8">
        <Breadcrumbs items={[
          { label: 'Dashboard', to: '/dashboard' },
          { label: 'Productos', to: '/dashboard/products' },
          { label: 'Crear Producto' }
        ]} />
        {/* Card de formulario */}
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Crear Producto</h1>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nombre <span className="text-red-500">*</span></label>
                <input type="text" name="nombre" value={form.nombre} onChange={handleChange} className={`input-field ${errors.nombre ? 'border-red-500' : ''}`} placeholder="Introduce el nombre del producto" />
                {errors.nombre && <p className="text-xs text-red-500 mt-1">{errors.nombre}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">SKU</label>
                <input type="text" name="sku" value={form.sku} onChange={handleChange} className="input-field" placeholder="Código único del producto" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Precio de Venta (ARS) <span className="text-red-500">*</span></label>
                <input type="number" name="precio_venta" value={form.precio_venta} onChange={handleChange} className={`input-field ${errors.precio_venta ? 'border-red-500' : ''}`} placeholder="Ej: 29999" />
                {errors.precio_venta && <p className="text-xs text-red-500 mt-1">{errors.precio_venta}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Costo de Compra (ARS) <span className="text-red-500">*</span></label>
                <input type="number" name="costo" value={form.costo} onChange={handleChange} className={`input-field ${errors.costo ? 'border-red-500' : ''}`} placeholder="Ej: 15000" />
                {errors.costo && <p className="text-xs text-red-500 mt-1">{errors.costo}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Stock Actual <span className="text-red-500">*</span></label>
                <input type="number" name="stock" value={form.stock} onChange={handleChange} className={`input-field ${errors.stock ? 'border-red-500' : ''}`} placeholder="Cantidad disponible" />
                {errors.stock && <p className="text-xs text-red-500 mt-1">{errors.stock}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Categoría</label>
                <input type="text" name="categoria" value={form.categoria} onChange={handleChange} className="input-field" placeholder="Ej: Panadería, Bebidas" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Proveedor</label>
                <input type="text" name="proveedor" value={form.proveedor} onChange={handleChange} className="input-field" placeholder="Nombre del proveedor" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Notas</label>
              <textarea name="notas" value={form.notas} onChange={handleChange} rows={3} className="input-field resize-y" placeholder="Notas adicionales sobre el producto..." />
            </div>
            {/* Imagen */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Cargar Imagen</label>
              <div className="flex items-center gap-4 mb-4">
                <input type="file" accept="image/*" onChange={handleImageChange} className="hidden" id="imageUpload" />
                <label htmlFor="imageUpload" className="btn-secondary cursor-pointer">Seleccionar Archivo</label>
                <span className="text-gray-500 text-sm">{image ? image.name : 'Ningún archivo seleccionado'}</span>
              </div>
              <div className="w-48 h-48 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center text-gray-400 text-center overflow-hidden">
                {imagePreview ? <img src={imagePreview} alt="Previsualización" className="w-full h-full object-cover rounded-lg" /> : 'Previsualización de imagen'}
              </div>
            </div>
            {/* Checkbox activo */}
            <div className="flex items-center">
              <input type="checkbox" name="activo" checked={form.activo} onChange={handleChange} className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" />
              <label className="ml-2 block text-sm font-medium text-gray-700">Producto Activo</label>
            </div>
            {/* Botones de acción */}
            <div className="flex justify-end gap-4 mt-8">
              <Link to="/dashboard/products" className="btn-secondary">Cancelar</Link>
              <button type="submit" className="btn-primary">Crear Producto</button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
};

export default CreateProductScreen;
