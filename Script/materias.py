
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

def tieneCorrelativasAprobadas(indiceMateria, materias, notasFinales, correlativas):
    contNoAprobadas = 0
    aproboCorrelativas = True
    for i in range(len(correlativas[indiceMateria])):
        if correlativas[indiceMateria][i]==1 and notasFinales[i] < 4:
            print(f"Correlativa no aprobada: {materias[i]}")
            contNoAprobadas += 1
    if contNoAprobadas > 0:
        aproboCorrelativas = False
    return aproboCorrelativas

def tieneRecursadas(materiasRecursar):
    tiene = False
    i = 0
    while i < len(materiasRecursar) and tiene == False:
        if materiasRecursar[i] == 1:
            tiene = True
        i += 1
    return tiene

def tieneCalendarioVacio(calendario):
    vacio = True
    i = 0
    while i < len(calendario) and vacio == True:
        if calendario[i] != -1:
            vacio = False
        i += 1
    return vacio


def estadoPackDe5Materias(calendario, materiasRecursar):
    vacio=tieneCalendarioVacio(calendario)
    recursadas=tieneRecursadas(materiasRecursar)
    print(f"Vacio: {vacio}, Recursadas: {recursadas}")
    if vacio==True and recursadas==False:
        return True
    return False

