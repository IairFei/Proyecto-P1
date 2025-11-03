import json
from ManejoDeDatos.validacionDeDatos import validarEntero
from Entidades.materias import promedio, eleccionDeMateriaAnio, eleccionDeMateriaCuatrimestre, mostrarMateriasDisponibles
from Logs.logs import log

def resetArchivoFlashcardsSinAprobar():
    archivo="ETAPA2/Archivos/flashcardsSinAprobar.csv"
    try:
        archFlash=open(archivo, mode="wt")
        archFlash.write("usuarioCreador;pregunta;respuesta;materia\n")
    except OSError as msg:
        print("ERROR:",msg)
        log("resetArchivoFlashcardsSinAprobar","ERROR",f"No se pudo resetear el archivo de flashcards sin aprobar: {msg}")
    else:
        archFlash.close()

def mostrarPreguntaFlashcard(pregunta):
    print("-"*5,"PREGUNTA","-"*5,"\n")
    print(pregunta,"\n",)

def mostrarRespuestaFlashcard(respuesta):
    print("-"*5,"RESPUESTA","-"*5,"\n")
    print(respuesta,"\n")

def contarFlashcards(archivo):
    arch=open(archivo,mode="rt")
    next(arch)
    count=0
    for lines in arch:
        count+=1
    arch.close()
    return count

def agregarFlashcardAMateria(materia_id, nueva_flashcard):
    arch = 'ETAPA2/Archivos/materias.json' 
    lineas_modificadas = []
    materia_encontrada = False
    try:
        with open(arch, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                try:
                    materia = json.loads(linea)
                except Exception:
                    if linea.strip():
                        lineas_modificadas.append(linea)
                    continue
                if str(materia.get('id')) == str(materia_id):
                    materia_encontrada = True
                    materia['flashcards'].append(nueva_flashcard)
                linea_para_guardar = json.dumps(materia, ensure_ascii=False) + '\n'
                lineas_modificadas.append(linea_para_guardar)
        if materia_encontrada:
            with open(arch, 'w', encoding='utf-8') as archivo:
                archivo.writelines(lineas_modificadas)
            print(f"¡Éxito! Flashcard agregada a la materia con id {materia_id}.")
            
        else:
            print(f"Error: Se leyó el archivo, pero no se encontró ninguna materia con el id {materia_id}.")
    except FileNotFoundError:
        print(f"Error: El archivo no existe en la ruta: {arch}")
        log("agregarFlashcardAMateria","ERROR",f"El archivo no existe en la ruta: {arch}")

def guardarFlashcard(flashcard,usuario):
    archivo="ETAPA2/Archivos/flashcardsSinAprobar.csv"
    while True:
        try:
            for clave in flashcard:
                pregunta=str(clave)
                respuesta=str(flashcard[clave][0])
                materia=flashcard[clave][1]
            #print(pregunta,respuesta,puntaje)
            archFlash=open(archivo, mode="at")
            archFlash.write(f"{usuario};{pregunta};{respuesta};{materia}\n")
        except OSError as msg:
            print("ERROR:",msg)
        else:
            archFlash.close()
            break

def ProponerFlashcard(usuario,idMateria):
    flashcard={}
    materia=idMateria
    print("ingrese la pregunta para la flashcard: ")
    pregunta=input(f"{usuario}: ")
    print("Ingrese la respuesta a la pregunta: ")
    respuesta=input(f"{usuario}: ")
    print("Flashcard creada con exito: \n")
    flashcard[pregunta]=respuesta,materia
    mostrarPreguntaFlashcard(pregunta)
    mostrarRespuestaFlashcard(respuesta)
    return flashcard

def aprobarFlashcards(usuario):
    while True:
        try:
            with open("ETAPA2/Archivos/flashcardsSinAprobar.csv", mode="rt") as archFlash:
                next(archFlash)
                cantidad=contarFlashcards("ETAPA2/Archivos/flashcardsSinAprobar.csv")
                for flashcard in archFlash:
                    print("Quedan un total de",cantidad,"flashcards para aprobar")
                    campos=flashcard.strip().split(";")
                    usuario=campos[0]
                    pregunta=campos[1]
                    respuesta=campos[2]
                    materia=campos[3]
                    puntaje=[]
                    print("Flashcard creada por:",usuario)
                    mostrarPreguntaFlashcard(pregunta)
                    mostrarRespuestaFlashcard(respuesta)
                    print("¿Que desea hacer?\n1- Aprobar la Flashcard\n2- Desaprobar la Flashcard")
                    opcion= validarEntero(1,2)
                    if opcion==1:
                        flashcard={}
                        flashcard[pregunta]=usuario,respuesta,puntaje
                        agregarFlashcardAMateria(materia, flashcard)
                        print("Flashcard aprobada exitosamente")
                    else:
                        print("Flashcard desaprobada exitosamente")
                    cantidad=cantidad-1
                resetArchivoFlashcardsSinAprobar()
                print("Flashcards procesadas exitosamente.")
        except (OSError,IOError):
            print("Error al abrir el archivo.")
            log("aprobarFlashcards","ERROR","Error al abrir el archivo de flashcards sin aprobar")
        break

def obtenerFlashcardsPorMateria(idMateria):
    flashcards=[]
    try:
        with open("ETAPA2/Archivos/materias.json", "r", encoding="utf-8") as archivoMaterias:
            for linea in archivoMaterias:
                try:
                    materia = json.loads(linea.strip())
                    if materia.get('id') == idMateria:
                        flashcards = materia.get('flashcards', [])
                        break
                except Exception:
                    continue
        if flashcards is None or len(flashcards) == 0:
            print("No hay flashcards disponibles para la materia elegida")
    except (IOError, OSError):
        print("Error al abrir el archivo de materias.")
        log("obtenerFlashcardsPorMateria","ERROR","Error al abrir el archivo de materias.json")
    return flashcards

def seleccionarFlashcards(listaFlashcards,usuario):
    seleccionadas=[]
    print("Las flashcards disponibles son:")
    for flashcard in listaFlashcards:
        for clave in flashcard:
            pregunta=str(clave)
            usuariocreador=flashcard[clave][0]
            respuesta=str(flashcard[clave][1])
            puntaje=flashcard[clave][1]
            mostrarPreguntaFlashcard(pregunta)
            print(f"Flashcard creada por: {usuariocreador}")
            print("¿Desea estudiar esta flashcard?")
            print("1- Si\n2- No")
            opcion= validarEntero(1,2)
            if opcion==1:
                flashcard={}
                flashcard[pregunta]=respuesta,puntaje
                seleccionadas.append(flashcard)
                print("Flashcard guardada.")
                log("seleccionarFlashcard","INFO",f"el se guardo flashcard -{pregunta}-")
            elif opcion==2:
                print("Flashcard omitida.")
    print(f"\nSelección finalizada. Has elegido {len(seleccionadas)} flashcards.")
    return seleccionadas

def actualizarPuntajes(materia_id, puntajeNuevo, preguntaFlashcard):
    arch = 'ETAPA2/Archivos/materias.json'
    lineas_modificadas = []
    materia_encontrada = False
    flashcard_actualizada = False
    try:
        with open(arch, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                try:
                    materia = json.loads(linea.strip())
                    if str(materia.get('id')) == str(materia_id):
                        materia_encontrada = True
                        flashcards = materia.get('flashcards', [])
                        for flashcard_dicc in flashcards:
                            if preguntaFlashcard in flashcard_dicc:
                                datos_flashcard = flashcard_dicc[preguntaFlashcard]
                                lista_puntajes = datos_flashcard[2]
                                lista_puntajes.append(puntajeNuevo)
                                flashcard_actualizada = True
                                break
                    linea_para_guardar = json.dumps(materia, ensure_ascii=False) + '\n'
                    lineas_modificadas.append(linea_para_guardar)
                except Exception:
                    lineas_modificadas.append(linea)
                    continue
        if materia_encontrada:
            with open(arch, 'w', encoding='utf-8') as archivo:
                archivo.writelines(lineas_modificadas)
            if flashcard_actualizada:
                print(f"¡Éxito! Puntaje ({puntajeNuevo}) añadido a la flashcard '{preguntaFlashcard}' en la materia {materia_id}.")
            else:
                print(f"Éxito al leer el archivo, pero no se encontró la flashcard '{preguntaFlashcard}' en la materia {materia_id}.")
        else:
            print(f"Error: Se leyó el archivo, pero no se encontró ninguna materia con el id {materia_id}.")

    except (FileNotFoundError, IOError, OSError):
        print(f"Error: El archivo no existe en la ruta: {arch}")
        log("actualizarPuntajes","ERROR",f"El archivo no existe en la ruta: {arch}")

def estudiarFlashcard(idMateria,usuario):
    flashcardsDisponibles=obtenerFlashcardsPorMateria(idMateria)
    if len(flashcardsDisponibles)>0:
        flashcardsAEstudiar=seleccionarFlashcards(flashcardsDisponibles,usuario)
        print(">>Iniciando sesion de estudio<<")
        for flashcard in flashcardsAEstudiar:
            for clave in flashcard:
                pregunta = str(clave)
                respuesta = str(flashcard[clave][0])
                mostrarPreguntaFlashcard(pregunta)
                print("1- Mostrar Respuesta")
                print("2- Saltear Flashcard")
                opcion= validarEntero(1,2)
                if opcion==1:
                    mostrarRespuestaFlashcard(respuesta)
                    print("Califique esta flashcard del 1 al 5:")
                    calificacion = validarEntero(1,5)
                    actualizarPuntajes(idMateria, calificacion, pregunta)
                    log("estudiarFlashcard","INFO",f"el usuario Califico la flashcard -{pregunta}-")
                elif opcion==2:
                    print("Flashcard omitida.")
                    log("estudiarFlashcard","INFO",f"el usuario omitio la flashcard -{pregunta}-")
                    break

def masInfo():
    print("\n" + "*" * 50)
    print("    SISTEMA DE FLASHCARDS  ")
    print("*" * 50 + "\n")

    print("1. ELEGIR MATERIA PARA CONTINUAR")
    print("   Se le pide al usuario elegir una materia, para que luego elija que hacer")
    print("1. Estudiar flashcards de la materia elegida")
    print("      Se muestran las flashcards disponibles para la materia seleccionada")
    print("      El usuario puede elegir cuales quiere estudiar.")
    print("2. Proponer nuevas flashcards para la materia elegida")
    print("      Se le permite al usuario enviar nuevas flashcards para su revisión.")

    print("\n" + "=" * 50 + "\n")

def menuFlashcards(usuarioActual):
    opcionDelMenuFlashcards = ""
    while True:
        try:
            print("=" * 35)
            print("       MENÚ DE FLASHCARDS ")
            print("=" * 35)
            print("1- Elegir Materia para continuar\n2- Mas Informacion\n0- Salir")
            print("-" * 35)
            opcion = validarEntero(0,2)
            if opcion==1:
                print(f"A continuacion, por favor elija para que materia para {opcionDelMenuFlashcards.lower()}:")
                anioElegido = eleccionDeMateriaAnio(usuarioActual["usuario"])
                cuatrimestreElegido = eleccionDeMateriaCuatrimestre(usuarioActual["usuario"])
                materiasDisponibles = mostrarMateriasDisponibles(anioElegido,cuatrimestreElegido,usuarioActual,mostrarTodas=True)
                print(f"Ingrese el numero de la materia a la que corresponde la flashcard (1 a  {len(materiasDisponibles)}):")
                Materia = validarEntero(1,len(materiasDisponibles))
                idMateria = materiasDisponibles[Materia-1]
                print("=" * 35)
                print("       MENÚ DE FLASHCARDS ")
                print("=" * 35)
                print("1- Estudiar Flashcards\n2- Proponer Flashcards\n0- Salir")
                print("-" * 35)
                opcion = validarEntero(0,2)
                if opcion==1:
                    estudiarFlashcard(idMateria,usuarioActual["usuario"])
                    
                elif opcion==2:
                    guardarFlashcard(ProponerFlashcard(usuarioActual["usuario"],idMateria),usuarioActual["usuario"])
                    print(">>Flashcard propuesta exitosamente<<")
                else:
                    break
            elif opcion==2:
                masInfo()
            else:
                break
        except ValueError:
            print("El valor ingresado no es correcto,intente nuevamente")
            log("menuFlashcards","ERROR","El valor ingresado no es correcto,intente nuevamente")