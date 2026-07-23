import streamlit as st
import pandas as pd

# Carregar a planilha (certifique-se que o nome está correto e sem acento)
df = pd.read_excel("secretarios_cosems_pb.csv")

st.title("Consulta Secretários de Saúde - Paraíba")

# Entrada do município
municipio = st.text_input("Digite o município:")

if municipio:
    # Busca case-insensitive
    resultado = df[df['Município'].str.lower() == municipio.lower()]
    
    if not resultado.empty:
        cir = resultado.iloc[0]['CIR']
        secretario = resultado.iloc[0]['Secretário']
        email = resultado.iloc[0]['E-mail']
        email_inst = resultado.iloc[0]['E-mail Institucional']
        telefone = resultado.iloc[0]['Telefone']
        telefone_inst = resultado.iloc[0]['Telefone Institucional']
        endereco = resultado.iloc[0]['Endereço da SMS']
        
        st.subheader(f"Município: {municipio}")
        st.write(f"**CIR:** {cir}")
        st.write(f"**Secretário:** {secretario}")
        st.write(f"**E-mail:** {email}")
        st.write(f"**E-mail Institucional:** {email_inst}")
        st.write(f"**Telefone:** {telefone}")
        st.write(f"**Telefone Institucional:** {telefone_inst}")
        st.write(f"**Endereço da SMS:** {endereco}")
    else:
        st.warning("Município não encontrado na base de dados.")
