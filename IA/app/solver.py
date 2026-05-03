import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from sympy import Eq, SympifyError, simplify, solve, sympify
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    standard_transformations,
    parse_expr,
)
from app.schemas import MathAnswer

load_dotenv()


def limpar_texto(texto):
    if not isinstance(texto, str):
        return texto

    texto = texto.lower().strip()

    # Remove frases comuns de pergunta
    frases_remover = ["quanto é", "calcule", "resolva", "resultado de"]
    for frase in frases_remover:
        texto = texto.replace(frase, "")

    # Tradução matemática
    substituicoes = {
        "raiz quadrada de ": "sqrt(",
        "raiz de ": "sqrt(",
        "elevado a ": "**",
        "vezes": "*",
        "dividido por": "/"
    }

    for palavra, simbolo in substituicoes.items():
        texto = texto.replace(palavra, simbolo)

    if "sqrt(" in texto and ")" not in texto:
        texto += ")"

    return texto.strip()


def answer_math_question(question: str, foto=None) -> MathAnswer:
    # 1. Filtro de Autoria (Garante que sua marca Wilson Rocha apareça)
    autoria_keywords = ["quem", "criador", "desenvolveu", "wilson", "dono"]
    if question and any(word in question.lower() for word in autoria_keywords):
        instrucao_ia = f"Sua identidade: Criada por Wilson Rocha do Nascimento. Responda: {question}"
        ai_answer = ask_openai(instrucao_ia)
        return MathAnswer(questao=question, resposta=ai_answer, fonte="openai")

    # 2. Lógica para resolver por FOTO
    if foto is not None:
        try:
            import base64
            bytes_data = foto.getvalue()
            base64_image = base64.b64encode(bytes_data).decode('utf-8')

            # Chama a função de visão (vamos criá-la abaixo)
            resposta_ia = ask_openai_com_imagem(base64_image, question)
            return MathAnswer(questao="Problema por imagem", resposta=resposta_ia, fonte="openai (vision)")
        except Exception as e:
            return MathAnswer(questao="Erro na imagem", resposta=f"Erro ao processar foto: {str(e)}", fonte="erro")

    # 3. Lógica para resolver por TEXTO (o que você já tinha)
    pergunta_limpa = limpar_texto(question)
    local_answer = solve_locally(pergunta_limpa)
    ai_answer = ask_openai(question, local_answer)

    return MathAnswer(questao=question, resposta=ai_answer, fonte="openai")


def ask_openai_com_imagem(base64_image, question=None):
    from openai import OpenAI
    import streamlit as st

    # Aqui está o ajuste: forçamos o cliente a usar a sua chave salva
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
