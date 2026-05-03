import streamlit as st
from app.solver import answer_math_question

# 1. Configuração da página (DEVE ser o primeiro comando do Streamlit)
st.set_page_config(page_title="Assistente Matemático IA", page_icon="🔢")

# 2. Configuração da Barra Lateral (Sua biografia)
with st.sidebar:
    st.subheader("⌨️ Guia de Símbolos")

    # Usando Markdown para uma lista mais elegante e clara
    st.markdown("""
    *   **+**  → Soma
    *   **-**  → Subtração
    *   **\***  → Multiplicação
    *   **/**  → Divisão
    *   **\*\*** ou `elevado a` → Potência
    *   `raiz de` → Raiz Quadrada
    *   **,** (vírgula) → O sistema converte para **.** (ponto)
    """)

    st.divider()

    # Sua biografia continua aqui abaixo...

    st.title("Sobre o Desenvolvedor")
    st.write("""
    Wilson Rocha do Nascimento é um profissional de TI de 25 anos, atuando como Auxiliar de CPD no Grupo Mateus. 
    Com 5 anos de experiência em suporte operacional e infraestrutura, ele está em seu último ano de estudos 
    (conclusão em 2026) e foca sua transição de carreira para Análise de Dados e programação em Python.
    """)
    st.divider()
    st.info("Focado em Evolução Profissional e Análise de Dados.")
# 3. Título Principal e Interface
st.title("🔢 Assistente Matemático")
st.markdown("Resolva equações complexas usando **IA** e **SymPy**.")

# 4. Campo de entrada e lógica
pergunta = st.text_input("Digite sua dúvida ou equação:",
                         placeholder="Ex: quanto é 20% de 500?")

# 5. Inicializar o histórico na memória se ele não existir
if 'historico' not in st.session_state:
    st.session_state['historico'] = []

# 6. Lógica do botão Resolver
if st.button("Resolver"):
    if pergunta:
        with st.spinner("Analisando o problema..."):
            resultado = answer_math_question(pergunta)

            # SALVAR NO HISTÓRICO: Guardamos a pergunta e a resposta
            item_historico = f"❓ {pergunta}  \n✅ {resultado.resposta}"
            st.session_state['historico'].insert(
                0, item_historico)  # Adiciona no topo

            st.subheader("Resultado:")
            st.write(resultado.resposta)
    else:
        st.warning("Por favor, digite uma pergunta ou equação para resolver.")

# 7. Exibir o Histórico na Barra Lateral (Sidebar)
with st.sidebar:
    st.divider()
    st.subheader("📜 Histórico de Cálculos")
    if st.session_state['historico']:
        for item in st.session_state['historico']:
            st.info(item)
            # Botão opcional para limpar o histórico
        if st.button("Limpar Histórico"):
            st.session_state['historico'] = []
            st.rerun()
    else:
        st.write("Nenhum cálculo realizado ainda.")
