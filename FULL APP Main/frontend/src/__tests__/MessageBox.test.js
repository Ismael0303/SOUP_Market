import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import MessageBox from '../components/MessageBox';

describe('MessageBox', () => {
  it('muestra el mensaje y aplica la clase según el tipo', () => {
    render(<MessageBox message="¡Éxito!" type="success" onClose={() => {}} />);
    const alert = screen.getByRole('alert');
    expect(alert).toHaveClass('bg-green-600');
    expect(screen.getByText('¡Éxito!')).toBeInTheDocument();
  });

  it('llama a onClose al hacer click en cerrar', () => {
    const onClose = jest.fn();
    render(<MessageBox message="Error" type="error" onClose={onClose} />);
    fireEvent.click(screen.getByRole('button'));
    expect(onClose).toHaveBeenCalled();
  });

  it('no renderiza nada cuando message es vacío', () => {
    const { container } = render(<MessageBox message="" />);
    expect(container.firstChild).toBeNull();
  });
});
