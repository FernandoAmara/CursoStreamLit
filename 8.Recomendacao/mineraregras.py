import streamlit as st
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt

st.set_page_config(page_title="Geração de Regras de Recomendação",
                   layout="wide")
st.title("Geração de Regras de Recomendação")

with st.sidebar:
    uploaded_file = st.file_uploader("Escolha o arquivo", type=['csv'])
    suporte_minimo = st.number_input("Suporte Mínimo", 0.0001,1.0,0.01,0.01)
    confianca_minima = st.number_input("Confiança Mínima", 0.0001,1.0,0.2,0.01)
    lift_minimo = st.number_input("Lift Mínimo", 0.0001,10.0,1.0,0.1)
    tamanho_minimo = st.number_input("Tamanho Mínimo", 1,10,2,1)
    processar = st.button("Processar")

if processar and uploaded_file is not None:
    try:
        transactions = []
        for line in uploaded_file:
            transaction = line.decode("utf-8").strip().split(',')
            transactions.append(transaction)
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df = pd.DataFrame(te_ary, columns=te.columns_)

        frequent_itemsets = apriori(df, min_support=suporte_minimo, use_colnames=True)
        regras = association_rules(frequent_itemsets, metric='confidence',
                                   min_threshold=confianca_minima)
        regras_filtradas = regras[(regras['lift'] >= lift_minimo) &
                                 (regras['antecedents'].apply(lambda x: len(x)>= tamanho_minimo )) ]
    
        if not regras_filtradas.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.header("Transações")
                st.dataframe(df)
            with col2:
                st.header("Regras Encontradas")
                st.dataframe(regras_filtradas)
            with col3:
                st.header("Visualização")
                fig,ax = plt.subplots()
                scatter = ax.scatter(regras_filtradas['support'], regras_filtradas['confidence'],
                                     alpha=0.5,c=regras_filtradas['lift'], cmap='viridis')
                plt.colorbar(scatter, label='Lift')
                ax.set_title("Regras de Associação")
                ax.set_xlabel("Suporte")
                ax.set_ylabel("Confiança")
                st.pyplot(fig)
            
            st.header("Resumo das Regras")
            st.write(f"Total de Regras Geradas: {len(regras_filtradas)}")
            st.write(f"Suporte Médio: {regras_filtradas['support'].mean():.4f}")
            st.write(f"Confiança Média: {regras_filtradas['confidence'].mean():.4f}")
            st.write(f"Lift Médio: {regras_filtradas['lift'].mean():.4f}")

            st.download_button(label="Exportar Regras como CSV",
                               data=regras_filtradas.to_csv(index=False),
                               file_name="regras_associacao.csv",
                               mime='text/csv')
        else:
            st.write("Nenhuma regra foi encontrada com os parâmetros definidos")

        
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
