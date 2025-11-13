import { useState, useEffect, useRef } from 'react';
import StatBox from './StatBox';

function ML({ data, showMessage, showError }) {
  const [model, setModel] = useState('random_forest');
  const [targetCol, setTargetCol] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [testSize, setTestSize] = useState(0.2);
  const confusionRef = useRef(null);
  const importanceRef = useRef(null);

  useEffect(() => {
    if (results) {
      // Renderizar matriz de confusão
      if (results.confusion_matrix_plot && confusionRef.current) {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = results.confusion_matrix_plot;
        confusionRef.current.innerHTML = '';
        confusionRef.current.appendChild(tempDiv);
        
        const scripts = tempDiv.getElementsByTagName('script');
        Array.from(scripts).forEach(script => {
          const newScript = document.createElement('script');
          newScript.text = script.text;
          confusionRef.current.appendChild(newScript);
        });
      }
      
      // Renderizar importância de features
      if (results.feature_importance_plot && importanceRef.current) {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = results.feature_importance_plot;
        importanceRef.current.innerHTML = '';
        importanceRef.current.appendChild(tempDiv);
        
        const scripts = tempDiv.getElementsByTagName('script');
        Array.from(scripts).forEach(script => {
          const newScript = document.createElement('script');
          newScript.text = script.text;
          importanceRef.current.appendChild(newScript);
        });
      }
    }
  }, [results]);

  const models = [
    { value: 'random_forest', label: 'Random Forest' },
    { value: 'decision_tree', label: 'Decision Tree' },
    { value: 'knn', label: 'K-Nearest Neighbors' },
    { value: 'logistic_regression', label: 'Logistic Regression' }
  ];

  const handleTrain = async () => {
    if (!targetCol) {
      showError('Selecione a coluna alvo');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/train', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data: data.data,
          model_type: model,
          target_column: targetCol,
          test_size: testSize
        })
      });

      const result = await response.json();

      if (response.ok) {
        setResults(result);
        showMessage('Modelo treinado com sucesso');
      } else {
        showError(result.error || 'Erro no treinamento');
      }
    } catch (err) {
      showError('Erro ao conectar com o servidor');
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Machine Learning</h2>

      <div className="form-group">
        <label htmlFor="model-select">Modelo:</label>
        <select
          id="model-select"
          value={model}
          onChange={(e) => setModel(e.target.value)}
        >
          {models.map(m => (
            <option key={m.value} value={m.value}>{m.label}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="target-select">Coluna Alvo:</label>
        <select
          id="target-select"
          value={targetCol}
          onChange={(e) => setTargetCol(e.target.value)}
        >
          <option value="">Selecione...</option>
          {data.columns.map(col => (
            <option key={col} value={col}>{col}</option>
          ))}
        </select>
      </div>

            <div className="form-group">
        <label htmlFor="test-size">
          Tamanho do Teste: {(testSize * 100).toFixed(0)}%
        </label>
        <input
          id="test-size"
          type="range"
          min="0.1"
          max="0.4"
          step="0.05"
          value={testSize}
          onChange={(e) => setTestSize(parseFloat(e.target.value))}
          style={{ width: "100%" }}
        />
        <small style={{ color: "#666" }}>
          Treino: {((1 - testSize) * 100).toFixed(0)}% | Teste:{" "}
          {(testSize * 100).toFixed(0)}%
        </small>
      </div>

      <button className="btn" onClick={handleTrain} disabled={loading}>
        {loading ? 'Treinando...' : 'Treinar Modelo'}
      </button>

      {results && (
        <div>
          <div className="stats">
            <StatBox
              title="Acurácia (Treino)"
              value={`${(results.train_accuracy * 100).toFixed(2)}%`}
            />
            <StatBox
              title="Acurácia (Teste)"
              value={`${(results.accuracy * 100).toFixed(2)}%`}
            />
            <StatBox
              title="Precisão"
              value={`${(results.precision * 100).toFixed(2)}%`}
            />
            <StatBox
              title="Recall"
              value={`${(results.recall * 100).toFixed(2)}%`}
            />
            <StatBox
              title="F1 Score"
              value={`${(results.f1_score * 100).toFixed(2)}%`}
            />
          </div>

          {results.train_accuracy && results.accuracy && (
            <div style={{ 
              marginTop: '1rem', 
              padding: '1rem', 
              background: Math.abs(results.train_accuracy - results.accuracy) > 0.1 ? '#fff3cd' : '#d4edda',
              borderRadius: '8px',
              border: `1px solid ${Math.abs(results.train_accuracy - results.accuracy) > 0.1 ? '#ffc107' : '#28a745'}`
            }}>
              <strong>
                {Math.abs(results.train_accuracy - results.accuracy) > 0.1 
                  ? ' Possível Overfitting' 
                  : ' Modelo Balanceado'}
              </strong>
              <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.9rem' }}>
                Diferença entre treino e teste: {(Math.abs(results.train_accuracy - results.accuracy) * 100).toFixed(2)}%
              </p>
            </div>
          )}

          {results.confusion_matrix_plot && (
            <div style={{ marginTop: '2rem' }}>
              <h3>Matriz de Confusão</h3>
              <div ref={confusionRef}></div>
            </div>
          )}

          {results.feature_importance_plot && (
            <div style={{ marginTop: '2rem' }}>
              <h3>Importância das Features</h3>
              <div ref={importanceRef}></div>
            </div>
          )}

          {results.classification_report && (
            <div style={{ marginTop: '2rem' }}>
              <h3>Relatório de Classificação</h3>
              <pre style={{ 
                background: '#f5f5f5', 
                padding: '1rem', 
                borderRadius: '8px',
                overflow: 'auto',
                fontSize: '0.9rem'
              }}>
                {results.classification_report}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ML;
