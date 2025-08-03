import React from 'react';
import { Link } from 'react-router-dom';

// Recibe un array de objetos: [{ label: 'Dashboard', to: '/dashboard' }, ...]
const Breadcrumbs = ({ items }) => (
  <nav className="text-sm text-gray-500 mb-6" aria-label="Breadcrumb">
    <ol className="list-none p-0 inline-flex">
      {items.map((item, idx) => (
        <li key={idx} className="flex items-center">
          {item.to ? (
            <Link to={item.to} className="hover:underline">{item.label}</Link>
          ) : (
            <span className="text-blue-600 font-semibold">{item.label}</span>
          )}
          {idx < items.length - 1 && <span className="mx-2">/</span>}
        </li>
      ))}
    </ol>
  </nav>
);

export default Breadcrumbs; 