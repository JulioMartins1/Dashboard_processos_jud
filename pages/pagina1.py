# pagina1.py
import dash
from dash import html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Registro da página
dash.register_page(__name__, path='/', name='Página 1')

# Carregar dados
file_path = r"C:\Users\julio\OneDrive\Área de Trabalho\BANCO DE DADOS 2019 (TODOS OS BANCOS) - NOVA COLETA - Nova Tabulacao 9 - TABLEAU VERSAO 5 (sentencas por assunto + classe).xlsx"
df = pd.read_excel(file_path, sheet_name='BANCO_DADOS_2019')

# Garantir tipo numérico
df['F2_VALOR_CAUSA'] = pd.to_numeric(df['F2_VALOR_CAUSA'], errors='coerce')

# Layout com cores melhoradas e organização visual
layout = html.Div([
    html.H1("PROCESSOS JUDICIAIS ITAÚ, BRADESCO E SANTANDER: VISÃO GERAL",
            style={'textAlign': 'center', 'color': '#34495E', 'marginBottom': '30px'}),

    html.Div([
        html.Div([
            html.Label("Banco:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='dropdown_banco',
                options=[{'label': 'Todos', 'value': 'Todos'}] +
                        [{'label': banco, 'value': banco} for banco in df['BANCO'].unique()],
                value='Todos', searchable=True, clearable=False
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Assunto Principal:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='dropdown_assunto',
                options=[{'label': 'Todos', 'value': 'Todos'}] +
                        [{'label': assunto, 'value': assunto} for assunto in df['F2_ASSUNTO_PRINCIPAL (nível 3)'].unique()],
                value='Todos', searchable=True, clearable=False
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
    ], style={'marginBottom': '25px'}),

    html.Div([
        html.Div([html.H4("Total Processos"), html.Div(id='card_processos', style={'fontSize': '24px', 'color': '#2980B9'})],
                 style={'width': '48%', 'display': 'inline-block', 'padding': '15px',
                        'borderRadius': '8px', 'backgroundColor': '#ECF0F1', 'textAlign': 'center'}),

        html.Div([html.H4("Processos sem Valor"), html.Div(id='card_nao_cadastrado', style={'fontSize': '24px', 'color': '#C0392B'})],
                 style={'width': '48%', 'display': 'inline-block', 'float': 'right', 'padding': '15px',
                        'borderRadius': '8px', 'backgroundColor': '#ECF0F1', 'textAlign': 'center'}),
    ], style={'marginBottom': '30px'}),

    html.Div([
        dcc.Graph(id='grafico_pizza_posicao', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='grafico_pizza_banco', style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
    ], style={'marginBottom': '30px'}),

    dcc.Graph(id='grafico_barras_classificacao'),

    html.Div(id='tabela_estatisticas', style={'marginTop': '30px'})
])

@callback(
    Output('grafico_pizza_posicao', 'figure'),
    Output('grafico_pizza_banco', 'figure'),
    Output('grafico_barras_classificacao', 'figure'),
    Output('card_processos', 'children'),
    Output('card_nao_cadastrado', 'children'),
    Output('tabela_estatisticas', 'children'),
    Input('dropdown_banco', 'value'),
    Input('dropdown_assunto', 'value')
)
def atualizar_dashboard(banco, assunto):
    df_filtrado = df.copy()
    if banco != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['BANCO'] == banco]
    if assunto != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['F2_ASSUNTO_PRINCIPAL (nível 3)'] == assunto]

    pizza_posicao = px.pie(df_filtrado, names='F2 POSIÇÃO OCUPADA PELO BANCO', hole=0.6, title="Posição Ocupada", 
                           color_discrete_sequence=px.colors.sequential.RdBu)
    pizza_posicao.update_traces(textposition='outside', textinfo='percent+label')

    pizza_banco = px.pie(df_filtrado, names='BANCO', hole=0.6, title="Banco", 
                         color_discrete_sequence=px.colors.sequential.RdBu)
    pizza_banco.update_traces(textposition='outside', textinfo='percent+label')

    classificacao_counts = df_filtrado['CLASSIFICAÇÃO SENTENÇA'].value_counts().reset_index()
    classificacao_counts.columns = ['Classificação', 'Quantidade']
    classificacao_counts = classificacao_counts.sort_values('Quantidade', ascending=True)

    barras_classificacao = px.bar(classificacao_counts,
                                  x='Quantidade', y='Classificação', orientation='h',
                                  title="Classificação Sentença",
                                  color='Quantidade', color_continuous_scale=px.colors.sequential.Viridis)

    processos = len(df_filtrado)
    nao_cadastrado = df_filtrado['F2_VALOR_CAUSA'].isna().sum()

    estatisticas = df_filtrado.groupby('BANCO')['F2_VALOR_CAUSA'].agg(['sum', 'mean', 'min', 'max', 'std']).round(2).reset_index()
    estatisticas.columns = ['BANCO', 'Soma', 'Média', 'Mínimo', 'Máximo', 'Desvio Padrão']

    tabela = html.Table([
        html.Thead([html.Tr([html.Th(col, style={'borderBottom':'2px solid #34495E', 'padding':'8px'}) for col in estatisticas.columns])]),
        html.Tbody([html.Tr([html.Td(estatisticas.iloc[i][col], style={'borderBottom':'1px solid #ddd', 'padding':'8px'}) for col in estatisticas.columns]) for i in range(len(estatisticas))])
    ], style={'width': '100%', 'borderCollapse': 'collapse', 'textAlign': 'center'})

    return pizza_posicao, pizza_banco, barras_classificacao, processos, nao_cadastrado, tabela
