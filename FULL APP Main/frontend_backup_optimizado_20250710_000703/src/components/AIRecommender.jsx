import React, { useState } from 'react';
import { getAIRecommendations } from '../api/aiApi';
import { useNavigate } from 'react-router-dom';

export default function AIRecommender() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const data = await getAIRecommendations(query);
      setResult(data);
    } catch (err) {
      setError(err.message || 'Error desconocido');
    }
    setLoading(false);
  };

  const goToProduct = (id) => {
    navigate(`/dashboard/products/edit/${id}`);
  };

  const goToBusiness = (id) => {
    navigate(`/dashboard/businesses/edit/${id}`);
  };

  return (
    <div className="max-w-xl mx-auto my-8 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-4 text-center">Asistente de Recomendaciones IA</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="¿Qué necesitas? (ej: pan barato en Palermo)"
          className="border rounded px-3 py-2"
        />
        <button type="submit" disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          {loading ? 'Buscando...' : 'Consultar'}
        </button>
      </form>
      {error && <p className="text-red-600 mt-2">{error}</p>}
      {result && (
        <div className="mt-6">
          {result.producto_preferencial && (
            <div className="mb-6 p-4 border-2 border-blue-500 rounded bg-blue-50">
              <h3 className="text-lg font-semibold mb-2 text-blue-700">Producto preferencial recomendado</h3>
              <div className="flex flex-col gap-2">
                <span className="font-bold">{result.producto_preferencial.nombre}</span>
                <span>Tipo: {result.producto_preferencial.tipo_producto || result.producto_preferencial.tipo}</span>
                {result.producto_preferencial.precio_venta && <span>Precio: ${result.producto_preferencial.precio_venta}</span>}
                <button
                  className="mt-2 bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
                  onClick={() => goToProduct(result.producto_preferencial.id)}
                >
                  Ver producto
                </button>
                {result.producto_preferencial.negocio_id && (
                  <button
                    className="mt-2 bg-indigo-600 text-white px-3 py-1 rounded hover:bg-indigo-700"
                    onClick={() => goToBusiness(result.producto_preferencial.negocio_id)}
                  >
                    Ver negocio
                  </button>
                )}
              </div>
            </div>
          )}
          {result.otras_recomendaciones && result.otras_recomendaciones.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold mb-2">Otras recomendaciones</h3>
              <ul className="list-disc pl-5">
                {result.otras_recomendaciones.map(p => (
                  <li key={p.id} className="mb-2 flex flex-col gap-1">
                    <span className="font-bold">{p.nombre}</span>
                    <span>Tipo: {p.tipo_producto || p.tipo}</span>
                    {p.precio_venta && <span>Precio: ${p.precio_venta}</span>}
                    <div className="flex gap-2 mt-1">
                      <button
                        className="bg-green-600 text-white px-2 py-1 rounded hover:bg-green-700"
                        onClick={() => goToProduct(p.id)}
                      >
                        Ver producto
                      </button>
                      {p.negocio_id && (
                        <button
                          className="bg-indigo-600 text-white px-2 py-1 rounded hover:bg-indigo-700"
                          onClick={() => goToBusiness(p.negocio_id)}
                        >
                          Ver negocio
                        </button>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {(!result.producto_preferencial && (!result.otras_recomendaciones || result.otras_recomendaciones.length === 0)) && (
            <p className="text-gray-600">No se encontraron recomendaciones para tu consulta.</p>
          )}
        </div>
      )}
    </div>
  );
} 