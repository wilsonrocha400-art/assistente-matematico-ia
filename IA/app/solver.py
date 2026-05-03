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


def answer_math_question(question: str) -> MathAnswer:
    # Limpa o texto (Ex: 'Raiz de 9' vira 'sqrt(9)')
    pergunta_limpa = limpar_texto(question)

    # Aqui o sistema usa as funções de cálculo
    # (Certifique-se que solve_locally e ask_openai existem no seu projeto)
    local_answer = solve_locally(pergunta_limpa)
  # Definindo a instrução de autoria para o Wilson
    instrucao_ia = f"Sua identidade: Criada por Wilson Rocha do Nascimento. Responda: {pergunta_limpa}"

    # Chamando a IA com a nova instrução
    ai_answer = ask_openai(instrucao_ia, local_answer)
    if ai_answer:
        return MathAnswer(questao=question, resposta=ai_answer, fonte="openai")
