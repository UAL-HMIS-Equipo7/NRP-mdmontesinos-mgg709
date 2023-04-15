from NRP import NRP

RUTA_STAKEHOLDERS = "stakeholder_data.csv"
RUTA_REQUISITOS = "requisito_data.csv"
ESFUERZO_MAXIMO = 10

nrp = NRP(10)
nrp.cargar_stakeholders(RUTA_STAKEHOLDERS)
nrp.cargar_requisitos(RUTA_REQUISITOS)
nrp.mostrar_requisitos()
nrp.mostrar_stakeholders()
solucion = nrp.calcular_solucion()


