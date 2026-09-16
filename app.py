import pandas as pd
import streamlit as st

st.set_page_config(layout="wide", page_title="Consulta de Secretários", page_icon="🔍")

# --- TRUQUE CSS ATUALIZADO: Design moderno e espaçamentos equilibrados ---
st.markdown(
    """
    <style>
        /* Ajuste do container principal */
        .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
        
        /* Estilização dos cards/fichas para dar profundidade */
        div[data-testid="stVerticalBlock"] > div {
            border-radius: 0px;
        }
        
        /* Customização discreta de títulos */
        h2, h3 {
            color: #1E3A8A;
            font-weight: 600 !important;
        }
        
        /* Ajuste de margens de parágrafos */
        .stMarkdown p { margin-bottom: 0.5rem !important; }
    </style>
    """,
    unsafe_allow_html=True
)

if "indice_secretario_consultado" not in st.session_state:
    st.session_state["indice_secretario_consultado"] = None

# --- CARREGAMENTO SEGURO DOS DADOS ---
try:
    # 🌟 Tenta ler primeiro usando VÍRGULA como separador
    df = pd.read_csv("secretarios_cosems_pb.csv", sep=",", encoding="utf-8-sig", dtype=str, skip_blank_lines=True)
except Exception:
    # 🔄 Caso dê erro, tenta ler usando PONTO E VÍRGULA como plano B
    df = pd.read_csv("secretarios_cosems_pb.csv", sep=";", encoding="utf-8-sig", dtype=str, skip_blank_lines=True)
    
df = df.dropna(how="all")

# MAPEAMENTO INTELIGENTE: Corrigido e adaptado
mapeamento_colunas = {}
for col in df.columns:
    col_limpa = col.strip().lower().replace("-", "").replace(" ", "")
    if "municip" in col_limpa: mapeamento_colunas[col] = "Município"
    elif "secretar" in col_limpa or "nome" in col_limpa: mapeamento_colunas[col] = "Secretário"
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

# Higieniza textos bases de pesquisa
df["Município"] = df["Município"].astype(str).str.strip()
df["Secretário"] = df["Secretário"].astype(str).str.strip()

# --- PAINEL LATERAL DE BUSCA (MELHORIA ESTÉTICA) ---
with st.sidebar:
    st.header("🔍 Painel de Busca")
    st.write("Selecione:")
    
    busca_termo = st.text_input("Digite o Município ou Secretário:", value="")
    
    if busca_termo.strip():
        termo = busca_termo.lower().strip()
        filtro = df["Município"].str.lower().str.contains(termo) | df["Secretário"].str.lower().str.contains(termo)
        registros_encontrados = df[filtro]
        
        if not registros_encontrados.empty:
            opcoes_secretarios = {}
            for idx, row in registros_encontrados.iterrows():
                muni = row["Município"]
                sec = f" ({row['Secretário']})" if pd.notna(row["Secretário"]) and row["Secretário"].strip() and row["Secretário"].lower() != 'nan' else ""
                opcoes_secretarios[f"{muni}{sec}"] = idx
            
            # Garante que a opção em branco fique no topo fixo sem quebrar o sorted()
            lista_ordenada = ["-- Selecione o registro --"] + sorted(list(opcoes_secretarios.keys()))
            
            selecao = st.selectbox("Registros localizados:", lista_ordenada)
            
            if selecao and selecao != "-- Selecione o registro --":
                st.session_state["indice_secretario_consultado"] = opcoes_secretarios[selecao]
            else:
                st.session_state["indice_secretario_consultado"] = None
        else:
            st.session_state["indice_secretario_consultado"] = None
            st.sidebar.warning("Nenhum registro localizado.")
    else:
        st.session_state["indice_secretario_consultado"] = None

# --- ÁREA PRINCIPAL (FICHA DE EXIBIÇÃO DE ALTO IMPACTO VISUAL) ---
st.title("🏛️ Sistema de Consulta — Secretarias de Saúde da Paraíba")

# Adiciona validação para garantir que o índice salvo realmente existe no DataFrame atual
if st.session_state["indice_secretario_consultado"] is not None and st.session_state["indice_secretario_consultado"] in df.index:
    s_idx = st.session_state["indice_secretario_consultado"]
    
    # Cabeçalho da ficha com visual "Card" usando container interno
    with st.container(border=True):
        st.subheader(f"📍 Ficha Institucional — {df.loc[s_idx, 'Município']}")
        st.markdown("---")
        
        # Estrutura limpa em colunas
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            st.markdown(f"👤 **Secretário(a) de Saúde:**<br><span style='font-size: 18px; color: #2563EB; font-weight: bold;'>{df.loc[s_idx, 'Secretário']}</span>", unsafe_allow_html=True)
            st.write("") # Espaçador
            v_em = df.loc[s_idx, "Email"]
            st.write(f"📧 **E-mail Pessoal:** {v_em if pd.notna(v_em) and str(v_em).lower() != 'nan' else '_Não informado_'}")
            v_emi = df.loc[s_idx, "Email Institucional"]
            st.write(f"🏢 **E-mail Institucional:** {v_emi if pd.notna(v_emi) and str(v_emi).lower() != 'nan' else '_Não informado_'}")
            
        with f_col2:
            st.markdown(f"🗺️ **Região de Saúde (CIR):**<br><span style='font-size: 18px; color: #10B981; font-weight: bold;'>{df.loc[s_idx, 'Região de Saúde']}</span>", unsafe_allow_html=True)
            st.write("") # Espaçador
            v_tl = df.loc[s_idx, "Telefone"]
            st.write(f"📱 **Telefone Celular:** {v_tl if pd.notna(v_tl) and str(v_tl).lower() != 'nan' else '_Não informado_'}")
            v_tli = df.loc[s_idx, "Telefone Institucional"]
            st.write(f"☎️ **Telefone Institucional:** {v_tli if pd.notna(v_tli) and str(v_tli).lower() != 'nan' else '_Não informado_'}")
        
        st.markdown("---")
        
        # Coleta das strings de rodapé do card
        v_end = df.loc[s_idx, 'Endereço da SEMUS']
        v_fund = df.loc[s_idx, 'Fundo de Saúde']
        v_cnpj = df.loc[s_idx, 'CNPJ']
        
        txt_end = v_end if pd.notna(v_end) and str(v_end).lower() != 'nan' else 'Não informado'
        txt_fund = v_fund if pd.notna(v_fund) and str(v_fund).lower() != 'nan' else 'Não informado'
        txt_cnpj = v_cnpj if pd.notna(v_cnpj) and str(v_cnpj).lower() != 'nan' else 'Não informado'
        
        # Faixa consolidada mais estilosa dentro do card
        st.info(f"🏢 **Endereço da SEMUS:** {txt_end} \n\n 🏥 **Fundo de Saúde:** {txt_fund} | 📋 **CNPJ:** {txt_cnpj}")

else:
    # Estado inicial amigável quando nenhum município está selecionado ou se reiniciado
    st.markdown("---")
    st.info("💡 **Aguardando consulta:** Utilize o menu ao lado esquerdo para digitar o nome de uma cidade ou gestor e abrir a ficha cadastral completa.")

# --- RODAPÉ DISCRETO ---
st.markdown("---")
st.markdown("<p style='text-align:right; font-size:12px; color:#A3A3A3;'>Bartolomeu Lima - Corecon-ES 1541</p>", unsafe_allow_html=True)
