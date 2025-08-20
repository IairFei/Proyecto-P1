from cargaDeDatos import cargaDeMaterias

materiasDisponibles = []

calendario = [["Lun", ""],["Mar", ""],["Mie",""],["Jue",""],["Vie",""]]
def inicializarDatos():
    global materiasDisponibles
    materiasDisponibles = cargaDeMaterias()

def mostrarMaterias(anio, cuatrimestre):
    materiasAElegir = []
    cont = 1
    print(f"Materias disponibles para el año {anio} y cuatrimestre {cuatrimestre}:")
    for materia in materiasDisponibles:
        if materia[0] == anio and materia[1] == cuatrimestre:
            print(f"{cont}- {materia[2]}")
            materiasAElegir.append(materia)
            cont+=1
    return materiasAElegir

def agregarMateriaAlCalendario(diaElegido, materiaAgregar):
    if calendario[diaElegido][1] != "":
        print(f"El día {calendario[diaElegido][0]} ya tiene una materia asignada: {calendario[diaElegido][1]}.")
        print("No se puede agregar otra materia en este día.")
    else:
        calendario[diaElegido][1] = materiaAgregar[2]
        print(f"Materia '{materiaAgregar[2]}' agregada al día {calendario[diaElegido][0]}.")
    print("Calendario actualizado:")
    for dia in calendario:
        print(f"{dia[0]}: {dia[1]}")


