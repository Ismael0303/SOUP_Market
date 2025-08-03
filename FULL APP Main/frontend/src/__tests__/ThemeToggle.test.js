import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ThemeToggle from '../components/ThemeToggle';

describe('ThemeToggle', () => {
  it('muestra el texto correcto y alterna el modo', () => {
    const setDark = jest.fn();
    render(<ThemeToggle dark={false} setDark={setDark} />);
    expect(screen.getByText('☀️ Modo Claro')).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button'));
    expect(setDark).toHaveBeenCalled();
  });
}); 