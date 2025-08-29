from vallidacionDeDatos import estaDentroDelRango, charValido
from calendario import verCalendario, inscribirseAMateria
from materias import mostrarMateriasDisponibles, buscarNombreMateriaPorIndice, buscarMateriaPorIndice, buscarMateriaPorNombre

    
def inicioDePrograma():
    print("Elija una opción:\n1- Anotarse a materias\n2- Estado 'Pack de 5 materias'\n3- Cargar nota de materia\n4- Dar de baja una materia\n5- Ver calendario\n6- Ver notas\n0- Salir\n")
    opcionElegida = int(input("Usuario: "))
    print("-----------------------------------------------------")
    while opcionElegida != 0:
        while estaDentroDelRango(0,6,opcionElegida) == False:
            print("Opción inválida. Por favor, elija una opción válida.")
            print("Elija una opción:\n1- Anotarse a materias\n2- Estado 'Pack de 5 materias'\n3- Cargar nota de materia\n4- Dar de baja una materia\n5- Ver calendario\n6- Ver notas\n0- Salir\n")
            opcionElegida = int(input("Usuario: "))
            print("-----------------------------------------------------")
        if opcionElegida == 1:
            print("Ingrese el año de la materia (1-5): ")
            anioElegido = int(input("Usuario: "))
            while estaDentroDelRango(1,5,anioElegido) == False:
                print("Año inválido. Por favor, ingrese un año válido (1-5).")
                print("Ingrese el año de la materia (1-5): ")
                anioElegido = int(input("Usuario: "))  
            print("Ingrese el cuatrimestre de la materia (1-2): ")
            cuatrimestreElegido = int(input("Usuario: "))
            while estaDentroDelRango(1,2,cuatrimestreElegido) == False:
                print("Cuatrimestre inválido. Por favor, ingrese un cuatrimestre válido (1-2).")
                print("Ingrese el cuatrimestre de la materia (1-2): ")
                cuatrimestreElegido = int(input("Usuario: "))
            materiasDisponibles = mostrarMateriasDisponibles(anioElegido,cuatrimestreElegido,materias)
            print(f"Ingrese el numero de la materia que desea inscribirse (1 a  {len(materiasDisponibles)}):")
            materiaElegida = int(input("Usuario: "))
            while estaDentroDelRango(1, len(materiasDisponibles), materiaElegida)==False:
                print(f"Numero inválido. Por favor, ingrese un numero entre 1 y {len(materiasDisponibles)}).")
                print(f"Ingrese el numero de la materia que desea inscribirse (1 a {len(materiasDisponibles)}):")
                materiaElegida = int(input("Usuario: "))
            inscripcionCorrecta = inscribirseAMateria(materiasDisponibles[materiaElegida-1], materias, diasCalendario,calendario)
            if inscripcionCorrecta == False:
                print("No se pudo inscribir a la materia, todos los dias estan ocupados.")
            else:
                print("La inscripcion se realizo con exito.")
            print("Elija una opción:\n1- Anotarse a materias\n2- Estado 'Pack de 5 materias'\n3- Cargar nota de materia\n4- Dar de baja una materia\n5- Ver calendario\n6- Ver notas\n0- Salir\n")
            opcionElegida = int(input("Usuario: "))
            print("-----------------------------------------------------")
        if opcionElegida == 3:
            print("Ingrese el nombre de la materia que desea cargar la nota:")
            nombreMateria = input("Usuario: ")
            print(f"Usted ingreso la materia: {nombreMateria}")
            print("El nombre es correcto? (s/n)")
            nombreCorrecto = input("Usuario: ")
            while charValido(nombreCorrecto) == False:
                print("Caracter inválido. Por favor, ingrese 's' para sí o 'n' para no.")
                print("El nombre es correcto? (s/n)")
                nombreCorrecto = input("Usuario: ")
            if nombreCorrecto.lower().strip() == 'n':
                print("Operacion cancelada. Volviendo al menú principal.")
            else:
                indiceMateria = buscarMateriaPorNombre(nombreMateria, materias)
                print(f"Cargando nota para la materia: {materias[indiceMateria].split('.',3)[2]}")
                
                print("Ingrese la nota del primer parcial (0-10):")
                notaP1 = int(input("Usuario: "))
                while estaDentroDelRango(0,10,notaP1) == False:
                    print("Nota inválida. Por favor, ingrese una nota válida (0-10).")
                    print("Ingrese la nota del primer parcial (0-10):")
                    notaP1 = int(input("Usuario: "))
                print("Ingrese la nota del segundo parcial (0-10):")
                notaP2 = int(input("Usuario: "))
                while estaDentroDelRango(0,10,notaP2) == False:
                    print("Nota inválida. Por favor, ingrese una nota válida (0-10).")
                    print("Ingrese la nota del segundo parcial (0-10):")
                    notaP2 = int(input("Usuario: "))
                p1[indiceMateria] = notaP1
                p2[indiceMateria] = notaP2
                nFinal = (notaP1 + notaP2)//2
                notaFinal[indiceMateria] = nFinal
                if notaP1 >= 4 and notaP2 >= 4:
                    materiasAprobadas[indiceMateria] = 1
                    print("Materia aprobada.")
                elif notaP1 < 4 or notaP2 < 4:
                    materiasRecursar[indiceMateria] = 1
                    print("Materia para recursar.")
                print(f"Notas cargadas correctamente. Nota final: {notaFinal}")
            
            
            
        """if opcionElegida == 2:
            estado = estadoPackDe5Materias()
            print(f"Estado 'Pack de 5 materias': {estado}")  """

        if opcionElegida == 5:
            #verCalendario(calendario, materias)
            inicioDePrograma()
            

        

if __name__ == "__main__":
    diasCalendario = [0,1,2,3,4]
    calendario=[[-1],[-1],[-1],[-1],[-1]]
    materiasAprobadas = [0]*52
    materiasRecursar = [0]*52
    p1 = [0]*52
    p2 = [0]*52
    notaFinal = [0]*52
    materias = ["1.1.Fundamentos de Informatica", "1.1.Sistemas de Información I", "1.1.Pensamiento Critico y Comunicacion", "1.1.Teoría de Sistemas", "1.1.Elementos de Álgebra y Geometría", "1.2.Programación I", "1.2.Sistemas de Representación", "1.2.Matemática Discreta", "1.2.Fundamentos de Química", "1.2.Arquitectura de Computadores", "1.2.Álgebra", "2.1.Programación II", "2.1.Sistemas de Información II", "2.1.Sistemas Operativos", "2.1.Física I", "2.1.Cálculo I", "2.2.Programación III", "2.2.Paradigma Orientado a Objetos", "2.2.Fundamentos de Telecomunicaciones", "2.2.Ingeniería de Datos I", "2.2.Cálculo II", "3.1.Proceso de Desarrollo de Software", "3.1.Seminario de Integración Profesional", "3.1.Teleinformática y Redes", "3.1.Ingeniería de Datos II", "3.1.Probabilidad y Estadística", "3.1.Examen de Inglés", "3.2.Aplicaciones Interactivas", "3.2.Ingeniería de Software", "3.2.Física II", "3.2.Teoría de la Computación", "3.2.Estadística Avanzada", "4.1.Desarrollo de Aplicaciones I", "4.1.Dirección de Proyectos Informáticos", "4.1.Ciencia de Datos", "4.1.Seguridad e Integridad de la Información", "4.1.Modelado y Simulación", "4.2.Desarrollo de Aplicaciones II", "4.2.Evaluación de Proyectos Informáticos", "4.2.Inteligencia Artificial", "4.2.Tecnología y Medio Ambiente", "4.2.Práctica Profesional Supervisada", "4.2.Optativa 1", "5.1.Arquitectura de Aplicaciones", "5.1.Tendencias Tecnológicas", "5.1.Proyecto Final de Ingeniería en Informática", "5.1.Calidad de Software", "5.1.Optativa 2", "5.2.Negocios Tecnológicos", "5.2.Tecnología e Innovación", "5.2.Derecho Informático", "5.2.Optativa 3"]
    inicioDePrograma()


