import streamlit as st
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
from datetime import date
from io import StringIO

st.set_page_config(page_title="Sistema de Análise e Previsão de Séries Temporais", 
                   layout="wide")

st.title("Sistema de Análise e Previsão de Séries Temporais")

with st.sidebar:
    uploaded_file = st.file_uploader("Escolha o arquivo:", type=['csv'])
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        data = pd.read_csv(stringio, header=None)
        data_inicio = date(2000,1,1)
        periodo = st.date_input("Período Inicial da Série", data_inicio)
        periodo_previsao = st.number_input("Informe quantos meses quer prever", min_value=1, max_value=48, value=12)
        processar = st.button("Processar")

if uploaded_file is not None and processar:
    try:
        ts_data = pd.Series(data.iloc[:,0].values, index= pd.date_range(
                start=periodo, periods=len(data), freq='M'  ))
        decomposicao = seasonal_decompose(ts_data, model='additive')
        fig_decomposicao = decomposicao.plot()
        fig_decomposicao.set_size_inches(10,8)

        modelo = SARIMAX(ts_data,order=(2,0,0), seasonal_order=(0,1,1,12))
        modelo_fit = modelo.fit()
        previsao = modelo_fit.forecast(steps=periodo_previsao)

        fig_previsao, ax = plt.subplots(figsize=(10,5))
        ax = ts_data.plot(ax=ax)
        previsao.plot(ax=ax, style='r--')

        col1, col2, col3  = st.columns([3,3,2])
        with col1:
            st.write("Decomposição")
            st.pyplot(fig_decomposicao)
        with col2:
            st.write("Previsão")
            st.pyplot(fig_previsao)
        with col3:
            st.write("Dados da Previsão")
            st.dataframe(previsao)

        
    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")
    
