import React, { useState } from 'react';
import StatBox from './StatBox';

function Analysis({ data, showError }) {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalysis = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: data.data })
      });

      const result = await response.json();

      if (response.ok) {
        setAnalysis(result);
      } else {
        showError(result.error || 'Erro na análise');
      }
    } catch (err) {
      showError('Erro ao conectar com o servidor');
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Análise Estatística</h2>
      <button className="btn" onClick={handleAnalysis} disabled={loading}>
        {loading ? 'Analisando...' : 'Realizar Análise'}
      </button>

      {analysis && (
        <>
          <div className="stats">
            <StatBox title="Total de Registros" value={analysis.total_rows} />
            <StatBox title="Total de Colunas" value={analysis.total_columns} />
            <StatBox title="Valores Nulos" value={analysis.null_values} />
          </div>

          <h3>Estatísticas Descritivas</h3>
          <div style={{ overflowX: 'auto' }}>
            <table>
              <thead>
                <tr>
                  <th>Coluna</th>
                  <th>Média</th>
                  <th>Mediana</th>
                  <th>Desvio Padrão</th>
                  <th>Mínimo</th>
                  <th>Máximo</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(analysis.statistics).map(([col, stats]) => (
                  <tr key={col}>
                    <td>{col}</td>
                    <td>{stats.mean?.toFixed(2) || 'N/A'}</td>
                    <td>{stats.median?.toFixed(2) || 'N/A'}</td>
                    <td>{stats.std?.toFixed(2) || 'N/A'}</td>
                    <td>{stats.min?.toFixed(2) || 'N/A'}</td>
                    <td>{stats.max?.toFixed(2) || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}

export default Analysis;
