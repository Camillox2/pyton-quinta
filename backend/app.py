from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from utils.carregador_dados import CarregadorDados
from utils.visualizador_dados import VisualizadorDados
from utils.modelos_ml import GerenciadorModelosML

app = Flask(__name__)
CORS(app)

carregador_dados = CarregadorDados()
visualizador = VisualizadorDados()
gerenciador_ml = GerenciadorModelosML()

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Arquivo vazio'}), 400
        
        df = pd.read_csv(file)
        
        return jsonify({
            'data': df.to_dict('records'),
            'columns': df.columns.tolist(),
            'shape': df.shape
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    try:
        data = request.json.get('data')
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        df = pd.DataFrame(data)
        
        stats = {}
        for col in df.select_dtypes(include=['number']).columns:
            stats[col] = {
                'mean': float(df[col].mean()),
                'median': float(df[col].median()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max())
            }
        
        return jsonify({
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'null_values': int(df.isnull().sum().sum()),
            'statistics': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/visualize', methods=['POST'])
def visualize_data():
    try:
        data = request.json.get('data')
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        df = pd.DataFrame(data)
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        charts = {}
        
        if len(numeric_cols) > 0:
            dist_fig = visualizador.plot_distribution(df, numeric_cols[0])
            charts['distribution'] = dist_fig.to_html(full_html=False)
        
        if len(numeric_cols) > 1:
            corr_fig = visualizador.plot_correlation_heatmap(df)
            charts['correlation'] = corr_fig.to_html(full_html=False)
        
        if 'latitude' in df.columns and 'longitude' in df.columns:
            geo_fig = visualizador.plot_geographic_map(df, 'latitude', 'longitude')
            charts['geographic'] = geo_fig.to_html(full_html=False)
        
        return jsonify(charts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/train', methods=['POST'])
def train_model():
    try:
        data = request.json.get('data')
        model_type = request.json.get('model_type')
        target_column = request.json.get('target_column')
        
        if not data or not model_type or not target_column:
            return jsonify({'error': 'Dados incompletos'}), 400
        
        df = pd.DataFrame(data)
        
        if target_column not in df.columns:
            return jsonify({'error': 'Coluna alvo não encontrada'}), 400
        
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        model = gerenciador_ml.train_model(X, y, model_type)
        metrics = gerenciador_ml.evaluate_model(model, X, y)
        
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json.get('data')
        model_type = request.json.get('model_type')
        
        if not data or not model_type:
            return jsonify({'error': 'Dados incompletos'}), 400
        
        df = pd.DataFrame(data)
        
        predictions = gerenciador_ml.predict(model_type, df)
        
        return jsonify({'predictions': predictions.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
