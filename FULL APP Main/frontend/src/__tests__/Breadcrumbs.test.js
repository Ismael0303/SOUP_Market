import React from 'react';
import { render, screen } from '@testing-library/react';
import Breadcrumbs from '../components/Breadcrumbs';
import { MemoryRouter } from 'react-router-dom';

describe('Breadcrumbs', () => {
  it('muestra la ruta completa', () => {
    render(
      <MemoryRouter>
        <Breadcrumbs items={[
          { label: 'Dashboard', to: '/dashboard' },
          { label: 'Productos', to: '/dashboard/products' },
          { label: 'Crear Producto' }
        ]} />
      </MemoryRouter>
    );
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Productos')).toBeInTheDocument();
    expect(screen.getByText('Crear Producto')).toBeInTheDocument();
  });
}); 