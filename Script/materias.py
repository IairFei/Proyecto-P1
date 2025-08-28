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