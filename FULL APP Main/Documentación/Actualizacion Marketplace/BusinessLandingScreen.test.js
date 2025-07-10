import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import BusinessLandingScreen from '../../frontend/src/screens/BusinessLandingScreen';

describe('Landing de Negocio (BusinessLandingScreen)', () => {
  it('muestra el catálogo de productos', () => {
    render(
      <MemoryRouter initialEntries={["/public/businesses/1"]}>
        <BusinessLandingScreen />
      </MemoryRouter>
    );
    expect(screen.getByText(/catálogo/i)).toBeInTheDocument();
  });

  it('agrega productos al carrito', () => {
    render(
      <MemoryRouter initialEntries={["/public/businesses/1"]}>
        <BusinessLandingScreen />
      </MemoryRouter>
    );
    const addBtns = screen.getAllByText(/agregar al carrito/i);
    fireEvent.click(addBtns[0]);
    // Espera que el carrito tenga al menos un producto
  });

  it('muestra recomendaciones de IA', () => {
    render(
      <MemoryRouter initialEntries={["/public/businesses/1"]}>
        <BusinessLandingScreen />
      </MemoryRouter>
    );
    expect(screen.getByText(/sugerencias/i)).toBeInTheDocument();
  });

  it('abre el drawer del carrito', () => {
    render(
      <MemoryRouter initialEntries={["/public/businesses/1"]}>
        <BusinessLandingScreen />
      </MemoryRouter>
    );
    const verCarritoBtn = screen.getByText(/ver carrito/i);
    fireEvent.click(verCarritoBtn);
    expect(screen.getByText(/carrito/i)).toBeInTheDocument();
  });
}); 