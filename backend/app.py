from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from utils.carregador_dados import CarregadorDados
from utils.visualizador_dados import VisualizadorDados
from utils.modelos_ml import GerenciadorModelosML

MODEL_MAP = {
    'random_forest': 'Random Forest',
    'decision_tree': 'Decision Tree',
    'knn': 'K-Nearest Neighbors',
    'logistic_regression': 'Logistic Regression'
}

app = Flask(__name__)
CORS(app)

carregador_dados = CarregadorDados()
gerenciador_ml = GerenciadorModelosML()

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        print('Recebendo upload...')
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Arquivo vazio'}), 400
        
        print(f'Lendo arquivo: {file.filename}')
        df = pd.read_csv(file)
        print(f'Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas')
        
        # Converter NaN para None para JSON válido
        df = df.astype(object).where(pd.notna(df), None)
        
        return jsonify({
            'data': df.to_dict('records'),
            'columns': df.columns.tolist(),
            'shape': df.shape
        })
    except Exception as e:
        print(f'Erro no upload: {str(e)}')
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
        
        df = pd.DataFrame(data).convert_dtypes()
        visualizador = VisualizadorDados(df)
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
        
        charts = {}
        
        if len(numeric_cols) > 0:
            dist_fig = visualizador.plot_distribution(numeric_cols[0])
            charts['distribution'] = dist_fig.to_html(full_html=False)
        
        if len(numeric_cols) > 1:
            corr_fig = visualizador.plot_correlation_heatmap()
            charts['correlation'] = corr_fig.to_html(full_html=False)
        
        if len(categorical_cols) > 0:
            pie_fig = visualizador.plot_pie_chart(categorical_cols[0])
            charts['pie'] = pie_fig.to_html(full_html=False)
        
        if 'Country' in df.columns or 'country' in df.columns:
            location_col = 'Country' if 'Country' in df.columns else 'country'
            try:
                geo_fig = visualizador.plot_geographic_map(location_col)
                charts['geographic'] = geo_fig.to_html(full_html=False)
            except:
                pass  
        
        return jsonify(charts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/train', methods=['POST'])
def train_model():
    try:
        data = request.json.get('data')
        model_type = request.json.get('model_type')
        target_column = request.json.get('target_column')
        test_size = request.json.get('test_size', 0.2)
        
        if not data or not model_type or not target_column:
            return jsonify({'error': 'Dados incompletos'}), 400
        
        df = pd.DataFrame(data).convert_dtypes()
        model_key = MODEL_MAP.get(model_type)
        if not model_key:
            return jsonify({'error': 'Modelo não suportado'}), 400
        
        if target_column not in df.columns:
            return jsonify({'error': 'Coluna alvo não encontrada'}), 400
        
        X = df.drop(columns=[target_column])
        y = df[target_column].fillna('Missing')

        gerenciador_ml.prepare_data(X, y, test_size=test_size)
        gerenciador_ml.train_model(model_key)
        metrics = gerenciador_ml.evaluate_model()

        # Gerar gráficos
        import plotly.graph_objects as go
        import plotly.express as px
        
        # Matriz de confusão
        cm = metrics['confusion_matrix']
        fig_cm = px.imshow(cm, 
                          text_auto=True,
                          labels=dict(x="Predito", y="Real", color="Quantidade"),
                          title="Matriz de Confusão",
                          color_continuous_scale='Blues')
        fig_cm.update_layout(template='plotly_white', height=500)
        
        # Importância de features (se disponível)
        feature_importance_html = None
        importance_df = gerenciador_ml.get_feature_importance()
        if importance_df is not None:
            top_features = importance_df.head(15)
            fig_importance = px.bar(top_features, 
                                   x='importance', 
                                   y='feature',
                                   orientation='h',
                                   title='Top 15 - Importância das Features',
                                   labels={'importance': 'Importância', 'feature': 'Feature'})
            fig_importance.update_layout(template='plotly_white', height=500)
            feature_importance_html = fig_importance.to_html(full_html=False)

        response_payload = {
            'accuracy': metrics['accuracy'],
            'precision': metrics['precision'],
            'recall': metrics['recall'],
            'f1_score': metrics['f1_score'],
            'train_accuracy': metrics['train_accuracy'],
            'confusion_matrix': metrics['confusion_matrix'],
            'classification_report': metrics['classification_report'],
            'confusion_matrix_plot': fig_cm.to_html(full_html=False),
            'feature_importance_plot': feature_importance_html
        }

        return jsonify(response_payload)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json.get('data')
        model_type = request.json.get('model_type')
        
        if not data or not model_type:
            return jsonify({'error': 'Dados incompletos'}), 400
        
        df = pd.DataFrame(data).convert_dtypes()
        
        predictions = gerenciador_ml.predict(df)
        
        return jsonify({'predictions': predictions.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
