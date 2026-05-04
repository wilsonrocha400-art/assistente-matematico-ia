import sympy
import re


def answer_math_question(question: str):
    class Result:
        pass
    res = Result()

    # 1. Tradutor e Limpeza de Dados
    input_limpo = question.lower()
    input_limpo = input_limpo.replace("quanto é ", "")
    input_limpo = input_limpo.replace("% de ", "/100 * ")
    input_limpo = input_limpo.replace("%", "/100")
    input_limpo = input_limpo.replace(
        "elevado a", "**").replace("^", "**").replace(",", ".")

    # Corrige 2x para 2*x e x2 para x**2
    input_limpo = re.sub(r'(\d)x', r'\1*x', input_limpo)
    input_limpo = input_limpo.replace(
        "x2", "x**2").replace("raiz de ", "sqrt(")

    if "sqrt(" in input_limpo and ")" not in input_limpo:
        input_limpo += ")"

    # 2. Filtro de Autoria
    if "wilson" in input_limpo or "criador" in input_limpo:
        res.resposta = "Esta IA foi desenvolvida por Wilson Rocha do Nascimento, focado em Análise de Dados."
        return res

    # 3. Processamento de Cálculo com Tratamento de Erro
    try:
        if "x" in input_limpo:
            # Resolve como Equação
            if "=" in input_limpo:
                partes = input_limpo.split("=")
                equacao = f"({partes[0]}) - ({partes[1]})"
            else:
                equacao = input_limpo

            x = sympy.Symbol('x')
            solucao = sympy.solve(equacao, x)
            res.resposta = f"Para a equação **{question}**, o valor de x é: **{solucao}**"
        else:
            # Resolve como Conta Normal
            resultado_calculado = sympy.sympify(input_limpo)
            res.resposta = f"O resultado de **{question}** é: **{resultado_calculado}**"

    except Exception:
        res.resposta = "Não entendi a expressão. Use 'x' para equações ou '**' para potência (ex: 3**3)."

    return res
