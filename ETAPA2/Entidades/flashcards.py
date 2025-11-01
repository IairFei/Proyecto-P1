import json
from ManejoDeDatos.validacionDeDatos import estaDentroDelRango
from Entidades.materias import mostrarMateriasDisponibles


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
        count=+1
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
                    if linea.strip():
                        lineas_modificadas.append(linea)
                    continue
                if str(materia.get('id')) == str(materia_id):
                    materia_encontrada = True
                    materia['flashcards'].append(nueva_flashcard)
                linea_para_guardar = json.dumps(materia) + '\n'
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


    
#para usar, asignar el nombre del archivo, pasar la flashcard y el usuario que la propone.
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
            print(">>Flashcards procesadas exitosamente<<")

        except OSError as msg:
            print("ERROR:",msg)
        else:
            archFlash.close()
            break

def estudiarFlashcard():
    print("testing")

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
