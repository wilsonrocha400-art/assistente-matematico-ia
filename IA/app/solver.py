import sympy


def answer_math_question(question: str):
    class Result:
        pass
    res = Result()

    # Criamos um "tradutor" para termos comuns
    # Isso permite que você digite de forma mais natural
    input_limpo = question.lower().replace(
        "elevado a", "**").replace("^", "**").replace(",", ".")

    try:
        # Filtro de Autoria (Mantendo o que já tínhamos)
        if "wilson" in input_limpo or "criador" in input_limpo:
            res.resposta = "Este sistema foi desenvolvido por **Wilson Rocha do Nascimento**."
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
            res.resposta = f"Para a equação **{question}**, o valor de x é: **{solucao}**"
        else:
            # Resolve conta normal
            resultado_calculado = sympy.sympify(input_limpo)
            res.resposta = f"O resultado de **{question}** é: **{resultado_calculado}**"

    except Exception:
        res.resposta = "Não entendi a expressão. Use 'x' para equações ou '**' para potência (ex: 3**3)."

    return res
