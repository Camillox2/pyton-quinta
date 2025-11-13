from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
import pandas as pd
import joblib


class GerenciadorModelosML:
    MODELS = {
        'Random Forest': RandomForestClassifier,
        'Decision Tree': DecisionTreeClassifier,
        'K-Nearest Neighbors': KNeighborsClassifier,
        'Logistic Regression': LogisticRegression
    }

    MODEL_PARAMS = {
        'Random Forest': {
            'n_estimators': {'type': 'slider', 'min': 10, 'max': 200, 'default': 100, 'step': 10},
            'max_depth': {'type': 'slider', 'min': 2, 'max': 50, 'default': 10, 'step': 1},
            'min_samples_split': {'type': 'slider', 'min': 2, 'max': 20, 'default': 2, 'step': 1}
        },
        'Decision Tree': {
            'max_depth': {'type': 'slider', 'min': 2, 'max': 50, 'default': 10, 'step': 1},
            'min_samples_split': {'type': 'slider', 'min': 2, 'max': 20, 'default': 2, 'step': 1},
            'min_samples_leaf': {'type': 'slider', 'min': 1, 'max': 20, 'default': 1, 'step': 1}
        },
        'K-Nearest Neighbors': {
            'n_neighbors': {'type': 'slider', 'min': 1, 'max': 30, 'default': 5, 'step': 1},
            'weights': {'type': 'select', 'options': ['uniform', 'distance'], 'default': 'uniform'},
            'metric': {'type': 'select', 'options': ['euclidean', 'manhattan', 'minkowski'], 'default': 'euclidean'}
        },
        'Logistic Regression': {
            'C': {'type': 'slider', 'min': 0.1, 'max': 10.0, 'default': 1.0, 'step': 0.1},
            'max_iter': {'type': 'slider', 'min': 100, 'max': 1000, 'default': 100, 'step': 100}
        }
    }

    def __init__(self):
        self.model = None
        self.model_name = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None

    def prepare_data(self, X, y, test_size=0.2, random_state=42):
        self.feature_names = X.columns.tolist() if isinstance(X, pd.DataFrame) else None
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        return self.X_train, self.X_test, self.y_train, self.y_test

    def train_model(self, model_name, params=None):
        if model_name not in self.MODELS:
            raise ValueError(f"Modelo '{model_name}' não disponível")
        if self.X_train is None or self.y_train is None:
            raise ValueError("Dados não preparados. Execute prepare_data() primeiro")
        
        params = params or {}
        model_class = self.MODELS[model_name]
        self.model = model_class(**params)
        self.model_name = model_name
        self.model.fit(self.X_train, self.y_train)
        return self.model

    def evaluate_model(self):
        if self.model is None:
            raise ValueError("Modelo não treinado")
        
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        metrics = {
            'train_accuracy': accuracy_score(self.y_train, y_train_pred),
            'test_accuracy': accuracy_score(self.y_test, y_test_pred),
            'precision': precision_score(self.y_test, y_test_pred, average='weighted', zero_division=0),
            'recall': recall_score(self.y_test, y_test_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(self.y_test, y_test_pred, average='weighted', zero_division=0),
            'confusion_matrix': confusion_matrix(self.y_test, y_test_pred),
            'classification_report': classification_report(self.y_test, y_test_pred, zero_division=0)
        }
        return metrics

    def predict(self, X):
        if self.model is None:
            raise ValueError("Modelo não treinado")
        return self.model.predict(X)

    def get_feature_importance(self):
        if self.model is None:
            raise ValueError("Modelo não treinado")
        
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            feature_names = self.feature_names or [f'Feature {i}' for i in range(len(importances))]
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': importances
            }).sort_values('importance', ascending=False)
            return importance_df
        return None

    def save_model(self, filepath):
        if self.model is None:
            raise ValueError("Modelo não treinado")
        joblib.dump({
            'model': self.model,
            'model_name': self.model_name,
            'feature_names': self.feature_names
        }, filepath)

    def load_model(self, filepath):
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.model_name = model_data['model_name']
        self.feature_names = model_data.get('feature_names')
