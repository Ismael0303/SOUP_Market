import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import AIRecommender from './AIRecommender';

describe('AIRecommender', () => {
  it('renderiza el componente y sugerencias', () => {
    render(
      <MemoryRouter>
        <AIRecommender />
      </MemoryRouter>
    );
    expect(screen.getByText(/sugerencias/i)).toBeInTheDocument();
    // Puedes agregar más asserts según la lógica de sugerencias
  });
}); 