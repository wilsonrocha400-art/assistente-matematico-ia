import streamlit as st
from openai import OpenAI
import base64

# 1. Função de Visão (para fotos)


def ask_openai_com_imagem(base64_image, question=None):
    # Tenta pegar a chave de duas formas para não dar erro
    api_key = st.secrets.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    prompt = question if question else "Resolva este problema matemático passo a passo."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content

# 2. Funções auxiliares (deixe-as aqui antes da função principal)


def solve_locally(query):
    # Aqui vai sua lógica do SymPy que você já tinha
    return None


def ask_openai(question, local_result=None):
    api_key = st.secrets.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    # Sua lógica de texto aqui
    return "Resposta da IA"

# 3. FUNÇÃO PRINCIPAL (O coração do sistema)


def answer_math_question(question: str, foto=None):
    # Se tiver foto, ele vai direto para a visão
    if foto is not None:
        try:
            bytes_data = foto.getvalue()
            base64_image = base64.b64encode(bytes_data).decode('utf-8')
            resposta = ask_openai_com_imagem(base64_image, question)
            # Criando um objeto simples para o Streamlit ler

            class Result:
                pass
            r = Result()
            r.resposta = resposta
            return r
        except Exception as e:
            class Result:
                pass
            r = Result()
            r.resposta = f"Erro na imagem: {str(e)}"
            return r

    # Se for texto, ele faz o caminho normal
    resposta_texto = ask_openai(question)

    class Result:
        pass
    r = Result()
    r.resposta = resposta_texto
    return r
