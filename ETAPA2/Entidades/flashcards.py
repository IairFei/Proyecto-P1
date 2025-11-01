import json
from Entidades.materias import buscarMateriaPorIndice, guardarMateria, mostrarMateriasDisponibles
from ManejoDeDatos.validacionDeDatos import estaDentroDelRango, eleccionDeMateriaAnio, eleccionDeMateriaCuatrimestre
import random
#+from Entidades.materias import promedio 

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

def agregar_flashcard_a_materia(materia_id, nueva_flashcard): #le tengo que pasar el id de alguna manera.
    arch = 'ETAPA2/Archivos/materias.json' 
    lineas_modificadas = []
    materia_encontrada = False
    try:
        with open(arch, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                try:
                    materia = json.loads(linea)
                except Exception:
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
        else:
            print(f"Error: Se leyó el archivo, pero no se encontró ninguna materia con el id {materia_id}.")
    except FileNotFoundError:
        print(f"Error: El archivo no existe en la ruta: {arch}")
    except Exception as e:
        print(f"Ocurrió un error inesperado durante la operación: {e}")

def eliminarDeListaPorAprobar(flashcard):
    arch = 'ETAPA2/Archivos/flashcardsSinAprobar.csv'
    lineas_modificadas = []
    flashcard_encontrada = False
    try:
        with open(arch, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                usuarioCreador, pregunta, respuesta, materia_id = linea.strip().split(";")
                if pregunta != flashcard[0] or respuesta != flashcard[1] or usuarioCreador != flashcard[3]:
                    lineas_modificadas.append(linea)
                else:
                    flashcard_encontrada = True
        if flashcard_encontrada:
            with open(arch, 'w', encoding='utf-8') as archivo:
                archivo.writelines(lineas_modificadas)
            print(f"¡Éxito! Flashcard eliminada de la lista de por aprobar.")
        else:
            print(f"Error: Se leyó el archivo, pero no se encontró la flashcard.")
    except FileNotFoundError:
        print(f"Error: El archivo no existe en la ruta: {arch}")
    except Exception as e:
        print(f"Ocurrió un error inesperado durante la operación: {e}")

def guardarFlashcard(archivo,flashcard,usuario): 
    while True:
        try:
            pregunta=flashcard[0]
            respuesta=flashcard[1]
            materia=flashcard[2]
            archFlash=open(archivo, mode="at")
            archFlash.write(f"{usuario["usuario"]};{pregunta};{respuesta};{materia}\n")
        except OSError as msg:
            print("ERROR:",msg)
        else:
            archFlash.close()
            break
   

def ProponerFlashcard(usuario):
    
    while True:
        try:
            anio=eleccionDeMateriaAnio(usuario["usuario"])
            cuatrimestre=eleccionDeMateriaCuatrimestre(usuario["usuario"])
            materias=mostrarMateriasDisponibles(anio,cuatrimestre, usuario, mostrarTodas=True)
            materiaSeleccionada=int(input(f"{usuario["usuario"]}:"))
            while estaDentroDelRango(1,len(materias),materiaSeleccionada)==False:
                raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
            materiaID=materias[materiaSeleccionada-1]
            break
        except ValueError as msg:
            print("ERROR:",msg)
    print("ingrese la pregunta para la flashcard: ")
    pregunta=input(f"{usuario["usuario"]}: ")
    print("Ingrese la respuesta a la pregunta: ")
    respuesta=input(f"{usuario["usuario"]}: ")
    print("flashcard creada con exito: \n")
    flashcard=(pregunta,respuesta,materiaID)
    mostrarPreguntaFlashcard(pregunta)
    mostrarRespuestaFlashcard(respuesta)
    return flashcard


def aprobarFlashcards(usuario):
    while True:
        try:
            archFlash=open("ETAPA2/Archivos/flashcardsSinAprobar.csv", mode="rt")
            cantidad=contarFlashcards("ETAPA2/Archivos/flashcardsSinAprobar.csv")
            for flashcard in archFlash:
                print("Quedan un total de",cantidad,"flashcards para aprobar")
                campos=flashcard.strip().split(";")
                usuarioCreador=campos[0]
                pregunta=campos[1]
                respuesta=campos[2]
                materia=buscarMateriaPorIndice(int(campos[3].strip()))
                puntaje=[]
                flashcard=(pregunta, respuesta, [] , usuarioCreador)
                print("flashcard creada por:",usuarioCreador)
                print("Materia asociada a la flashcard:",materia["nombre"])
                mostrarPreguntaFlashcard(pregunta)
                mostrarRespuestaFlashcard(respuesta)
                print("¿Que desea hacer?")
                print("│ 1. Aprobar la Flashcard     │")
                print("│ 2. Desaprobar la Flashcard  │")
                print("│ 3. Salir                    │")
                while True:
                    try:
                        opcion=int(input(f"{usuario}: "))
                        if estaDentroDelRango(1,3,opcion)==False:
                            raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
                        if opcion==1:
                            agregar_flashcard_a_materia(materia["id"], flashcard)
                            eliminarDeListaPorAprobar(flashcard)
                            print(f"Flashcard para la materia {materia['nombre']} aprobada exitosamente")
                            break
                        elif opcion==2:
                            print(f"Flashcard para la materia {materia['nombre']} desaprobada exitosamente")
                            eliminarDeListaPorAprobar(flashcard)
                            break
                        else:
                            break
                    except ValueError:
                        print("El valor ingresado no es correcto,intente nuevamente")
                cantidad=cantidad-1
            print(">>Flashcards procesadas exitosamente<<")
        except OSError as msg:
            print("ERROR:",msg)
        else:
            archFlash.close()
            break

def estudiarFlashcard(usuarioActual):
    while True:
        try:
            anio=eleccionDeMateriaAnio(usuarioActual["usuario"])
            cuatrimestre=eleccionDeMateriaCuatrimestre(usuarioActual["usuario"])
            materias=mostrarMateriasDisponibles(anio,cuatrimestre, usuarioActual, mostrarTodas=True)
            if len(materias)==0:
                print("No hay materias con flashcards aprobadas en este año y cuatrimestre")
                return
            materiaSeleccionada=int(input(f"{usuarioActual["usuario"]}:"))
            while estaDentroDelRango(1,len(materias),materiaSeleccionada)==False:
                raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
            materiaID=materias[materiaSeleccionada-1]
            materia=buscarMateriaPorIndice(int(materiaID))
            flashcards=materia["flashcards"]
            if len(flashcards)==0:
                print("No hay flashcards aprobadas para esta materia")
                return
            flashcardsDeSesion=[]
            while True:
                if len(flashcardsDeSesion)==len(flashcards):
                    print(">>Ha estudiado todas las flashcards disponibles para esta materia<<")
                    break
                while True:
                    elegida=random.randint(0,len(flashcards)-1)
                    if elegida not in flashcardsDeSesion:
                        break
                flashcardsDeSesion.append(elegida)
                flashcard = flashcards[elegida]
                pregunta = flashcard[0]
                respuesta = flashcard[1]
                puntajes = flashcard[2]
                usuarioCreador = flashcard[3]
                print(f"Flashcard creada por: {usuarioCreador}")
                mostrarPreguntaFlashcard(pregunta)
                input("Presione ENTER para ver la respuesta...")
                mostrarRespuestaFlashcard(respuesta)
                while True:
                    try:
                        puntaje = int(input("Ingrese un puntaje del 1 al 5 para esta flashcard (0 para no puntuar): "))
                        while estaDentroDelRango(0, 5, puntaje) == False:
                            raise ValueError("Puntaje fuera de rango.")
                        if puntaje != 0:
                            puntajes.append(puntaje)
                            flashcard[2] = puntajes
                            materia["flashcards"][elegida] = flashcard
                            guardarMateria(materia)
                        break
                    except ValueError:
                        print("Puntaje inválido, intente nuevamente.")
                seguir = input("¿Desea seguir estudiando? (s/n): ").strip().lower()
                if seguir != "s":
                    print(">>Fin de la sesión de estudio<<")
                    break
            break
        except ValueError as msg:
            print("ERROR:",msg)

def masInfo():
    print("\n" + "*" * 50)
    print("  ♦  SISTEMA DE FLASHCARDS  ♦")
    print("*" * 50 + "\n")

    print("👉 1. ESTUDIAR FLASHCARDS")
    print("   Se muestran las flashcards que han sido previamente aprobadas.")
    print("\n" + "—" * 50)

    print("📝 2. PROPONER FLASHCARDS")
    print("   Envía nuevas flashcards a los administradores para su revisión y activación.")

    print("\n" + "=" * 50 + "\n")


def menuFlashcard(usuario):
    archivo="ETAPA2/Archivos/flashcardsSinAprobar.csv"
    while True:
        try:
            print("=" * 35)
            print("      🎯 MENÚ DE FLASHCARDS 🎯")
            print("=" * 35)
            print("│ 1. Estudiar Flashcards     │")
            print("│ 2. Proponer Flashcards     │")
            print("│ 3. Más Información         │")
            print("│ 4. Salir                   │")
            print("-" * 35)
            opcion=int(input(f"{usuario["usuario"]}: "))
            if estaDentroDelRango(1,4,opcion)==False:
                raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
            if opcion==1:
                estudiarFlashcard(usuario)
            elif opcion==2:
                guardarFlashcard(archivo,ProponerFlashcard(usuario),usuario)
                print(">>Flashcard propuesta exitosamente<<")
            elif opcion==3:
                masInfo()
            else:
                break
            
        except ValueError:
            print("El valor ingresado no es correcto,intente nuevamente")

