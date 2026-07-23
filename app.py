import pandas as pd
import streamlit as st

# Carregar a planilha CSV (salva com separador de vírgula)
df = pd.read_csv(
    "secretarios_cosems_pb.csv",
    encoding="latin1",   # garante leitura de acentos
    on_bad_lines="skip",
    header=0             # primeira linha como cabeçalho
)

# Normalizar nomes das colunas (remove espaços e caracteres invisíveis)
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace("﻿", "")  # remove BOM invisível, se existir

st.title("Consulta Secretários de Saúde - Paraíba")

# Entrada do município
municipio = st.text_input("Digite o município:")

if municipio:
    if "Municipio" in df.columns:
        # Busca case-insensitive
        resultado = df[df["Municipio"].str.lower() == municipio.lower()]
        
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
    else:
        st.error("A coluna 'Municipio' não foi encontrada na planilha.")

# Debug opcional: mostrar colunas carregadas
# st.write(df.columns.tolist())
