# pagina3.py
import dash
from dash import html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import unicodedata

# Registro da página
dash.register_page(__name__, path='/pagina3', name='Página 3')

# Carregar dados
file_path = r"C:\Users\julio\OneDrive\Área de Trabalho\BANCO DE DADOS 2019 (TODOS OS BANCOS) - NOVA COLETA - Nova Tabulacao 9 - TABLEAU VERSAO 5 (sentencas por assunto + classe).xlsx"
df = pd.read_excel(file_path, sheet_name='BANCO_DADOS_2019')

# Normalizar colunas
df.columns = [
    unicodedata.normalize('NFKD', col).encode('ascii', 'ignore').decode('ascii').replace(' ', '_')
    for col in df.columns
]

# Converter valores
df['F2_VALOR_CAUSA'] = pd.to_numeric(df['F2_VALOR_CAUSA'], errors='coerce')

def filter_df(assunto, posicao, classificacao, banco, comarca):
    dff = df.copy()
    if assunto != 'Todos': dff = dff[dff['F2_ASSUNTO_PRINCIPAL_(nivel_3)'] == assunto]
    if posicao != 'Todos': dff = dff[dff['F2_POSICAO_OCUPADA_PELO_BANCO'] == posicao]
    if classificacao != 'Todos': dff = dff[dff['CLASSIFICACAO_SENTENCA'] == classificacao]
    if banco != 'Todos': dff = dff[dff['BANCO'] == banco]
    if comarca != 'Todos': dff = dff[dff['F1_COMARCA'] == comarca]
    return dff

# Layout da página
layout = html.Div([
    html.H2(
        "PROCESSOS JUDICIAIS: COMARCA E VALOR DA CAUSA",
        style={'textAlign': 'center', 'color': '#34495E', 'marginBottom': '30px'}
    ),

    # Filtros alinhados em linha
    html.Div([
        html.Div([
            html.Label("Assunto Principal", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='f3_assunto',
                options=[{'label':'Todos','value':'Todos'}] + [{'label':a,'value':a} for a in df['F2_ASSUNTO_PRINCIPAL_(nivel_3)'].unique()],
                value='Todos', clearable=False
            )
        ], style={'flex': '1', 'paddingRight': '10px'}),

        html.Div([
            html.Label("Posição Ocupada", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='f3_posicao',
                options=[{'label':'Todos','value':'Todos'}] + [{'label':p,'value':p} for p in df['F2_POSICAO_OCUPADA_PELO_BANCO'].unique()],
                value='Todos', clearable=False
            )
        ], style={'flex': '1', 'paddingRight': '10px'}),

        html.Div([
            html.Label("Classificação Sentença", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='f3_classificacao',
                options=[{'label':'Todos','value':'Todos'}] + [{'label':c,'value':c} for c in df['CLASSIFICACAO_SENTENCA'].unique()],
                value='Todos', clearable=False
            )
        ], style={'flex': '1', 'paddingRight': '10px'}),

        html.Div([
            html.Label("Banco", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='f3_banco',
                options=[{'label':'Todos','value':'Todos'}] + [{'label':b,'value':b} for b in df['BANCO'].unique()],
                value='Todos', clearable=False
            )
        ], style={'flex': '1', 'paddingRight': '10px'}),

        html.Div([
            html.Label("Comarca", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='f3_comarca',
                options=[{'label':'Todos','value':'Todos'}] + [{'label':com,'value':com} for com in df['F1_COMARCA'].unique()],
                value='Todos', clearable=False
            )
        ], style={'flex': '1'})
    ], style={'display': 'flex', 'marginBottom': '30px'}),

    # Gráficos de rosca
    html.Div([
        dcc.Graph(id='f3_pie_posicao', style={'width':'48%','display':'inline-block'}),
        dcc.Graph(id='f3_pie_banco', style={'width':'48%','display':'inline-block','float':'right'})
    ], style={'marginBottom':'30px'}),

    # Tabela com divisões e alinhamento
    html.Div(id='tabela_valor')
])

# Callback para atualizar tabela e gráficos
@callback(
    Output('tabela_valor','children'),
    Output('f3_pie_posicao','figure'),
    Output('f3_pie_banco','figure'),
    Input('f3_assunto','value'),
    Input('f3_posicao','value'),
    Input('f3_classificacao','value'),
    Input('f3_banco','value'),
    Input('f3_comarca','value')
)
def update_pagina3(assunto, posicao, classificacao, banco, comarca):
    dff = filter_df(assunto, posicao, classificacao, banco, comarca)

    # Estatísticas por comarca
    stats = dff.groupby('F1_COMARCA')['F2_VALOR_CAUSA'] \
        .agg(N_Causas_Valor_Cadastrado='count', Total_Valor_Causa='sum', Media='mean', Valor_Minimo='min', Valor_Maximo='max', Desvio_Padrao='std') \
        .round(2) \
        .reset_index()

    # Tabela HTML com divisões e alinhamento
    tabela = html.Table([
        html.Thead(html.Tr([html.Th(col, style={'border':'1px solid #ccc','padding':'8px','textAlign':'center'}) for col in stats.columns])),
        html.Tbody([
            html.Tr([html.Td(stats.iloc[i][col], style={'border':'1px solid #ccc','padding':'8px','textAlign':'center'}) for col in stats.columns])
            for i in range(len(stats))
        ])
    ], style={'width':'100%','borderCollapse':'collapse','marginBottom':'30px'})

    # Gráficos de rosca
    fig1 = px.pie(dff, names='F2_POSICAO_OCUPADA_PELO_BANCO', hole=0.5, title='Posição Ocupada', color_discrete_sequence=px.colors.sequential.RdBu)
    fig1.update_traces(textposition='outside', textinfo='percent+label')
    fig1.update_layout(title_x=0.5)

    fig2 = px.pie(dff, names='BANCO', hole=0.5, title='Banco', color_discrete_sequence=px.colors.sequential.RdBu)
    fig2.update_traces(textposition='outside', textinfo='percent+label')
    fig2.update_layout(title_x=0.5)

    return tabela, fig1, fig2
