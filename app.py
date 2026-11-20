import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from dotenv import load_dotenv
import os
import urllib3

# Desabilita aviso de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Delivery Insights | iFood", layout="wide")

# 2. INJEÇÃO DE CSS (Refinamento Premium - Dark Glassmorphism)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background-color: #050505; }
    h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown { color: #ffffff !important; font-family: 'Inter', sans-serif !important; }
    h1 { font-weight: 800 !important; letter-spacing: -1.5px; font-size: 3rem !important; }
    h2, h3 { font-weight: 600 !important; letter-spacing: -0.5px; }
    p, .stMarkdown p { color: #888888 !important; font-weight: 400; }
    
    div[data-testid="stMetric"] { background: rgba(20, 20, 20, 0.6); backdrop-filter: blur(10px); border-radius: 16px; padding: 24px; border: 1px solid rgba(255, 255, 255, 0.05); border-left: 4px solid #ea1d2c; box-shadow: 0 10px 40px rgba(0,0,0,0.5); transition: transform 0.3s ease; }
    div[data-testid="stMetric"]:hover { transform: translateY(-5px); }
    div[data-testid="stMetric"] label { color: #666666 !important; font-weight: 600; text-transform: uppercase; font-size: 11px; letter-spacing: 1.5px; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 800; font-size: 38px; letter-spacing: -1px; }
    
    @keyframes pulse-red { 0% { box-shadow: 0 0 0 0 rgba(234, 29, 44, 0.7); } 70% { box-shadow: 0 0 0 15px rgba(234, 29, 44, 0); } 100% { box-shadow: 0 0 0 0 rgba(234, 29, 44, 0); } }
    .stButton > button { background-color: #ea1d2c !important; border-radius: 50px !important; border: none !important; padding: 20px 40px !important; transition: all 0.3s ease !important; box-shadow: 0 4px 20px rgba(234, 29, 44, 0.4) !important; width: 100% !important; margin-top: 20px !important; animation: pulse-red 2s infinite !important; }
    .stButton > button p { color: #ffffff !important; font-weight: 800 !important; font-size: 20px !important; letter-spacing: 1px !important; font-family: 'Inter', sans-serif !important; }
    .stButton > button:hover { background-color: #ff2a3a !important; transform: scale(1.02) !important; box-shadow: 0 8px 30px rgba(234, 29, 44, 0.6) !important; animation: none !important; }
    
    hr { border-color: rgba(255, 255, 255, 0.05) !important; }
    .stMarkdown table { background-color: transparent; border-radius: 12px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.1); }
    .stMarkdown th, .stMarkdown td { border: none !important; border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important; padding: 12px 16px !important; color: #d0d0d0 !important; }
    .stMarkdown th { background-color: rgba(255, 255, 255, 0.03) !important; color: #ffffff !important; font-weight: 600; text-transform: uppercase; font-size: 12px; letter-spacing: 1px; }
    
    div[data-testid="stMarkdownContainer"] blockquote { background-color: rgba(20, 20, 20, 0.4) !important; border-left: 4px solid #ea1d2c !important; border-radius: 12px !important; padding: 20px 25px !important; margin-top: 20px !important; margin-bottom: 20px !important; }
    div[data-testid="stMarkdownContainer"] blockquote p { color: #a0a0a0 !important; font-size: 15px !important; line-height: 1.6 !important; }
    div[data-testid="stMarkdownContainer"] blockquote strong { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# 3. PIPELINE DE DADOS (Tradução Profunda e Contexto Brasil)
@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/food_delivery_time_prediction.csv")
    df.columns = df.columns.str.strip().str.lower()
    
    # 1. Renomeando Colunas
    df = df.rename(columns={
        "road_distance_km": "Distancia_KM",
        "time_taken_min": "Tempo_Minutos",
        "traffic_level": "Transito",
        "weather": "Clima",
        "cuisine_type": "Restaurante",
        "rider_rating": "Nota_Entregador",
        "preparation_time_min": "Tempo_Preparo",
        "delivery_priority": "Prioridade"
    })
    
    # 2. Traduzindo os VALORES para a realidade brasileira
    traducoes = {
        "Clima": {"Clear": "Limpo", "Rain": "Chuva", "Cloudy": "Nublado", "Storm": "Tempestade", "Fog": "Nevoeiro", "Snow": "Neve", "Windy": "Ventania"},
        "Transito": {"Low": "Baixo", "Moderate": "Moderado", "High": "Alto", "Severe": "Severo", "Jam": "Engarrafamento"}
    }
    for coluna, mapa in traducoes.items():
        if coluna in df.columns:
            df[coluna] = df[coluna].replace(mapa)
    
    df = df.dropna().drop_duplicates()
    return df

df = carregar_dados()

def format_br(valor, casas=1):
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")

# 4. CABEÇALHO
st.title("Delivery Insights.")
st.markdown("Análise de logística e recomendações estratégicas baseadas em dados.")
st.write("") 

# 5. MÉTRICAS
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Entregas", f"{len(df):,}".replace(",", "."))
col2.metric("Tempo Médio", f"{format_br(df['Tempo_Minutos'].mean())} min")
col3.metric("Distância Média", f"{format_br(df['Distancia_KM'].mean())} km")
col4.metric("Nota Entregador", f"{df['Nota_Entregador'].mean():.1f} ⭐")

st.write("")
st.divider() 

# 6. GRÁFICOS E ANÁLISE
dark_color = '#888888'
grid_color = 'rgba(255, 255, 255, 0.05)'
bg_color = 'rgba(0,0,0,0)'

st.subheader("1. Análise Exploratória")
# ... (Os gráficos 1, 2 e 3 continuam iguais, só garanta que o código anterior foi mantido) ...
fig1 = px.scatter(df, x="Distancia_KM", y="Tempo_Minutos", color="Clima", title="Hipótese 1: O clima e a distância impactam o tempo de entrega?", color_discrete_sequence=px.colors.qualitative.Pastel)
fig1.update_layout(plot_bgcolor=bg_color, paper_bgcolor=bg_color, font=dict(color=dark_color, family="Inter"), title_font=dict(size=14, color="#ffffff"), xaxis=dict(title="Distância (km)", showgrid=False), yaxis=dict(title="Tempo (min)", showgrid=True, gridcolor=grid_color))
st.plotly_chart(fig1, use_container_width=True)

col_g1, col_g2 = st.columns(2)
with col_g1:
    fig2 = px.bar(df.groupby("Transito")["Tempo_Minutos"].mean().reset_index(), x="Transito", y="Tempo_Minutos", title="Hipótese 2: O trânsito aumenta o tempo?", color_discrete_sequence=['#ea1d2c'])
    fig2.update_layout(plot_bgcolor=bg_color, paper_bgcolor=bg_color, font=dict(color=dark_color, family="Inter"), title_font=dict(size=14, color="#ffffff"), xaxis=dict(title="Nível de Trânsito", showgrid=False), yaxis=dict(title="Tempo (min)", showgrid=True, gridcolor=grid_color))
    st.plotly_chart(fig2, use_container_width=True)

with col_g2:
    fig3 = px.scatter(df, x="Tempo_Preparo", y="Tempo_Minutos", title="Hipótese 3: O preparo é o gargalo?", color_discrete_sequence=['#ea1d2c'], opacity=0.5)
    fig3.update_layout(plot_bgcolor=bg_color, paper_bgcolor=bg_color, font=dict(color=dark_color, family="Inter"), title_font=dict(size=14, color="#ffffff"), xaxis=dict(title="Tempo de Preparo (min)", showgrid=False), yaxis=dict(title="Tempo de Entrega (min)", showgrid=True, gridcolor=grid_color))
    st.plotly_chart(fig3, use_container_width=True)

# 7. MATRIZ DE CORRELAÇÃO LIMPA E BRASILEIRA
st.subheader("2. Matriz de Correlação (Investigação de Causa Raiz)")
numeric_df = df.select_dtypes(include=['float64', 'int64'])
corr_matrix = numeric_df.corr()

# Renomeando e arredondando para 2 casas decimais
nomes_pt = {
    "order_hour": "Hora do Pedido", "is_weekend": "Fim de Semana", "is_festival": "Feriado",
    "rider_experience_years": "Exp. Entregador", "Nota_Entregador": "Nota Entregador",
    "restaurant_rating": "Nota Restaurante", "order_items": "Itens do Pedido",
    "Tempo_Preparo": "Tempo de Preparo", "Distancia_KM": "Distância",
    "number_of_signals": "Sinais de Trânsito", "average_speed_kmph": "Velocidade Média",
    "Tempo_Minutos": "Tempo de Entrega"
}
corr_matrix = corr_matrix.rename(index=nomes_pt, columns=nomes_pt).round(2)

fig4 = px.imshow(corr_matrix, text_auto=True, aspect="auto", 
                 title="Quais variáveis têm maior correlação com o Tempo de Entrega?",
                 color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
fig4.update_layout(plot_bgcolor=bg_color, paper_bgcolor=bg_color, font=dict(color=dark_color, family="Inter"), title_font=dict(size=14, color="#ffffff"))
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# 8. SEÇÃO DA IA COM CONTEXTO BRASIL
st.subheader("3. Recomendações Estratégicas (Prescritiva)")
st.markdown("A IA formula hipóteses, valida com os dados e propõe melhorias.")

if st.button("GERAR RELATÓRIO ESTRATÉGICO"):
    with st.spinner("Analisando hipóteses..."):
        api_key = os.getenv("GROQ_API_KEY")
        resumo = df.describe().to_string()
        
        # PROMPT REFORÇADO COM CONTEXTO BRASILEIRO
        prompt = f"""
        Você é um consultor sênior de operações do iFood. 
        Analise os dados e traga a realidade operacional brasileira (ex: trânsito de São Paulo, chuvas de verão, etc.).

        Dados:
        {resumo}

        Instruções OBRIGATÓRIAS:
        1. IDIOMA: Português do Brasil (pt-BR). Sem emojis.
        2. NÃO use "Percentil 25/75". Use "Pedidos mais rápidos/lentos".
        3. Formate números com vírgula decimal.
        
        Estrutura do Relatório:
        
        **1. Levantamento de Hipóteses (Contexto Brasil):**
        - Liste 3 hipóteses de negócio aplicáveis ao Brasil (ex: "A chuva de verão em SP aumenta o tempo em X%").
        
        **2. Validação e Diagnóstico:**
        - Valide ou refute cada hipótese com base nos dados e correlações.
        
        **3. Causa Raiz:**
        - Explique o motivo operacional (ex: trânsito, restaurante, distância).
        
        **4. Propostas de Melhoria:**
        - 3 ações práticas baseadas nos dados.
        """
        
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}
        
        try:
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, verify=False, timeout=60)
            if response.status_code == 200:
                texto_ia = response.json()['choices'][0]['message']['content']
                st.markdown(texto_ia) 
            else:
                st.error(f"Erro na API: {response.status_code}")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")

# 9. SEÇÃO "SOBRE O PROJETO"
st.markdown("""
> **Sobre este Projeto**
> 
> Este dashboard foi desenvolvido para demonstrar habilidades práticas em **Engenharia de Dados, Análise Exploratória e Integração de LLMs**.
> 
> **Origem dos Dados:** A base bruta foi extraída do Kaggle (dataset "Food Delivery Time Prediction"), contendo 50.000 registros de operações de delivery.
> 
> **Tratamento (ETL):** Os dados passaram por um pipeline em Python (Pandas), onde foram traduzidos para o português, limpos (remoção de nulos e duplicatas) e formatados para o padrão brasileiro.
> 
> **Tecnologias:** Python, Pandas, Streamlit, Plotly e Groq API (modelo GPT-OSS-120B) para geração de insights.
""")