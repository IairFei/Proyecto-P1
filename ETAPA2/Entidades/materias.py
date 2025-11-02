from ManejoDeDatos.validacionDeDatos import eleccionDeMateriaCuatrimestre, eleccionDeMateriaAnio, validarEntero, validarTexto
from Logs.logs import log
from ManejoDeDatos.Usuarios.usuarios import guardarUsuario
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
    except (IOError, OSError):
        print("Error al abrir el archivo.")
        return

def buscarNombreMateriaPorIndice(indice, materias):
    materia = materias[indice].split(".",3)
    nombreDeMateria = materia[2]
    return nombreDeMateria

def obtenerCantidadDeMaterias():
    cantidad = 0
    try:
        with open("ETAPA2/Archivos/materias.json", "r", encoding="utf-8") as archivoMaterias:
            for linea in archivoMaterias:
                cantidad += 1
    except (IOError, OSError):
        print("Error al abrir el archivo.")
    return cantidad

def obtenerCantidadDeInscriptosEnMaterias():
    cantidadInscriptosPorMateria = []
    try:
        with open("ETAPA2/Archivos/materias.json", "r", encoding="utf-8") as archivoMaterias:
            for linea in archivoMaterias:
                try:
                    materia = json.loads(linea.strip())
                    cantidadInscriptosPorMateria.append((materia.get('nombre'), materia.get('inscriptos', 0)))
                except Exception:
                    continue
    except (IOError, OSError):
        print(f"Error al obtener la cantidad de inscriptos en materias.")
    return cantidadInscriptosPorMateria

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
    except (IndexError, FileNotFoundError):
        print("Error al abrir el archivo.")
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
    except (IOError, OSError):
        print(f"Error al verificar correlativas.")
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
    del usuario['notas'][str(indicemateria)]
    log("darDeBajaNotas", "INFO", f"Notas de la materia {indicemateria} eliminadas del usuario {usuario['usuario']}.")

def cargarNotas(usuarioActual,materia,diaIngresado):
    usuario = usuarioActual['usuario']
    try: 
        print(f"Cargando notas para la materia: {materia["nombre"]}.")
        log("cargarNotas", "INFO", f"Usuario {usuario} está cargando notas para la materia: {materia["nombre"]}.")
        while True:
            print("¿Que nota desea cargar?\n1- Primer parcial\n2- Segundo parcial\n3- Final regular\n0- Volver al menu principal")
            opcion = validarEntero(0,3)
            log("cargarNotas", "INFO", f"Usuario {usuario} seleccionó la opción {opcion} para cargar nota.")
            
            if opcion == 0:
                log("cargarNotas", "INFO", f"Usuario decidió volver al menú principal")
                guardarUsuario(usuarioActual)
                break
            
            elif opcion == 1:
                print("Ingrese la nota del primer parcial (0-10):")
                notaP1 = validarEntero(0,10)
                usuarioActual["notas"][str(materia["id"])]["parcial1"] = notaP1
                guardarUsuario(usuarioActual)
                log("cargarNotas", "INFO", f"Usuario {usuario} cargó la nota {notaP1} para el primer parcial.")
    
            elif opcion == 2:
                if usuarioActual["notas"][str(materia["id"])]["parcial1"] == None:
                    print("No se puede cargar nota de segundo parcial sin nota de primer parcial.")
                    log("cargarNotas", "INFO", f"Usuario {usuario} intentó cargar nota de segundo parcial sin tener nota de primer parcial.")
                else:
                    print("Ingrese la nota del segundo parcial (0-10):")
                    notaP2 = validarEntero(0,10)
                    usuarioActual["notas"][str(materia["id"])]["parcial2"] = notaP2
                    log("cargarNotas", "INFO", f"Usuario {usuario} cargó la nota {notaP2} para el segundo parcial.")
                    if usuarioActual["notas"][str(materia["id"])]["parcial1"] < 4 or usuarioActual["notas"][str(materia["id"])]["parcial2"] < 4:
                        usuarioActual["notas"][str(materia["id"])]["recursa"] = True
                        usuarioActual["notas"][str(materia["id"])]["parcial1"] = None
                        usuarioActual["notas"][str(materia["id"])]["parcial2"] = None
                        usuarioActual["notas"][str(materia["id"])]["final"] = None
                        print("Materia asignada a recursar y eliminada del calendario.")
                        eliminarMateriaDelCalendario(usuarioActual,diaIngresado)
                        break
                    guardarUsuario(usuarioActual)
                    
            else:
                if usuarioActual["notas"][str(materia["id"])]["parcial1"] == None or usuarioActual["notas"][str(materia["id"])]["parcial2"] == None:
                    print("No se pueden cargar notas de final sin notas parciales.")
                else:
                    print("Ingrese la nota final (0-10):")
                    notaFinalInput = validarEntero(0,10)
                    usuarioActual["notas"][str(materia["id"])]["final"] = notaFinalInput
                    log("cargarNotas", "INFO", f"Usuario {usuario} cargó la nota {notaFinalInput} para el final.")   
                    usuarioActual["notas"][str(materia["id"])]["final"] = notaFinalInput

                    if usuarioActual["notas"][str(materia["id"])]["final"] >= 4:
                        usuarioActual["notas"][str(materia["id"])]["nota_final"] = calcularNotaFinal(usuarioActual,materia)
                        usuarioActual["notas"][str(materia["id"])]["recursa"] = False
                        usuarioActual["notas"][str(materia["id"])]["aprobada"] = True
                        log("cargarNotas", "INFO", f"Usuario {usuario} aprobó la materia {materia["id"]} con promedio final {usuarioActual["notas"][str(materia["id"])]["nota_final"]}.")
                        print("Materia aprobada.")
                        eliminarMateriaDelCalendario(usuarioActual,diaIngresado)
                    else:
                        usuarioActual["notas"][str(materia["id"])]["recursa"] = True
                        usuarioActual["notas"][str(materia["id"])]["parcial1"] = None
                        usuarioActual["notas"][str(materia["id"])]["parcial2"] = None
                        usuarioActual["notas"][str(materia["id"])]["final"] = None
                        print("Materia asignada a recursar y eliminada del calendario.")
                        log("cargarNotas", "INFO", f"Usuario {usuario} no aprobó la materia {materia["id"]} con nota final {usuarioActual["notas"][str(materia["id"])]["final"]}, deberá recursar.")
                        eliminarMateriaDelCalendario(usuarioActual,diaIngresado)
                    guardarUsuario(usuarioActual)
                    break       
    except (IOError,OSError):
        print("Error al abrir el archivo de notas.")

def calcularNotaFinal(usuarioActual,materia):
    p1 = usuarioActual["notas"][str(materia["id"])]["parcial1"]
    p2 = usuarioActual["notas"][str(materia["id"])]["parcial2"]
    final = usuarioActual["notas"][str(materia["id"])]["final"]
    notaFinal = ((p1+p2)/2+final)/2
    return notaFinal

def eliminarMateriaDelCalendario(usuarioActual,diaIngresado):
    dias=("Lunes", "Martes", "Miercoles", "Jueves", "Viernes")
    materiaID= usuarioActual["calendario"][dias[diaIngresado-1]]
    materia=buscarMateriaPorIndice(materiaID)
    usuarioActual["calendario"][dias[diaIngresado-1]] = None
    materia['inscriptos'] -= 1
    guardarMateria(materia)
    guardarUsuario(usuarioActual)
    log("eliminarMateriaRecursada", "INFO", f"Materia del dia {dias[diaIngresado-1]} eliminada del calendario.")

def verNotas(usuarioActual, materia):
    while True:
        id_materia = str(materia["id"])
        notas = usuarioActual.get("notas", {})
        if id_materia not in notas:
            print(f"No hay notas cargadas para la materia '{materia['nombre']}'.")
        else:
            nota_materia = notas[id_materia]
            print(f"Notas de {materia['nombre']}:")
            print(f"  Primer parcial: {nota_materia.get('parcial1', 'Sin cargar')}")
            print(f"  Segundo parcial: {nota_materia.get('parcial2', 'Sin cargar')}")
            print(f"  Final: {nota_materia.get('final', 'Sin cargar')}")
            print(f"  Nota final: {nota_materia.get('nota_final', 'Sin cargar')}")
            print(f"  Aprobada: {'Sí' if nota_materia.get('aprobada', False) else 'No'}")
            print(f"  Recursa: {'Sí' if nota_materia.get('recursa', False) else 'No'}")
        print("¿Desea ver las notas de otra materia? (s/n): ")
        opcion = validarTexto(("s","si","n","no"))
        if opcion != 's' and opcion != 'si':
            break
        anio = eleccionDeMateriaAnio(usuarioActual["usuario"])
        cuatrimestre = eleccionDeMateriaCuatrimestre(usuarioActual["usuario"])
        indices = mostrarMateriasDisponibles(anio, cuatrimestre, usuarioActual, mostrarTodas=True)
        if not indices:
            print("No hay materias disponibles para ese año y cuatrimestre.")
            continue
        print("Seleccione el número de la materia para ver sus notas:")
        for i in range(len(indices)):
            materia_info = buscarMateriaPorIndice(indices[i])
            print(f"{i+1}- {materia_info['nombre']}")
        seleccion = validarEntero(1,len(indices))
        nueva_materia = buscarMateriaPorIndice(indices[seleccion - 1])
        verNotas(usuarioActual, nueva_materia)  # recursividad
        break
    return

#SACA PROMEDIOS
promedio= lambda lista: sum(lista) / len(lista)

def promedioCursada(usuarioActual):
    notas=[]
    for materiaID, materiaNotas in usuarioActual['notas'].items():
        if materiaNotas['nota_final'] is not None:
            notas.append(materiaNotas['nota_final'])
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
    except (IOError, OSError):
        print(f"Error al obtener materias pack de 5.")
    return materiasPackDe5

def guardarMateria(materia_actualizada):
    try:
        materias = []
        materia_actualizada_id = materia_actualizada.get('id')
        with open("ETAPA2/Archivos/materias.json", "r", encoding="utf-8") as archivoMaterias:
            for linea in archivoMaterias:
                try:
                    materia = json.loads(linea.strip())
                    if materia.get('id') == materia_actualizada_id:
                        materias.append(materia_actualizada)
                    else:
                        materias.append(materia)
                except Exception:
                    continue
        with open("ETAPA2/Archivos/materias.json", "w", encoding="utf-8") as archivoMaterias:
            for materia in materias:
                archivoMaterias.write(json.dumps(materia, ensure_ascii=False) + "\n")
    except (OSError, IOError):
        print(f"Error al guardar la materia.")
    except Exception as e:
        print(f"Error al guardar la materia: {e}")


def crearArchivoMaterias():
    data_inicial = """{"id": 1, "nombre": "Fundamentos de Informatica", "año": 1, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 2, "nombre": "Sistemas de Informacion I", "año": 1, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 3, "nombre": "Pensamiento Critico y Comunicacion", "año": 1, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 4, "nombre": "Teoria de Sistemas", "año": 1, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 5, "nombre": "Elementos de Algebra y Geometria", "año": 1, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 6, "nombre": "Programacion I", "año": 1, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 7, "nombre": "Sistemas de Representacion", "año": 1, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 8, "nombre": "Matematica Discreta", "año": 1, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 9, "nombre": "Fundamentos de Quimica", "año": 1, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 10, "nombre": "Arquitectura de Computadores", "año": 1, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 11, "nombre": "Algebra", "año": 1, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 12, "nombre": "Programacion II", "año": 2, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 13, "nombre": "Sistemas de Informacion II", "año": 2, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 14, "nombre": "Sistemas Operativos", "año": 2, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 15, "nombre": "Fisica I", "año": 2, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 16, "nombre": "Calculo I", "año": 2, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 17, "nombre": "Programacion III", "año": 2, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 18, "nombre": "Paradigma Orientado a Objetos", "año": 2, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 19, "nombre": "Fundamentos de Telecomunicaciones", "año": 2, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 20, "nombre": "Ingenieria de Datos I", "año": 2, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 21, "nombre": "Calculo II", "año": 2, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 22, "nombre": "Proceso de Desarrollo de Software", "año": 3, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 23, "nombre": "Seminario de Integracion Profesional", "año": 3, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 24, "nombre": "Teleinformatica y Redes", "año": 3, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 25, "nombre": "Ingenieria de Datos II", "año": 3, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 26, "nombre": "Probabilidad y Estadistica", "año": 3, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 27, "nombre": "Examen de Ingles", "año": 3, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 28, "nombre": "Aplicaciones Interactivas", "año": 3, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 29, "nombre": "Ingenieria de Software", "año": 3, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 30, "nombre": "Fisica II", "año": 3, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 31, "nombre": "Teoria de la Computacion", "año": 3, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 32, "nombre": "Estadistica Avanzada", "año": 3, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 33, "nombre": "Desarrollo de Aplicaciones I", "año": 4, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 34, "nombre": "Direccion de Proyectos Informaticos", "año": 4, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 35, "nombre": "Ciencia de Datos", "año": 4, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 36, "nombre": "Seguridad e Integridad de la Informacion", "año": 4, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 37, "nombre": "Modelado y Simulacion", "año": 4, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 38, "nombre": "Desarrollo de Aplicaciones II", "año": 4, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 39, "nombre": "Evaluacion de Proyectos Informaticos", "año": 4, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 40, "nombre": "Inteligencia Artificial", "año": 4, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 41, "nombre": "Tecnologia y Medio Ambiente", "año": 4, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 42, "nombre": "Practica Profesional Supervisada", "año": 4, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 43, "nombre": "Optativa 1", "año": 4, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 44, "nombre": "Arquitectura de Aplicaciones", "año": 5, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 45, "nombre": "Tendencias Tecnologicas", "año": 5, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 46, "nombre": "Proyecto Final de Ingenieria en Informatica", "año": 5, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 47, "nombre": "Calidad de Software", "año": 5, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 48, "nombre": "Optativa 2", "año": 5, "cuatrimestre": 1, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 49, "nombre": "Negocios Tecnologicos", "año": 5, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 50, "nombre": "Tecnologia e Innovacion", "año": 5, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 51, "nombre": "Derecho Informatico", "año": 5, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}
{"id": 52, "nombre": "Optativa 3", "año": 5, "cuatrimestre": 2, "inscriptos": 0, "correlativas": [], "flashcards": []}"""

    ruta = "ETAPA2/Archivos/materias.json"
    try:
        # Intentar abrir en modo lectura
        with open(ruta, "r", encoding="utf-8") as archivoMaterias:
            pass  # ya existe, no hacemos nada
    except FileNotFoundError:
        # Si no existe, lo creamos con los datos hardcodeados
        try:
            with open(ruta, "w", encoding="utf-8") as archivoMaterias:
                archivoMaterias.write(data_inicial)
            print("Archivo de materias creado correctamente.")
        except Exception as e:
            print(f"Error al crear el archivo de materias: {e}")

