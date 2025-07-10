import React from 'react';
import { render, act } from '@testing-library/react';
import { CartProvider, useCart } from './CartContext';

describe('CartContext', () => {
  function TestComponent() {
    const { cart, addToCart, removeFromCart, clearCart } = useCart();
    return (
      <div>
        <button onClick={() => addToCart({ id: 1, nombre: 'Pan', precio: 10 })}>Agregar</button>
        <button onClick={() => removeFromCart(1)}>Eliminar</button>
        <button onClick={clearCart}>Limpiar</button>
        <span data-testid="cart-length">{cart.length}</span>
      </div>
    );
  }

  it('agrega productos al carrito', () => {
    const { getByText, getByTestId } = render(
      <CartProvider>
        <TestComponent />
      </CartProvider>
    );
    act(() => {
      getByText('Agregar').click();
    });
    expect(getByTestId('cart-length').textContent).toBe('1');
  });

  it('elimina productos del carrito', () => {
    const { getByText, getByTestId } = render(
      <CartProvider>
        <TestComponent />
      </CartProvider>
    );
    act(() => {
      getByText('Agregar').click();
      getByText('Eliminar').click();
    });
    expect(getByTestId('cart-length').textContent).toBe('0');
  });

  it('limpia el carrito', () => {
    const { getByText, getByTestId } = render(
      <CartProvider>
        <TestComponent />
      </CartProvider>
    );
    act(() => {
      getByText('Agregar').click();
      getByText('Limpiar').click();
    });
    expect(getByTestId('cart-length').textContent).toBe('0');
  });
}); 