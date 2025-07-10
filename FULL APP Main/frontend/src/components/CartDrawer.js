import React from 'react';
import { useCart } from '../context/CartContext';

const CartDrawer = ({ open, onClose }) => {
  const { cart, removeFromCart, updateQty, clearCart, getTotal } = useCart();
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black bg-opacity-30">
      <div className="w-full max-w-md bg-white h-full shadow-xl p-6 flex flex-col">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">Carrito</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-red-600 text-2xl">&times;</button>
        </div>
        <div className="flex-1 overflow-y-auto">
          {cart.length === 0 ? (
            <div className="text-center text-gray-400 py-12">El carrito está vacío.</div>
          ) : (
            <ul className="space-y-4">
              {cart.map(item => (
                <li key={item.id} className="flex items-center gap-4 border-b pb-2">
                  <div className="flex-1">
                    <div className="font-semibold">{item.nombre}</div>
                    <div className="text-sm text-gray-500">${item.precio_venta?.toFixed(2)} x {item.qty}</div>
                  </div>
                  <input type="number" min={1} value={item.qty} onChange={e => updateQty(item.id, parseInt(e.target.value))} className="w-16 border rounded px-2 py-1" />
                  <button onClick={() => removeFromCart(item.id)} className="text-red-500 hover:underline ml-2">Eliminar</button>
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="mt-6 border-t pt-4">
          <div className="flex justify-between font-bold text-lg mb-4">
            <span>Total:</span>
            <span>${getTotal().toFixed(2)}</span>
          </div>
          <button onClick={clearCart} className="w-full bg-gray-200 hover:bg-gray-300 text-gray-700 py-2 rounded mb-2">Vaciar carrito</button>
          <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded">Finalizar compra</button>
        </div>
      </div>
    </div>
  );
};

export default CartDrawer; 