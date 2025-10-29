from ManejoDeDatos.validacionDeDatos import estaDentroDelRango, charValido
from Entidades.calendario import verCalendario, inscribirseAMateria, darDeBajaMateria
from Entidades.materias import buscarMateriaPorIndice, mostrarMateriasDisponibles, promedioCursada, obtenerMateriasPackDe5, estadoPackDe5Materias, cargarNotas
from Entidades.flashcards import menuFlashcard
from ManejoDeDatos.Usuarios.usuarios import login, tipoUsuario, cambiarRol, validarNombreUsuarioEnSistema, getUsuarioPorNombreUsuario, guardarUsuario,menuAjustes
from ManejoDeDatos.Usuarios.altaUsuario import altaUsuario, inicializarUsuariosFake
from ManejoDeArchivos.verificarArchvos import verificarArchivos
from Logs.logs import log


def menuPrincipal(usuario):
    print("-----------------------------------------------------")
    tipoUsuarioEncontrado = tipoUsuario(usuario)
    print(f"Tipo de usuario: {tipoUsuarioEncontrado}")
    if tipoUsuarioEncontrado == "Administrator":
        print("Menú Principal - Usuario Administrador")
        print("Elija una opción:\n1- Ver calendario\n2- Ver notas\n3- Ver promedio de carrera\n4- Baja de usuario\n5- Cambiar rol de usuario\n6- Ajustes\n0- Salir\n")
    else:
        print("Menú Principal - Usuario Estándar")
        print("Elija una opción:\n1- Anotarse a materias\n2- Estado 'Pack de 5 materias'\n3- Cargar nota de materia\n4- Dar de baja una materia\n5- Ver calendario\n6- Ver notas\n7- Ver promedio de carrera\n8- Practicar con Flashcards\n9- Ajustes\n0- Salir\n")
    opcionElegida = int(input(f"{usuario}: "))
    print("-----------------------------------------------------")
    log("menuPrincipal", "INFO", f"Usuario {usuario} seleccionó la opción {opcionElegida} en el menú principal.")
    return opcionElegida, tipoUsuarioEncontrado

def eleccionDeMateriaAnio(usuario):
    print("Ingrese el año de la materia (1-5): ")
    anioElegido = int(input(f"{usuario}: "))
    while estaDentroDelRango(1,5,anioElegido) == False:
        print("Año inválido. Por favor, ingrese un año válido (1-5).")
        print("Ingrese el año de la materia (1-5): ")
        anioElegido = int(input(f"{usuario}: "))
    log("eleccionDeMateriaAnio", "INFO", f"Usuario {usuario} eligió el año {anioElegido} para la materia.")  
    return anioElegido

def eleccionDeMateriaCuatrimestre(usuario):
    print("Ingrese el cuatrimestre de la materia (1-2): ")
    cuatrimestreElegido = int(input(f"{usuario}: "))
    while estaDentroDelRango(1,2,cuatrimestreElegido) == False:
        print("Cuatrimestre inválido. Por favor, ingrese un cuatrimestre válido (1-2).")
        print("Ingrese el cuatrimestre de la materia (1-2): ")
        cuatrimestreElegido = int(input(f"{usuario}: "))
    log("eleccionDeMateriaCuatrimestre", "INFO", f"Usuario {usuario} eligió el cuatrimestre {cuatrimestreElegido} para la materia.")
    return cuatrimestreElegido

def menuInicial(diasCalendario, calendario, materias, p1, p2, finales, notaFinal, materiasAprobadas, materiasRecursar, correlativas, usuario):
    dias=("Lunes", "Martes", "Miercoles", "Jueves", "Viernes")
    try:
        usuarioActual = getUsuarioPorNombreUsuario(usuario)
        opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
        while opcionElegida != 0:
            while estaDentroDelRango(0,9,opcionElegida) == False:
                print("Opción inválida. Por favor, elija una opción válida.")
                opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
        
        #INSCRIPCION A MATERIA
            if opcionElegida == 1 and tipoUsuarioEncontrado == "User":
                anioElegido = eleccionDeMateriaAnio(usuario)
                cuatrimestreElegido = eleccionDeMateriaCuatrimestre(usuario)
                materiasDisponibles = mostrarMateriasDisponibles(anioElegido,cuatrimestreElegido,usuarioActual)
                if len(materiasDisponibles)==0:
                    print("No hay materias disponibles para inscribirse en este año y cuatrimestre.")
                    log("menuInicial", "INFO", f"Usuario {usuario} no tiene materias disponibles para inscribirse en el año {anioElegido} y cuatrimestre {cuatrimestreElegido}.")
                    opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
                    continue
                print(f"Ingrese el numero de la materia que desea inscribirse (1 a  {len(materiasDisponibles)}):")
                materiaElegida = int(input(f"{usuario}: "))
                log("menuInicial", "INFO", f"Usuario {usuario} eligió la materia número {materiaElegida} para inscribirse.")
                while estaDentroDelRango(1, len(materiasDisponibles), materiaElegida)==False:
                    print(f"Numero inválido. Por favor, ingrese un numero entre 1 y {len(materiasDisponibles)}).")
                    print(f"Ingrese el numero de la materia que desea inscribirse (1 a {len(materiasDisponibles)}):")
                    materiaElegida = int(input(f"{usuario}: "))
                inscribirseAMateria(materiasDisponibles[materiaElegida-1], usuarioActual)
                opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
            elif opcionElegida == 1 and tipoUsuarioEncontrado == "Administrator":
                print("Funcionalidad de 'Ver calendario' para Administradores no implementada aún.")
                opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)

        #PACK DE 5 MATERIAS
            if opcionElegida == 2 and tipoUsuarioEncontrado == "User":
                estado = estadoPackDe5Materias(usuarioActual)
                log("menuInicial", "INFO", f"Usuario {usuario} consultó el estado del 'Pack de 5 materias': {estado}.")
                if estado == True:
                    print("Cumple con las condiciones para el 'Pack de 5 materias'.")
                    print("¿Querés que te anotemos en las próximas 5 materias siguiendo el plan de estudios? (s/n): ")
                    respuesta = input(f"{usuario}: ")
                    log("menuInicial", "INFO", f"Usuario {usuario} respondió '{respuesta}' a la inscripción al 'Pack de 5 materias'.")
                    while charValido(respuesta) == False:
                        print("Caracter inválido. Por favor, ingrese 's' para sí o 'n' para no.")
                        print("¿Querés que te anotemos en las próximas 5 materias siguiendo el plan de estudios? (s/n): ")
                        respuesta = input(f"{usuario}: ")
                        log("menuInicial", "INFO", f"Usuario {usuario} respondió '{respuesta}' a la inscripción al 'Pack de 5 materias'.")
                    if respuesta.lower().strip() == 'n':
                        print("Operacion cancelada. Volviendo al menú principal.")
                        log("menuInicial", "INFO", f"Usuario {usuario} canceló la inscripción al 'Pack de 5 materias'.")
                        opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
                    else:
                        lista5Materias = obtenerMateriasPackDe5(usuarioActual)
                        for i in range(len(lista5Materias)):
                            inscribirseAMateria(lista5Materias[i], usuarioActual)
                        print("Inscripción al 'Pack de 5 materias' completada. Tu calendario quedó así:")
                        log("menuInicial", "INFO", f"Usuario {usuario} se inscribió al 'Pack de 5 materias': {lista5Materias}.")
                        verCalendario(usuarioActual)
                else:
                    print("No cumple con las condiciones para el 'Pack de 5 materias'.")
                    log("menuInicial", "INFO", f"Usuario {usuario} no cumple con las condiciones para el 'Pack de 5 materias'.")
                opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
            elif opcionElegida == 2 and tipoUsuarioEncontrado == "Administrator":
                print("Funcionalidad de 'Ver notas' para Administradores no implementada aún.")
                opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)

        #CARGA DE NOTAS
            if opcionElegida == 3 and tipoUsuarioEncontrado == "User":
                print("Ingrese el numero del dia de la materia que desea cargar la nota:")
                verCalendario(usuarioActual)
                diaIngresado = int(input(f"{usuario}: "))
                materia = buscarMateriaPorIndice(usuarioActual["calendario"][dias[diaIngresado-1]])
                log("menuInicial", "INFO", f"Usuario {usuario} eligió el día {diaIngresado} para cargar la nota.")
                if usuarioActual["calendario"][dias[diaIngresado-1]] is not None:
                    cargarNotas(usuarioActual,materia,diaIngresado)
                    opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
                else:
                    print("No hay materia asignada a ese día. Volviendo al menú principal.")
                    log("menuInicial", "INFO", f"Usuario {usuario} intentó cargar nota en un día sin materia asignada. Volviendo al menú principal.")
                    opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
            
            elif opcionElegida == 3 and tipoUsuarioEncontrado == "Administrator":
                print("Funcionalidad de 'Ver promedio de carrera' para Administradores no implementada aún.")
                opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
        
        #DAR DE BAJA
            if opcionElegida == 4 and tipoUsuarioEncontrado == "User":
                print("Ingrese el numero del dia de la materia que desea dar de baja:")
                verCalendario(usuarioActual)
                diaIngresado = int(input(f"{usuario}: "))
                if usuarioActual["calendario"][dias[diaIngresado-1]] is not None:
                    materia = buscarMateriaPorIndice(usuarioActual["calendario"][dias[diaIngresado-1]])
                    print(f"¿Desea dar de baja la materia {materia['nombre']}? (s/n): ")
                    respuesta = input(f"{usuario}: ")
                    while charValido(respuesta) == False:
                        print("Caracter inválido. Por favor, ingrese 's' para sí o 'n' para no.")
                        print(f"¿Desea dar de baja la materia {materia['nombre']}? (s/n): ")
                        respuesta = input(f"{usuario}: ")
                    if respuesta.lower().strip() == 'n':
                        print("Operacion cancelada. Volviendo al menú principal.")
                        opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
                    else:
                        darDeBajaMateria(usuarioActual, diaIngresado)                    
                        opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
                else:
                    print("No hay materia asignada para ese día. Volviendo al menú principal.")
                    opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
            elif opcionElegida == 4 and tipoUsuarioEncontrado == "Administrator":
                print("Funcionalidad de 'Baja de usuario' para Administradores no implementada aún.")
                opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
                
        # VER CALENDARIO
            if opcionElegida == 5 and tipoUsuarioEncontrado == "User":
                verCalendario(usuarioActual)
                opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
            elif opcionElegida == 5 and tipoUsuarioEncontrado == "Administrator":
                usuarioACambiar= input("Ingrese el nombre de usuario al que desea cambiar el rol: ").strip().lower()
                usuarioACambiar = validarNombreUsuarioEnSistema(usuarioACambiar)
                while usuarioACambiar is None:
                    print("El usuario ingresado no existe. Por favor, ingrese un usuario válido.")
                    usuarioACambiar = input("Ingrese el nombre de usuario al que desea cambiar el rol: ").strip().lower()
                    usuarioACambiar = validarNombreUsuarioEnSistema(usuarioACambiar)
                nuevoRol = int(input("Ingrese el nuevo rol para el usuario (1- User/2-Administrator): "))
                while not estaDentroDelRango(1, 2, nuevoRol):
                    print("Opción inválida. Por favor, ingrese 1 para User o 2 para Administrator.")
                    nuevoRol = int(input("Ingrese el nuevo rol para el usuario (1- User/2-Administrator): "))
                if nuevoRol == 1:
                    nuevoRol = "User"
                else:
                    nuevoRol = "Administrator"
                resultadoCambioDeRol = cambiarRol(nuevoRol, usuarioACambiar)
                if resultadoCambioDeRol:
                    print(f"El rol del usuario {usuarioACambiar[0].strip()} ha sido cambiado a {nuevoRol}.")
                else:
                    print("No se pudo cambiar el rol del usuario.")
                opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)

        # VER NOTAS
            if opcionElegida == 6 and tipoUsuarioEncontrado == "User":
                notaMateria = []
                anioElegido = eleccionDeMateriaAnio(usuario)
                cuatrimestreElegido = eleccionDeMateriaCuatrimestre(usuario)
                materiasDisponibles = mostrarMateriasDisponibles(anioElegido,cuatrimestreElegido,materias,calendario, notaFinal, True)
                print(f"Ingrese el numero de la materia de la que desea ver sus notas (1 a  {len(materiasDisponibles)}):")
                materiaElegida = int(input(f"{usuario}: "))
                while estaDentroDelRango(1, len(materiasDisponibles), materiaElegida)==False:
                    print(f"Numero inválido. Por favor, ingrese un numero entre 1 y {len(materiasDisponibles)}).")
                    print(f"Ingrese el numero de la materia de la que desea ver sus notas (1 a {len(materiasDisponibles)}):")
                    materiaElegida = int(input(f"{usuario}: "))
                indiceMateria = materiasDisponibles[materiaElegida-1]
                Esvacio = lambda: p1[indiceMateria] + p2[indiceMateria] + finales[indiceMateria] + notaFinal[indiceMateria] == 0
                if  Esvacio():
                    print(f"No se encuentran notas cargadas para la materia {materias[indiceMateria].split(".")[2]}.")
                else:
                    print(f"Mostrando notas de la materia: {materias[indiceMateria].split(".")[2]}")
                    if p1[indiceMateria] != 0:
                        notaMateria.append(p1[indiceMateria])
                        print(f"Primer Parcial: {p1[indiceMateria]}")
                    if p2[indiceMateria] != 0:
                        notaMateria.append(p2[indiceMateria])
                        print(f"Segundo Parcial: {p2[indiceMateria]}")
                    if finales[indiceMateria] != 0:
                        notaMateria.append(finales[indiceMateria])
                        print(f"Examen Final: {finales[indiceMateria]}")
                    if notaFinal[indiceMateria] != 0:
                        notaMateria.append(notaFinal[indiceMateria])
                        print(f"Nota final: {notaFinal[indiceMateria]}")
                    print(f"La nota más alta es: {max(notaMateria)} y la más baja es: {min(notaMateria)}")
                opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
        
        #VER PROMEDIO CURSADA
            if opcionElegida == 7 and tipoUsuarioEncontrado == "User":
                print("Notas")
                promedioCursada(notaFinal)
                opcionElegida = menuPrincipal(usuario)

        #VER OPCIONES FLASHCARDS  
            if opcionElegida == 8 and tipoUsuarioEncontrado == "User":
                menuFlashcard()
                opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)
        
        #AJUSTES DE LA CUENTA (CAMBIO DE CONTRASEÑA Y CERRAR SESION)
            if opcionElegida == 9 and tipoUsuarioEncontrado == "User" or opcionElegida == 6 and tipoUsuarioEncontrado == "Administrator":
                cierraSesion = menuAjustes(usuario)
                if cierraSesion:
                    print("Cerrando sesión.\n-----------------------------------------------------")
                    menuLoginPrincipal(diasCalendario, calendario, materias, p1, p2, finales, notaFinal, materiasAprobadas, materiasRecursar, correlativas)
                opcionElegida, tipoUsuarioEncontrado = menuPrincipal(usuario)

        print("Gracias por usar el sistema. ¡Hasta luego!")
    except KeyboardInterrupt as ki:
        print("\nProceso interrumpido por el usuario.")
    except Exception as e:
        print(f"Error: {e}")

def menuLoginPrincipal(diasCalendario, calendario, materias, p1, p2, finales, notaFinal, materiasAprobadas, materiasRecursar, correlativas):
    try:
        #inicializarUsuariosFake()
        print("Bienvenido al sistema de gestión académica.\nPor favor, elija una de las siguientes opciones: \n1-Iniciar sesión\n2-Crear usuario\n3-Salir")
        opcionElegida = int(input("Opción: "))
        while estaDentroDelRango(1,3,opcionElegida) == False:
            print("Opción inválida. Por favor, elija una opción válida.")
            print("Por favor, elija una de las siguientes opciones: \n1-Iniciar sesión\n2-Crear usuario\n3-Salir")
            opcionElegida = int(input("Opción: "))
        log("main", "INFO", f"Opción elegida en el menú de login: {opcionElegida}")
        inicioDeSesionExitoso, usuario = menuLogin(opcionElegida)
        if usuario is None or inicioDeSesionExitoso is False:
            print("Inicio de sesión fallido. Saliendo del programa.")
            log("main", "INFO", "Inicio de sesión fallido.")
            return
    except (Exception, KeyboardInterrupt) as e:
        print(f"Ocurrió un error durante el inicio de sesión: {e}")
        log("main", "ERROR", f"Ocurrió un error durante el inicio de sesión: {e}")
        return
    else:
        print(f"Acceso concedido. Bienvenido {usuario}.")
        log("main", "INFO", f"Usuario {usuario} ha iniciado sesión correctamente.")
        menuInicial(diasCalendario, calendario, materias, p1, p2, finales, notaFinal, materiasAprobadas, materiasRecursar, correlativas, usuario)
        
def inicioDeSesion(usuario=None):
    inicioDeSesionExitoso = False
    try:
        if usuario is None:
            inicioDeSesionExitoso, usuario = login()
            intentosRestantes = 3
            while inicioDeSesionExitoso == False and intentosRestantes > 0:
                log("inicioDeSesion", "WARNING", f"Intento fallido de inicio de sesión para el usuario {usuario}. Intentos restantes: {intentosRestantes-1}.")
                print("Acceso denegado. Inténtelo de nuevo.")
                intentosRestantes -= 1
                print(f"Le quedan {intentosRestantes} intentos.")
                if intentosRestantes == 0:
                    print("Ha agotado todos los intentos. Saliendo del programa.")
                    log("inicioDeSesion", "WARNING", f"Usuario {usuario} ha agotado todos los intentos de inicio de sesión.")
                    raise Exception("Acceso denegado.")
                inicioDeSesionExitoso, usuario = login()               
        return inicioDeSesionExitoso, usuario
    except Exception as e:
        print(f"Error: {e}")

def menuLogin(opcionElegida):
    inicioDeSesionExitoso = False
    try:
        if opcionElegida == 1:
            inicioDeSesionExitoso, usuario = inicioDeSesion()            
        elif opcionElegida == 2:
            usuario = altaUsuario()
            inicioSesion = input("¿Desea iniciar sesión ahora? (s/n): ")
            if charValido(inicioSesion) == False:
                print("Caracter inválido. Por favor, ingrese 's' para sí o 'n' para no.")
                inicioSesion = input("¿Desea iniciar sesión ahora? (s/n): ")
            if inicioSesion.lower().strip() == 's':
                inicioDeSesionExitoso = True
            else:
                main()
        else:
            print("Saliendo del programa. ¡Hasta luego!")
            exit()
        return inicioDeSesionExitoso, usuario
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Inicialización de variables
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
    menuLoginPrincipal(diasCalendario, calendario, materias, p1, p2, finales, notaFinal, materiasAprobadas, materiasRecursar, correlativas)
        
if __name__ == "__main__":
    verificarArchivos()
    main()