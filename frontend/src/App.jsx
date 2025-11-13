import React, { useState } from 'react';
import Upload from './components/Upload';
import Analysis from './components/Analysis';
import Visualizations from './components/Visualizations';
import ML from './components/ML';
import Navigation from './components/Navigation';
import Alert from './components/Alert';

function App() {
  const [currentPage, setCurrentPage] = useState('upload');
  const [data, setData] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const showMessage = (msg) => {
    setMessage(msg);
    setError('');
    setTimeout(() => setMessage(''), 3000);
  };

  const showError = (err) => {
    setError(err);
    setMessage('');
  };

  return (
    <div>
      <div className="header">
        <h1>Sistema de Análise de Dados</h1>
      </div>

      <Navigation
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
        hasData={!!data}
      />

      <div className="container">
        <Alert message={message} error={error} />

        {currentPage === 'upload' && (
          <Upload
            setData={setData}
            showMessage={showMessage}
            showError={showError}
            setCurrentPage={setCurrentPage}
          />
        )}

        {currentPage === 'analysis' && data && (
          <Analysis data={data} showError={showError} />
        )}

        {currentPage === 'visualizations' && data && (
          <Visualizations data={data} showError={showError} />
        )}

        {currentPage === 'ml' && data && (
          <ML data={data} showMessage={showMessage} showError={showError} />
        )}
      </div>
    </div>
  );
}

export default App;
