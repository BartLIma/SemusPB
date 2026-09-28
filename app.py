import pandas as pd
import streamlit as st
import urllib.parse
import unicodedata

st.set_page_config(layout="wide", page_title="Consulta de Secretários", page_icon="🔍")

# --- TRUQUE CSS ATUALIZADO ---
st.markdown(
    """
    <style>
        .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
        div[data-testid="stVerticalBlock"] > div { border-radius: 0px; }
        h2, h3 { color: #1E3A8A; font-weight: 600 !important; }
        .stMarkdown p { margin-bottom: 0.5rem !important; }
    </style>
    """,
    unsafe_allow_html=True
)

if "indice_secretario_consultado" not in st.session_state:
    st.session_state["indice_secretario_consultado"] = None

# --- CARREGAMENTO SEGURO DOS DADOS ---
encodings_para_testar = ["utf-8-sig", "ISO-8859-1", "cp1252"]
df = None

for enc in encodings_para_testar:
    try:
        df = pd.read_csv("secretarios_cosems_pb.csv", sep=",", encoding=enc, dtype=str, skip_blank_lines=True)
        break
    except Exception:
        continue

if df is None:
    for enc in encodings_para_testar:
        try:
            df = pd.read_csv("secretarios_cosems_pb.csv", sep=";", encoding=enc, dtype=str, skip_blank_lines=True)
            break
        except Exception:
            continue

if df is None:
    st.error("❌ Não foi possível ler o arquivo 'secretarios_cosems_pb.csv'. Verifique se o arquivo está na pasta ou se o formato é válido.")
    st.stop()
    
df = df.dropna(how="all")

# Função robusta para limpar cabeçalhos (remove acentos, espaços e pontuações)
def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto.strip().lower().replace("-", "").replace(" ", "").replace("_", "")

# --- MAPEAMENTO SEM FALHAS PARA O ENDEREÇO E COLUNAS ---
mapeamento_colunas = {}
for col in df.columns:
    col_limpa = normalizar_texto(col)
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

# Garante a existência de todas as colunas necessárias na estrutura do DataFrame
lista_colunas_secretarios = ["Município", "Secretário", "Email", "Email Institucional", "Telefone", "Telefone Institucional", "Endereço da SEMUS", "Fundo de Saúde", "CNPJ", "Região de Saúde"]
for col_nome in lista_colunas_secretarios:
    if col_nome not in df.columns:
        df[col_nome] = ""

df["Município"] = df["Município"].astype(str).str.strip()
df["Secretário"] = df["Secretário"].astype(str).str.strip()
# --- PAINEL LATERAL DE BUSCA ---
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

# --- ÁREA PRINCIPAL ---
st.title("🏛️ Sistema de Consulta — Secretarias de Saúde da Paraíba")

if st.session_state["indice_secretario_consultado"] is not None and st.session_state["indice_secretario_consultado"] in df.index:
    s_idx = st.session_state["indice_secretario_consultado"]
    
    municipio_atual = df.loc[s_idx, 'Município']
    secretario_atual = df.loc[s_idx, 'Secretário']
    regiao_atual = df.loc[s_idx, 'Região de Saúde']
    
    # Tratamento individual e seguro para exibição
    def obter_valor_valido(campo):
        val = df.loc[s_idx, campo]
        if pd.isna(val) or str(val).lower() == 'nan' or str(val).strip() == "":
            return "Não informado"
        return str(val).strip()

    txt_em = obter_valor_valido("Email")
    txt_emi = obter_valor_valido("Email Institucional")
    txt_tl = obter_valor_valido("Telefone")
    txt_tli = obter_valor_valido("Telefone Institucional")
    txt_end = obter_valor_valido("Endereço da SEMUS")
    txt_fund = obter_valor_valido("Fundo de Saúde")
    txt_cnpj = obter_valor_valido("CNPJ")

    # --- GERADOR DE TEXTO PARA EXPORTAÇÃO ---
    texto_exportacao = f"""### 📍 FICHA INSTITUCIONAL — {municipio_atual.upper()}
    
👤 **Secretário(a):** {secretario_atual}
🗺️ **Região de Saúde (CIR):** {regiao_atual}
📧 **E-mail Pessoal:** {txt_em}
🏢 **E-mail Institucional:** {txt_emi}
📱 **Telefone Celular:** {txt_tl}
☎️ **Telefone Institucional:** {txt_tli}
🏢 **Endereço da SEMUS:** {txt_end}
🏥 **Fundo de Saúde:** {txt_fund}
📋 **CNPJ:** {txt_cnpj}
"""

    col_ficha, col_mapa = st.columns([1.2, 0.8], gap="large")
    
    with col_ficha:
        with st.container(border=True):
            st.subheader(f"📍 Ficha Institucional — {municipio_atual}")
            st.markdown("---")
            
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                st.markdown(f"👤 **Secretário(a) de Saúde:**<br><span style='font-size: 18px; color: #2563EB; font-weight: bold;'>{secretario_atual}</span>", unsafe_allow_html=True)
                st.write("") 
                st.write(f"📧 **E-mail Pessoal:** {txt_em}")
                st.write(f"🏢 **E-mail Institucional:** {txt_emi}")
                
            with f_col2:
                st.markdown(f"🗺️ **Região de Saúde (CIR):**<br><span style='font-size: 18px; color: #10B981; font-weight: bold;'>{regiao_atual}</span>", unsafe_allow_html=True)
                st.write("") 
                st.write(f"📱 **Telefone Celular:** {txt_tl}")
                st.write(f"☎️ **Telefone Institucional:** {txt_tli}")
            
            st.markdown("---")
            st.info(f"🏢 **Endereço da SEMUS:** {txt_end}")
            st.warning(f"🏥 **Fundo de Saúde:** {txt_fund}  |  📋 **CNPJ:** {txt_cnpj}")

    with col_mapa:
        with st.container(border=True):
            st.subheader("🛠️ Ações e Localização")
            st.markdown("---")
            
            c1, c2 = st.columns(2)
            with c1:
                st.download_button(
                    label="📥 Baixar Dados (TXT)",
                    data=texto_exportacao,
                    file_name=f"ficha_saude_{municipio_atual.lower().replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with c2:
                with st.popover("📋 Copiar Dados", use_container_width=True):
                    st.code(texto_exportacao, language="markdown")
            
                    st.markdown(" ")
                    st.markdown("🗺️ **Geolocalização Geográfica**")
            
            # Força a limpeza e codificação correta do termo de busca
            termo_mapa = f"{municipio_atual}, Paraiba, Brazil"
            query_localidade = urllib.parse.quote(termo_mapa)
            
            # Link absoluto completo com HTTPS forçado e sem concatenações truncadas
            url_embed = f"https://google.com{query_localidade}&t=&z=13&ie=UTF8&iwloc=&output=embed"
            
            # HTML blindado com aspas triplas para evitar que o navegador junte o domínio da aplicação com o link
            html_mapa = f"""
            <iframe 
                width="100%" 
                height="250" 
                frameborder="0" 
                scrolling="no" 
                marginheight="0" 
                marginwidth="0" 
                src="{url_embed}" 
                style="border: 1px solid #ccc; border-radius:4px;">
            </iframe>
            """
            
            st.markdown(html_mapa, unsafe_allow_html=True)

else:
    st.markdown("---")
    st.info("💡 **Aguardando consulta:** Utilize o menu ao lado esquerdo para digitar o nome de uma cidade ou gestor e abrir a ficha cadastral completa.")

# --- RODAPÉ DISCRETO ---
st.markdown("---")
st.markdown("<p style='text-align:right; font-size:12px; color:#A3A3A3;'>Bartolomeu Lima - Corecon-ES 1541</p>", unsafe_allow_html=True)

