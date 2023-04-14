class Stakeholder:

    def __init__(self, nombre: str, recomendadoPor: list[str] = []):
        self.nombre = nombre
        self.recomendadoPor = recomendadoPor
        self.importancia = len(recomendadoPor)

    def recomendar(self, stakeholder: str):
        self.recomendadoPor.append(stakeholder)
        self.importancia += 1

    def cancelarRecomendacion(self, stakeholder: str):
        if stakeholder in self.recomendadoPor: 
            self.recomendadoPor.remove(stakeholder)
            self.importancia -= 1
