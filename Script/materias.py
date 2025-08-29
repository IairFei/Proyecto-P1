def mostrarMateriasDisponibles(anio, cuatrimestre, materias):
    print(f"Mostrando materias disponibles para el año {anio}, cuatrimestre {cuatrimestre}:")
    indiceEnMaterias = 0
    contMateriasDisponibles = 1
    indices=[]
    for materia in materias: 
        materia = materia.split(".", 3)
        anioMateria= materia[0]
        cuatrimestreMateria= materia[1]
        if int(anioMateria) == anio and int(cuatrimestreMateria) == cuatrimestre:
            print(f"{contMateriasDisponibles}- {materia[2]}")
            indices.append(indiceEnMaterias)
            contMateriasDisponibles+=1
        indiceEnMaterias += 1
    return indices

def buscarNombreMateriaPorIndice(indice, materias):
    materia = materias[indice].split(".",3)
    nombreDeMateria = materia[2]
    return nombreDeMateria

def buscarMateriaPorIndice(indice, materias):
    materia = materias[indice].split(".",3)
    return materia

def buscarMateriaPorNombre(nombre, materias):
    cont = 0
    materiaEncontrada = False
    indiceEncontrado = -1
    while materiaEncontrada == False and cont < len(materias):
        materia = materias[cont].split(".",3)
        nombreDeMateria = materia[2]
        if nombreDeMateria.lower().strip() == nombre.lower().strip():
            indiceEncontrado = cont
            materiaEncontrada = True
            print(indiceEncontrado)
        cont += 1
    if materiaEncontrada == False:
        print("No se encontro la materia.")
    return indiceEncontrado