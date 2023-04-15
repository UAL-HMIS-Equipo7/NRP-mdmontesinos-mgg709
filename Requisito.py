from Stakeholder import Stakeholder
from Dependencia import Dependencia

COST = 4

class Requisito:

    def __init__(self, nombre: str, descripcion: str, recomendado_por: list[Stakeholder] = None, dependencias: list[Dependencia] = None):
        self._nombre = nombre
        self._descripcion = descripcion
        if recomendado_por is None:
            self._recomendado_por = []
        else:
            self._recomendado_por = recomendado_por
        if dependencias is None:
            self._dependencias = []
        else:
            self._dependencias = dependencias
        self._coste = COST

    def importancia(self):
        importancia = 0
        for stakeholder in self._recomendado_por:
            importancia += stakeholder.importancia()
        return importancia
    
    def aniadir_recomendacion(self, recomendador: Stakeholder):
        if recomendador not in self._recomendado_por:
            self._recomendado_por.append(recomendador)

    def cancelar_recomendacion(self, recomendador: Stakeholder):
        if recomendador in self._recomendado_por:
            self._recomendado_por.remove(recomendador)

    def __str__(self):
        return f"Requisito {self._nombre} ({self.importancia()})"

    def to_long_string(self):
        return f"Requisito {self._nombre} ({self.importancia()}), con descripción: {self._descripcion}, recomendado por {[x._nombre for x in self._recomendado_por]}, con dependencias: {[str(x) for x in self._dependencias]}"