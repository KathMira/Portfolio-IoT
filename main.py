import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
# Conexão com o banco de dados
engine = create_engine('postgresql://postgres:6865@localhost:5432/postgres')

# Função para carregar dados de uma view
def carrega_dados(view_name):
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)

# Título do dashboard
st.title('Dashboard de Temperaturas IoT')

# Gráfico 1: Média de temperatura por dia
st.header('Média de Temperatura por Dia')
data_avg_temp = carrega_dados('media_temperatura_salas_por_dia')
grafico1 = px.line(
    data_avg_temp,
    x='date',
    y='avg_temp',
    color='out_in',  # Diferenciar pelas categorias 'in' e 'out'
    labels={'out_in': 'Tipo'}
)

grafico1.update_layout(
    yaxis=dict(range=[0, data_avg_temp['avg_temp'].max() + 5])  # Adiciona margem ao topo
)

st.plotly_chart(grafico1)

st.header('Média de temperatura externa no dia por mês')
data_avg_temp = carrega_dados('media_temperatura_externa_no_dia_por_mes')
grafico2 = px.bar(
    data_avg_temp,
    x='hour', 
    y='avg_temp', 
    color='month',
    barmode='group'
    )

grafico2.update_layout(
    yaxis=dict(range=[data_avg_temp['avg_temp'].min() - 1, data_avg_temp['avg_temp'].max() + 5])  # Adiciona margem ao topo
)

st.plotly_chart(grafico2)

st.header('Média de temperatura interna no dia por mês')
data_avg_temp = carrega_dados('media_temperatura_interna_no_dia_por_mes')
grafico3 = px.bar(
    data_avg_temp,
    x='hour',
    y='avg_temp', 
    color='month',
    barmode='group'
    )

grafico3.update_layout(
    yaxis=dict(range=[data_avg_temp['avg_temp'].min() - 1, data_avg_temp['avg_temp'].max() + 5])  # Adiciona margem ao topo
)

st.plotly_chart(grafico3)