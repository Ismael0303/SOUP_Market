import React from 'react';

const MessageBox = ({ message, type = 'info', onClose }) => {
  if (!message) return null;
  const base = 'fixed bottom-6 right-6 z-50 px-6 py-4 rounded-lg shadow-lg text-white font-semibold flex items-center';
  const color = type === 'success' ? 'bg-green-600' : type === 'error' ? 'bg-red-600' : 'bg-blue-600';
  return (
    <div className={`${base} ${color}`} role="alert">
      <span>{message}</span>
      <button onClick={onClose} className="ml-4 text-white hover:text-gray-200 text-lg">&times;</button>
    </div>
  );
};

export default MessageBox; 