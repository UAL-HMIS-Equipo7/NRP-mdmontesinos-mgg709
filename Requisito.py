from Stakeholder import Stakeholder

COST = 5

class Requisito:

    def __init__(self, descripcion: str, recomendado_por: list[Stakeholder] = None):
        self._descripcion = descripcion
        if recomendado_por is None:
            self._recomendado_por = []
        else:
            self._recomendado_por = recomendado_por
        self._coste = COST

    def importancia(self):
        importancia = 0
        for stakeholder in self._recomendado_por:
            importancia += stakeholder.importancia()
        return importancia
    
    def recomendar(self, stakeholder: Stakeholder):
        if stakeholder not in self._recomendado_por:
            self._recomendado_por.append(stakeholder)

    def cancelar_recomendacion(self, stakeholder: Stakeholder):
        if stakeholder in self._recomendado_por: 
            self._recomendado_por.remove(stakeholder)

    