from ManejoDeDatos.validacionDeDatos import estaDentroDelRango, tieneNotasParciales, tieneNotaParcial1
from Logs.logs import log
import json

def mostrarMateriasDisponibles(anio, cuatrimestre, usuario, mostrarTodas=False):
    try:
        with open("ETAPA2/Archivos/materias.json", "r", encoding="utf-8") as archivoMaterias:
            contMateriasDisponibles = 1
            indices = []
            calendario_dict = usuario.get('calendario', {})
            notas_dict = usuario.get('notas', {})
            materias_en_calendario = []
            for _,id in calendario_dict.items():
                if id is not None:
                    materias_en_calendario.append(int(id))
            for linea in archivoMaterias:
                try:
                    materia = json.loads(linea.strip())
                except Exception:
                    continue
                anioMateria = materia.get('año')
                cuatrimestreMateria = materia.get('cuatrimestre')
                nombreMateria = materia.get('nombre')
                indice_materia = materia.get('id')
                if int(anioMateria) == anio and int(cuatrimestreMateria) == cuatrimestre:
                    nota_info = notas_dict.get(str(indice_materia), {})
                    aprobada = nota_info.get('aprobada', False)
                    if not mostrarTodas:
                        if indice_materia not in materias_en_calendario and not aprobada and tieneCorrelativasAprobadas(usuario, indice_materia):
                            print(f"{contMateriasDisponibles}- {nombreMateria}")
                            indices.append(indice_materia)
                            contMateriasDisponibles += 1
                    else:
                        print(f"{contMateriasDisponibles}- {nombreMateria}")
                        indices.append(indice_materia)
                        contMateriasDisponibles += 1
            return indices
    except Exception as e:
        print(e)
        return []

def buscarNombreMateriaPorIndice(indice, materias):
    materia = materias[indice].split(".",3)
    nombreDeMateria = materia[2]
    return nombreDeMateria

def buscarMateriaPorIndice(indice):
    try:
        with open("ETAPA2/Archivos/materias.json", "r", encoding="utf-8") as archivoMaterias:
            for linea in archivoMaterias:
                try:
                    materia = json.loads(linea.strip())
                    if materia.get('id') == indice:
                        return materia
                except Exception:
                    continue
    except (IndexError, FileNotFoundError) as e:
        print(e)
    return None

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

def tieneCorrelativasAprobadas(usuarioActual, idMateria):
    contNoAprobadas = 0
    aproboCorrelativas = True
    correlativas=[]
    try:
        with open("ETAPA2/Archivos/materias.json", "r", encoding="utf-8") as archivoMaterias:
            for linea in archivoMaterias:
                try:
                    materia = json.loads(linea.strip())
                    if materia.get('id') == idMateria:
                        correlativas = materia.get('correlativas', [])
                        break
                except Exception:
                    continue
        if correlativas is None or len(correlativas) == 0:
            return True
        notas = usuarioActual.get('notas', {})

        for correlativa in correlativas:
            nota_info = notas.get(str(correlativa), {})
            if nota_info['aprobada'] == False:
                print(f"Correlativa de {materia['nombre']} no aprobada: {buscarMateriaPorIndice(correlativa)['nombre']}")
                contNoAprobadas += 1

        if contNoAprobadas > 0:
            aproboCorrelativas = False
        return aproboCorrelativas
    except Exception as e:
        print(f"Error al verificar correlativas: {e}")
        aproboCorrelativas = False

def tieneRecursadas(usuarioActual):
    tiene = False
    notas= usuarioActual['notas'].keys()
    for nota in notas:
        if usuarioActual['notas'][nota]['recursa'] == True:
            tiene = True
            break
    return tiene

def tieneCalendarioVacio(usuarioCalendario):
    vacio = True
    for dia in usuarioCalendario.keys():
        if usuarioCalendario[dia] != None:
            vacio = False
    return vacio


def estadoPackDe5Materias(usuarioActual):
    vacio=tieneCalendarioVacio(usuarioActual['calendario'])
    recursadas=tieneRecursadas(usuarioActual)
    if vacio==True and recursadas==False:
        return True
    return False

def darDeBajaNotas(indicemateria, usuario):
    del usuario['notas'][indicemateria]
    log("darDeBajaNotas", "INFO", f"Notas de la materia {indicemateria} eliminadas del usuario {usuario['usuario']}.")

def cargarNotas(indiceMateria,p1,p2,finales,notaFinal,materias, calendario, diasCalendario, materiasAprobadas, materiasRecursar, usuario):
    print(f"Cargando notas para la materia: {buscarNombreMateriaPorIndice(indiceMateria,materias)}")
    log("cargarNotas", "INFO", f"Usuario {usuario} está cargando notas para la materia: {buscarNombreMateriaPorIndice(indiceMateria,materias)}")
    cond = 1
    while cond == 1:
        print("¿Que nota desea cargar?")
        print("1- Primer parcial")
        print("2- Segundo parcial")
        print("3- Final regular")
        print("0- Volver al menu principal")
        opcion = int(input("Usuario: "))
        log("cargarNotas", "INFO", f"Usuario {usuario} seleccionó la opción {opcion} para cargar nota.")
        while estaDentroDelRango(0,3,opcion) == False:
            print("Opcion inválida. Por favor, ingrese una opcion válida (1-3).")
            print("¿Que nota desea cargar?")
            print("1- Primer parcial")
            print("2- Segundo parcial")
            print("3- Final regular")
            print("0- Volver al menu principal")
            opcion = int(input("Usuario: "))
            log("cargarNotas", "INFO", f"Usuario {usuario} seleccionó la opción {opcion} para cargar nota.")
        if opcion == 0:
            cond = 0
            log("cargarNotas", "INFO", f"Usuario decidió volver al menú principal")
        elif opcion == 1:
            print("Ingrese la nota del primer parcial (0-10):")
            notaP1 = int(input("Usuario: "))
            log("cargarNotas", "INFO", f"Usuario {usuario} ingresó la nota {notaP1} para el primer parcial.")
            while estaDentroDelRango(0,10,notaP1) == False:
                print("Nota inválida. Por favor, ingrese una nota válida (0-10).")
                log("cargarNotas", "INFO", f"Usuario {usuario} ingresó una nota inválida {notaP1} para el primer parcial, se le pedirá ingresar otra nota.")
                print("Ingrese la nota del primer parcial (0-10):")
                notaP1 = int(input("Usuario: "))
                log("cargarNotas", "INFO", f"Usuario {usuario} ingresó la nota {notaP1} para el primer parcial.")
            p1[indiceMateria] = notaP1
            log("cargarNotas", "INFO", f"Usuario {usuario} cargó la nota {notaP1} para el primer parcial.")
        elif opcion == 2:
            if tieneNotaParcial1(p1,indiceMateria) == False:
                print("No se puede cargar nota de segundo parcial sin nota de primer parcial.")
                log("cargarNotas", "INFO", f"Usuario {usuario} intentó cargar nota de segundo parcial sin tener nota de primer parcial.")
            else:
                print("Ingrese la nota del segundo parcial (0-10):")
                notaP2 = int(input("Usuario: "))
                log("cargarNotas", "INFO", f"Usuario {usuario} ingresó la nota {notaP2} para el segundo parcial.")
                while estaDentroDelRango(0,10,notaP2) == False:
                    print("Nota inválida. Por favor, ingrese una nota válida (0-10).")
                    log("cargarNotas", "INFO", f"Usuario {usuario} ingresó una nota inválida {notaP2} para el segundo parcial, se le pedirá ingresar otra nota.")
                    print("Ingrese la nota del segundo parcial (0-10):")
                    notaP2 = int(input("Usuario: "))
                    log("cargarNotas", "INFO", f"Usuario {usuario} ingresó la nota {notaP2} para el segundo parcial.")
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
                log("cargarNotas", "INFO", f"Usuario {usuario} ingresó la nota {notaFinalInput} para el final.")
                while estaDentroDelRango(0,10,notaFinalInput) == False:
                    print("Nota inválida. Por favor, ingrese una nota válida (0-10).")
                    log("cargarNotas", "INFO", f"Usuario {usuario} ingresó una nota inválida {notaFinalInput} para el final, se le pedirá ingresar otra nota.")
                    print("Ingrese la nota final (0-10):")
                    notaFinalInput = int(input("Usuario: "))
                    log("cargarNotas", "INFO", f"Usuario {usuario} ingresó la nota {notaFinalInput} para el final.")
                finales[indiceMateria] = notaFinalInput
                if finales[indiceMateria] >= 4:
                    notaFinal[indiceMateria] = calcularNotaFinal(p1,p2,finales,indiceMateria)
                    materiasRecursar[indiceMateria] = 0
                    materiasAprobadas[indiceMateria] = 1
                    log("cargarNotas", "INFO", f"Usuario {usuario} aprobó la materia {buscarNombreMateriaPorIndice(indiceMateria,materias)} con nota final {notaFinal[indiceMateria]}.")
                    print("Materia aprobada.")
                    eliminarMateriaDelCalendario(indiceMateria,calendario,diasCalendario)
                else:
                    materiasRecursar[indiceMateria] = 1
                    print("Materia para recursar.")
                    log("cargarNotas", "INFO", f"Usuario {usuario} no aprobó la materia {buscarNombreMateriaPorIndice(indiceMateria,materias)} con nota final {finales[indiceMateria]}, deberá recursar.")
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
    log("eliminarMateriaDelCalendario", "INFO", f"Materia {indiceMateria} eliminada del calendario.")

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

def obtenerMateriasPackDe5(usuarioActual):
    materiasPackDe5=[]
    indice=0
    try:
        with open("ETAPA2/Archivos/materias.json", "r", encoding="utf-8") as archivoMaterias:
            for linea in archivoMaterias:
                try:
                    materia = json.loads(linea.strip())
                    if materia["id"] not in usuarioActual["notas"].keys():
                        materiasPackDe5.append(materia["id"])
                        if len(materiasPackDe5) == 5:
                            break
                except Exception:
                    continue
            return materiasPackDe5
    except Exception as e:
        print(f"Error al obtener materias pack de 5: {e}")
    return materiasPackDe5


