import streamlit as st
import plotly.express as px

st.header("Distribuição dos Dados")

if 'dados' not in st.session_state:
    st.error("Os dados não foram carregados")
else:
    dados = st.session_state['dados']
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.histogram(dados, x='VALOREMPENHO', 
                            title='Histograma do valor de Empenho')
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.box(dados, x='VALOREMPENHO', 
                            title='BoxPlot do valor de Empenho')
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        fig3 = px.histogram(dados, x='PIB', 
                            title='Histograma do PIB')
        st.plotly_chart(fig3, use_container_width=True)

        fig4 = px.box(dados, x='PIB', 
                            title='BoxPlot do PIB')
        st.plotly_chart(fig4, use_container_width=True)        