import streamlit as st
# Carregar a planilha (certifique-se que o nome está correto e sem acento)

dimport pandas as pd
import pandas as pd

df = pd.read_csv(
    "secretarios_cosems_pb.csv",
    sep=";",            # separador usado pelo Excel em português
    encoding="latin1",  # garante leitura de acentos
    on_bad_lines="skip" # ignora linhas inválidas
)


df = pd.read_csv("secretarios_cosems_pb.csv", sep=";", encoding="latin1", on_bad_lines="skip")


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
