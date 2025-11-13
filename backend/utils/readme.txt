# Módulo de Visualização de Dados
## Desenvolvido por: João

## Visão Geral

Este módulo é responsável por transformar dados brutos em visualizações interativas e informativas. 
Utiliza bibliotecas avançadas de visualização para criar gráficos que facilitam a compreensão e 
análise exploratória dos dados.

## Arquitetura e Responsabilidades

### Arquivo Principal
- *visualizador_dados.py*: Contém a classe VisualizadorDados com todas as funcionalidades de visualização

### Classe VisualizadorDados

Classe principal que gerencia a criação de todos os tipos de visualizações do sistema.

#### Atributos
- data: DataFrame pandas com os dados a serem visualizados
- Configurações de estilo: Define tema visual consistente

## Funcionalidades Principais

### 1. Gráfico de Distribuição

python
def plot_distribution(self, column, plot_type='histogram')


*Tipos Suportados*:
- *Histogram*: Distribuição de frequências
- *Box Plot*: Visualização de quartis e outliers
- *Violin Plot*: Combinação de box plot com densidade

*Características*:
- Detecta automaticamente tipo de variável (numérica/categórica)
- Ajusta número de bins automaticamente para histogramas
- Exibe estatísticas no gráfico (média, mediana)
- Identifica outliers em box plots

*Aplicações*:
- Análise de normalidade de variáveis
- Identificação de valores atípicos
- Comparação de distribuições

### 2. Matriz de Correlação

python
def plot_correlation_heatmap(self)


*Funcionalidade*:
- Calcula correlação de Pearson entre todas variáveis numéricas
- Gera heatmap colorido com escala de -1 a 1
- Adiciona valores numéricos em cada célula
- Identifica correlações fortes (>0.7 ou <-0.7)

*Interpretação*:
- Vermelho: correlação positiva forte
- Azul: correlação negativa forte
- Branco/Cinza: sem correlação

*Utilidade*:
- Detectar multicolinearidade
- Identificar features redundantes
- Encontrar relações entre variáveis

### 3. Gráfico de Barras

python
def plot_categorical_counts(self, column, top_n=10)


*Descrição*:
- Conta frequência de cada categoria
- Ordena por frequência decrescente
- Mostra top N categorias mais frequentes

*Customizações*:
- Número de categorias exibidas ajustável
- Cores diferentes para cada barra
- Rótulos de valor em cada barra

*Aplicação*:
- Análise de variáveis categóricas
- Identificação de classes dominantes
- Visualização de distribuição de grupos

### 4. Gráfico de Pizza

python
def plot_pie_chart(self, column, top_n=6)


*Características*:
- Agrupa categorias menos frequentes em "Outros"
- Exibe percentuais em cada fatia
- Cores distintas e legenda clara

*Limitações*:
- Recomendado para até 6-8 categorias
- Não ideal para muitas categorias pequenas

*Uso Ideal*:
- Proporções de categorias principais
- Visualização de composição percentual

### 5. Gráfico de Dispersão

python
def plot_scatter(self, x_col, y_col, color_col=None)


*Funcionalidades*:
- Relação entre duas variáveis numéricas
- Opção de colorir por terceira variável (categórica)
- Linha de tendência opcional
- Tamanho de pontos ajustável

*Análises Possíveis*:
- Correlação visual entre variáveis
- Identificação de clusters
- Detecção de padrões não-lineares

*Interatividade*:
- Zoom e pan
- Hover para ver valores exatos
- Seleção de pontos específicos

### 6. Mapa Geográfico

python
def plot_geographic_map(self, location_col, value_col=None, map_type='choropleth')


*Tipos de Mapa*:

*Choropleth (Coroplético)*:
- Países/regiões coloridos por intensidade
- Escala de cores para valores numéricos
- Ideal para distribuições geográficas

*Scatter Geo*:
- Pontos no mapa por localização
- Tamanho proporcional a valores
- Melhor para dados pontuais

*Funcionalidades*:
- Detecção automática de nomes de países
- Suporte para coordenadas lat/long
- Informações detalhadas no hover

*Validações*:
- Verifica nomes de países válidos
- Trata valores ausentes geograficamente
- Normaliza nomes de países (inglês padrão)

### 7. Visualização de Valores Faltantes

python
def plot_missing_values(self)


*Análise*:
- Identifica colunas com dados faltantes
- Gera gráfico de barras horizontal
- Ordena por quantidade de valores nulos

*Utilidade*:
- Diagnóstico de qualidade de dados
- Decisão sobre estratégia de imputação
- Identificação de problemas na coleta

## Integração com Sistema

### Com Backend (app.py)
- Endpoint /api/visualize usa este módulo
- Retorna HTML dos gráficos para frontend

### Com Carregador de Dados
- Recebe DataFrame preprocessado
- Valida tipos de colunas antes de plotar

### Com Frontend React
- Gráficos retornados como HTML interativo
- Renderizados com dangerouslySetInnerHTML
- Mantém interatividade do Plotly

## Tecnologias Utilizadas

### Plotly 5.18.0
*Principal biblioteca de visualização*
- Gráficos interativos e responsivos
- Suporte a zoom, pan, hover
- Exportação para imagens
- Tema customizável

### Matplotlib 3.8.2
*Visualizações estáticas*
- Fallback para gráficos simples
- Maior controle de formatação
- Integração com pandas

### Seaborn 0.13.0
*Visualizações estatísticas*
- Paletas de cores profissionais
- Gráficos estatísticos avançados
- Integração com matplotlib

## Configurações de Estilo

### Paleta de Cores
- Esquema consistente em todo sistema
- Cores acessíveis (contraste adequado)
- Diferenciação clara entre categorias

### Tipografia
- Tamanhos de fonte legíveis
- Rótulos claros e concisos
- Títulos descritivos

### Layout
- Grid para melhor leitura
- Margens apropriadas
- Legendas posicionadas estrategicamente

## Otimizações de Performance

### Para Grandes Datasets
- Amostragem inteligente para scatter plots
- Agregação para gráficos de barras
- Simplificação de polígonos em mapas

### Renderização
- Geração assíncrona de gráficos
- Cache de visualizações comuns
- Lazy loading no frontend

## Exemplos de Uso

### Criar Histograma
python
from utils.visualizador_dados import VisualizadorDados

visualizador = VisualizadorDados(dataframe)
fig = visualizador.plot_distribution('idade', 'histogram')
html = fig.to_html(full_html=False)


### Gerar Mapa de Correlação
python
fig = visualizador.plot_correlation_heatmap()
fig.show()


### Plotar Dispersão com Cor
python
fig = visualizador.plot_scatter('x', 'y', color_col='categoria')


## Tratamento de Casos Especiais

### Dados Vazios
- Verifica se DataFrame não está vazio
- Retorna mensagem apropriada
- Evita erros de renderização

### Valores Outliers
- Ajusta escala automaticamente
- Opção de remover outliers do plot
- Mantém informação original

### Muitas Categorias
- Agrupa categorias menores
- Limita número de items exibidos
- Mantém "Outros" para restante

## Acessibilidade

### Cores
- Paletas daltonism-friendly
- Contraste adequado
- Alternativas além de cor (padrões)

### Interatividade
- Tooltips informativos
- Zoom acessível por teclado
- Exportação para formatos estáticos

## Extensibilidade

### Adicionar Novos Gráficos
python
def plot_novo_grafico(self, params):
    fig = go.Figure()
    return fig


### Customizar Estilos
- Templates Plotly customizados
- Temas por contexto (claro/escuro)
- Branding corporativo

## Boas Práticas Implementadas

1. *Validação de Entrada*: Verifica tipos e valores antes de plotar
2. *Tratamento de Erros*: Try-catch com mensagens claras
3. *Documentação*: Docstrings em todos os métodos
4. *Reutilização*: Funções auxiliares para código comum
5. *Padrões*: Seguir guia de estilo de visualização

## Padrões de Visualização

### Cores Semânticas
- Verde: positivo, sucesso
- Vermelho: negativo, alerta
- Azul: neutro, informativo
- Amarelo: atenção, warning

### Hierarquia Visual
- Título: maior e mais destacado
- Subtítulo: contexto adicional
- Rótulos: menor mas legível
- Anotações: mínimas e relevantes

## Contribuição para o Sistema

Este módulo é essencial pois:
- Facilita compreensão de dados complexos
- Permite descoberta de padrões
- Comunica insights visualmente
- Melhora experiência do usuário
- Suporta tomada de decisão baseada em dados

## Desenvolvedor

*João*
- Responsável pelo módulo de visualização
- Implementação de gráficos interativos
- Otimização de performance visual
- Integração com Plotly e bibliotecas de visualização

## Roadmap Futuro

- Gráficos 3D interativos
- Animações temporais
- Dashboards customizáveis
- Exportação para PowerPoint
- Temas dark/light mode
- Gráficos de séries temporais avançados

## Notas Técnicas

- Todos os gráficos são interativos por padrão
- HTML gerado é standalone (sem dependências externas)
- Compatível com todos navegadores modernos
- Responsivo para mobile
- Performance otimizada para datasets médios (até 100k linhas)
