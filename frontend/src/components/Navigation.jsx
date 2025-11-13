import React from 'react';

function Navigation({ currentPage, setCurrentPage, hasData }) {
  return (
    <nav className="nav">
      <button
        className={currentPage === 'upload' ? 'active' : ''}
        onClick={() => setCurrentPage('upload')}
      >
        Upload de Dados
      </button>
      <button
        className={currentPage === 'analysis' ? 'active' : ''}
        onClick={() => setCurrentPage('analysis')}
        disabled={!hasData}
      >
        Análise Estatística
      </button>
      <button
        className={currentPage === 'visualizations' ? 'active' : ''}
        onClick={() => setCurrentPage('visualizations')}
        disabled={!hasData}
      >
        Visualizações
      </button>
      <button
        className={currentPage === 'ml' ? 'active' : ''}
        onClick={() => setCurrentPage('ml')}
        disabled={!hasData}
      >
        Machine Learning
      </button>
    </nav>
  );
}

export default Navigation;
