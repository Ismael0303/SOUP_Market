import React from 'react';

const ThemeToggle = ({ dark, setDark }) => (
  <button
    onClick={() => setDark(d => !d)}
    className="ml-4 px-3 py-2 rounded-lg bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100 font-semibold transition-colors"
    aria-label="Alternar modo oscuro"
  >
    {dark ? '🌙 Modo Oscuro' : '☀️ Modo Claro'}
  </button>
);

export default ThemeToggle; 