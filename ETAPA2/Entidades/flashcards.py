import json
from ManejoDeDatos.validacionDeDatos import estaDentroDelRango
from Entidades.materias import promedio, eleccionDeMateriaAnio, eleccionDeMateriaCuatrimestre, mostrarMateriasDisponibles

def resetArchivoFlashcardsSinAprobar():
    archivo="ETAPA2/Archivos/flashcardsSinAprobar.csv"
    try:
        archFlash=open(archivo, mode="wt")
        archFlash.write("usuarioCreador;pregunta;respuesta;materia\n")
    except OSError as msg:
        print("ERROR:",msg)
    else:
        archFlash.close()

def mostrarPreguntaFlashcard(pregunta):
    print("-"*5,"PREGUNTA","-"*5,"\n","\n")
    print(pregunta,"\n","\n")
    
def mostrarRespuestaFlashcard(respuesta):
    print("-"*5,"RESPUESTA","-"*5,"\n","\n")
    print(respuesta,"\n","\n")

def contarFlashcards(archivo):
    arch=open(archivo,mode="rt")
    count=0
    for lines in arch:
        count+=1
    arch.close()
    return count

def agregar_flashcard_a_materia(materia_id, nueva_flashcard):
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
    except Exception as e:
        print(f"Ocurrió un error inesperado durante la operación: {e}")

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
            archFlash=open("ETAPA2/Archivos/flashcardsSinAprobar.csv", mode="rt")
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
                print("¿Que desea hacer?")
                print("│ 1. Aprobar la Flashcard     │")
                print("│ 2. Desaprobar la Flashcard  │")
                while True:
                    try:
                        opcion=int(input(f"{usuario}: "))
                        if estaDentroDelRango(1,2,opcion)==False:
                            raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
                        if opcion==1:
                            flashcard={}
                            flashcard[pregunta]=usuario,respuesta,puntaje
                            agregar_flashcard_a_materia(materia, flashcard)
                            print("Flashcard aprobada exitosamente")
                            break
                        elif opcion==2:
                            print("Flashcard desaprobada exitosamente")
                            break
                    except ValueError:
                        print("El valor ingresado no es correcto,intente nuevamente")
                cantidad=cantidad-1
            resetArchivoFlashcardsSinAprobar()
            print(">>Flashcards procesadas exitosamente<<")

        except OSError as msg:
            print("ERROR:",msg)
        else:
            archFlash.close()
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
    except Exception as e:
        print(f"Error al buscar flashcards: {e}")
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
            print("│ 1. Si  │")
            print("│ 2. No  │")
            while True:
                try:
                    opcion=int(input(f"{usuario}: "))
                    if estaDentroDelRango(1,2,opcion)==False:
                        raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
                    if opcion==1:
                        flashcard={}
                        flashcard[pregunta]=respuesta,puntaje
                        seleccionadas.append(flashcard)
                        print("   ✅ ¡Guardada!")
                        break
                    elif opcion==2:
                        print("   ➡️ Omitida.")
                        break
                except ValueError:
                    print("El valor ingresado no es correcto,intente nuevamente")
    print(f"\n🎉 Selección finalizada. Has elegido {len(seleccionadas)} flashcards.")
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
                print(f"✅ ¡Éxito! Puntaje ({puntajeNuevo}) añadido a la flashcard '{preguntaFlashcard}' en la materia {materia_id}.")
            else:
                print(f"⚠️ Éxito al leer el archivo, pero no se encontró la flashcard '{preguntaFlashcard}' en la materia {materia_id}.")
        else:
            print(f"❌ Error: Se leyó el archivo, pero no se encontró ninguna materia con el id {materia_id}.")

    except FileNotFoundError:
        print(f"❌ Error: El archivo no existe en la ruta: {arch}")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado durante la operación: {e}")

def estudiarFlashcard(idMateria,usuario):
    flashcardsDisponibles=obtenerFlashcardsPorMateria(idMateria)
    if len(flashcardsDisponibles)>0:
        flashcardsAEstudiar=seleccionarFlashcards(flashcardsDisponibles,usuario)
        print(">>Iniciando sesion de estudio<<")
        for flashcard in flashcardsAEstudiar:
            for clave in flashcard:
                pregunta=str(clave)
                respuesta=str(flashcard[clave][0])
                puntaje=flashcard[clave][1]
                mostrarPreguntaFlashcard(pregunta)
                print("│ 1. Mostrar Respuesta  │")
                print("│ 2. Saltear            │")
                while True:
                    try:
                        opcion=int(input(f"{usuario}: "))
                        if estaDentroDelRango(1,2,opcion)==False:
                            raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
                        if opcion==1:
                            mostrarRespuestaFlashcard(respuesta)
                            print("Califique esta flashcard del 1 al 5:")
                            while True:
                                try:
                                    calificacion = int(input(f"{usuario}: "))
                                    if estaDentroDelRango(1,5,calificacion)==False:
                                        raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
                                    actualizarPuntajes(idMateria, calificacion, pregunta)
                                    break
                                except ValueError:
                                    print("El valor ingresado no es correcto,intente nuevamente")
                            break
                        elif opcion==2:
                            print("   ➡️ Omitida.")
                            break
                    except ValueError:
                        print("El valor ingresado no es correcto,intente nuevamente")

def masInfo():
    print("\n" + "*" * 50)
    print("  ♦  SISTEMA DE FLASHCARDS  ♦")
    print("*" * 50 + "\n")

    print("👉 1. ELEGIR MATERIA PARA CONTINUAR")
    print("   Se le pide al usuario elegir una materia, para que luego elija que hacer")
    print("📚 1. Estudiar flashcards de la materia elegida")
    print("      Se muestran las flashcards disponibles para la materia seleccionada")
    print("      El usuario puede elegir cuales quiere estudiar.")
    print("✍️ 2. Proponer nuevas flashcards para la materia elegida")
    print("      Se le permite al usuario enviar nuevas flashcards para su revisión.")

    print("\n" + "=" * 50 + "\n")

def menuFlashcards(usuarioActual):
    opcionDelMenuFlashcards = ""
    while True:
        try:
            print("=" * 35)
            print("      🎯 MENÚ DE FLASHCARDS 🎯")
            print("=" * 35)
            print("│ 1. Elegir Materia para continuar     │")
            print("│ 2. Más Información                   │")
            print("│ 0. Salir                             │")
            print("-" * 35)
            opcion=int(input(f"{usuarioActual["usuario"]}: "))
            if estaDentroDelRango(0,2,opcion)==False:
                raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
            if opcion==1:
                print(f"A continuacion, por favor elija para que materia para {opcionDelMenuFlashcards.lower()}:")
                anioElegido = eleccionDeMateriaAnio(usuarioActual["usuario"])
                cuatrimestreElegido = eleccionDeMateriaCuatrimestre(usuarioActual["usuario"])
                materiasDisponibles = mostrarMateriasDisponibles(anioElegido,cuatrimestreElegido,usuarioActual,mostrarTodas=True)
                print(f"Ingrese el numero de la materia a la que corresponde la flashcard (1 a  {len(materiasDisponibles)}):")
                Materia = int(input(f"{usuarioActual["usuario"]}: "))
                while estaDentroDelRango(1, len(materiasDisponibles), Materia)==False:
                    print(f"Numero inválido. Por favor, ingrese un numero entre 1 y {len(materiasDisponibles)}).")
                    print(f"Ingrese el numero de la materia a la que corresponde la flashcard (1 a {len(materiasDisponibles)}):")
                    Materia = int(input(f"{usuarioActual["usuario"]}: "))
                idMateria=materiasDisponibles[Materia-1]
                print("=" * 35)
                print("      🎯 MENÚ DE FLASHCARDS 🎯")
                print("=" * 35)
                print("│ 1. Estudiar Flashcards               │")
                print("│ 2. Proponer Flashcards               │")
                print("│ 0. Salir                             │")
                print("-" * 35)
                opcion=int(input(f"{usuarioActual["usuario"]}: "))
                if estaDentroDelRango(1,3,opcion)==False:
                    raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
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