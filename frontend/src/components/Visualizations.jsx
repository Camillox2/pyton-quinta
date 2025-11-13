import React, { useState, useEffect, useRef } from 'react';

function Visualizations({ data, showError }) {
  const [charts, setCharts] = useState(null);
  const [loading, setLoading] = useState(false);
  const distRef = useRef(null);
  const corrRef = useRef(null);
  const pieRef = useRef(null);
  const geoRef = useRef(null);

  useEffect(() => {
    if (charts) {
      // Injetar e executar scripts do Plotly
      if (charts.distribution && distRef.current) {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = charts.distribution;
        distRef.current.innerHTML = '';
        distRef.current.appendChild(tempDiv);
        
        // Executar scripts
        const scripts = tempDiv.getElementsByTagName('script');
        Array.from(scripts).forEach(script => {
          const newScript = document.createElement('script');
          newScript.text = script.text;
          distRef.current.appendChild(newScript);
        });
      }
      
      if (charts.correlation && corrRef.current) {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = charts.correlation;
        corrRef.current.innerHTML = '';
        corrRef.current.appendChild(tempDiv);
        
        const scripts = tempDiv.getElementsByTagName('script');
        Array.from(scripts).forEach(script => {
          const newScript = document.createElement('script');
          newScript.text = script.text;
          corrRef.current.appendChild(newScript);
        });
      }
      
      if (charts.pie && pieRef.current) {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = charts.pie;
        pieRef.current.innerHTML = '';
        pieRef.current.appendChild(tempDiv);
        
        const scripts = tempDiv.getElementsByTagName('script');
        Array.from(scripts).forEach(script => {
          const newScript = document.createElement('script');
          newScript.text = script.text;
          pieRef.current.appendChild(newScript);
        });
      }
      
      if (charts.geographic && geoRef.current) {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = charts.geographic;
        geoRef.current.innerHTML = '';
        geoRef.current.appendChild(tempDiv);
        
        const scripts = tempDiv.getElementsByTagName('script');
        Array.from(scripts).forEach(script => {
          const newScript = document.createElement('script');
          newScript.text = script.text;
          geoRef.current.appendChild(newScript);
        });
      }
    }
  }, [charts]);

  const handleVisualize = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/visualize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: data.data })
      });

      const result = await response.json();

      if (response.ok) {
        setCharts(result);
      } else {
        showError(result.error || 'Erro na visualização');
      }
    } catch (err) {
      console.error('Error fetching charts:', err);
      showError('Erro ao conectar com o servidor');
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Visualizações</h2>
      <button className="btn" onClick={handleVisualize} disabled={loading}>
        {loading ? 'Gerando...' : 'Gerar Gráficos'}
      </button>

      {charts && (
        <div>
          {charts.distribution && (
            <div style={{ marginBottom: '2rem' }}>
              <h3>Distribuição de Valores</h3>
              <div ref={distRef}></div>
            </div>
          )}
          {charts.pie && (
            <div style={{ marginBottom: '2rem' }}>
              <h3>Gráfico de Pizza</h3>
              <div ref={pieRef}></div>
            </div>
          )}
          {charts.correlation && (
            <div style={{ marginBottom: '2rem' }}>
              <h3>Matriz de Correlação</h3>
              <div ref={corrRef}></div>
            </div>
          )}
          {charts.geographic && (
            <div style={{ marginBottom: '2rem' }}>
              <h3>Distribuição Geográfica</h3>
              <div ref={geoRef}></div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Visualizations;
