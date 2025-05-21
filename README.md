# Dashboard de Processos Judiciais

Este repositório contém um _dashboard_ interativo desenvolvido com Dash/Plotly, que explora um conjunto de dados de processos judiciais para os bancos Itaú, Bradesco e Santander. A aplicação está dividida em quatro páginas, cada uma com filtros, indicadores e visualizações específicas:

---

## 📂 Estrutura do Projeto

/
│
├── app.py # entry‐point do Dash, config de páginas
├── requirements.txt # dependências Python
├── pages/ # diretório de páginas
│ ├── pagina1.py # Visão Geral
│ ├── pagina2.py # Comarca e Tempo
│ ├── pagina3.py # Comarca e Valor da Causa
│ └── pagina4.py # Sankey Hierárquico
└── assets/ # recursos estáticos (CSS, imagens…)

markdown
Copiar
Editar

---

## 🚀 Páginas

### Página 1 – Visão Geral  
- **Título:** `PROCESSOS JUDICIAIS ITAÚ, BRADESCO E SANTANDER: VISÃO GERAL`  
- **Filtros:** Banco, Assunto Principal  
- **Cards:**  
  - Total de processos  
  - Processos sem valor cadastrado  
- **Gráficos:**  
  - Duas roscas (Posição Ocupada / Banco)  
  - Gráfico de barras horizontais (Classificação de Sentença)  
- **Tabela de estatísticas** por banco (`soma`, `média`, `mínimo`, `máximo`, `desvio-padrão`)

### Página 2 – Comarca e Tempo  
- **Título:** `ANÁLISE DOS PROCESSOS POR COMARCA E POR TEMPO`  
- **Filtros:** Assunto Principal, Posição Ocupada, Classificação Sentença, Banco, Comarca  
- **Cards:**  
  - Número de comarcas distintas  
  - Total de processos  
- **Visualizações:**  
  - Barra horizontal (Processos por Comarca) com rolagem e escala logarítmica  
  - Linha temporal por **data de início** (contagem diária)  
  - Linha temporal por **data da última sentença** (contagem diária)

### Página 3 – Comarca e Valor da Causa  
- **Título:** `PROCESSOS JUDICIAIS: COMARCA E VALOR DA CAUSA`  
- **Mesmos filtros da Página 2**  
- **Tabela de estatísticas** por comarca:  
  - Nº de causas com valor cadastrado  
  - Soma, média, valor mínimo, valor máximo, desvio-padrão do valor da causa  
- **Duas roscas** (Posição Ocupada / Banco)

### Página 4 – Sankey Hierárquico de Assuntos  
- **Título:** `Fluxo Hierárquico de Assuntos (níveis 1–6)`  
- **Diagrama de Sankey** mostrando o fluxo do “nível 1 → nível 2 → … → nível 6” de assuntos, com cada link ponderado pela contagem de ocorrências.

---

## 🛠️ Tecnologias e Bibliotecas

- **Python 3.x**  
- **Dash** (Plotly) para construção do _frontend_  
- **Pandas** para tratamento de dados  
- **Plotly Express** e **Plotly Graph Objects** para gráficos  
- **unicodedata** para normalização de nomes de colunas  

---

## ⚙️ Como Executar Localmente

1. Clone este repositório:  
   ```bash
   git clone https://github.com/SEU_USUARIO/SEU_REPO.git
   cd SEU_REPO
Crie e ative um venv (opcional, mas recomendado):

bash
Copiar
Editar
python -m venv .venv
source .venv/bin/activate     # Linux/Mac  
.venv\Scripts\activate        # Windows
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Ajuste o caminho do arquivo Excel em cada página (variável file_path).

Inicie a aplicação:

bash
Copiar
Editar
python app.py
Acesse no navegador em http://127.0.0.1:8050.

📄 LICENSE
Este projeto está sob a licença MIT — veja o arquivo LICENSE para mais detalhes.

Feito com ❤️ e Plotly Dash!

Copiar
Editar


![image](https://github.com/user-attachments/assets/0568f702-08b3-4faa-bdc7-78eb5b3b1314)

![image](https://github.com/user-attachments/assets/5800c485-c81d-4483-9a44-a4e83a951bcf)

![image](https://github.com/user-attachments/assets/76168bdc-f917-46a6-a76f-7dced833d7cf)

![image](https://github.com/user-attachments/assets/0a9201f6-b72f-4af3-b43a-0563f00a79aa)
