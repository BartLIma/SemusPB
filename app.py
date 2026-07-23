import pandas as pd
import streamlit as st

# Carregar a planilha CSV (separador ponto e vírgula)
df = pd.read_csv(
    "secretarios_cosems_pb.csv",
    sep=";", 
    encoding="latin1", 
    on_bad_lines="skip",
    header=0
)

# Normalizar nomes das colunas
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace("﻿", "")  # remove BOM invisível

st.title("Consulta Secretários de Saúde - Paraíba")

# Criar lista de municípios únicos
municipios = sorted(df["Municipio"].dropna().unique())

# Selectbox para escolher município
municipio = st.selectbox("Selecione o município:", municipios)

if municipio:
    # Busca case-insensitive e tolerante a espaços
    resultado = df[df["Municipio"].str.lower().str.strip() == municipio.lower().strip()]
    
    if not resultado.empty:
        secretario = resultado.iloc[0].get("Secretario", "")
        email = resultado.iloc[0].get("Email", "")
        email_inst = resultado.iloc[0].get("Email Institucional", "")
        telefone = resultado.iloc[0].get("Telefone", "")
        telefone_inst = resultado.iloc[0].get("Telefone Institucional", "")
        endereco = resultado.iloc[0].get("Endereço da SEMUS", "")
        
        st.subheader(f"Município: {municipio}")
        st.write(f"**Secretário:** {secretario}")
        st.write(f"**E-mail:** {email}")
        st.write(f"**E-mail Institucional:** {email_inst}")
        st.write(f"**Telefone:** {telefone}")
        st.write(f"**Telefone Institucional:** {telefone_inst}")
        st.write(f"**Endereço da SEMUS:** {endereco}")
    else:
        st.warning("Município não encontrado na base de dados.")
