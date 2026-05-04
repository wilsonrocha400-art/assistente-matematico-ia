import sympy


def answer_math_question(question: str):
    class Result:
        pass
    res = Result()

# 10. Tradutor de termos (agora com a raiz corrigida)
# Tradutor para Porcentagem (Adicione estas linhas)
    input_limpo = input_limpo.replace("quanto é ", "")
    input_limpo = input_limpo.replace("% de ", "/100 * ")
    input_limpo = input_limpo.replace("%", "/100")
    input_limpo = question.lower().replace(
        "elevado a", "**").replace("^", "**").replace(",", ".")
    # 12. Corrige a falta do '*' entre número e x (ex: 2x vira 2*x)
    import re
    # Primeiro corrige o 2x para 2*x
    input_limpo = re.sub(r'(\d)x', r'\1*x', input_limpo)
    # Depois corrige o x2 e a raiz
    input_limpo = input_limpo.replace(
        "x2", "x**2").replace("raiz de ", "sqrt(")
    if "sqrt(" in input_limpo and ")" not in input_limpo:
        input_limpo += ")"
        # Filtro de Autoria (Mantendo o que já tínhamos)
    if "wilson" in input_limpo or "criador" in input_limpo:
        res.resposta = res.resposta = "Esta IA foi desenvolvida por Wilson Rocha do Nascimento, focado em Análise de Dados."
        return res

        # Tenta resolver como equação (se tiver 'x' ou '=') ou conta simples
    if "x" in input_limpo:
        # Se tiver um '=', o SymPy precisa que igualemos a zero
        if "=" in input_limpo:
            partes = input_limpo.split("=")
            equacao = f"({partes[0]}) - ({partes[1]})"
        else:
            equacao = input_limpo

        x = sympy.Symbol('x')
        solucao = sympy.solve(equacao, x)
        # Procure onde começa o cálculo e coloque o try:
    try:
        if "x" in input_limpo:
            # ... (seu código de resolver equação com 'x')
            if "=" in input_limpo:
                partes = input_limpo.split("=")
                equacao = f"({partes[0]}) - ({partes[1]})"
            else:
                equacao = input_limpo

            x = sympy.Symbol('x')
            solucao = sympy.solve(equacao, x)
            res.resposta = f"Para a equação **{question}**, o valor de x é: **{solucao}**"
        else:
            # Resolve conta normal
            resultado_calculado = sympy.sympify(input_limpo)
            res.resposta = f"O resultado de **{question}** é: **{resultado_calculado}**"

    except Exception:
        res.resposta = "Não entendi a expressão. Use 'x' para equações ou '**' para potência (ex: 3**3)."

    return res
