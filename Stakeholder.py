class Stakeholder:

    def __init__(self, nombre: str, recomendado_por: list = None):
        self._nombre = nombre
        if recomendado_por is None:
            self._recomendado_por = []
        else:
            self._recomendado_por = recomendado_por

    def importancia(self):
        return len(self._recomendado_por)

    def aniadir_recomendacion(self, recomendador: str):
        if recomendador not in self._recomendado_por:
            self._recomendado_por.append(recomendador)

    def cancelar_recomendacion(self, recomendador: str):
        if recomendador in self._recomendado_por: 
            self._recomendado_por.remove(recomendador)

    def __str__(self):
        return f"Stakeholder {self._nombre}, Importancia: {self.importancia()}, Recomendaciones: {self._recomendado_por}"
    
    def mostrar_recomendaciones(self):
        salida = f"El stakeholder {self._nombre} ha sido recomendado por: "
        for recomendador in self._recomendado_por:
            salida += f"\n\t- {recomendador}"
        return salida
