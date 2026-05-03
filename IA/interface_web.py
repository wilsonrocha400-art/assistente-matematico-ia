import streamlit as st
from app.solver import answer_math_question

# Configuração da página
st.set_page_config(page_title="Assistente Matemático IA", page_icon="🧮")

st.title("🧮 Assistente Matemático")
st.markdown("Resolva equações complexas usando **IA** e **SymPy**.")

# Campo de entrada
pergunta = st.text_input("Digite sua dúvida ou equação:", placeholder="Ex: quanto é 20% de 500?")

if st.button("Resolver"):
    if pergunta:
        with st.spinner('Processando...'):
            try:
                # Chama a lógica que você já construiu
                resultado = answer_math_question(pergunta)
                
                # Exibe o resultado de forma organizada
                st.success("Cálculo Finalizado!")
                st.subheader("Resultado:")
                st.code(resultado.resposta)
                
                st.info(f"Fonte da resposta: {resultado.fonte}")
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
    else:
        st.warning("Por favor, digite uma pergunta.")