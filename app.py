# 📑 Bloco 4 — Prestação de Contas / Execução
with st.expander("Prestação de Contas / Execução"):
    st.write(f"**Data de Envio da PC:** {resultado.iloc[0].get('Data de Envio da PC', '')}")
    st.write(f"**Dias de Atraso:** {resultado.iloc[0].get('Dias de Atraso', '')}")
    st.write(f"**Dias Após Envio da PC:** {resultado.iloc[0].get('Dias apos Envio da PC', '')}")
    st.write(f"**PC Informatizada:** {resultado.iloc[0].get('PC Informatizada', '')}")
    
    # Inclusão dos campos de risco logo após PC Informatizada
    st.write(f"**Nota de Risco:** {resultado.iloc[0].get('Nota de Risco', '')}")
    st.write(f"**Limite Toler Risco:** {resultado.iloc[0].get('Limite Toler  Risco', '')}")
    faixa_risco = resultado.iloc[0].get('Faixa de Risco', '')
    if pd.isna(faixa_risco):
        faixa_risco = "Não informado"
    st.write(f"**Faixa de Risco:** {faixa_risco}")

    st.write(f"**Grau de Prioridade:** {resultado.iloc[0].get('Grau de Prioridade', '')}")
    st.write(f"**Relatórios de Execução:** {resultado.iloc[0].get('Relatorios de Execucao', '')}")
    st.write(f"**Ação de Monitoramento:** {resultado.iloc[0].get('Acao de Monitoramnto', '')}")
    st.write(f"**Parecer Financeiro:** {resultado.iloc[0].get('Parecer Financeiro', '')}")
    st.write(f"**Parecer Tec-Mérito:** {resultado.iloc[0].get('Parecer Tec -Merito', '')}")
    st.write(f"**Análise de Equipamentos:** {resultado.iloc[0].get('Analise de Equipamentos', '')}")
    st.write(f"**Ação de Análise de PC:** {resultado.iloc[0].get('Acao de Analise de PC', '')}")
    st.write(f"**Percentual de Evolução da Análise:** {resultado.iloc[0].get('Percentual de Evolucoo da Analise', '')}")
    st.write(f"**Pareceres Incluídos na Plataforma:** {resultado.iloc[0].get('Pareceres Incluidos na Plataforma', '')}")
