import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import date

st.set_page_config(page_title="Visualizador de Ações", layout="wide")
st.title("Visualizador de Ações")

with st.sidebar:
    empresa_selecionada = st.selectbox("Selecione a empresa para visualizar:",
                                 ['AAPL','GOOGL','MSFT','AMZN','TSLA'] )
    start_date = st.date_input("Data de Início", value=date(2020,1,1))
    end_date = st.date_input("Data de Fim", value=date(2020,1,15))
    gerar_graficos = st.button("Gerar Gráficos")

if gerar_graficos :
    data = yf.download(empresa_selecionada, start=start_date, end=end_date)
    if data.size > 0:
        tab1, tab2, tab3, tab4 = st.tabs(["Preço Fechado Ajustado","Volume",
                                          "Gráfico de Velas","Dados"])
        with tab1:
            fig_close = go.Figure()
            fig_close.add_trace(go.Scatter(x=data.index, y=data['Adj Close'],
                            mode='lines', name='Preço Fechado Ajustado'))
            fig_close.update_layout(title=f'Histórico de Preços para {empresa_selecionada}',
                            xaxis_title='Data', yaxis_title='Preço')
            st.plotly_chart(fig_close, use_container_width=True)
        with tab2:
            fig_volume = go.Figure()
            fig_volume.add_trace(go.Bar(x=data.index, y=data['Volume']))
            fig_volume.update_layout(title=f'Volume de Negociação para a empresa {empresa_selecionada}',
                            xaxis_title='Data', yaxis_title='Volume')
            st.plotly_chart(fig_volume, use_container_width=True)
        with tab3:
            fig_candle = go.Figure(data=[go.Candlestick(x=data.index,
                            open=data['Open'],
                            high=data['High'],
                            low=data['Low'],
                            close=data['Close'])])
            fig_candle.update_layout(title=f'Gráfico de Velas para a empresa {empresa_selecionada}',
                            xaxis_title='Data', yaxis_title='Preço')
            st.plotly_chart(fig_candle, use_container_width=True)
        with tab4:
            st.dataframe(data)

    else:
        st.error("Erro ao carregar dados, por favor tente novamente")
    