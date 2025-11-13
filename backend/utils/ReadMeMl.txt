# Módulo de Machine Learning
## Desenvolvido por: João Victor
## Visão Geral

Este módulo implementa o núcleo de inteligência artificial do sistema, fornecendo algoritmos de 
machine learning para classificação, treinamento de modelos e predição. É responsável por toda 
a pipeline de aprendizado de máquina, desde a preparação até a avaliação.

## Arquitetura e Responsabilidades

### Arquivo Principal
- *modelos_ml.py*: Contém a classe GerenciadorModelosML com implementações de algoritmos de ML

### Classe GerenciadorModelosML

Classe central que gerencia todo o ciclo de vida dos modelos de machine learning.

#### Atributos Principais
- model: Modelo treinado atual
- model_name: Nome do modelo em uso
- X_train, X_test: Conjuntos de treino e teste (features)
- y_train, y_test: Conjuntos de treino e teste (target)
- feature_names: Nomes das features utilizadas

## Modelos Implementados

### 1. Random Forest (Floresta Aleatória)

*Classe*: RandomForestClassifier

*Características*:
- Ensemble de múltiplas árvores de decisão
- Reduz overfitting através de agregação
- Fornece importância de features

*Hiperparâmetros*:
- n_estimators: Número de árvores (10-200, padrão: 100)
- max_depth: Profundidade máxima (2-50, padrão: 10)
- min_samples_split: Amostras mínimas para split (2-20, padrão: 2)

*Vantagens*:
- Robusto a outliers
- Lida bem com dados não-lineares
- Baixo risco de overfitting

*Aplicações Ideais*:
- Problemas de classificação complexos
- Datasets com muitas features
- Quando importância de variáveis é relevante

### 2. Decision Tree (Árvore de Decisão)

*Classe*: DecisionTreeClassifier

*Características*:
- Modelo de decisão baseado em regras
- Fácil interpretação e visualização
- Aprendizado rápido

*Hiperparâmetros*:
- max_depth: Profundidade máxima (2-30, padrão: 5)
- min_samples_split: Amostras mínimas (2-20, padrão: 2)
- min_samples_leaf: Amostras mínimas na folha (1-10, padrão: 1)

*Vantagens*:
- Interpretabilidade alta
- Não requer normalização
- Captura relações não-lineares

*Desvantagens*:
- Tendência a overfitting
- Instável (pequenas mudanças nos dados alteram árvore)

*Aplicações Ideais*:
- Quando interpretabilidade é crucial
- Problemas com regras de decisão claras
- Prototipagem rápida

### 3. K-Nearest Neighbors (KNN)

*Classe*: KNeighborsClassifier

*Características*:
- Baseado em proximidade no espaço de features
- Não paramétrico (sem suposições sobre distribuição)
- Lazy learning (não treina modelo explícito)

*Hiperparâmetros*:
- n_neighbors: Número de vizinhos (3-20, padrão: 5)
- weights: Peso dos vizinhos ('uniform' ou 'distance')
- metric: Métrica de distância ('euclidean', 'manhattan')

*Vantagens*:
- Simples e intuitivo
- Eficaz para dados bem separados
- Funciona bem com poucas features

*Desvantagens*:
- Lento para predição em grandes datasets
- Sensível a escala das features
- Requer normalização

*Aplicações Ideais*:
- Datasets pequenos a médios
- Problemas com fronteiras complexas
- Sistemas de recomendação

### 4. Logistic Regression (Regressão Logística)

*Classe*: LogisticRegression

*Características*:
- Modelo linear para classificação
- Probabilístico (retorna probabilidades de classe)
- Rápido e eficiente

*Hiperparâmetros*:
- C: Regularização inversa (0.01-10, padrão: 1.0)
- penalty: Tipo de regularização ('l1', 'l2', 'none')
- max_iter: Iterações máximas (100-1000, padrão: 100)

*Vantagens*:
- Treinamento rápido
- Baixo overfitting
- Fornece probabilidades calibradas

*Desvantagens*:
- Assume linearidade
- Não captura interações complexas

*Aplicações Ideais*:
- Baseline para comparação
- Problemas linearmente separáveis
- Quando velocidade é crucial

## Funcionalidades Principais

### 1. Preparação de Dados

python
def prepare_data(self, X, y, test_size=0.2, random_state=42)


*Processo*:
- Divide dados em treino e teste
- Embaralha dados aleatoriamente
- Mantém proporção de classes (stratify)
- Armazena feature names

*Validações*:
- Verifica se X e y têm mesmo número de linhas
- Garante que há dados suficientes para split
- Valida tipos de dados

### 2. Treinamento de Modelo

python
def train_model(self, model_name, **params)


*Etapas*:
1. Seleciona modelo pelo nome
2. Instancia com parâmetros fornecidos
3. Treina no conjunto de treino
4. Armazena modelo treinado

*Parâmetros*:
- model_name: Nome do modelo (string)
- **params: Hiperparâmetros específicos do modelo

*Retorno*: Modelo treinado

### 3. Avaliação de Modelo

python
def evaluate_model(self)


*Métricas Calculadas*:

*Acurácia (Accuracy)*:
- Proporção de predições corretas
- Fórmula: (VP + VN) / Total
- Range: 0-1 (quanto maior, melhor)

*Precisão (Precision)*:
- Proporção de positivos corretos entre predições positivas
- Fórmula: VP / (VP + FP)
- Importante quando custo de falso positivo é alto

*Recall (Revocação)*:
- Proporção de positivos identificados corretamente
- Fórmula: VP / (VP + FN)
- Importante quando custo de falso negativo é alto

*F1-Score*:
- Média harmônica de precisão e recall
- Fórmula: 2 * (Precision * Recall) / (Precision + Recall)
- Balanceia precisão e recall

*Matriz de Confusão*:
- VP (Verdadeiros Positivos): acertos na classe positiva
- VN (Verdadeiros Negativos): acertos na classe negativa
- FP (Falsos Positivos): erros tipo I
- FN (Falsos Negativos): erros tipo II

*Relatório de Classificação*:
- Métricas detalhadas por classe
- Support (número de amostras por classe)
- Médias (macro, weighted)

### 4. Importância de Features

python
def get_feature_importance(self)


*Funcionalidade*:
- Extrai importância de cada feature
- Disponível para Random Forest e Decision Tree
- Retorna DataFrame ordenado por importância

*Aplicação*:
- Seleção de features
- Entendimento do modelo
- Redução de dimensionalidade

### 5. Predição

python
def predict(self, X)


*Processo*:
- Valida formato dos dados
- Aplica modelo treinado
- Retorna classes preditas

*Validações*:
- Verifica se modelo foi treinado
- Confirma número de features correto
- Garante tipos de dados compatíveis

### 6. Salvamento e Carregamento

python
def save_model(self, filepath)
def load_model(self, filepath)


*Persistência*:
- Usa joblib para serialização eficiente
- Salva modelo completo e metadados
- Permite reutilização sem retreinamento

## Pipeline de Machine Learning

### Fluxo Completo

1. *Preparação*:
   - Dados preprocessados pelo carregador
   - Split treino/teste

2. *Treinamento*:
   - Seleção de modelo
   - Configuração de hiperparâmetros
   - Fit nos dados de treino

3. *Avaliação*:
   - Predição no conjunto de teste
   - Cálculo de métricas
   - Análise de erros

4. *Otimização* (opcional):
   - Ajuste de hiperparâmetros
   - Cross-validation
   - Grid search

5. *Deploy*:
   - Salvamento do modelo
   - Uso em produção para predições

## Integração com Sistema

### Com Backend (app.py)
- Endpoint /api/train: treina modelo
- Endpoint /api/predict: faz predições
- Retorna métricas formatadas para frontend

### Com Carregador de Dados
- Recebe dados preprocessados
- Usa encoders para consistência
- Valida formato de entrada

### Com Frontend React
- Recebe configurações de usuário
- Exibe métricas visualmente
- Permite retreinamento interativo

## Tecnologias Utilizadas

### Scikit-learn 1.3.2

*Algoritmos*:
- Modelos de classificação prontos
- Pipeline de preprocessamento
- Métricas de avaliação

*Utilidades*:
- train_test_split: divisão de dados
- Métricas: accuracy, precision, recall, f1
- Confusion matrix: matriz de confusão

### Joblib 1.3.2

*Serialização*:
- Salvamento eficiente de modelos
- Compressão automática
- Compatibilidade entre versões

## Boas Práticas Implementadas

### 1. Validação de Dados
- Verifica tipos antes de treinar
- Valida dimensões de arrays
- Trata valores nulos

### 2. Random State
- Seed fixo para reprodutibilidade
- Resultados consistentes
- Facilita debugging

### 3. Stratify
- Mantém proporção de classes no split
- Evita viés em dados desbalanceados
- Melhora generalização

### 4. Avaliação Completa
- Múltiplas métricas
- Treino e teste separados
- Relatório detalhado

## Otimizações de Performance

### Para Grandes Datasets
- Batch prediction
- Modelos mais simples (Logistic Regression)
- Sampling estratificado

### Para Muitas Features
- Random Forest (lida bem)
- Seleção de features importante
- Redução de dimensionalidade

## Tratamento de Casos Especiais

### Classes Desbalanceadas
- class_weight='balanced' em alguns modelos
- SMOTE para oversampling (extensão futura)
- Métricas apropriadas (F1 em vez de accuracy)

### Overfitting
- Regularização (L1, L2)
- Limitação de profundidade
- Early stopping

### Underfitting
- Modelos mais complexos (Random Forest)
- Mais features
- Engenharia de features

## Exemplo de Uso Completo

python
from utils.modelos_ml import GerenciadorModelosML

gerenciador = GerenciadorModelosML()

gerenciador.prepare_data(X, y, test_size=0.2)

gerenciador.train_model('Random Forest', 
                        n_estimators=100, 
                        max_depth=10)

metrics = gerenciador.evaluate_model()
print(f"Acurácia: {metrics['test_accuracy']:.2%}")

gerenciador.save_model('modelo_final.pkl')

predictions = gerenciador.predict(X_novo)


## Contribuição para o Sistema

Este módulo é o coração da inteligência do sistema:
- Permite predições automatizadas
- Fornece insights baseados em dados
- Suporta tomada de decisão
- Escalável para novos algoritmos
- Base para features avançadas de IA

## Desenvolvedor

*Erick Borger*
- Responsável pelo módulo de machine learning
- Implementação de algoritmos de classificação
- Otimização de hiperparâmetros
- Pipeline de treinamento e avaliação

## Roadmap Futuro

- Modelos de regressão
- Deep learning com TensorFlow
- AutoML para otimização automática
- Ensemble methods customizados
- Explicabilidade (SHAP, LIME)
- Online learning
- Transfer learning

## Notas Técnicas

- Compatível com scikit-learn API
- Modelos serializáveis
- Thread-safe para produção
- Logging detalhado para debugging
- Métricas customizáveis por problema
