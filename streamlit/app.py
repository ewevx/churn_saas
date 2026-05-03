import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- 1. CONFIGURAÇÃO E CARREGAMENTO ---
st.set_page_config(page_title="Churn Strategy Command Center", layout="wide", page_icon="💰")

@st.cache_data
def load_and_prepare():
    # Carrega o dataset Gold (já tratado no notebook)
    df = pd.read_csv('telcon_churn_cleaned_gold.csv')
    df.columns = [col.lower() for col in df.columns]
    
    # Nova Métrica de Negócio: LTV (Lifetime Value)
    # LTV bruto = quanto o cliente já deixou na empresa até hoje
    if 'ltv' not in df.columns:
        df['ltv'] = df['totalcharges']
    
    # Garantir churn_numeric para cálculos
    if 'churn_numeric' not in df.columns:
        df['churn_numeric'] = df['churn'].apply(lambda x: 1 if str(x).lower() in ['yes', '1', '1.0'] else 0)
        
    return df

df = load_and_prepare()

# --- 2. SIDEBAR - SIMULADOR DE RETENÇÃO (BUSINESS CASE) ---
st.sidebar.header("📊 Simulador de Impacto")
st.sidebar.markdown("Se o time de CS agir, quanto podemos salvar?")
taxa_sucesso = st.sidebar.slider("Taxa de Sucesso na Retenção (%)", 0, 100, 20) / 100
custo_contato = st.sidebar.number_input("Custo por Contato ($)", value=15.0)

# --- 3. INTERFACE PRINCIPAL ---
st.title("🛡️ Churn Defense: Estratégia e Faturamento")
st.markdown("---")

# Abas focadas em Valor de Negócio
tab_financeiro, tab_perfil, tab_prioridade = st.tabs([
    "💵 Impacto Financeiro & LTV", 
    "👤 Perfil do Risco", 
    "🎯 Matriz de Priorização"
])

# --- TAB 1: IMPACTO FINANCEIRO & LTV ---
with tab_financeiro:
    # Filtro para predições de churn (assumindo que a coluna se chama 'predicted_churn')
    pred_col = 'predicted_churn' if 'predicted_churn' in df.columns else 'previsao'
    
    if pred_col in df.columns:
        clientes_em_risco = df[df[pred_col] == 1]
        mrr_em_risco = clientes_em_risco['monthlycharges'].sum()
        ltv_perdido = clientes_em_risco['ltv'].sum()
        
        # Cálculos do Simulador
        mrr_salvo = mrr_em_risco * taxa_sucesso
        investimento = len(clientes_em_risco) * custo_contato
        roi = (mrr_salvo * 12) - investimento # ROI anualizado
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("MRR em Risco (Mensal)", f"${mrr_em_risco:,.2f}", delta="Perda Imediata", delta_color="inverse")
        c2.metric("LTV Acumulado em Risco", f"${ltv_perdido:,.2f}", help="Soma de tudo que esses clientes já pagaram")
        c3.metric("MRR Recuperável (Est.)", f"${mrr_salvo:,.2f}", delta=f"{taxa_sucesso:.0%} de sucesso")
        c4.metric("ROI Anual Estimado", f"${roi:,.2f}", delta="Pós-investimento")
        
        st.markdown("### Perda de Receita se nada for feito (Projeção 12 meses)")
        df_projecao = pd.DataFrame({
            'Meses': range(1, 13),
            'Perda_Acumulada': [mrr_em_risco * i for i in range(1, 13)]
        })
        fig_proj = px.area(df_projecao, x='Meses', y='Perda_Acumulada', 
                           title="Sangramento de Receita Acumulado",
                           color_discrete_sequence=['#e74c3c'])
        st.plotly_chart(fig_proj, use_container_width=True)
    else:
        st.error(f"Coluna de predição '{pred_col}' não encontrada.")

# --- TAB 2: PERFIL DO RISCO (POR QUE ELES SAEM?) ---
with tab_perfil:
    st.subheader("Análise de Agrupamento: Quem são os clientes em risco?")
    
    # Comparando clientes Saudáveis vs Risco em variáveis chave
    col_var = st.selectbox("Selecione a variável para analisar o perfil:", 
                          ['contract', 'internetservice', 'techsupport', 'paymentmethod'])
    
    fig_perfil = px.histogram(df, x=col_var, color="churn", barmode="group",
                             title=f"Distribuição de Churn por {col_var.capitalize()}",
                             color_discrete_map={'Yes': '#e74c3c', 'No': '#2ecc71'})
    st.plotly_chart(fig_perfil, use_container_width=True)
    
    st.info("**Insight de Negócio:** Se as barras vermelhas forem proporcionalmente maiores em 'Month-to-month' ou 'Fiber optic', o problema pode estar no modelo de contrato ou na estabilidade técnica.")

# --- TAB 3: MATRIZ DE PRIORIZAÇÃO ---
with tab_prioridade:
    st.subheader("Matriz de Prioridade: High-Value / High-Risk")
    
    if 'healthscore' in df.columns:
        # Criando a Matriz de Quadrantes
        # X = Saúde (HealthScore), Y = Valor (MonthlyCharges)
        fig_matrix = px.scatter(df, x="healthscore", y="monthlycharges", 
                               color="healthstatus", 
                               hover_data=['tenure', 'contract'],
                               title="Onde devemos focar? (Clientes mais caros com menor saúde)",
                               labels={'healthscore': 'Saúde do Cliente', 'monthlycharges': 'Mensalidade ($)'},
                               color_discrete_map={'Crítico': 'red', 'Alerta': 'orange', 'Saudável': 'green'})
        
        # Linhas de quadrante (Média de valor e linha crítica de saúde)
        fig_matrix.add_hline(y=df['monthlycharges'].mean(), line_dash="dot", annotation_text="Ticket Médio")
        fig_matrix.add_vline(x=30, line_dash="dot", annotation_text="Limite Crítico")
        
        st.plotly_chart(fig_matrix, use_container_width=True)
        
        st.markdown("#### Top 10 Clientes 'VIP em Risco' (Alta Mensalidade + Saúde Crítica)")
        vip_risco = df[(df['healthscore'] < 30)].sort_values('monthlycharges', ascending=False).head(10)
        st.table(vip_risco[['healthscore', 'monthlycharges', 'tenure', 'contract', 'paymentmethod']])
    else:
        st.warning("Coluna 'healthscore' necessária para esta aba.")