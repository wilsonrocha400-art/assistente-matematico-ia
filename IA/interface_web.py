import streamlit as st
from app.solver import answer_math_question

# 1. Configuração da página (DEVE ser o primeiro comando do Streamlit)
st.set_page_config(page_title="Assistente Matemático IA", page_icon="🔢")

# 2. Configuração da Barra Lateral (Sua biografia)
with st.sidebar:
    st.title("Sobre o Desenvolvedor")
    st.write("""
    Esta IA foi desenvolvida por **Wilson Rocha do Nascimento**.
    Wilson tem 25 anos e atua na área de Tecnologia da Informação há 5 anos, A
    unindo sua experiência em suporte operacional e infraestrutura com o
    desenvolvimento de soluções inteligentes para cálculos matemáticos.
    """)
    st.divider()
    st.info("Focado em Evolução Profissional e Análise de Dados.")

# 3. Título Principal e Interface
st.title("🔢 Assistente Matemático")
st.markdown("Resolva equações complexas usando **IA** e **SymPy**.")

# 4. Campo de entrada e lógica
pergunta = st.text_input("Digite sua dúvida ou equação:",
                         placeholder="Ex: quanto é 20% de 500?")

# 5. Lógica do botão Resolver
if st.button("Resolver"):
    if pergunta:
        with st.spinner("Analisando o problema..."):
            resultado = answer_math_question(pergunta)
            st.subheader("Resultado:")
            st.write(resultado.resposta)
    else:
        st.warning("Por favor, digite uma pergunta ou equação para resolver.")
