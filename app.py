import pandas as pd
import streamlit as st

# Carregar a planilha CSV
import pandas as pd
import streamlit as st

# Carregar a planilha CSV
df = pd.read_csv(
    "secretarios_cosems_pb.csv",
    sep=";",            # separador usado pelo Excel em português
    encoding="latin1",  # garante leitura de acentos
    on_bad_lines="skip" # ignora linhas inválidas
)

# Normalizar nomes das colunas (remove espaços extras)
df.columns = df.columns.str.strip()

st.title("Consulta Secretários de Saúde - Paraíba")

# Entrada do município
municipio = st.text_input("Digite o município:")

if municipio:
    # Localiza automaticamente a coluna que contém "municipio"
    col_municipio = [c for c in df.columns if "municipio" in c.lower()]
    
    if col_municipio:
        col_municipio = col_municipio[0]
        # Busca case-insensitive
        resultado = df[df[col_municipio].str.lower() == municipio.lower()]
        
        if not resultado.empty:
            cir = resultado.iloc[0].get("CIR", "")
            secretario = resultado.iloc[0].get("Secretário", "")
            email = resultado.iloc[0].get("E-mail", "")
            email_inst = resultado.iloc[0].get("E-mail Institucional", "")
            telefone = resultado.iloc[0].get("Telefone", "")
            telefone_inst = resultado.iloc[0].get("Telefone Institucional", "")
            endereco = resultado.iloc[0].get("Endereço da SMS", "")
            
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
    else:
        st.error("A coluna 'Município' não foi encontrada na planilha.")

# garante que a primeira linha seja usada como cabeçalho



# Normalizar nomes das colunas (remove espaços extras)
df.columns = df.columns.str.strip()

st.title("Consulta Secretários de Saúde - Paraíba")

# Entrada do município
municipio = st.text_input("Digite o município:")

if municipio:
    # Localiza automaticamente a coluna que contém "municipio"
    col_municipio = [c for c in df.columns if "municipio" in c.lower()]
    
    if col_municipio:
        col_municipio = col_municipio[0]
        # Busca case-insensitive
        resultado = df[df[col_municipio].str.lower() == municipio.lower()]
        
        if not resultado.empty:
            cir = resultado.iloc[0].get("CIR", "")
            secretario = resultado.iloc[0].get("Secretário", "")
            email = resultado.iloc[0].get("E-mail", "")
            email_inst = resultado.iloc[0].get("E-mail Institucional", "")
            telefone = resultado.iloc[0].get("Telefone", "")
            telefone_inst = resultado.iloc[0].get("Telefone Institucional", "")
            endereco = resultado.iloc[0].get("Endereço da SMS", "")
            
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
    else:
        st.error("A coluna 'Município' não foi encontrada na planilha.")
