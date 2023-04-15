from enum import Enum

class TipoDependencia(Enum):
    I = "I"
    J = "J"
    X = "X"

class Dependencia:

    def __init__(self, requisito: str, tipo: TipoDependencia):
        self._requisito = requisito
        self._tipo = tipo

    def __str__(self):
        return f"{self._requisito}-{self._tipo}"


