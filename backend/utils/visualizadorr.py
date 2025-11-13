import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype

class VisualizadorDados:
    def __init__(self, data):
        self.data = data
        sns.set_style("whitegrid")

    def plot_distribution(self, column, plot_type='histogram'):
        if column not in self.data.columns:
            raise ValueError(f"Coluna '{column}' não encontrada")

        if is_numeric_dtype(self.data[column]):
            if plot_type == 'histogram':
                fig = px.histogram(self.data, x=column, title=f'Distribuição de {column}', nbins=30)
            elif plot_type == 'box':
                fig = px.box(self.data, y=column, title=f'Box Plot de {column}')
            elif plot_type == 'violin':
                fig = px.violin(self.data, y=column, title=f'Violin Plot de {column}')
        else:
            value_counts = self.data[column].value_counts()
            fig = px.bar(x=value_counts.index, y=value_counts.values, 
                        title=f'Distribuição de {column}', labels={'x': column, 'y': 'Frequência'})
        
        fig.update_layout(template='plotly_white', height=500)
        return fig

    def plot_correlation_heatmap(self):
        numeric_data = self.data.select_dtypes(include='number')
        if numeric_data.shape[1] < 2:
            raise ValueError("Não há colunas numéricas suficientes para correlação")
        
        corr_matrix = numeric_data.corr()
        fig = px.imshow(corr_matrix, text_auto='.2f', title='Matriz de Correlação',
                       color_continuous_scale='RdBu_r', aspect='auto')
        fig.update_layout(height=600, template='plotly_white')
        return fig

    def plot_categorical_counts(self, column, top_n=10):
        if column not in self.data.columns:
            raise ValueError(f"Coluna '{column}' não encontrada")
        
        value_counts = self.data[column].value_counts().head(top_n)
        fig = px.bar(x=value_counts.index, y=value_counts.values, title=f'Top {top_n} - {column}',
                    labels={'x': column, 'y': 'Frequência'}, text=value_counts.values)
        fig.update_traces(textposition='outside')
        fig.update_layout(template='plotly_white', height=500)
        return fig

    def plot_pie_chart(self, column, top_n=8):
        if column not in self.data.columns:
            raise ValueError(f"Coluna '{column}' não encontrada.")
        
        value_counts = self.data[column].value_counts().head(top_n)
        fig = px.pie(values=value_counts.values, names=value_counts.index, 
                    title=f'Distribuição de {column}', hole=0.3)
        fig.update_layout(template='plotly_white', height=500)
        return fig

    def plot_scatter(self, x_column, y_column, color_column=None):
        if x_column not in self.data.columns or y_column not in self.data.columns:
            raise ValueError("Colunas não encontradas")
        
        fig = px.scatter(self.data, x=x_column, y=y_column, color=color_column,
                        title=f'{y_column} vs {x_column}', opacity=0.7)
        fig.update_layout(template='plotly_white', height=500)
        return fig

    def plot_grouped_bar(self, category_col, value_col, group_col):
        grouped_data = self.data.groupby([category_col, group_col])[value_col].mean().reset_index()
        fig = px.bar(grouped_data, x=category_col, y=value_col, color=group_col, barmode='group',
                    title=f'{value_col} por {category_col} e {group_col}')
        fig.update_layout(template='plotly_white', height=500)
        return fig

    def plot_missing_values(self):
        missing = self.data.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        
        if len(missing) == 0:
            return None
        
        fig = px.bar(x=missing.index, y=missing.values, title='Valores Faltantes por Coluna',
                    labels={'x': 'Coluna', 'y': 'Número de Valores Faltantes'}, text=missing.values)
        fig.update_traces(textposition='outside')
        fig.update_layout(template='plotly_white', height=500)
        return fig

    def plot_geographic_map(self, location_column, value_column=None, map_type='choropleth'):
        if location_column not in self.data.columns:
            raise ValueError(f"Coluna '{location_column}' não encontrada")
        
        if value_column and value_column in self.data.columns:
            map_data = self.data.groupby(location_column)[value_column].agg(['count', 'mean']).reset_index()
            map_data.columns = [location_column, 'count', 'avg_value']
        else:
            map_data = self.data[location_column].value_counts().reset_index()
            map_data.columns = [location_column, 'count']
        
        if map_type == 'choropleth':
            fig = px.choropleth(map_data, locations=location_column, locationmode='country names',
                               color='count', hover_name=location_column, hover_data={'count': True},
                               title=f'Distribuição Geográfica por {location_column}',
                               color_continuous_scale='Viridis')
        else:
            fig = px.scatter_geo(map_data, locations=location_column, locationmode='country names',
                                size='count', hover_name=location_column,
                                title=f'Distribuição Geográfica por {location_column}',
                                projection='natural earth')
        
        fig.update_layout(template='plotly_white', height=600, geo=dict(showframe=False, showcoastlines=True))
        return fig