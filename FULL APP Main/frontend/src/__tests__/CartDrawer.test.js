import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import CartDrawer from '../components/CartDrawer';
import { CartProvider } from '../context/CartContext';

describe('CartDrawer', () => {
  it('renderiza productos en el carrito', () => {
    const initialCart = [{ id: 1, nombre: 'Pan', precio: 10 }];
    render(
      <CartProvider initialCart={initialCart}>
        <CartDrawer open={true} onClose={() => {}} />
      </CartProvider>
    );
    expect(screen.getByText(/pan/i)).toBeInTheDocument();
  });

  it('elimina productos del carrito', () => {
    const initialCart = [{ id: 1, nombre: 'Pan', precio: 10 }];
    render(
      <CartProvider initialCart={initialCart}>
        <CartDrawer open={true} onClose={() => {}} />
      </CartProvider>
    );
    const eliminarBtn = screen.getByLabelText(/eliminar/i);
    fireEvent.click(eliminarBtn);
    expect(screen.queryByText(/pan/i)).not.toBeInTheDocument();
  });

  it('vacía el carrito', () => {
    const initialCart = [
      { id: 1, nombre: 'Pan', precio: 10 },
      { id: 2, nombre: 'Café', precio: 15 }
    ];
    render(
      <CartProvider initialCart={initialCart}>
        <CartDrawer open={true} onClose={() => {}} />
      </CartProvider>
    );
    const vaciarBtn = screen.getByText(/vaciar carrito/i);
    fireEvent.click(vaciarBtn);
    expect(screen.queryByText(/pan/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/café/i)).not.toBeInTheDocument();
  });
}); 