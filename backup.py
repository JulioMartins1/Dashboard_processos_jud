from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Carregar os dados
file_path = r"C:\Users\julio\OneDrive\Área de Trabalho\BANCO DE DADOS 2019 (TODOS OS BANCOS) - NOVA COLETA - Nova Tabulacao 9 - TABLEAU VERSAO 5 (sentencas por assunto + classe).xlsx"
df = pd.read_excel(file_path, sheet_name='BANCO_DADOS_2019')

# Garantir que a coluna 'F2_VALOR_CAUSA' seja numérica (convertendo valores inválidos para NaN)
df['F2_VALOR_CAUSA'] = pd.to_numeric(df['F2_VALOR_CAUSA'], errors='coerce')

# Criar o aplicativo Dash
app = Dash(__name__)

# Layout da dashboard
app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'},
    children=[
        html.H1("PROCESSOS JUDICIAIS ITAÚ, BRADESCO E SANTANDER: VISÃO GERAL", style={'textAlign': 'center', 'color': '#4CAF50'}),
        
        # Filtros organizados com barra de pesquisa
        html.Div([ 
            html.Div([
                html.Label("Selecione o Banco:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='dropdown_banco',
                    options=[{'label': 'Todos', 'value': 'Todos'}] + [{'label': banco, 'value': banco} for banco in df['BANCO'].unique()],
                    value='Todos',  # Valor inicial
                    searchable=True,  # Habilita a pesquisa
                    style={'width': '100%', 'padding': '10px', 'marginTop': '5px'}
                ),
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),

            html.Div([
                html.Label("Selecione o Assunto Principal:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='dropdown_assunto',
                    options=[{'label': 'Todos', 'value': 'Todos'}] + [{'label': assunto, 'value': assunto} for assunto in df['F2_ASSUNTO_PRINCIPAL (nível 3)'].unique()],
                    value='Todos',  # Valor inicial
                    searchable=True,  # Habilita a pesquisa
                    style={'width': '100%', 'padding': '10px', 'marginTop': '5px'}
                ),
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'float': 'right'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}),

        # Cards de contagem
        html.Div([
            html.Div([
                html.H4("Processos"),
                html.Div(id='card_processos', style={'fontSize': '24px', 'fontWeight': 'bold'})
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'border': '1px solid #4CAF50', 'borderRadius': '5px', 'textAlign': 'center', 'backgroundColor': '#f1f1f1'}),

            html.Div([
                html.H4("Processos com valor da causa não cadastrada"),
                html.Div(id='card_processos_nao_cadastrados', style={'fontSize': '24px', 'fontWeight': 'bold'})
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'border': '1px solid #4CAF50', 'borderRadius': '5px', 'textAlign': 'center', 'backgroundColor': '#f1f1f1'}),
        ], style={'marginBottom': '20px'}),

        # Gráficos
        html.Div([
            dcc.Graph(id='grafico_pizza_posicao', style={'display': 'inline-block', 'width': '48%', 'padding': '10px'}),
            dcc.Graph(id='grafico_pizza_banco', style={'display': 'inline-block', 'width': '48%', 'padding': '10px'}),
        ], style={'marginBottom': '20px', 'display': 'flex', 'justifyContent': 'space-between'}),

        # Gráfico de barras
        dcc.Graph(id='grafico_barras_classificacao', style={'marginBottom': '20px'}),

        # Tabela com as estatísticas de "F2_VALOR_CAUSA" por "BANCO"
        html.Div(id='tabela_estatisticas', style={'marginTop': '30px'})
    ]
)

# Função de callback para atualizar os gráficos e as tabelas
@app.callback(
    Output('grafico_pizza_posicao', 'figure'),
    Output('grafico_pizza_banco', 'figure'),
    Output('grafico_barras_classificacao', 'figure'),
    Output('card_processos', 'children'),
    Output('card_processos_nao_cadastrados', 'children'),
    Output('tabela_estatisticas', 'children'),
    Input('dropdown_banco', 'value'),
    Input('dropdown_assunto', 'value')
)
def atualizar_dashboard(banco_selecionado, assunto_selecionado):
    # Filtrar os dados com base no banco e no assunto principal selecionado
    if banco_selecionado != 'Todos':
        df_filtrado = df[df['BANCO'] == banco_selecionado]
    else:
        df_filtrado = df
    
    if assunto_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['F2_ASSUNTO_PRINCIPAL (nível 3)'] == assunto_selecionado]

    # Gráfico de pizza para "F2 POSIÇÃO OCUPADA PELO BANCO"
    fig_pizza_posicao = px.pie(df_filtrado, names='F2 POSIÇÃO OCUPADA PELO BANCO', 
                               title=f'Distribuição por Posição Ocupada - Banco: {banco_selecionado}, Assunto: {assunto_selecionado}',
                               hole=0.3, 
                               color_discrete_sequence=px.colors.sequential.Plasma)  # Paleta de cores

    # Gráfico de pizza para "BANCO"
    fig_pizza_banco = px.pie(df, names='BANCO', 
                             title='Distribuição por Banco',
                             hole=0.3, 
                             color_discrete_sequence=px.colors.sequential.Plasma)  # Paleta de cores

    # Gráfico de barras vertical para "CLASSIFICAÇÃO SENTENÇA"
    # Contagem dos valores de "CLASSIFICAÇÃO SENTENÇA"
    classificacao_counts = df_filtrado['CLASSIFICAÇÃO SENTENÇA'].value_counts().reset_index()
    classificacao_counts.columns = ['CLASSIFICAÇÃO SENTENÇA', 'Contagem']
    
    # Ordenar os dados do maior para o menor
    classificacao_counts = classificacao_counts.sort_values(by='Contagem', ascending=True)

    fig_barras_classificacao = px.bar(classificacao_counts,
                                      y='CLASSIFICAÇÃO SENTENÇA',  # Colocando "CLASSIFICAÇÃO SENTENÇA" no eixo Y
                                      x='Contagem',  # Colocando "Contagem" no eixo X
                                      title=f'Contagem de CLASSIFICAÇÃO SENTENÇA - Banco: {banco_selecionado}, Assunto: {assunto_selecionado}',
                                      labels={'CLASSIFICAÇÃO SENTENÇA': 'Classificação Sentença', 'Contagem': 'Contagem'},
                                      color='Contagem',
                                      color_continuous_scale='Viridis')  # Paleta de cores para gráfico de barras

    # Card de "Processos"
    processos_count = df_filtrado.shape[0]  # Contagem total de processos
    
    # Card de "Processos com valor da causa não cadastrada"
    processos_nao_cadastrados_count = df_filtrado[df_filtrado['F2_VALOR_CAUSA'].isna() | (df_filtrado['F2_VALOR_CAUSA'] == 0)].shape[0]
    
    # Calcular estatísticas de "F2_VALOR_CAUSA" por "BANCO"
    estatisticas = df_filtrado.groupby('BANCO')['F2_VALOR_CAUSA'].agg(['sum', 'mean', 'min', 'max', 'std']).reset_index()
    estatisticas.columns = ['BANCO', 'Soma', 'Média', 'Mínimo', 'Máximo', 'Desvio Padrão']
    
    # Arredondar as estatísticas para 2 casas decimais
    estatisticas['Soma'] = estatisticas['Soma'].round(2)
    estatisticas['Média'] = estatisticas['Média'].round(2)
    estatisticas['Mínimo'] = estatisticas['Mínimo'].round(2)
    estatisticas['Máximo'] = estatisticas['Máximo'].round(2)
    estatisticas['Desvio Padrão'] = estatisticas['Desvio Padrão'].round(2)
    
    # Criar a tabela de estatísticas com alinhamento adequado
    tabela_estatisticas = html.Table([ 
        html.Thead(
            html.Tr([html.Th(col, style={'padding': '8px', 'textAlign': 'center', 'backgroundColor': '#4CAF50', 'color': 'white'}) for col in estatisticas.columns])
        ),
        html.Tbody([ 
            html.Tr([html.Td(estatisticas.iloc[i][col], style={'padding': '8px', 'textAlign': 'right'}) for col in estatisticas.columns]) 
            for i in range(len(estatisticas))
        ])
    ], style={'width': '100%', 'borderCollapse': 'collapse', 'border': '1px solid #ddd', 'marginTop': '20px'})

    return fig_pizza_posicao, fig_pizza_banco, fig_barras_classificacao, processos_count, processos_nao_cadastrados_count, tabela_estatisticas

# Rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)
