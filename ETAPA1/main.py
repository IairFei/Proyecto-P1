from ManejoDeDatos.vallidacionDeDatos import estaDentroDelRango, charValido
from Entidades.calendario import verCalendario, inscribirseAMateria, darDeBajaMateria
from Entidades.materias import mostrarMateriasDisponibles, promedioCursada, obtenerMateriasPackDe5, estadoPackDe5Materias, cargarNotas

def menuPrincipal():
    print("-----------------------------------------------------")
    print("Elija una opción:\n1- Anotarse a materias\n2- Estado 'Pack de 5 materias'\n3- Cargar nota de materia\n4- Dar de baja una materia\n5- Ver calendario\n6- Ver notas\n7- Ver promedio de carrera\n0- Salir\n")
    opcionElegida = int(input("Usuario: "))
    print("-----------------------------------------------------")
    return opcionElegida

def eleccionDeMateriaAnio():
    print("Ingrese el año de la materia (1-5): ")
    anioElegido = int(input("Usuario: "))
    while estaDentroDelRango(1,5,anioElegido) == False:
        print("Año inválido. Por favor, ingrese un año válido (1-5).")
        print("Ingrese el año de la materia (1-5): ")
        anioElegido = int(input("Usuario: "))  
    return anioElegido
def eleccionDeMateriaCuatrimestre():
    print("Ingrese el cuatrimestre de la materia (1-2): ")
    cuatrimestreElegido = int(input("Usuario: "))
    while estaDentroDelRango(1,2,cuatrimestreElegido) == False:
        print("Cuatrimestre inválido. Por favor, ingrese un cuatrimestre válido (1-2).")
        print("Ingrese el cuatrimestre de la materia (1-2): ")
        cuatrimestreElegido = int(input("Usuario: "))
    return cuatrimestreElegido    
def inicioDePrograma():
    opcionElegida = menuPrincipal()
    while opcionElegida != 0:
        while estaDentroDelRango(0,7,opcionElegida) == False:
            print("Opción inválida. Por favor, elija una opción válida.")
            opcionElegida = menuPrincipal()
    #INSCRIPCION A MATERIA
        if opcionElegida == 1:
            anioElegido = eleccionDeMateriaAnio()
            cuatrimestreElegido = eleccionDeMateriaCuatrimestre()
            materiasDisponibles = mostrarMateriasDisponibles(anioElegido,cuatrimestreElegido,materias,calendario, notaFinal, True)            
            print(f"Ingrese el numero de la materia que desea inscribirse (1 a  {len(materiasDisponibles)}):")
            materiaElegida = int(input("Usuario: "))
            while estaDentroDelRango(1, len(materiasDisponibles), materiaElegida)==False:
                print(f"Numero inválido. Por favor, ingrese un numero entre 1 y {len(materiasDisponibles)}).")
                print(f"Ingrese el numero de la materia que desea inscribirse (1 a {len(materiasDisponibles)}):")
                materiaElegida = int(input("Usuario: "))
            inscribirseAMateria(materiasDisponibles[materiaElegida-1], materias, diasCalendario,calendario, notaFinal, correlativas)
            opcionElegida = menuPrincipal()

    #PACK DE 5 MATERIAS
        if opcionElegida == 2:
            estado = estadoPackDe5Materias(calendario, materiasRecursar)
            if estado == True:
                print("Cumple con las condiciones para el 'Pack de 5 materias'.")
                print("¿Querés que te anotemos en las próximas 5 materias siguiendo el plan de estudios? (s/n): ")
                respuesta = input("Usuario: ")
                while charValido(respuesta) == False:
                    print("Caracter inválido. Por favor, ingrese 's' para sí o 'n' para no.")
                    print("¿Querés que te anotemos en las próximas 5 materias siguiendo el plan de estudios? (s/n): ")
                    respuesta = input("Usuario: ")
                if respuesta.lower().strip() == 'n':
                    print("Operacion cancelada. Volviendo al menú principal.")
                    opcionElegida = menuPrincipal()
                else:
                    lista5Materias = obtenerMateriasPackDe5(materiasAprobadas, materias, correlativas, notaFinal)
                    for i in range(len(lista5Materias)):
                        inscribirseAMateria(lista5Materias[i], materias, diasCalendario,calendario, notaFinal, correlativas)
                    print("Inscripción al 'Pack de 5 materias' completada. Tu calendario quedó así:")
                    verCalendario(calendario, materias)
            else:
                print("No cumple con las condiciones para el 'Pack de 5 materias'.")
            opcionElegida = menuPrincipal()

    #CARGA DE NOTAS
        if opcionElegida == 3:
            print("Ingrese el numero del dia de la materia que desea cargar la nota:")
            verCalendario(calendario, materias)
            diaIngresado = int(input("Usuario: "))
            if calendario[diaIngresado-1] != -1:
                cargarNotas(calendario[diaIngresado-1],p1,p2,finales,notaFinal,materias, calendario, diasCalendario, materiasAprobadas, materiasRecursar)
                opcionElegida = menuPrincipal()
            else:
                print("No hay materia asignada para ese día. Volviendo al menú principal.")
                opcionElegida = menuPrincipal()
    
    #DAR DE BAJA
        if opcionElegida == 4:
            print("Ingrese el numero del dia de la materia que desea dar de baja:")
            verCalendario(calendario, materias)
            diaIngresado = int(input("Usuario: "))
            if calendario[diaIngresado-1] != -1:
                indiceMateria = calendario[diaIngresado-1]
                materia = materias[indiceMateria].split(".",3)
                print(f"¿Desea dar de baja la materia {materia[2]}? (s/n): ")
                respuesta = input("Usuario: ")
                while charValido(respuesta) == False:
                    print("Caracter inválido. Por favor, ingrese 's' para sí o 'n' para no.")
                    print(f"¿Desea dar de baja la materia {materia[2]}? (s/n): ")
                    respuesta = input("Usuario: ")
                if respuesta.lower().strip() == 'n':
                    print("Operacion cancelada. Volviendo al menú principal.")
                    opcionElegida = menuPrincipal()
                else:
                    darDeBajaMateria(diaIngresado,calendario,diasCalendario,p1,p2,notaFinal)                    
                    opcionElegida = menuPrincipal()
            else:
                print("No hay materia asignada para ese día. Volviendo al menú principal.")
                opcionElegida = menuPrincipal()


    # VER CALENDARIO
        if opcionElegida == 5:
            verCalendario(calendario, materias)
            opcionElegida = menuPrincipal()

    # VER NOTAS
        if opcionElegida == 6:
            anioElegido = eleccionDeMateriaAnio()
            cuatrimestreElegido = eleccionDeMateriaCuatrimestre()
            materiasDisponibles = mostrarMateriasDisponibles(anioElegido,cuatrimestreElegido,materias,calendario, notaFinal, False)
            print(f"Ingrese el numero de la materia de la que desea ver sus notas (1 a  {len(materiasDisponibles)}):")
            materiaElegida = int(input("Usuario: "))
            while estaDentroDelRango(1, len(materiasDisponibles), materiaElegida)==False:
                print(f"Numero inválido. Por favor, ingrese un numero entre 1 y {len(materiasDisponibles)}).")
                print(f"Ingrese el numero de la materia de la que desea ver sus notas (1 a {len(materiasDisponibles)}):")
                materiaElegida = int(input("Usuario: "))
            indiceMateria = materiasDisponibles[materiaElegida-1]
            Esvacio = lambda: p1[indiceMateria] + p2[indiceMateria] + finales[indiceMateria] + notaFinal[indiceMateria] == 0
            if  Esvacio():
                print(f"No se encuentran notas cargadas para la materia {materias[indiceMateria].split(".")[2]}.")
            else:
                print(f"Mostrando notas de la materia: {materias[indiceMateria].split(".")[2]}")
                if p1[indiceMateria] != 0:
                    print(f"Primer Parcial: {p1[indiceMateria]}")
                if p2[indiceMateria] != 0:
                    print(f"Segundo Parcial: {p2[indiceMateria]}")
                if finales[indiceMateria] != 0:
                    print(f"Examen Final: {finales[indiceMateria]}")
                if notaFinal[indiceMateria] != 0:
                    print(f"Nota final: {notaFinal[indiceMateria]}")
            opcionElegida = menuPrincipal()

    #VER PROMEDIO CURSADA
        if opcionElegida == 7:
    
            print("Notas")
            promedioCursada(notaFinal)
            opcionElegida = menuPrincipal()
          

if __name__ == "__main__":
    diasCalendario = [0,1,2,3,4]
    calendario=[-1,-1,-1,-1,-1]
    materiasAprobadas = [0]*52
    materiasRecursar = [0]*52
    p1 = [0]*52
    p2 = [0]*52
    finales = [0]*52
    notaFinal = [0]*52
    materias = ["1.1.Fundamentos de Informatica", "1.1.Sistemas de Informacion I", "1.1.Pensamiento Critico y Comunicacion", "1.1.Teoria de Sistemas", "1.1.Elementos de Algebra y Geometria", "1.2.Programacion I", "1.2.Sistemas de Representacion", "1.2.Matematica Discreta", "1.2.Fundamentos de Quimica", "1.2.Arquitectura de Computadores", "1.2.Algebra", "2.1.Programacion II", "2.1.Sistemas de Informacion II", "2.1.Sistemas Operativos", "2.1.Fisica I", "2.1.Calculo I", "2.2.Programacion III", "2.2.Paradigma Orientado a Objetos", "2.2.Fundamentos de Telecomunicaciones", "2.2.Ingenieria de Datos I", "2.2.Calculo II", "3.1.Proceso de Desarrollo de Software", "3.1.Seminario de Integracion Profesional", "3.1.Teleinformatica y Redes", "3.1.Ingenieria de Datos II", "3.1.Probabilidad y Estadistica", "3.1.Examen de Ingles", "3.2.Aplicaciones Interactivas", "3.2.Ingenieria de Software", "3.2.Fisica II", "3.2.Teoria de la Computacion", "3.2.Estadistica Avanzada", "4.1.Desarrollo de Aplicaciones I", "4.1.Direccion de Proyectos Informaticos", "4.1.Ciencia de Datos", "4.1.Seguridad e Integridad de la Informacion", "4.1.Modelado y Simulacion", "4.2.Desarrollo de Aplicaciones II", "4.2.Evaluacion de Proyectos Informaticos", "4.2.Inteligencia Artificial", "4.2.Tecnologia y Medio Ambiente", "4.2.Practica Profesional Supervisada", "4.2.Optativa 1", "5.1.Arquitectura de Aplicaciones", "5.1.Tendencias Tecnologicas", "5.1.Proyecto Final de Ingenieria en Informatica", "5.1.Calidad de Software", "5.1.Optativa 2", "5.2.Negocios Tecnologicos", "5.2.Tecnologia e Innovacion", "5.2.Derecho Informatico", "5.2.Optativa 3"]
    correlativas=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    inicioDePrograma()


