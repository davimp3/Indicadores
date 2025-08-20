import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import datetime

# ---- CONFIGURAÇÕES INICIAIS DA PÁGINA ----
st.set_page_config(layout="wide")

# ---- INJEÇÃO DE CSS PERSONALIZADO PARA ESPAÇAMENTO ----
st.markdown("""
<style>
    /* Reduz o espaçamento acima dos títulos de seções */
    .st-emotion-cache-1g03c80 { /* stHeader */
        margin-top: -30px;
    }
    .st-emotion-cache-17lsv9n { /* stSubheader */
        margin-top: -30px;
    }
    /* Reduz o espaçamento entre o divisor e os elementos */
    [data-testid="stVerticalBlock"] > [data-testid="stColumn"] {
        margin-top: -30px;
    }

    /* Reduz o tamanho da fonte das métricas */
    [data-testid="stMetricLabel"] p {
        font-size: 16px; /* Tamanho da fonte do rótulo (ex: "Verba Total") */
    }
    [data-testid="stMetricValue"] {
        font-size: 28px; /* Tamanho da fonte do valor (ex: "R$ 134.500,00") */
    }

</style>
""", unsafe_allow_html=True)



total_verba_gerenciada = 134500
total_leads = 17180
ctr_topo = 3.5 
ctr_meio = 1.2
ctr_fundo = 0.5
total_impressoes = 520000
total_alcance = 230000
total_frequencia = 2.2


verba_meta = total_verba_gerenciada * 0.6
verba_google = total_verba_gerenciada * 0.4
leads_meta = total_leads * 0.7
leads_google = total_leads * 0.3
impressoes_meta = total_impressoes * 0.55
impressoes_google = total_impressoes * 0.45
alcance_meta = total_alcance * 0.6
alcance_google = total_alcance * 0.4

# Simulação do funil
funil_data = pd.DataFrame(dict(
    stage=["Total Leads", "Primeiro Contato", "Reunião", "Proposta", "Contrato"],
    value=[1000, 700, 500, 300, 100],  
    ciclo_dias=[3, 5, 8, 15, 20]
))
total_dias_ciclo = funil_data['ciclo_dias'].sum()
funil_data['percent_dias'] = (funil_data['ciclo_dias'] / total_dias_ciclo) * 100

novos_labels_y = ["Custo Total Lead", "Custo Total Primeiro Contato", "Custo Total Reunião", "Custo Total Proposta", "Custo Total Contrato"]
funil_data['stage_labels'] = novos_labels_y

funil_data['text_ciclo_label'] = funil_data.apply(
    lambda row: f"{row['stage_labels']}: {row['ciclo_dias']} dias ({row['percent_dias']:.1f}%)", axis=1
)

funil_data['cac_por_etapa'] = total_verba_gerenciada / funil_data['value']
funil_data['text_cac_label'] = funil_data.apply(
    lambda row: f"{row['stage_labels']}: R$ {row['cac_por_etapa']:,.2f}", axis=1
)


df_cpl = pd.DataFrame({
    'date': pd.to_datetime(['2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01', '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01', '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01']),
    'lead_source': ['Google Ads'] * 8 + ['Facebook Ads'] * 8 + ['Tráfego Orgânico'] * 8,
    'cost_per_lead': [5.5, 5.8, 6.0, 6.2, 6.1, 6.5, 6.4, 6.6, 4.8, 5.2, 5.5, 5.9, 6.3, 6.8, 7.0, 7.2, 3.0, 2.9, 2.8, 2.75, 2.7, 2.7, 2.65, 2.6]
})

df_budget = pd.DataFrame({
    'date': pd.to_datetime(['2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01', '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01']),
    'client_segment': ['Pequenas Empresas'] * 8 + ['Clientes Corporativos'] * 8,
    'managed_budget': [10000, 12000, 15000, 18000, 20000, 22000, 24000, 26000, 50000, 55000, 60000, 68000, 75000, 82000, 88000, 95000]
})

df_satisfaction = pd.DataFrame({
    'date': pd.to_datetime(['2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01', '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01']),
    'client_segment': ['Clientes Gold'] * 8 + ['Novos Clientes'] * 8,
    'satisfaction_score': [90, 91, 92, 91, 93, 94, 95, 96, 75, 78, 80, 79, 82, 85, 84, 86]
})


st.sidebar.title("Filtros")

st.sidebar.divider()

st.sidebar.subheader("Filtros de Data")

today = datetime.datetime.now()
next_year = today.year + 1
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

d = st.sidebar.date_input(
    "Seleção do Período",
    (jan_1, datetime.date(next_year, 1, 7)),
    jan_1,
    dec_31,
    format="MM.DD.YYYY",
)

start_time = st.sidebar.slider(
    label="Data Range",
)

st.sidebar.divider()

st.sidebar.subheader("Clientes")

options = st.sidebar.multiselect(
    "Cliente(s)",
    ["Green", "Yellow", "Red", "Blue", "All"],
    default=["All"],
)

st.sidebar.divider()

st.sidebar.subheader("Categorias")

options2 = st.sidebar.multiselect(
    "Categoria(s)",
    ["Green", "Yellow", "Red", "Blue", "All"],
    default=["All"],
)

st.title("Dashboard de Marketing e Vendas")

# --- FUNIL DE VENDAS ---
st.header("Análise do Funil de Vendas")
col_ciclo, col_funil, col_cac = st.columns([1.2, 1.6, 1.2])

with col_ciclo:
    st.subheader("Ciclo Médio")
    fig_ciclo = px.bar(
        funil_data,
        x='ciclo_dias',
        y='stage_labels',
        orientation='h',
        title="Tempo de Vendas",
        text='text_ciclo_label',
        template="plotly_dark"
        # O 'category_orders' foi removido daqui
    )
    # --- INÍCIO DA ALTERAÇÃO DE ORDEM ---
    # Inverte a ordem do eixo Y para alinhar com o funil (de cima para baixo)
    fig_ciclo.update_yaxes(visible=False, autorange="reversed")
    # --- FIM DA ALTERAÇÃO ---
    fig_ciclo.update_traces(textposition='inside', textfont_size=12)
    fig_ciclo.update_layout(
        xaxis_visible=False, 
        yaxis_title=None, 
        showlegend=False,
        margin=dict(t=40, b=5, l=5, r=5)
    )
    st.plotly_chart(fig_ciclo, use_container_width=True)

with col_funil:
    st.subheader("Funil de Conversão")
    fig_funil = px.funnel(
        funil_data,
        x='value',
        y='stage',
        title="Funil de Conversão",
        text='stage',
        template="plotly_dark"
    )
    fig_funil.update_traces(
        textposition='inside',
        hoverinfo='x+y',
        hovertemplate='<b>%{customdata[0]}</b><br>Valor: %{x}<extra></extra>',
        customdata=funil_data[['stage_labels']]
    )
    fig_funil.update_yaxes(categoryorder='array', categoryarray=funil_data['stage'], visible=False)
    fig_funil.update_layout(
        margin=dict(t=40, b=5, l=5, r=5)
    )
    st.plotly_chart(fig_funil, use_container_width=True)

with col_cac:
    st.subheader("CAC (Custo de Aquisição)")
    fig_cac = px.bar(
        funil_data,
        x='cac_por_etapa',
        y='stage_labels',
        orientation='h',
        title="CAC por Etapa",
        text='text_cac_label',
        template="plotly_dark"
        # O 'category_orders' foi removido daqui
    )
    # --- INÍCIO DA ALTERAÇÃO DE ORDEM ---
    # Inverte a ordem do eixo Y para alinhar com o funil (de cima para baixo)
    fig_cac.update_yaxes(visible=False, autorange="reversed")
    # --- FIM DA ALTERAÇÃO ---
    fig_cac.update_traces(textposition='inside', textfont_size=12)
    fig_cac.update_layout(
        xaxis_visible=False, 
        yaxis_title=None, 
        showlegend=False, 
        xaxis_autorange='reversed',
        margin=dict(t=40, b=5, l=5, r=5)
    )
    st.plotly_chart(fig_cac, use_container_width=True)


st.divider()

# --- VISÃO GERAL DO DESEMPENHO ---
st.header("Visão Geral do Desempenho")
col_pizza, col_metrics_geral = st.columns([40, 60])

with col_pizza:
    dados_teste_graph = {
        'Categorias': ['Eletrônicos', 'Roupas', 'Alimentos', 'Livros'],
        'Vendas': [4000, 2500, 3000, 1500]
    }
    df = pd.DataFrame(dados_teste_graph)

    pizza_pie = px.pie(
        df,
        values='Vendas',
        names='Categorias',
        title='Total de Clientes por Segmento de Mercado'
    )
    pizza_pie.update_layout(legend=dict(yanchor="middle", y=0.5, xanchor="right", x=0))
    st.plotly_chart(pizza_pie, use_container_width=True)

with col_metrics_geral:
    st.subheader("Verba Gerenciada e Leads")
    metric_verba_total, metric_leads_total = st.columns(2)
    with metric_verba_total:
        st.metric(
            label="Verba Total Gerenciada",
            value=f"R$ {total_verba_gerenciada:,.2f}"
        )
    with metric_leads_total:
        st.metric(
            label="Quantidade de Leads",
            value=f"{total_leads:,}".replace(",", ".")
        )
        
    st.markdown("<br>", unsafe_allow_html=True)

    metric_verba_meta, metric_verba_google = st.columns(2)
    with metric_verba_meta:
        st.metric(label="Verba Meta", value=f"R$ {verba_meta:,.2f}", delta="60%")
    with metric_verba_google:
        st.metric(label="Verba Google", value=f"R$ {verba_google:,.2f}", delta="40%")
        
    st.markdown("<br>", unsafe_allow_html=True)

    metric_leads_meta, metric_leads_google = st.columns(2)
    with metric_leads_meta:
        st.metric(label="Leads Meta", value=f"{int(leads_meta):,}".replace(",", "."), delta="70%")
    with metric_leads_google:
        st.metric(label="Leads Google", value=f"{int(leads_google):,}".replace(",", "."), delta="30%")


st.divider()

# --- EVOLUÇÃO DAS MÉTRICAS ---
st.header("Evolução das Métricas Chave")
lead_linechart, verba_linechart = st.columns(2)

with lead_linechart:
    fig_cpl = px.line(
        df_cpl,
        x='date',
        y='cost_per_lead',
        color='lead_source',
        title='Custo por Lead (CPL) ao Longo do Tempo',
        markers=True,
        labels={'date': 'Mês', 'cost_per_lead': 'Custo por Lead (R$)', 'lead_source': 'Fonte do Lead'}
    )
    fig_cpl.update_layout(xaxis=dict(tickformat="%b"), hovermode="x unified", template="plotly_dark")
    st.plotly_chart(fig_cpl, use_container_width=True)

with verba_linechart:
    fig_budget = px.line(
        df_budget,
        x='date',
        y='managed_budget',
        color='client_segment',
        title='Verba Gerenciada ao Longo do Tempo',
        markers=True,
        labels={'date': 'Mês', 'managed_budget': 'Verba Gerenciada (R$)', 'client_segment': 'Segmento'}
    )
    fig_budget.update_layout(xaxis=dict(tickformat="%b"), hovermode="x unified", template="plotly_dark")
    st.plotly_chart(fig_budget, use_container_width=True)


st.divider()

# --- MÉTRICAS DE FUNIL E MÍDIA ---
st.header("Métricas de Funil e Mídia")

st.subheader("Taxas de Clique (CTR)")
topofunil, meiofunil, fundofunil = st.columns([33, 33, 33])
with topofunil:
    st.metric(label="Topo Funil", value=f"{ctr_topo:.1f}%")
with meiofunil:
    st.metric(label="Meio Funil", value=f"{ctr_meio:.1f}%")
with fundofunil:
    st.metric(label="Fundo Funil", value=f"{ctr_fundo:.1f}%")


st.subheader("Métricas de Mídia")
col_impressao, col_alcance, col_frequencia = st.columns([33, 33, 33])
with col_impressao:
    st.metric(label="Impressões", value=f"{total_impressoes:,}".replace(",", "."))
    subcol_imp_meta, subcol_imp_google = st.columns(2)
    with subcol_imp_meta:
        st.markdown(f"<small>Meta: {int(impressoes_meta):,}".replace(",", ".") + "</small>", unsafe_allow_html=True)
    with subcol_imp_google:
        st.markdown(f"<small>Google: {int(impressoes_google):,}".replace(",", ".") + "</small>", unsafe_allow_html=True)

with col_alcance:
    st.metric(label="Alcance", value=f"{total_alcance:,}".replace(",", "."))
    subcol_alc_meta, subcol_alc_google = st.columns(2)
    with subcol_alc_meta:
        st.markdown(f"<small>Meta: {int(alcance_meta):,}".replace(",", ".") + "</small>", unsafe_allow_html=True)
    with subcol_alc_google:
        st.markdown(f"<small>Google: {int(alcance_google):,}".replace(",", ".") + "</small>", unsafe_allow_html=True)

with col_frequencia:
    st.metric(label="Frequência", value=f"{total_frequencia:.2f}")


st.divider()

# --- SATISFAÇÃO DO CLIENTE ---
st.header("Satisfação do Cliente")
fig_satisfaction = px.line(
    df_satisfaction,
    x='date',
    y='satisfaction_score',
    color='client_segment',
    title='Satisfação do Cliente ao Longo do Tempo',
    markers=True,
    labels={'date': 'Mês', 'satisfaction_score': 'Pontuação de Satisfação (0-100)', 'client_segment': 'Segmento de Cliente'}
)
fig_satisfaction.update_layout(
    xaxis=dict(tickformat="%b"),
    yaxis_range=[60, 100],
    hovermode="x unified",
    template="plotly_dark"
)
st.plotly_chart(fig_satisfaction, use_container_width=True)