from ETAPA2.ManejoDeDatos.validacionDeDatos import estaDentroDelRango, tieneNotasParciales, tieneNotaParcial1

def mostrarMateriasDisponibles(anio, cuatrimestre, materias, calendario, notaFinal, mostrarTodas=False):
    print(f"Mostrando materias disponibles para el año {anio}, cuatrimestre {cuatrimestre}:")
    indiceEnMaterias = 0
    contMateriasDisponibles = 1
    indices=[]
    for materia in materias: 
        materia = materia.split(".", 3)
        anioMateria= materia[0]
        cuatrimestreMateria= materia[1]
        if int(anioMateria) == anio and int(cuatrimestreMateria) == cuatrimestre:
            if mostrarTodas == False and indiceEnMaterias not in calendario and notaFinal[indiceEnMaterias] == 0:
                print(f"{contMateriasDisponibles}- {materia[2]}")
                indices.append(indiceEnMaterias)
                contMateriasDisponibles+=1
            elif mostrarTodas == True:
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
    if vacio==True and recursadas==False:
        return True
    return False

def darDeBajaNotas(indiceMateria,p1,p2,notaFinal):
    p1[indiceMateria] = 0
    p2[indiceMateria] = 0
    notaFinal[indiceMateria] = 0

def cargarNotas(indiceMateria,p1,p2,finales,notaFinal,materias, calendario, diasCalendario, materiasAprobadas, materiasRecursar):
    print(f"Cargando notas para la materia: {buscarNombreMateriaPorIndice(indiceMateria,materias)}")
    cond = 1
    while cond == 1:
        print("¿Que nota desea cargar?")
        print("1- Primer parcial")
        print("2- Segundo parcial")
        print("3- Final regular")
        print("0- Volver al menu principal")
        opcion = int(input("Usuario: "))
        while estaDentroDelRango(0,3,opcion) == False:
            print("Opcion inválida. Por favor, ingrese una opcion válida (1-3).")
            print("¿Que nota desea cargar?")
            print("1- Primer parcial")
            print("2- Segundo parcial")
            print("3- Final regular")
            print("0- Volver al menu principal")
            opcion = int(input("Usuario: "))
        if opcion == 0:
            cond = 0
        elif opcion == 1:
            print("Ingrese la nota del primer parcial (0-10):")
            notaP1 = int(input("Usuario: "))
            while estaDentroDelRango(0,10,notaP1) == False:
                print("Nota inválida. Por favor, ingrese una nota válida (0-10).")
                print("Ingrese la nota del primer parcial (0-10):")
                notaP1 = int(input("Usuario: "))
            p1[indiceMateria] = notaP1
        elif opcion == 2:
            if tieneNotaParcial1(p1,indiceMateria) == False:
                print("No se puede cargar nota de segundo parcial sin nota de primer parcial.")
            else:
                print("Ingrese la nota del segundo parcial (0-10):")
                notaP2 = int(input("Usuario: "))
                while estaDentroDelRango(0,10,notaP2) == False:
                    print("Nota inválida. Por favor, ingrese una nota válida (0-10).")
                    print("Ingrese la nota del segundo parcial (0-10):")
                    notaP2 = int(input("Usuario: "))
                p2[indiceMateria] = notaP2
                if p2[indiceMateria] < 4 and p1[indiceMateria] < 4:
                    materiasRecursar[indiceMateria] = 1
                    print("Materia para recursar.")
                    eliminarMateriaDelCalendario(indiceMateria,calendario,diasCalendario)
                    cond = 0
        else:
            if tieneNotasParciales(p1,p2,indiceMateria) == False:
                print("No se pueden cargar notas de final sin notas parciales.")
            else:
                print("Ingrese la nota final (0-10):")
                notaFinalInput = int(input("Usuario: "))
                while estaDentroDelRango(0,10,notaFinalInput) == False:
                    print("Nota inválida. Por favor, ingrese una nota válida (0-10).")
                    print("Ingrese la nota final (0-10):")
                    notaFinalInput = int(input("Usuario: "))
                finales[indiceMateria] = notaFinalInput
                if finales[indiceMateria] >= 4:
                    notaFinal[indiceMateria] = calcularNotaFinal(p1,p2,finales,indiceMateria)
                    materiasRecursar[indiceMateria] = 0
                    materiasAprobadas[indiceMateria] = 1
                    print("Materia aprobada.")
                    eliminarMateriaDelCalendario(indiceMateria,calendario,diasCalendario)
                else:
                    materiasRecursar[indiceMateria] = 1
                    print("Materia para recursar.")
                    eliminarMateriaDelCalendario(indiceMateria,calendario,diasCalendario)
                cond = 0

def calcularNotaFinal(p1,p2,finales,indiceMateria):
    notaFinal = (p1[indiceMateria] + p2[indiceMateria] + finales[indiceMateria])//3
    return notaFinal

def eliminarMateriaDelCalendario(indiceMateria,calendario,diasCalendario):
    for i in range(len(calendario)):
        if calendario[i] == indiceMateria:
            calendario[i] = -1
            diasCalendario.append(i)
            diasCalendario.sort()

#SACA PROMEDIOS
promedio= lambda lista: sum(lista) / len(lista)

def promedioCursada(notaFinal):
    notas=[]
    for i in range(len(notaFinal)):
        if notaFinal[i]!=0:
            notas.append(notaFinal[i])
            print()
    if len(notas)==0:
        print("No hay ninguna materia con nota final cargada")
    else:
        prom=promedio(notas)
        print("El promedio de la cursada es de",prom)

def obtenerMateriasPackDe5(materiasAprobadas, materias, correlativas, notaFinal):
    materiasPackDe5=[]
    indice=0
    while len(materiasPackDe5)<5 and indice<len(materiasAprobadas):
        if materiasAprobadas[indice]==0 and tieneCorrelativasAprobadas(indice,materias,notaFinal,correlativas)==True:
            materiasPackDe5.append(indice)
        indice+=1
    return materiasPackDe5


