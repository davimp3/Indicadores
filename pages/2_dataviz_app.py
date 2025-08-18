import streamlit as st
import pandas as pd
import plotly.express as px
from Dados.data_loader import initialize_session_kapthae,initialize_session_leads

st.set_page_config(
    layout="wide"
)


initialize_session_leads()
df_lead = st.session_state['leads']


initialize_session_kapthae()
df_kapthae = st.session_state['kapthae']



colpizza, colmetric = st.columns([40,60])
    
with colpizza:
    
    dados_teste_graph = {
    'Categorias': ['Eletrônicos', 'Roupas', 'Alimentos', 'Livros'],
    'Vendas': [4000, 2500, 3000, 1500]
    }
    df = pd.DataFrame(dados_teste_graph)

    pizza_pie = px.pie(
        df,
        values='Vendas',
        names='Categorias',
        title='Segmento de Mercado'
        )
    
    st.plotly_chart(pizza_pie, use_container_width=True)




with colmetric:

    st.metric(
        label="Verba Total Gerenciada",
        value=134,
        border=True
    )

    st.metric(
        label="Quantidade de Leads:",
        value=1718,
        border=True
    )

st.divider()


st.subheader("Taxa de CLiques")
topofunil, meiofunil, fundofunil = st.columns([33,33,33])
with topofunil:
    st.metric(
        label="Topo Funil",
        value=130,
        border=True
    )
with meiofunil:
    
    st.metric(
        label="Meio Funil",
        value=2345,
        border=True
    )
with fundofunil:
    st.metric(
        label="Fundo Funil",
        value=325,
        border=True
    )
st.divider()

lead_linechart, verba_linechart = st.columns([50, 50])

with lead_linechart:
    data = {
    'date': pd.to_datetime([
        '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01',
        '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01',
        '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01',
    ]),
    'lead_source': [
        'Google Ads'] * 8 + ['Facebook Ads'] * 8 + ['Tráfego Orgânico'] * 8,
    'cost_per_lead': [
        5.50, 5.80, 6.00, 6.20, 6.10, 6.50, 6.40, 6.60,       # Google Ads: CPL sobe e flutua um pouco
        4.80, 5.20, 5.50, 5.90, 6.30, 6.80, 7.00, 7.20,       # Facebook Ads: CPL com tendência de alta mais forte
        3.00, 2.90, 2.80, 2.75, 2.70, 2.70, 2.65, 2.60        # Orgânico: CPL baixo e estável
    ]
}
    df_cpl = pd.DataFrame(data)

    fig = px.line(
    df_cpl,
    x='date',              # Eixo X é a data
    y='cost_per_lead',     # Eixo Y é o custo por lead
    color='lead_source',   # Cor da linha por fonte de lead
    title='Custo por Lead (CPL) ao Longo do Tempo',
    markers=True,          # Adiciona marcadores para cada ponto de dado
    labels={
        'date': 'Data',
        'cost_per_lead': 'Custo por Lead (R$)',
        'lead_source': 'Fonte do Lead'
    }
)


    fig.update_layout(
        xaxis_title='Mês',
        yaxis_title='Custo por Lead (R$)',
        xaxis=dict(tickformat="%b"), # Formata o eixo X para mostrar apenas o mês
        hovermode="x unified",
        template="plotly_dark"
    )


    st.plotly_chart(fig, use_container_width=True)

with verba_linechart:
    data = {
    'date': pd.to_datetime([
        '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01',
        '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01',
    ]),
    'client_segment': [
        'Pequenas Empresas'] * 8 + ['Clientes Corporativos'] * 8,
    'managed_budget': [
        10000, 12000, 15000, 18000, 20000, 22000, 24000, 26000,    # Pequenas: crescimento gradual e constante
        50000, 55000, 60000, 68000, 75000, 82000, 88000, 95000     # Corporativos: crescimento mais acelerado
    ]
    }

    df_budget = pd.DataFrame(data)

    fig = px.line(
    df_budget,
    x='date',              # Eixo X é a data
    y='managed_budget',    # Eixo Y é a verba gerenciada
    color='client_segment',# A cor é baseada no segmento do cliente
    title='Verba Gerenciada ao Longo do Tempo',
    markers=True,
    labels={
        'date': 'Mês',
        'managed_budget': 'Verba Gerenciada (R$)',
        'client_segment': 'Segmento de Cliente'
    }
)

# Ajusta o layout do gráfico
    fig.update_layout(
    xaxis_title='Mês',
    yaxis_title='Verba Gerenciada (R$)',
    xaxis=dict(tickformat="%b"), # Formata o eixo X para mostrar apenas o mês
    hovermode="x unified",
    template="plotly_dark"
    )

# 4. Exibe o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Métricas")
col_impressao, col_alcance, col_frequencia = st.columns([33, 33, 33])

with col_impressao:
    st.metric(
        label="Impressões",
        value=30,
        border=True
    )

with col_alcance:
    st.metric(
        label="Alcance",
        value=45,
        border=True
    )
    
with col_frequencia:
    st.metric(
        label="Frequência",
        value=78,
        border=True
    )

col_cs = st.columns(1)


data = {
    'date': pd.to_datetime([
        '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01',
        '2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01'
    ]),
    'client_segment': [
        'Clientes Gold'] * 8 + ['Novos Clientes'] * 8,
    'satisfaction_score': [
        90, 91, 92, 91, 93, 94, 95, 96,      # Clientes Gold: alta satisfação, com melhora contínua
        75, 78, 80, 79, 82, 85, 84, 86       # Novos Clientes: satisfação menor, mas com tendência de alta
    ]
}

# 2. Converte o dicionário em um DataFrame
df_satisfaction = pd.DataFrame(data)


# 3. Cria o gráfico de linha com Plotly Express
fig = px.line(
    df_satisfaction,
    x='date',              # Eixo X é a data
    y='satisfaction_score',# Eixo Y é a pontuação de satisfação
    color='client_segment',# A cor da linha é baseada no segmento do cliente
    title='Satisfação do Cliente ao Longo do Tempo',
    markers=True,
    labels={
        'date': 'Mês',
        'satisfaction_score': 'Pontuação de Satisfação (0-100)',
        'client_segment': 'Segmento de Cliente'
    }
)

# Ajusta o layout do gráfico
fig.update_layout(
    xaxis_title='Mês',
    yaxis_title='Pontuação de Satisfação',
    xaxis=dict(tickformat="%b"),
    yaxis_range=[60, 100], # Ajusta o range do eixo Y para melhor visualização
    hovermode="x unified",
    template="plotly_dark"
)

# 4. Exibe o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)