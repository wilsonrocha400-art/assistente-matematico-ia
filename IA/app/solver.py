import streamlit as st
import sympy

def answer_math_question(question: str, foto=None):
    # Criamos um objeto para simular o resultado
    class Result: pass
    res = Result()

    if not question:
        res.resposta = "Por favor, digite uma conta (ex: 3 + 3 * 3 / 3 + 3)"
        return res

    try:
        # O SymPy resolve a conta matematicamente
        # transformando o texto em uma expressão real
        resultado_calculado = sympy.sympify(question)
        
        res.resposta = f"Calculado via SymPy (Gratuito):\n\nO resultado de {question} é: **{resultado_calculado}**"
        
        # Se for a pergunta sobre quem criou:
        autoria = ["quem", "criador", "wilson"]
        if any(word in question.lower() for word in autoria):
            res.resposta = "Este Assistente Matemático foi desenvolvido por **Wilson Rocha do Nascimento**."
            
    except Exception as e:
        res.resposta = "Não consegui entender essa conta. Tente usar apenas números e sinais (+, -, *, /)."

    return res