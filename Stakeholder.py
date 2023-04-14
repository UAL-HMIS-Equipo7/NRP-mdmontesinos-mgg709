class Stakeholder:

    def __init__(self, nombre: str, recomendado_por: list = None):
        self._nombre = nombre
        if recomendado_por is None:
            self._recomendado_por = []
        else:
            self._recomendado_por = recomendado_por

    def importancia(self):
        return self._recomendado_por.count()

    def recomendar(self, stakeholder: str):
        self._recomendado_por.append(stakeholder)

    def cancelar_recomendacion(self, stakeholder: str):
        if stakeholder in self._recomendado_por: 
            self._recomendado_por.remove(stakeholder)
