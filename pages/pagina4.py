import dash
from dash import html, dcc, callback, Output, Input
import plotly.graph_objects as go
import pandas as pd
import unicodedata

# Registro da página
dash.register_page(__name__, path='/pagina4', name='Página 4')

# Carregar dados
file_path = r"C:\Users\julio\OneDrive\Área de Trabalho\BANCO DE DADOS 2019 (TODOS OS BANCOS) - NOVA COLETA - Nova Tabulacao 9 - TABLEAU VERSAO 5 (sentencas por assunto + classe).xlsx"
df = pd.read_excel(file_path, sheet_name='BANCO_DADOS_2019')

# Normalizar colunas (remover acentos, converter espaços para _)
df.columns = [
    unicodedata.normalize('NFKD', col)
    .encode('ascii','ignore')
    .decode('ascii')
    .replace(' ', '_')
    for col in df.columns
]

# Converter valores e criar coluna de contagem
df['F2_VALOR_CAUSA'] = pd.to_numeric(df['F2_VALOR_CAUSA'], errors='coerce')
df['count'] = 1

# Definir nomes dos níveis (após normalização)
levels = [
    'F2_ASSUNTO_PRINCIPAL_(nivel_1)',
    'F2_ASSUNTO_PRINCIPAL_(nivel_2)',
    'F2_ASSUNTO_PRINCIPAL_(nivel_3)',
    'F2_ASSUNTO_PRINCIPAL_(nivel_4)',
    'F2_ASSUNTO_PRINCIPAL_(nivel_5)',
    'F2_ASSUNTO_PRINCIPAL (nível 6 - tratado)',
]

# Layout da página
layout = html.Div([
    html.H2('Fluxo Hierárquico de Assuntos (níveis 1–6)', style={'textAlign': 'center', 'marginBottom': '20px'}),
    dcc.Graph(id='sankey_graph')
])

# Callback para gerar Sankey
def generate_sankey(df):
    # Criar lista de rótulos únicos mantendo a ordem
    labels = []
    for lvl in levels:
        if lvl in df.columns:
            labels.extend(df[lvl].dropna().unique().tolist())
    labels = list(dict.fromkeys(labels))
    idx = {label: i for i, label in enumerate(labels)}

    # Construir links
    source, target, value = [], [], []
    for frm, to in zip(levels[:-1], levels[1:]):
        if frm in df.columns and to in df.columns:
            grp = df.groupby([frm, to])['count'].sum().reset_index()
            for _, row in grp.iterrows():
                source.append(idx[row[frm]])
                target.append(idx[row[to]])
                value.append(row['count'])

    sankey = go.Sankey(
        arrangement='snap',
        node=dict(label=labels, pad=10, thickness=15),
        link=dict(source=source, target=target, value=value)
    )
    fig = go.Figure(sankey)
    fig.update_layout(margin=dict(t=40, l=0, r=0, b=0),
                      title_text='Fluxo Hierárquico de Assuntos (níveis 1–6)',
                      title_x=0.5)
    return fig

@callback(
    Output('sankey_graph', 'figure'),
    Input('sankey_graph', 'id')
)
def render_sankey(_):
    fig = generate_sankey(df)
    return fig
