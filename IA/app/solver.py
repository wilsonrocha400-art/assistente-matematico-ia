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
    frases_remover = ["quanto é", "calcule", "resolva", "resultado de", "?"]
    for frase in frases_remover:
        texto = texto.replace(frase, "")
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

TRANSFORMATIONS = standard_transformations + \
    (implicit_multiplication_application,)


def answer_math_question(question: str) -> MathAnswer:
    # 1. Limpa o texto da pergunta
    pergunta_limpa = limpar_texto(question)
    
    # 2. Usa a pergunta limpa para calcular
    local_answer = solve_locally(pergunta_limpa)
    ai_answer = ask_openai(pergunta_limpa, local_answer)

    if ai_answer:
        return MathAnswer(questao=question, resposta=ai_answer, fonte="openai")

    if ai_answer:
        return MathAnswer(questao=question, resposta=ai_answer, fonte="openai")

    return MathAnswer(questao=question, resposta=local_answer, fonte="sympy")


def solve_locally(question: str) -> str:
    expression = extract_math_expression(question)

    if not expression:
        return (
            "Nao consegui identificar a expressao matematica. "
            "Tente escrever algo como: Resolva 3x - 5 = 10."
        )

    try:
        if "=" in expression:
            left_text, right_text = expression.split("=", 1)
            left = parse_math(left_text)
            right = parse_math(right_text)
            equation = Eq(left, right)
            variables = sorted(equation.free_symbols,
                               key=lambda item: item.name)
            result = solve(equation, variables[0]) if variables else []

            if result:
                variable = variables[0]
                return (
                    f"Equacao identificada: {equation}\n"
                    f"Variavel: {variable}\n"
                    f"Solucao: {variable} = {result}"
                )

            return f"Equacao identificada: {equation}\nNao encontrei solucao simbolica."

        parsed = parse_math(expression)
        simplified = simplify(parsed)
        return f"Expressao identificada: {parsed}\nForma simplificada: {simplified}"

    except (SympifyError, SyntaxError, ValueError, TypeError) as error:
        return (
            "Tive dificuldade para resolver essa questao automaticamente.\n"
            f"Detalhe tecnico: {error}"
        )


def ask_openai(question: str, local_answer: str) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4.1")

    prompt = f"""
Voce e uma IA tutora de matematica para estudantes brasileiros.
Responda em portugues do Brasil.
Explique passo a passo, de forma curta e clara.
Quando houver conta, mostre o raciocinio antes da resposta final.
Se a resolucao local abaixo tiver erro ou for insuficiente, corrija com cuidado.

Questao do aluno:
{question}

Resolucao local gerada pelo sistema:
{local_answer}
""".strip()

    response = client.responses.create(
        model=model,
        instructions="Voce e um tutor de matematica paciente, preciso e didatico.",
        input=prompt,
    )

    return response.output_text


def extract_math_expression(question: str) -> str:
    text = question.lower()
    text = text.replace("quanto e", "")
    text = text.replace("quanto é", "")
    text = text.replace("resolva", "")
    text = text.replace("simplifique", "")
    text = text.replace("^", "**")
    text = text.replace("÷", "/")
    text = text.replace("×", "*")

    percent_match = re.search(
        r"(\d+(?:[,.]\d+)?)\s*%\s*de\s*(\d+(?:[,.]\d+)?)", text)
    if percent_match:
        percent = percent_match.group(1).replace(",", ".")
        value = percent_match.group(2).replace(",", ".")
        return f"({percent}/100)*{value}"

    allowed = re.findall(r"[0-9a-z+\-*/().=,\s]+", text)
    expression = " ".join(allowed).strip()
    return expression.replace(",", ".")


def parse_math(expression: str):
    try:
        return parse_expr(expression, transformations=TRANSFORMATIONS)
    except Exception:
        return sympify(expression)


if __name__ == "__main__":
    print("--- Assistente Matemático Iniciado (digite 'sair' para encerrar) ---")

    while True:
        pergunta = input("\nDigite sua pergunta matemática: ")

        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Encerrando... Até logo!")
            break

        try:
            resultado = answer_math_question(pergunta)
            print(f"Resultado: {resultado.resposta}")
            print(f"Fonte utilizada: {resultado.fonte}")
        except Exception as e:
            print(f"Erro ao processar: {e}")
