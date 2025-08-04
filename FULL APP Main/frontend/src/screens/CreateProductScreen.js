// frontend/src/screens/CreateProductScreen.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Breadcrumbs from '../components/Breadcrumbs';
import { useNotification } from '../context/NotificationContext';
import { createProduct } from '../api/productApi';

const CreateProductScreen = () => {
  const [form, setForm] = useState({
    nombre: '',
    descripcion: '',
    precio: '',
    precio_venta: '',
    tipo_producto: '',
    negocio_id: '',
  });
  const [errors, setErrors] = useState({});
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const { showNotification } = useNotification();

  // Validación simple
  const validate = () => {
    const newErrors = {};
    if (!form.nombre) newErrors.nombre = 'El nombre es obligatorio';
    if (!form.precio) newErrors.precio = 'El precio base es obligatorio';
    if (!form.precio_venta) newErrors.precio_venta = 'El precio de venta es obligatorio';
    if (!form.tipo_producto) newErrors.tipo_producto = 'El tipo de producto es obligatorio';
    if (!form.negocio_id) newErrors.negocio_id = 'El ID del negocio es obligatorio';
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) {
      showNotification('Por favor corrige los errores del formulario.', 'error');
      return;
    }

    const productData = {
      nombre: form.nombre,
      descripcion: form.descripcion || undefined,
      precio: parseFloat(form.precio),
      tipo_producto: form.tipo_producto,
      negocio_id: form.negocio_id,
      precio_venta: parseFloat(form.precio_venta),
    };

    try {
      await createProduct(productData);
      showNotification('Producto creado correctamente', 'success');
    } catch (err) {
      console.error('Error al crear producto:', err);
      showNotification(err.message || 'Error al crear el producto.', 'error');
    }
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
                <label className="block text-sm font-medium text-gray-700 mb-1">Precio Base (ARS) <span className="text-red-500">*</span></label>
                <input type="number" name="precio" value={form.precio} onChange={handleChange} className={`input-field ${errors.precio ? 'border-red-500' : ''}`} placeholder="Ej: 15000" />
                {errors.precio && <p className="text-xs text-red-500 mt-1">{errors.precio}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Precio de Venta (ARS) <span className="text-red-500">*</span></label>
                <input type="number" name="precio_venta" value={form.precio_venta} onChange={handleChange} className={`input-field ${errors.precio_venta ? 'border-red-500' : ''}`} placeholder="Ej: 29999" />
                {errors.precio_venta && <p className="text-xs text-red-500 mt-1">{errors.precio_venta}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tipo de Producto <span className="text-red-500">*</span></label>
                <select name="tipo_producto" value={form.tipo_producto} onChange={handleChange} className={`input-field ${errors.tipo_producto ? 'border-red-500' : ''}`}>
                  <option value="">Selecciona una opción</option>
                  <option value="PHYSICAL_GOOD">Bien físico</option>
                  <option value="SERVICE_BY_HOUR">Servicio por hora</option>
                  <option value="SERVICE_BY_PROJECT">Servicio por proyecto</option>
                  <option value="DIGITAL_GOOD">Bien digital</option>
                </select>
                {errors.tipo_producto && <p className="text-xs text-red-500 mt-1">{errors.tipo_producto}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">ID del Negocio <span className="text-red-500">*</span></label>
                <input type="text" name="negocio_id" value={form.negocio_id} onChange={handleChange} className={`input-field ${errors.negocio_id ? 'border-red-500' : ''}`} placeholder="UUID del negocio" />
                {errors.negocio_id && <p className="text-xs text-red-500 mt-1">{errors.negocio_id}</p>}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
              <textarea name="descripcion" value={form.descripcion} onChange={handleChange} rows={3} className="input-field resize-y" placeholder="Descripción del producto..." />
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
