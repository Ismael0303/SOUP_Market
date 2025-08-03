import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import publicApi from '../../frontend/src/api/publicApi';
import { useCart } from './CartContext';
import AIRecommender from '../../frontend/src/components/AIRecommender';

const BusinessLandingScreen = () => {
  const { id } = useParams();
  const [business, setBusiness] = useState(null);
  const [products, setProducts] = useState([]);
  const { addToCart } = useCart();

  useEffect(() => {
    const fetchBusiness = async () => {
      const b = await publicApi.getPublicBusiness(id);
      setBusiness(b);
      const prods = await publicApi.getPublicProductsByBusiness(id);
      setProducts(prods);
    };
    fetchBusiness();
  }, [id]);

  if (!business) return <div className="p-8 text-center">Cargando negocio...</div>;

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-4xl font-bold text-blue-700 mb-2">{business.nombre}</h1>
      <p className="text-gray-600 mb-6">{business.descripcion}</p>
      <AIRecommender businessId={id} />
      <h2 className="text-2xl font-bold mt-8 mb-4">Catálogo</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.map(product => (
          <div key={product.id} className="bg-white rounded-xl shadow p-4 flex flex-col">
            <div className="font-semibold text-lg mb-1">{product.nombre}</div>
            <div className="text-gray-500 text-sm mb-2">{product.descripcion}</div>
            <div className="text-green-600 font-bold mb-2">${product.precio_venta?.toFixed(2)}</div>
            <button onClick={() => addToCart(product)} className="bg-blue-600 hover:bg-blue-700 text-white py-2 rounded">Agregar al carrito</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BusinessLandingScreen; 