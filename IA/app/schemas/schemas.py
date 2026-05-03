from pydantic import BaseModel


class MathAnswer(BaseModel):
    questao: str
    resposta: str
    fonte: str
