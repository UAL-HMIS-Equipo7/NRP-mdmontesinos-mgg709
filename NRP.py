from Requisito import Requisito
from Stakeholder import Stakeholder
import csv

class NRP:

    def __init__(self, limite_esfuerzo: int):
        self._limite_esfuerzo = limite_esfuerzo
        self._requisitos: list[Requisito] = []
        self._stakeholders: list[Stakeholder] = []

    def cargar_stakeholders(self, ruta: str):
        stakeholders = []

        with open(ruta, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Columnas en CSV para Stakeholder: {row.keys()}')
                    
                stakeholder = Stakeholder(row["nombre"], row["recomendado_por"].split(";"))
                stakeholders.append(stakeholder)
                
                line_count += 1

            print(f'Cargados {line_count} stakeholders.\n')
        
        self._stakeholders = stakeholders

    def cargar_requisitos(self, ruta: str):
        if len(self._stakeholders) == 0:
            raise ValueError("Debe cargar los stakeholders antes que los requisitos.")

        requisitos = []

        with open(ruta, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Columnas en CSV para Requisito: {row.keys()}')
                
                recomendado_por = []
                for stakeholder_name in row["recomendado_por"].split(";"):
                    stakeholder_index  = [index for (index, item) in enumerate(self._stakeholders) if item._nombre == stakeholder_name]
                    if len(stakeholder_index) == 0:
                        raise ValueError(f"Stakeholder {stakeholder_name} no encontrado")
                    stakeholder = self._stakeholders[stakeholder_index[0]]
                    recomendado_por.append(stakeholder)
                    
                requisito = Requisito(row["nombre"], row["descripcion"], recomendado_por)
                requisitos.append(requisito)
                
                line_count += 1

            print(f'Cargados {line_count} requisitos.\n')
        
        self._requisitos = requisitos

    def mostrar_requisitos(self):
        print(" --- Requisitos --- ")
        for requisito in self._requisitos:
            print(requisito.to_long_string())
        print()

    def mostrar_stakeholders(self):
        print(" --- Stakeholders --- ")
        for stakeholder in self._stakeholders:
            print(stakeholder)
        print()
        
    def calcular_solucion(self):
        solucion = {}
        requisitos = sorted(self._requisitos, key=lambda r: r.importancia(), reverse=True)
        esfuerzo = 0
        sprintActual = []
        for requisito in requisitos:    
            if (esfuerzo + requisito._coste <= self._limite_esfuerzo):
                sprintActual.append(requisito)
                esfuerzo += requisito._coste
            else:
                solucion["Sprint " + str(len(solucion)+1)] = list(sprintActual)
                sprintActual = [requisito]
                esfuerzo = requisito._coste
        solucion["Sprint " + str(len(solucion)+1)] = list(sprintActual)

        print(" --- Solución --- ")
        for sprint in solucion:
            print("- " + sprint)
            for requisito in solucion[sprint]:
                print(requisito)
            print()

        return solucion


    
