from Dependencia import Dependencia
from Requisito import Requisito
from Stakeholder import Stakeholder
import csv

RUTA_STAKEHOLDERS_POR_DEFECTO = "stakeholder_data.csv"
RUTA_REQUISITOS_POR_DEFECTO = "requisito_data.csv"
ESFUERZO_POR_DEFECTO = 5
MENSAJE_NO_VALIDO = "Opción no válida."

class NRP:

    def __init__(self, limite_esfuerzo: int = ESFUERZO_POR_DEFECTO):
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

        stakeholders = procesar_stakeholders(nombres_stakeholders, recomendaciones)

        print(f'Cargados {line_count} stakeholders.\n')
        
        self._stakeholders = stakeholders

    def cargar_requisitos(self, ruta: str):
        if len(self._stakeholders) == 0:
            raise ValueError("Debe cargar los stakeholders antes que los requisitos.")

        requisitos = []
        line_count = 0

        with open(ruta, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            dependencias = {}
            for row in csv_reader:
                if line_count == 0:
                    print(f'Columnas en CSV para Requisito: {row.keys()}')

                nombre_requisito = row["nombre"].strip()

                if nombre_requisito == "":
                    raise ValueError(f"Debe introducir un nombre para el requisito en la línea {line_count+1}.")
                
                recomendado_por = procesar_recomendaciones_requisito(nombre_requisito, row["recomendado_por"].split(";"), self._stakeholders)
                dependencias[nombre_requisito] = row["dependencias"].split(";")
                    
                requisito = Requisito(nombre_requisito, row["descripcion"].strip(), recomendado_por)
                requisitos.append(requisito)
                
                line_count += 1

        for requisito in requisitos:
            requisito._dependencias = procesar_dependencias_requisito(requisito._nombre, dependencias[requisito._nombre], requisitos)

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
            if (requisito._coste > self._limite_esfuerzo):
                continue

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
    
    def iniciar_por_consola(self):
        print(" --- NRP --- ")

        self.obtener_esfuerzo_por_consola()

        ruta_stakeholders = input(f"\nIntroduzca la ruta del fichero de stakeholders ({RUTA_STAKEHOLDERS_POR_DEFECTO}): ")
        if ruta_stakeholders == "":
            ruta_stakeholders = RUTA_STAKEHOLDERS_POR_DEFECTO
        self.cargar_stakeholders(ruta_stakeholders)

        ruta_requisitos = input(f"Introduzca la ruta del fichero de requisitos ({RUTA_REQUISITOS_POR_DEFECTO}): ")
        if ruta_requisitos == "":
            ruta_requisitos = RUTA_REQUISITOS_POR_DEFECTO
        self.cargar_requisitos(ruta_requisitos)

        self.mostrar_opciones_menu()

    def mostrar_opciones_menu(self):
        print("\n\n\n\n\n\n\n\n\n\n\n")
        print(" --- Menú --- ")
        print("1. Mostrar requisitos")
        print("2. Mostrar stakeholders")
        print("3. Obtener recomendaciones de stakeholder")
        print("4. Calcular solución")
        print("5. Consultar esfuerzo")
        print("6. Modificar esfuerzo")
        print("7. Salir")
        input_opcion = input("\nIntroduzca una opción: ")
        while not input_opcion.isdigit():
            print(MENSAJE_NO_VALIDO)
            input_opcion = input("\nIntroduzca una opción: ")
        opcion = int(input_opcion)
        print("\n\n\n\n\n\n\n\n\n\n\n")
        if opcion == 1:
            self.mostrar_requisitos()
        elif opcion == 2:
            self.mostrar_stakeholders()
        elif opcion == 3:
            self.obtener_recomendaciones_stakeholder()
        elif opcion == 4:
            self.calcular_solucion()
        elif opcion == 5:
            self.mostrar_esfuerzo()
        elif opcion == 6:
            self.obtener_esfuerzo_por_consola()
        elif opcion == 7:
            return
        else:
            print(MENSAJE_NO_VALIDO)
        input("Presione ENTER para continuar...")
        self.mostrar_opciones_menu()

    def mostrar_esfuerzo(self):
        print(" --- Esfuerzo --- ")
        print(f"Limite de esfuerzo: {self._limite_esfuerzo}")
        print()

    def obtener_esfuerzo_por_consola(self):
        limite_esfuerzo = input("Introduzca el límite de esfuerzo: ")
        while not limite_esfuerzo.isdigit() or int(limite_esfuerzo) <= 0:
            print(MENSAJE_NO_VALIDO)
            limite_esfuerzo = input("Introduzca el límite de esfuerzo: ")
        self._limite_esfuerzo = int(limite_esfuerzo)
    
    def obtener_recomendaciones_stakeholder(self):
        stakeholder_input = input("Introduzca el nombre del stakeholder: ")

        stakeholder_index  = [index for (index, item) in enumerate(self._stakeholders) if item._nombre == stakeholder_input]

        if len(stakeholder_index) == 0:
            print(f"Stakeholder {stakeholder_input} no encontrado\n")
        else:
            stakeholder = self._stakeholders[stakeholder_index[0]]
            print(stakeholder.mostrar_recomendaciones())
        print()

    
def procesar_dependencias_requisito(nombre_requisito:str, nombres_dependencias: list[str], requisitos: list[Requisito]) -> list[Dependencia]:
    dependencias = []
    nombres_requisitos = [requisito._nombre for requisito in requisitos]
    for dependencia_name in nombres_dependencias:
        dependencia_name = dependencia_name.strip()
        if dependencia_name == "":
            continue

        dependencia_split = dependencia_name.split(".")

        if len(dependencia_split) != 2:
            raise ValueError(f"El requisito {nombre_requisito} tiene una dependencia mal formada: {dependencia_name}.")
        
        requisito_asociado, tipo = dependencia_split

        requisito_asociado = requisito_asociado.strip()
        tipo = tipo.strip().upper()

        if requisito_asociado == "" or tipo not in ["I", "J", "X"]:
            raise ValueError(f"El requisito {nombre_requisito} tiene una dependencia mal formada: {dependencia_name}.")

        if requisito_asociado not in nombres_requisitos:
            raise ValueError(f"Requisito {requisito_asociado} no encontrado para el requisito {nombre_requisito}.")
        
        if requisito_asociado == nombre_requisito:
            raise ValueError(f"El requisito {nombre_requisito} no puede depender de sí mismo.")
        
        if requisito_asociado in [dependencia._requisito for dependencia in dependencias]:
            raise ValueError(f"El requisito {nombre_requisito} tiene una dependencia duplicada: {requisito_asociado}.")

        dependencia = Dependencia(requisito_asociado, tipo)
        dependencias.append(dependencia)

    return dependencias
    
def procesar_recomendaciones_requisito(nombre_requisito:str, nombres_stakeholders_recomendadores: list[str], stakeholders: list[Stakeholder]) -> list[Stakeholder]:
    recomendado_por = []
    for stakeholder_name in nombres_stakeholders_recomendadores:
        stakeholder_name = stakeholder_name.strip()
        if stakeholder_name == "":
            continue

        stakeholder_index  = [index for (index, item) in enumerate(stakeholders) if item._nombre == stakeholder_name]

        if len(stakeholder_index) == 0:
            raise ValueError(f"Stakeholder {stakeholder_name} no encontrado para el requisito {nombre_requisito}.")
        
        stakeholder = stakeholders[stakeholder_index[0]]

        if stakeholder in recomendado_por:
            raise ValueError(f"El requisito {nombre_requisito} no puede ser recomendado varias veces por el stakeholder {stakeholder._nombre}.")

        recomendado_por.append(stakeholder)
    return recomendado_por

def procesar_stakeholders(nombres_stakeholders: list[str], recomendaciones: dict[str, list[str]]) -> list[Stakeholder]:
    stakeholders = []
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
    return stakeholders

    
