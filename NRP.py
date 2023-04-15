from Requisito import Requisito
from Stakeholder import Stakeholder
import csv

class NRP:

    def __init__(self, limite_esfuerzo: int):
        self._limite_esfuerzo = limite_esfuerzo
        self._requisitos: list[Requisito] = []
        self._stakeholders: list[Stakeholder] = []

    def cargar_stakeholders(self, ruta: str):
        nombres_stakeholders = []
        recomendaciones = {}
        stakeholders = []

        with open(ruta, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Columnas en CSV para Stakeholder: {row.keys()}')
                
                nombre_stakeholder = row["nombre"].strip()
                if nombre_stakeholder == "":
                    raise ValueError(f"Debe introducir un nombre para el stakeholder en la línea {line_count+1}.")
                
                nombres_stakeholders.append(nombre_stakeholder)
                recomendaciones[row["nombre"]] = row["recomendado_por"].split(";")            
                
                line_count += 1

        for stakeholder_name in nombres_stakeholders:
            stakeholder = Stakeholder(stakeholder_name)

            for recomendador in recomendaciones[stakeholder_name]:
                recomendador = recomendador.strip()
                if recomendador == "":
                    continue

                if recomendador == stakeholder_name:
                    raise ValueError(f"El stakeholder {stakeholder_name} no puede recomendarse a sí mismo.")
                
                if recomendador in stakeholder._recomendado_por:
                    raise ValueError(f"El stakeholder {stakeholder_name} no puede ser recomendado varias veces por {recomendador}.")

                if recomendador not in nombres_stakeholders:
                    raise ValueError(f"Stakeholder {recomendador} no encontrado para el stakeholder {stakeholder_name}.")
                
                stakeholder.aniadir_recomendacion(recomendador)

            stakeholders.append(stakeholder)

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

                nombre_requisito = row["nombre"].strip()

                if nombre_requisito == "":
                    raise ValueError(f"Debe introducir un nombre para el requisito en la línea {line_count+1}.")
                
                recomendado_por = []
                for stakeholder_name in row["recomendado_por"].split(";"):
                    stakeholder_name = stakeholder_name.strip()
                    if stakeholder_name == "":
                        continue

                    stakeholder_index  = [index for (index, item) in enumerate(self._stakeholders) if item._nombre == stakeholder_name]

                    if len(stakeholder_index) == 0:
                        raise ValueError(f"Stakeholder {stakeholder_name} no encontrado para el requisito {row['nombre']}.")
                    
                    stakeholder = self._stakeholders[stakeholder_index[0]]

                    if stakeholder in recomendado_por:
                        raise ValueError(f"El requisito {nombre_requisito} no puede ser recomendado varias veces por el stakeholder {stakeholder._nombre}.")

                    recomendado_por.append(stakeholder)
                    
                requisito = Requisito(nombre_requisito, row["descripcion"].strip(), recomendado_por)
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
        sprint_actual = []
        for requisito in requisitos:    
            if (esfuerzo + requisito._coste <= self._limite_esfuerzo):
                sprint_actual.append(requisito)
                esfuerzo += requisito._coste
            else:
                solucion["Sprint " + str(len(solucion)+1)] = list(sprint_actual)
                sprint_actual = [requisito]
                esfuerzo = requisito._coste
        solucion["Sprint " + str(len(solucion)+1)] = list(sprint_actual)

        print(" --- Solución --- ")
        for sprint in solucion:
            print("- " + sprint)
            for requisito in solucion[sprint]:
                print(requisito)
            print()

        return solucion


    
