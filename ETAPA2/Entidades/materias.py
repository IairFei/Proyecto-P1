from ManejoDeDatos.validacionDeDatos import estaDentroDelRango,eleccionDeMateriaCuatrimestre, eleccionDeMateriaAnio
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
    del usuario['notas'][str(indicemateria)]
    log("darDeBajaNotas", "INFO", f"Notas de la materia {indicemateria} eliminadas del usuario {usuario['usuario']}.")

def cargarNotas(usuarioActual,materia,diaIngresado):
    usuario = usuarioActual['usuario']
    try:
        print(f"Cargando notas para la materia: {materia["nombre"]}.")
        log("cargarNotas", "INFO", f"Usuario {usuario} está cargando notas para la materia: {materia["nombre"]}.")
        while True:
            try:
                print("¿Que nota desea cargar?\n1- Primer parcial\n2- Segundo parcial\n3- Final regular\n0- Volver al menu principal")
                opcion = int(input("Usuario: "))
                log("cargarNotas", "INFO", f"Usuario {usuario} seleccionó la opción {opcion} para cargar nota.")
                assert estaDentroDelRango(0,3,opcion)
                if opcion == 0:
                    log("cargarNotas", "INFO", f"Usuario decidió volver al menú principal")
                    guardarUsuario(usuarioActual)
                    break
                
                elif opcion == 1:
                    print("Ingrese la nota del primer parcial (0-10):")
                    notaP1 = int(input("Usuario: "))
                    log("cargarNotas", "INFO", f"Usuario {usuario} ingresó la nota {notaP1} para el primer parcial.")
                    assert estaDentroDelRango(0,10,notaP1)
                    usuarioActual["notas"][str(materia["id"])]["parcial1"] = notaP1
                    guardarUsuario(usuarioActual)
                    log("cargarNotas", "INFO", f"Usuario {usuario} cargó la nota {notaP1} para el primer parcial.")
        
                elif opcion == 2:
                    if usuarioActual["notas"][str(materia["id"])]["parcial1"] == None:
                        print("No se puede cargar nota de segundo parcial sin nota de primer parcial.")
                        log("cargarNotas", "INFO", f"Usuario {usuario} intentó cargar nota de segundo parcial sin tener nota de primer parcial.")
                    else:
                        print("Ingrese la nota del segundo parcial (0-10):")
                        notaP2 = int(input("Usuario: "))
                        log("cargarNotas", "INFO", f"Usuario {usuario} ingresó la nota {notaP2} para el segundo parcial.")
                        assert estaDentroDelRango(0,10,notaP2)
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
                        notaFinalInput = int(input("Usuario: "))
                        log("cargarNotas", "INFO", f"Usuario {usuario} ingresó la nota {notaFinalInput} para el final.")
                        assert estaDentroDelRango(0,10,notaFinalInput)
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
                
            except (AssertionError,ValueError):
                print("Opcion inválida. Por favor, ingrese una opcion válida.\n")            
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

        opcion = input("¿Desea ver las notas de otra materia? (s/n): ").strip().lower()
        if opcion != 's':
            break
        try:
            anio = eleccionDeMateriaAnio(usuarioActual["usuario"])
            cuatrimestre = eleccionDeMateriaCuatrimestre(usuarioActual["usuario"])
        except ValueError:
            print("Año o cuatrimestre inválido.")
            continue
        indices = mostrarMateriasDisponibles(anio, cuatrimestre, usuarioActual, mostrarTodas=True)
        if not indices:
            print("No hay materias disponibles para ese año y cuatrimestre.")
            continue
        print("Seleccione el número de la materia para ver sus notas:")
        for i in range(len(indices)):
            materia_info = buscarMateriaPorIndice(indices[i])
            print(f"{i+1}- {materia_info['nombre']}")
        try:
            seleccion=int(input("Número de materia: "))
            if estaDentroDelRango(1, len(indices), seleccion):
                nueva_materia = buscarMateriaPorIndice(indices[seleccion - 1])
                verNotas(usuarioActual, nueva_materia)  # recursividad
                break
            else:
                print("Selección inválida.")
                continue
        except (ValueError, TypeError):
            print("Selección inválida.")
            continue
    return

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
    except Exception as e:
        print(f"Error al guardar la materia: {e}")
