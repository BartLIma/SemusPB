import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

# --- TRUQUE CSS: Identidade visual padronizada (Ganho máximo de campo de visão) ---
st.markdown(
    """
    <style>
        .block-container { padding-top: 1.2rem !important; padding-bottom: 1rem !important; }
        [data-testid="stSidebarUserContent"] { padding-top: 1.2rem !important; }
        h1 { margin-top: -1.2rem !important; margin-bottom: 0.5rem !important; }
        h3 { margin-top: 0.5rem !important; margin-bottom: 0.5rem !important; }
        .stMarkdown p { margin-bottom: 0.4rem !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# Senha fixa padronizada do seu ecossistema
senha_correta = "ditre123"

if "acesso_liberado" not in st.session_state:
    st.session_state["acesso_liberado"] = False

if "indice_secretario_consultado" not in st.session_state:
    st.session_state["indice_secretario_consultado"] = None

# --- TELA DE LOGIN SEGURA ---
if not st.session_state["acesso_liberado"]:
    st.title("🔐 Painel Secretários - Autenticação")
    col_login, _ = st.columns(2)
    with col_login:
        senha = st.text_input("Digite a senha para acessar:", type="password")
        if st.button("Entrar", use_container_width=True):
            if senha == senha_correta:
                st.session_state["acesso_liberado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta! Tente novamente.")

# --- APLICATIVO PRINCIPAL LIBERADO (SOMENTE CONSULTA) ---
if st.session_state["acesso_liberado"]:
    
    # Carregamento resiliente do arquivo de dados dos secretários
    try:
        df = pd.read_csv("secretarios_cosems_pb.csv", sep=";", encoding="utf-8-sig", dtype=str, skip_blank_lines=True)
    except Exception:
        df = pd.read_csv("secretarios_cosems_pb.csv", sep=",", encoding="utf-8-sig", dtype=str, skip_blank_lines=True)
        
    df = df.dropna(how="all")

    # 🌟 MAPEAMENTO INTELIGENTE: Adapta os cabeçalhos para o padrão exato exigido pelas suas colunas
    mapeamento_colunas = {}
    for col in df.columns:
        col_limpa = col.strip().lower().replace("-", "").replace(" ", "")
        if "municip" in col_limpa: mapeamento_colunas[col] = "Município"
        elif "secretar" in col_limpa: mapeamento_colunas[col] = "Secretário"
        elif "emailinstitucional" in col_limpa: mapeamento_colunas[col] = "Email Institucional"
        elif "email" in col_limpa: mapeamento_colunas[col] = "Email"
        elif "telefoneinstitucional" in col_limpa: mapeamento_colunas[col] = "Telefone Institucional"
        elif "telefon" in col_limpa: mapeamento_colunas[col] = "Telefone"
        elif "enderec" in col_limpa: mapeamento_colunas[col] = "Endereço da SEMUS"
        elif "fundodesaud" in col_limpa: mapeamento_colunas[col] = "Fundo de Saúde"
        elif "cnpj" in col_limpa: mapeamento_colunas[col] = "CNPJ"
        elif "regiaodesaud" in col_limpa: mapeamento_colunas[col] = "Região de Saúde"

    df = df.rename(columns=mapeamento_colunas)

    # Criação de colunas de segurança caso falte alguma no CSV de origem
    lista_colunas_secretarios = ["Município", "Secretário", "Email", "Email Institucional", "Telefone", "Telefone Institucional", "Endereço da SEMUS", "Fundo de Saúde", "CNPJ", "Região de Saúde"]
    for col_nome in lista_colunas_secretarios:
        if col_nome not in df.columns:
            df[col_nome] = ""

    # Higieniza textos bases de pesquisa para não travar com espaços falsos
    df["Município"] = df["Município"].astype(str).str.strip()
    df["Secretário"] = df["Secretário"].astype(str).str.strip()

    st.title("🔍 Consulta de Secretários de Saúde - Paraíba")
    
    # 🌟 CAIXA DE BUSCA INTELIGENTE EM BRANCO (Identidade do Proj_GPS)
    busca_termo = st.text_input("Digite o nome do Município ou do Secretário para pesquisar:", value="")
    
    if busca_termo.strip():
        termo = busca_termo.lower().strip()
        # Filtra de forma cruzada: localiza se o termo está contido no nome do município OU no nome do secretário
        filtro = df["Município"].str.lower().str.contains(termo) | df["Secretário"].str.lower().str.contains(termo)
        registros_encontrados = df[filtro]
        
        if not registros_encontrados.empty:
            # Estrutura a lista reativa de resultados encontrados
            opcoes_secretarios = {"-- Selecione um registro da lista --": None}
            for idx, row in registros_encontrados.iterrows():
                muni = row["Município"]
                sec = f" ({row['Secretário']})" if pd.notna(row["Secretário"]) and row["Secretário"].strip() and row["Secretário"].lower() != 'nan' else ""
                opcoes_secretarios[f"{muni}{sec}"] = idx
            
            selecao = st.selectbox("Selecione o registro exato para abrir a ficha:", sorted(opcoes_secretarios.keys()))
            if selecao and opcoes_secretarios[selecao] is not None:
                st.session_state["indice_secretario_consultado"] = opcoes_secretarios[selecao]
        else:
            st.session_state["indice_secretario_consultado"] = None
            st.warning("Nenhum secretário ou município correspondente foi localizado.")
    else:
        st.session_state["indice_secretario_consultado"] = None
        st.info("💡 Por favor, digite o nome de uma cidade ou secretário acima para realizar a consulta.")
    # --- EXIBIÇÃO DA FICHA CADASTRAL ENXUGADA (MEMÓRIA DE SESSÃO ATIVA) ---
    if st.session_state["indice_secretario_consultado"] is not None:
        s_idx = st.session_state["indice_secretario_consultado"]
        st.markdown("---")
        st.subheader(f"👤 Ficha Institucional — Município de {df.loc[s_idx, 'Município']}")
        
        # Estrutura em duas colunas limpas para economizar espaço de visão vertical
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            st.write(f"**Secretário de Saúde:** {df.loc[s_idx, 'Secretário']}")
            v_em = df.loc[s_idx, "Email"]
            st.write(f"**E-mail Pessoal:** {v_em if pd.notna(v_em) and str(v_em).lower() != 'nan' else ''}")
            v_emi = df.loc[s_idx, "Email Institucional"]
            st.write(f"**E-mail Institucional:** {v_emi if pd.notna(v_emi) and str(v_emi).lower() != 'nan' else ''}")
        with f_col2:
            st.write(f"**Região de Saúde (CIR):** {df.loc[s_idx, 'Região de Saúde']}")
            v_tl = df.loc[s_idx, "Telefone"]
            st.write(f"**Telefone Celular:** {v_tl if pd.notna(v_tl) and str(v_tl).lower() != 'nan' else ''}")
            v_tli = df.loc[s_idx, "Telefone Institucional"]
            st.write(f"**Telefone Institucional:** {v_tli if pd.notna(v_tli) and str(v_tli).lower() != 'nan' else ''}")
        
        # Coleta das strings de rodapé para a montagem da faixa consolidada
        v_end = df.loc[s_idx, 'Endereço da SEMUS']
        v_fund = df.loc[s_idx, 'Fundo de Saúde']
        v_cnpj = df.loc[s_idx, 'CNPJ']
        
        txt_end = v_end if pd.notna(v_end) and str(v_end).lower() != 'nan' else 'Não informado'
        txt_fund = v_fund if pd.notna(v_fund) and str(v_fund).lower() != 'nan' else 'Não informado'
        txt_cnpj = v_cnpj if pd.notna(v_cnpj) and str(v_cnpj).lower() != 'nan' else 'Não informado'
        
        # 🌟 FAIXA DE DESTAQUE ECONOMIZADORA: Reúne endereço, fundo e CNPJ lado a lado
        st.info(f"🏢 **Endereço da SEMUS:** {txt_end} | 🏥 **Fundo de Saúde:** {txt_fund} | 📋 **CNPJ:** {txt_cnpj}")

# --- RODAPÉ DISCRETO PADRONIZADO DO SEU ECOSSISTEMA ---
st.markdown("---")
st.markdown("<p style='text-align:right; font-size:12px; color:green;'>Bartolomeu Lima - Corecon-ES 1541</p>", unsafe_allow_html=True)
