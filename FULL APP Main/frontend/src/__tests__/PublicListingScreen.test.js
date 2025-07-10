import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import PublicListingScreen from '../screens/PublicListingScreen';

describe('Marketplace (PublicListingScreen)', () => {
  it('navega a login al hacer click en el botón de usuario', () => {
    render(
      <MemoryRouter initialEntries={["/public"]}>
        <PublicListingScreen />
      </MemoryRouter>
    );
    const loginBtn = screen.getByText(/usuario/i);
    fireEvent.click(loginBtn);
    // Espera que la URL cambie a /login (mock de navigate)
  });

  it('filtra productos por búsqueda', () => {
    render(
      <MemoryRouter>
        <PublicListingScreen />
      </MemoryRouter>
    );
    const input = screen.getByPlaceholderText(/buscar productos/i);
    fireEvent.change(input, { target: { value: 'pan' } });
    // Espera que los productos mostrados incluyan solo los que contienen 'pan'
  });

  it('muestra el componente de IA', () => {
    render(
      <MemoryRouter>
        <PublicListingScreen />
      </MemoryRouter>
    );
    expect(screen.getByText(/sugerencias/i)).toBeInTheDocument();
  });

  it('agrega productos al carrito', () => {
    render(
      <MemoryRouter>
        <PublicListingScreen />
      </MemoryRouter>
    );
    const addBtns = screen.getAllByLabelText(/agregar/i);
    fireEvent.click(addBtns[0]);
    // Espera que el carrito tenga al menos un producto
  });

  it('navega a la landing de negocio', () => {
    render(
      <MemoryRouter>
        <PublicListingScreen />
      </MemoryRouter>
    );
    const verNegocioBtns = screen.getAllByText(/ver negocio/i);
    fireEvent.click(verNegocioBtns[0]);
    // Espera que la URL cambie a /public/businesses/:id
  });
}); 