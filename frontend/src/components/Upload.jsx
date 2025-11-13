import React, { useState } from 'react';

function Upload({ setData, showMessage, showError, setCurrentPage }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      showError('Selecione um arquivo CSV');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      });

      console.log('Response status:', response.status);
      console.log('Response ok:', response.ok);

      const result = await response.json();
      console.log('Result:', result);

      if (response.ok) {
        setData(result);
        showMessage('Arquivo carregado com sucesso');
        setCurrentPage('analysis');
      } else {
        showError(result.error || 'Erro ao carregar arquivo');
      }
    } catch (err) {
      console.error('Erro completo:', err);
      showError('Erro ao conectar com o servidor: ' + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Upload de Arquivo CSV</h2>
      <div className="form-group">
        <label htmlFor="file-input">Selecione um arquivo CSV:</label>
        <input
          id="file-input"
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
        />
      </div>
      <button className="btn" onClick={handleUpload} disabled={loading}>
        {loading ? 'Carregando...' : 'Carregar Arquivo'}
      </button>
    </div>
  );
}

export default Upload;
