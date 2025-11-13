import React from 'react';

function Alert({ message, error }) {
  if (!message && !error) return null;

  return (
    <>
      {message && <div className="alert alert-success">{message}</div>}
      {error && <div className="alert alert-error">{error}</div>}
    </>
  );
}

export default Alert;
