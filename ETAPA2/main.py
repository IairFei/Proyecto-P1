from ManejoDeDatos.validacionDeDatos import estaDentroDelRango, charValido, eleccionDeMateriaAnio, eleccionDeMateriaCuatrimestre
from Entidades.calendario import verCalendario, inscribirseAMateria, darDeBajaMateria
from Entidades.materias import verNotas,buscarMateriaPorIndice, mostrarMateriasDisponibles, promedioCursada, obtenerMateriasPackDe5, estadoPackDe5Materias, cargarNotas
from Entidades.flashcards import menuFlashcard,aprobarFlashcards,masInfo,guardarFlashcard,ProponerFlashcard
from ManejoDeDatos.Usuarios.usuarios import login, tipoUsuario, cambiarRol, validarNombreUsuarioEnSistema, getUsuarioPorNombreUsuario, guardarUsuario,menuAjustes,darDeBajaUsuario
from ManejoDeDatos.Usuarios.altaUsuario import altaUsuario, inicializarUsuariosFake
from Logs.logs import log


def menuPrincipal(usuario):
    print("-----------------------------------------------------")
    tipoUsuarioEncontrado = tipoUsuario(usuario)
    print(f"Tipo de usuario: {tipoUsuarioEncontrado}")
    if tipoUsuarioEncontrado == "Administrator":
        print("Menú Principal - Rol: Administrador")
        print("Elija una opción:\n1- Baja de usuario\n2- Cambiar rol de usuario\n3- Procesar flashcards\n4- Generar reporte\n5- Ajustes\n0- Salir\n")
    else:
        print("Menú Principal - Rol: Estudiante")
        print("Elija una opción:\n1- Anotarse a materias\n2- Estado 'Pack de 5 materias'\n3- Cargar nota de materia\n4- Dar de baja una materia\n5- Ver calendario\n6- Ver notas\n7- Ver promedio de carrera\n8- Practicar con Flashcards\n9- Ajustes\n0- Salir\n")
    print("-----------------------------------------------------")

def menuInicial(usuario):
    dias=("Lunes", "Martes", "Miercoles", "Jueves", "Viernes")
    cierraSesion = False
    try:
        usuarioActual = getUsuarioPorNombreUsuario(usuario)
        tipoUsuarioEncontrado = tipoUsuario(usuario)
        while True:
            menuPrincipal(usuario)
            opcionElegida = int(input(f"{usuario}: "))
            while estaDentroDelRango(0,9,opcionElegida) == False:
                print("Opción inválida. Por favor, elija una opción válida.")
                opcionElegida = int(input(f"{usuario}: "))

        #INSCRIPCION A MATERIA
            if opcionElegida == 1 and tipoUsuarioEncontrado == "User":
                anioElegido = eleccionDeMateriaAnio(usuario)
                cuatrimestreElegido = eleccionDeMateriaCuatrimestre(usuario)
                materiasDisponibles = mostrarMateriasDisponibles(anioElegido,cuatrimestreElegido,usuarioActual)
                if len(materiasDisponibles)==0:
                    print("No hay materias disponibles para inscribirse en este año y cuatrimestre.")
                    log("menuInicial", "INFO", f"Usuario {usuario} no tiene materias disponibles para inscribirse en el año {anioElegido} y cuatrimestre {cuatrimestreElegido}.")
                    continue
                print(f"Ingrese el numero de la materia que desea inscribirse (1 a  {len(materiasDisponibles)}):")
                materiaElegida = int(input(f"{usuario}: "))
                log("menuInicial", "INFO", f"Usuario {usuario} eligió la materia número {materiaElegida} para inscribirse.")
                while estaDentroDelRango(1, len(materiasDisponibles), materiaElegida)==False:
                    print(f"Numero inválido. Por favor, ingrese un numero entre 1 y {len(materiasDisponibles)}).")
                    print(f"Ingrese el numero de la materia que desea inscribirse (1 a {len(materiasDisponibles)}):")
                    materiaElegida = int(input(f"{usuario}: "))
                inscribirseAMateria(materiasDisponibles[materiaElegida-1], usuarioActual)
                
            elif opcionElegida == 1 and tipoUsuarioEncontrado == "Administrator":
                print("Ingrese el nombre de usuario que desea dar de baja: ")
                usuarioABorrar = input(f"{usuario}: ").strip().lower()
                resultadoBaja = darDeBajaUsuario(usuarioABorrar)
                if resultadoBaja:
                    print(f"El usuario {usuarioABorrar} ha sido dado de baja del sistema.")
                else:
                    print("No se pudo dar de baja al usuario. Verifique que el nombre de usuario sea correcto.")
                

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
                
            elif opcionElegida == 2 and tipoUsuarioEncontrado == "Administrator":
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
                

        #CARGA DE NOTAS
            if opcionElegida == 3 and tipoUsuarioEncontrado == "User":
                print("Ingrese el numero del dia de la materia que desea cargar la nota:")
                verCalendario(usuarioActual)
                diaIngresado = int(input(f"{usuario}: "))
                materia = buscarMateriaPorIndice(usuarioActual["calendario"][dias[diaIngresado-1]])
                log("menuInicial", "INFO", f"Usuario {usuario} eligió el día {diaIngresado} para cargar la nota.")
                if usuarioActual["calendario"][dias[diaIngresado-1]] is not None:
                    cargarNotas(usuarioActual,materia,diaIngresado)
                else:
                    print("No hay materia asignada a ese día. Volviendo al menú principal.")
                    log("menuInicial", "INFO", f"Usuario {usuario} intentó cargar nota en un día sin materia asignada. Volviendo al menú principal.")
            
            elif opcionElegida == 3 and tipoUsuarioEncontrado == "Administrator":
                aprobarFlashcards(usuario)                
        
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
                        
                    else:
                        darDeBajaMateria(usuarioActual, diaIngresado)                    
                        
                else:
                    print("No hay materia asignada para ese día. Volviendo al menú principal.")
                    
            elif opcionElegida == 4 and tipoUsuarioEncontrado == "Administrator":                
                print("Seleccione el reporte que desea generar:\n1- Reporte de usuarios\n2- Reporte de materias\n3- Reporte de flashcards\n")
                opcionElegida = int(input(f"{usuario}: "))
                while estaDentroDelRango(1,3,opcionElegida) == False:
                    print("Opción inválida. Por favor, elija una opción válida.")
                    print("Seleccione el reporte que desea generar:\n1- Reporte de usuarios\n2- Reporte de materias\n3- Reporte de flashcards\n")
                    opcionElegida = int(input(f"{usuario}: "))
                seGeneroReporte = generarReporte(opcionElegida)
                if seGeneroReporte:
                    print("Reporte generado exitosamente.")
                else:
                    print("Opción de reporte inválida.")
        # VER CALENDARIO
            if opcionElegida == 5 and tipoUsuarioEncontrado == "User":
                verCalendario(usuarioActual)

        # VER NOTAS

            if opcionElegida == 6 and tipoUsuarioEncontrado == "User":
                anioElegido = eleccionDeMateriaAnio(usuario)
                cuatrimestreElegido = eleccionDeMateriaCuatrimestre(usuario)
                materiasDisponibles = mostrarMateriasDisponibles(anioElegido,cuatrimestreElegido,usuarioActual, True)
                print(f"Ingrese el numero de la materia de la que desea ver sus notas (1 a  {len(materiasDisponibles)}, 0 para volver atrás) :")
                materiaElegida = int(input(f"{usuario}: "))
                while estaDentroDelRango(0, len(materiasDisponibles), materiaElegida)==False:
                    if materiaElegida==0:
                        menuPrincipal(usuario)
                    print(f"Numero inválido. Por favor, ingrese un numero entre 1 y {len(materiasDisponibles)}).")
                    print(f"Ingrese el numero de la materia de la que desea ver sus notas (1 a {len(materiasDisponibles)}):")
                    materiaElegida = int(input(f"{usuario}: "))
                materia= buscarMateriaPorIndice(materiasDisponibles[materiaElegida-1])
                verNotas(usuarioActual, materia)
        
        #VER PROMEDIO CURSADA
            if opcionElegida == 7 and tipoUsuarioEncontrado == "User":
                print("Notas")
                #promedioCursada(notaFinal)
            elif opcionElegida == 7 and tipoUsuarioEncontrado == "Administrator":
                print("Funcionalidad de 'Procesar flashcards' para Administradores no implementada aún.")

        #VER OPCIONES FLASHCARDS  
            if opcionElegida == 8 and tipoUsuarioEncontrado == "User":
                    opcionDelMenuFlashcads = ""
                    while True:
                        try:
                            print("=" * 35)
                            print("      🎯 MENÚ DE FLASHCARDS 🎯")
                            print("=" * 35)
                            print("│ 1. Elegir Materia para continuar     │")
                            print("│ 2. Más Información                   │")
                            print("│ 3. Salir                             │")
                            print("-" * 35)
                            opcion=int(input(f"{usuario}: "))
                            if estaDentroDelRango(1,3,opcion)==False:
                                raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
                            if opcion==1:
                                print(f"A continuacion, por favor elija para que materia para {opcionDelMenuFlashcads.lower()}:")
                                anioElegido = eleccionDeMateriaAnio(usuario)
                                cuatrimestreElegido = eleccionDeMateriaCuatrimestre(usuario)
                                materiasDisponibles = mostrarMateriasDisponibles(anioElegido,cuatrimestreElegido,usuarioActual,mostrarTodas=True)
                                print(f"Ingrese el numero de la materia a la que corresponde la flashcard (1 a  {len(materiasDisponibles)}):")
                                Materia = int(input(f"{usuario}: "))
                                while estaDentroDelRango(1, len(materiasDisponibles), Materia)==False:
                                    print(f"Numero inválido. Por favor, ingrese un numero entre 1 y {len(materiasDisponibles)}).")
                                    print(f"Ingrese el numero de la materia a la que corresponde la flashcard (1 a {len(materiasDisponibles)}):")
                                    Materia = int(input(f"{usuario}: "))
                                idMateria=materiasDisponibles[Materia-1]
                                print("=" * 35)
                                print("      🎯 MENÚ DE FLASHCARDS 🎯")
                                print("=" * 35)
                                print("│ 1. Estudiar Flashcards               │")
                                print("│ 2. Proponer Flashcards               │")
                                print("│ 3. Salir                             │")
                                print("-" * 35)
                                opcion=int(input(f"{usuario}: "))
                                if estaDentroDelRango(1,3,opcion)==False:
                                    raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
                                if opcion==1:
                                    estudiarFlashcard(idMateria,usuario)
                                elif opcion==2:
                                    guardarFlashcard(ProponerFlashcard(usuario,idMateria),usuario)
                                    print(">>Flashcard propuesta exitosamente<<")
                                else:
                                    break
                            elif opcion==2:
                                masInfo()
                            else:
                                break
                        except ValueError:
                            print("El valor ingresado no es correcto,intente nuevamente")
                    menuPrincipal(usuario)
            elif opcionElegida == 8 and tipoUsuarioEncontrado == "Administrator":
                print("Funcionalidad de 'Menu Flashcards' para Administradores no implementada aún.")
        
        #AJUSTES DE LA CUENTA (CAMBIO DE CONTRASEÑA Y CERRAR SESION)
            if opcionElegida == 9 and tipoUsuarioEncontrado == "User" or opcionElegida == 5 and tipoUsuarioEncontrado == "Administrator":
                cierraSesion = menuAjustes(usuario)
                if cierraSesion:
                    print("Cerrando sesión.\n-----------------------------------------------------")
                    break
            if opcionElegida == 0:
                break       

        if cierraSesion == True:
            menuLoginPrincipal()
        else:
            print("Gracias por usar el sistema. ¡Hasta luego!")
            
    except ValueError as e:
        print(f"Error: {e}")
        log("menuInicial", "ERROR", f"Error en el menú inicial para el usuario {usuario}: {e}")
        menuInicial(usuario)

def menuLoginPrincipal():
    try:
        #inicializarUsuariosFake()
        print("Bienvenido al sistema de gestión académica.\nPor favor, elija una de las siguientes opciones: \n1-Iniciar sesión\n2-Crear usuario\n3-Salir")
        opcionElegida = int(input("Opción: "))
        if opcionElegida is None or opcionElegida == "" or opcionElegida not in [1,2,3]:
            raise ValueError("Opción inválida.")
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
    except ValueError as e:
        print("Opción inválida, ingrese un número correspondiente a las opciones.")
        print(f"Error: {e}")
        menuLoginPrincipal()
        return
    else:
        print(f"Acceso concedido. Bienvenido {usuario}.")
        log("main", "INFO", f"Usuario {usuario} ha iniciado sesión correctamente.")
        menuInicial(usuario)
        
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
    menuLoginPrincipal()
        
if __name__ == "__main__":
    main()