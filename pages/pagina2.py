# pagina2.py
import dash
from dash import html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import unicodedata

# Registro da página
dash.register_page(__name__, path='/pagina2', name='Página 2')

# Carregar dados
file_path = r"C:\Users\julio\OneDrive\Área de Trabalho\BANCO DE DADOS 2019 (TODOS OS BANCOS) - NOVA COLETA - Nova Tabulacao 9 - TABLEAU VERSAO 5 (sentencas por assunto + classe).xlsx"
df = pd.read_excel(file_path, sheet_name='BANCO_DADOS_2019')

# Normalizar nomes de colunas (remover acentos e espaços)
df.columns = [
    unicodedata.normalize('NFKD', col).encode('ascii', 'ignore').decode('ascii').replace(' ', '_')
    for col in df.columns
]

# Converter datas e valores numéricos
df['F2_DATA_INICIO_DISTRIBUICAO'] = pd.to_datetime(df['F2_DATA_INICIO_DISTRIBUICAO'], errors='coerce')
df['F1_ULT_SENTENCA_DATA'] = pd.to_datetime(df['F1_ULT_SENTENCA_DATA'], errors='coerce')
df['F2_VALOR_CAUSA'] = pd.to_numeric(df['F2_VALOR_CAUSA'], errors='coerce')

# Layout da página
layout = html.Div([
    html.H2(
        "ANÁLISE DOS PROCESSOS POR COMARCA E POR TEMPO",
        style={'textAlign': 'center', 'color': '#34495E', 'marginBottom': '30px'}
    ),

    # Filtros
    html.Div([
        html.Div([
            html.Label("Assunto Principal", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='filter_assunto',
                options=[{'label': 'Todos', 'value': 'Todos'}] +
                        [{'label': a, 'value': a} for a in df['F2_ASSUNTO_PRINCIPAL_(nivel_3)'].unique()],
                value='Todos', clearable=False
            )
        ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),
        html.Div([
            html.Label("Posição Ocupada", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='filter_posicao',
                options=[{'label': 'Todos', 'value': 'Todos'}] +
                        [{'label': p, 'value': p} for p in df['F2_POSICAO_OCUPADA_PELO_BANCO'].unique()],
                value='Todos', clearable=False
            )
        ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),
        html.Div([
            html.Label("Classificação Sentença", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='filter_classificacao',
                options=[{'label': 'Todos', 'value': 'Todos'}] +
                        [{'label': c, 'value': c} for c in df['CLASSIFICACAO_SENTENCA'].unique()],
                value='Todos', clearable=False
            )
        ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),
        html.Div([
            html.Label("Banco", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='filter_banco',
                options=[{'label': 'Todos', 'value': 'Todos'}] +
                        [{'label': b, 'value': b} for b in df['BANCO'].unique()],
                value='Todos', clearable=False
            )
        ], style={'width': '19%', 'display': 'inline-block', 'marginRight': '1%'}),
        html.Div([
            html.Label("Comarca", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='filter_comarca',
                options=[{'label': 'Todos', 'value': 'Todos'}] +
                        [{'label': com, 'value': com} for com in df['F1_COMARCA'].unique()],
                value='Todos', clearable=False
            )
        ], style={'width': '19%', 'display': 'inline-block'})
    ], style={'marginBottom': '30px'}),

    # Cards de resumo
    html.Div([
        html.Div([
            html.H4("Comarcas Distintas", style={'marginBottom': '10px'}),
            html.Div(id='card_comarcas', style={'fontSize': '24px', 'color': '#2980B9'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '15px',
                  'backgroundColor': '#ECF0F1', 'borderRadius': '8px', 'textAlign': 'center'}),
        html.Div([
            html.H4("Total Processos", style={'marginBottom': '10px'}),
            html.Div(id='card_total', style={'fontSize': '24px', 'color': '#C0392B'})
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right', 'padding': '15px',
                  'backgroundColor': '#ECF0F1', 'borderRadius': '8px', 'textAlign': 'center'})
    ], style={'marginBottom': '30px'}),

    # Gráfico de barras por comarca com rolagem
    html.Div(
        dcc.Graph(id='bar_comarca', style={'width': '100%', 'height': '1200px'}),
        style={
            'overflowY': 'auto',
            'maxHeight': '800px',
            'border': '1px solid #ccc',
            'padding': '5px',
            'marginBottom': '30px'
        }
    ),

    # Gráfico de linha: Ano de Início do Processo (contagem diária)
    dcc.Graph(id='line_inicio', style={'width': '100%', 'height': '400px', 'marginBottom': '30px'}),

    # Gráfico de linha: Última Sentença (contagem diária)
    dcc.Graph(id='line_ultima', style={'width': '100%', 'height': '400px', 'marginBottom': '30px'})
])

# Função de filtragem
def filter_df(assunto, posicao, classificacao, banco, comarca):
    dff = df.copy()
    if assunto != 'Todos': dff = dff[dff['F2_ASSUNTO_PRINCIPAL_(nivel_3)'] == assunto]
    if posicao != 'Todos': dff = dff[dff['F2_POSICAO_OCUPADA_PELO_BANCO'] == posicao]
    if classificacao != 'Todos': dff = dff[dff['CLASSIFICACAO_SENTENCA'] == classificacao]
    if banco != 'Todos': dff = dff[dff['BANCO'] == banco]
    if comarca != 'Todos': dff = dff[dff['F1_COMARCA'] == comarca]
    return dff

@callback(
    Output('card_comarcas', 'children'),
    Output('card_total', 'children'),
    Output('bar_comarca', 'figure'),
    Output('line_inicio', 'figure'),
    Output('line_ultima', 'figure'),
    Input('filter_assunto', 'value'),
    Input('filter_posicao', 'value'),
    Input('filter_classificacao', 'value'),
    Input('filter_banco', 'value'),
    Input('filter_comarca', 'value')
)
def update_all(assunto, posicao, classificacao, banco, comarca):
    dff = filter_df(assunto, posicao, classificacao, banco, comarca)

    # Cards
    card_comarcas = dff['F1_COMARCA'].nunique()
    card_total = len(dff)

    # Barra Comarca
    counts = dff['F1_COMARCA'].value_counts().reset_index(name='Contagem').sort_values('Contagem')
    counts.columns = ['F1_COMARCA', 'Contagem']
    fig_bar = px.bar(
        counts, x='Contagem', y='F1_COMARCA', orientation='h',
        title='Processos por Comarca', color='Contagem', color_continuous_scale=px.colors.sequential.Plasma
    )
    fig_bar.update_layout(title_x=0.5, bargap=0.05)

    # Linha Inicio (contagem por data)
    inicio = dff['F2_DATA_INICIO_DISTRIBUICAO'].dt.date.value_counts().sort_index().reset_index()
    inicio.columns = ['Data', 'Contagem']
    fig_inicio = px.line(inicio, x='Data', y='Contagem', title='ANO DE INÍCIO DO PROCESSO')
    fig_inicio.update_layout(title_x=0.5)

    # Linha Ultima (contagem por data)
    ultima = dff['F1_ULT_SENTENCA_DATA'].dt.date.value_counts().sort_index().reset_index()
    ultima.columns = ['Data', 'Contagem']
    fig_ultima = px.line(ultima, x='Data', y='Contagem', title='ÚLTIMA SENTENÇA')
    fig_ultima.update_layout(title_x=0.5)

    return card_comarcas, card_total, fig_bar, fig_inicio, fig_ultima
