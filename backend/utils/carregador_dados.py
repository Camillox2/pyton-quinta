import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


class CarregadorDados:
    def _init_(self):
        self.data = None
        self.label_encoders = {}

    def load_csv(self, file):
        try:
            self.data = pd.read_csv(file)
            return self.data
        except Exception as e:
            raise ValueError(f"Erro ao carregar arquivo CSV: {str(e)}")

    def get_data_info(self):
        if self.data is None:
            return None
        
        info = {
            'n_rows': len(self.data),
            'n_columns': len(self.data.columns),
            'columns': list(self.data.columns),
            'dtypes': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'memory_usage': self.data.memory_usage(deep=True).sum() / 1024**2
        }
        return info

    def get_column_types(self):
        if self.data is None:
            return None
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.data.select_dtypes(include=['object']).columns.tolist()
        
        return {
            'numeric': numeric_cols,
            'categorical': categorical_cols
        }

    def preprocess_data(self, target_column=None):
        if self.data is None:
            raise ValueError("Nenhum dado carregado")
        
        df = self.data.copy()
        
        if target_column and target_column in df.columns:
            y = df[target_column]
            X = df.drop(columns=[target_column])
        else:
            X = df
            y = None
        
        categorical_cols = X.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                X[col] = self.label_encoders[col].fit_transform(X[col].astype(str))
            else:
                X[col] = self.label_encoders[col].transform(X[col].astype(str))
        
        X = X.fillna(X.mean() if len(X.select_dtypes(include=[np.number]).columns) > 0 else 0)
        
        if y is not None and y.dtype == 'object':
            if 'target' not in self.label_encoders:
                self.label_encoders['target'] = LabelEncoder()
                y = self.label_encoders['target'].fit_transform(y.astype(str))
            else:
                y = self.label_encoders['target'].transform(y.astype(str))
        
        return X, y

    def get_statistics(self):
        if self.data is None:
            return None
        return self.data.describe()
        