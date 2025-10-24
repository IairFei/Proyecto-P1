from ManejoDeDatos.validacionDeDatos import estaDentroDelRango

def mostrarPreguntaFlashcard(pregunta):
    print("-"*5,"PREGUNTA","-"*5,"\n","\n")
    print(pregunta,"\n","\n")
    
def mostrarRespuestaFlashcard(respuesta):
    print("-"*5,"RESPUESTA","-"*5,"\n","\n")
    print(respuesta,"\n","\n")

def guardarFlashcard(flashcard):
    while True:
        try:
            for clave in flashcard:
                pregunta=str(clave)
                respuesta=str(flashcard[clave][0])
                puntaje=str(flashcard[clave][1])
            #print(pregunta,respuesta,puntaje)
            archFlash=open("ETAPA2/Archivos/flashcardsSinAprobar.csv", mode="at")
            archFlash.write(str(pregunta+";"+respuesta+";"+puntaje+"\n"))
            print("HASTA ACA LLEGAMOS LOL")
        except OSError as msg:
            print("ERROR:",msg)
        else:
            archFlash.close()
            break
   


def ProponerFlashcard():
    flashcard={}
    puntaje=-1
    print("ingrese la pregunta para la flashcard: ")
    pregunta=input("usuario: ")
    print("Ingrese la respuesta a la pregunta: ")
    respuesta=input("usuario: ")
    print("flashcard creada con exito: \n")
    flashcard[pregunta]=respuesta,puntaje
    mostrarPreguntaFlashcard(pregunta)
    mostrarRespuestaFlashcard(respuesta)
    return flashcard

def estudiarFlashcard():
    print("testing")

def masInfo():
    print("""------------------\nEl sistema de Flashcards funciona de la siguiente manera:
          \n->Ingresando la opcion 1, se muestran las flashcards aprobadas por un administrador para cada materia.
          \n->Ingresando la opcion 2, se proponen nuevas flashcards para que los administradores puedan revisarla y habilitarla para el uso de todos los estudiantes\n---------------- """)


def menuFlashcard():
    while True:
        try:
            print("Ingrese el numero de la opcion a elegir.")
            print("OPCIONES:")
            print("1.Estudiar Flashcards\n2.Proponer Flashcards\n3.Mas informacion\n4.Salir\n")
            opcion=int(input("usuario: "))
            
            if estaDentroDelRango(1,4,opcion)==False:
                raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
            if opcion==1:
                estudiarFlashcard()
            elif opcion==2:
                guardarFlashcard(ProponerFlashcard())
            elif opcion==3:
                masInfo()
            else:
                break
            
        except ValueError:
            print("El valor ingresado no es correcto,intente nuevamente")

