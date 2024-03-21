import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

st.set_page_config(page_title="Teste de Normalidade", layout="wide")
st.title("Teste de Normalidade")

with st.sidebar:
    upload_file = st.file_uploader("Escolha o arquivo:",type=['csv'],
                                   accept_multiple_files=False)
    process_button = st.button("Processar")

if process_button and upload_file is not None:
    try:
        data = pd.read_csv(upload_file, header=0)
        if data.empty or data.iloc[:,0].isnull().all():
            st.error("O arquivo está vazio ou a primeira coluna não tem dados válidos")
        else:
            col1, col2 = st.columns(2)
            with col1:
                fig_hist, ax_hist = plt.subplots()
                ax_hist.hist(data.iloc[:,0].dropna(),bins="auto",
                             color='blue', alpha=0.7, rwidth=0.85)
                ax_hist.set_title("Histograma")
                st.pyplot(fig_hist)
            with col2:
                fig_qq, ax_qq = plt.subplots()
                stats.probplot(data.iloc[:,0].dropna(), dist='norm', plot=ax_qq)
                ax_qq.set_title("QQ Plot")
                st.pyplot(fig_qq)

            shapiro_test = stats.shapiro(data.iloc[:,0].dropna())
            st.write(f"Valor de P: {shapiro_test.pvalue:.5f}")
            if shapiro_test.pvalue > 0.05:
                st.success("Não existem evidências suficientes para rejeitar a hipótese de normalidade dos dados")
            else:
                st.warning("Existem evidências suficientes para rejeitar a hipótese de normalidade dos dados")
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")