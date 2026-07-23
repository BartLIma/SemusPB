import streamlit as st
import pandas as pd

# Carregar a planilha do COSEMS-PB
df = pd.read_excel("secretários_cosems_pb.xlsx")

st.title("Consulta Secretários de Saúde - Paraíba")

# Entrada do usuário
municipio = st.text_input("Digite o município:")

if municipio:
    # Busca na planilha (case-insensitive)
    resultado = df[df['Município'].str.lower() == municipio.lower()]
    
    if not resultado.empty:
        secretario = resultado.iloc[0]['Secretário']
        email = resultado.iloc[0]['E-mail']
        telefone = resultado.iloc[0]['Telefone']
        
        st.write(f"**Município:** {municipio}")
        st.write(f"**Secretário:** {secretario}")
        st.write(f"**E-mail:** {email}")
        st.write(f"**Telefone:** {telefone}")
    else:
        st.warning("Município não encontrado na base de dados.")
