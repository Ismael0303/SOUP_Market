import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App';
import { MemoryRouter } from 'react-router-dom';

describe('SPA Navigation', () => {
  it('sidebar está presente y se puede navegar', () => {
    render(
      <MemoryRouter initialEntries={['/dashboard/products']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText('Productos')).toBeInTheDocument();
    // Puedes extender este test para simular clicks y navegación
  });
}); 