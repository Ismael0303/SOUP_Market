import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import MessageBox from '../components/MessageBox';

describe('MessageBox', () => {
  it('muestra el mensaje y tipo', () => {
    render(<MessageBox message="¡Éxito!" type="success" onClose={() => {}} />);
    expect(screen.getByText('¡Éxito!')).toBeInTheDocument();
  });
  it('llama a onClose al hacer click en cerrar', () => {
    const onClose = jest.fn();
    render(<MessageBox message="Error" type="error" onClose={onClose} />);
    fireEvent.click(screen.getByRole('button'));
    expect(onClose).toHaveBeenCalled();
  });
}); 