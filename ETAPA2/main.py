from ManejoDeDatos.validacionDeDatos import eleccionDeMateriaAnio, eleccionDeMateriaCuatrimestre, validarTexto, validarEntero
from Entidades.calendario import verCalendario, inscribirseAMateria, darDeBajaMateria
from Entidades.materias import crearArchivoMaterias, verNotas, buscarMateriaPorIndice, mostrarMateriasDisponibles, promedioCursada, obtenerMateriasPackDe5, estadoPackDe5Materias, cargarNotas
from Entidades.flashcards import aprobarFlashcards, menuFlashcards
from ManejoDeDatos.Usuarios.usuarios import crearUsuariosCsv, crearUsuariosJson, login, tipoUsuario, cambiarRol, validarNombreUsuarioEnSistema, getUsuarioPorNombreUsuario, menuAjustes, darDeBajaUsuario
from ManejoDeDatos.Usuarios.altaUsuario import altaUsuario, inicializarUsuariosFake
from ManejoDeArchivos.archivosSalida import generarReporte
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
    usuarioActual = getUsuarioPorNombreUsuario(usuario)
    tipoUsuarioEncontrado = tipoUsuario(usuario)
    while True:
        menuPrincipal(usuario)
        opcionElegida = validarEntero(0,9)

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
            materiaElegida = validarEntero(1,len(materiasDisponibles))
            log("menuInicial", "INFO", f"Usuario {usuario} eligió la materia número {materiaElegida} para inscribirse.")
            inscribirseAMateria(materiasDisponibles[materiaElegida-1], usuarioActual)
            verCalendario(usuarioActual)
    #DAR DE BAJA USUARIO (ADMIN)
        elif opcionElegida == 1 and tipoUsuarioEncontrado == "Administrator":
            print("Ingrese el nombre de usuario que desea dar de baja: ")
            usuarioABorrar = input(f"{usuario}: ").strip().lower()
            resultadoBaja = darDeBajaUsuario(usuarioABorrar)
            if resultadoBaja:
                print(f"El usuario {usuarioABorrar} ha sido dado de baja del sistema.")
            else:
                print("No se pudo dar de baja al usuario. Verifique que el nombre de usuario sea correcto.")

    #PACK DE 5 MATERIAS
        elif opcionElegida == 2 and tipoUsuarioEncontrado == "User":
            estado = estadoPackDe5Materias(usuarioActual)
            log("menuInicial", "INFO", f"Usuario {usuario} consultó el estado del 'Pack de 5 materias': {estado}.")
            if estado == True:
                print("Cumple con las condiciones para el 'Pack de 5 materias'.")
                print("¿Querés que te anotemos en las próximas 5 materias siguiendo el plan de estudios? (s/n): ")
                respuesta = validarTexto(("s","si","n","no"))
                log("menuInicial", "INFO", f"Usuario {usuario} respondió '{respuesta}' a la inscripción al 'Pack de 5 materias'.")
                if respuesta == 'n' or respuesta == 'no':
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
            
    #CAMBIAR ROL A USUARIO
        elif opcionElegida == 2 and tipoUsuarioEncontrado == "Administrator":
            usuarioACambiar= input("Ingrese el nombre de usuario al que desea cambiar el rol: ").strip().lower()
            usuarioACambiar = validarNombreUsuarioEnSistema(usuarioACambiar)
            while usuarioACambiar is None:
                print("El usuario ingresado no existe. Por favor, ingrese un usuario válido.")
                usuarioACambiar = input("Ingrese el nombre de usuario al que desea cambiar el rol: ").strip().lower()
                usuarioACambiar = validarNombreUsuarioEnSistema(usuarioACambiar)
            print("Ingrese el nuevo rol para el usuario (1- User/2-Administrator): ")
            nuevoRol = validarEntero(1,2)
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
        elif opcionElegida == 3 and tipoUsuarioEncontrado == "User":
            print("Ingrese el numero del dia de la materia que desea cargar la nota:")
            verCalendario(usuarioActual)
            diaIngresado = validarEntero(1,5)
            materia = buscarMateriaPorIndice(usuarioActual["calendario"][dias[diaIngresado-1]])
            log("menuInicial", "INFO", f"Usuario {usuario} eligió el día {diaIngresado} para cargar la nota.")
            if usuarioActual["calendario"][dias[diaIngresado-1]] is not None:
                cargarNotas(usuarioActual,materia,diaIngresado)
            else:
                print("No hay materia asignada a ese día. Volviendo al menú principal.")
                log("menuInicial", "INFO", f"Usuario {usuario} intentó cargar nota en un día sin materia asignada. Volviendo al menú principal.")

    #APROBAR FLASHCARDS
        elif opcionElegida == 3 and tipoUsuarioEncontrado == "Administrator":
            aprobarFlashcards(usuario)                

    #DAR DE BAJA
        elif opcionElegida == 4 and tipoUsuarioEncontrado == "User":
            print("Ingrese el numero del dia de la materia que desea dar de baja:")
            verCalendario(usuarioActual)
            diaIngresado = int(input(f"{usuario}: "))
            if usuarioActual["calendario"][dias[diaIngresado-1]] is not None:
                materia = buscarMateriaPorIndice(usuarioActual["calendario"][dias[diaIngresado-1]])
                print(f"¿Desea dar de baja la materia {materia['nombre']}? (s/n): ")
                respuesta = validarTexto(("s","si","n","no"))
                if respuesta == 'n' or respuesta == 'no':
                    print("Operacion cancelada. Volviendo al menú principal.")
                else:
                    darDeBajaMateria(usuarioActual, diaIngresado)                    
            else:
                print("No hay materia asignada para ese día. Volviendo al menú principal.")

    #GENERAR REPORTE
        elif opcionElegida == 4 and tipoUsuarioEncontrado == "Administrator":                
                print("Seleccione el reporte que desea generar:\n1- Reporte de materias\n2- Reporte de pack5materias\n3- Report de mejores flashcards\n4- Report de materias con mas flashcards\n5- Reporte de usuarios\n0- Volver al menu")
                opcionElegida = validarEntero(0,5)
                seGeneroReporte = generarReporte(opcionElegida)
                if seGeneroReporte== "salir":
                    print("Volviendo a Menu.")
                elif seGeneroReporte :
                    print("Reporte generado exitosamente.")
                else:
                    print("Opción de reporte inválida.")

    # VER CALENDARIO
        elif opcionElegida == 5 and tipoUsuarioEncontrado == "User":
            verCalendario(usuarioActual)

    # VER NOTAS
        elif opcionElegida == 6 and tipoUsuarioEncontrado == "User":
            anioElegido = eleccionDeMateriaAnio(usuario)
            cuatrimestreElegido = eleccionDeMateriaCuatrimestre(usuario)
            materiasDisponibles = mostrarMateriasDisponibles(anioElegido,cuatrimestreElegido,usuarioActual, True)
            print(f"Ingrese el numero de la materia de la que desea ver sus notas (1 a  {len(materiasDisponibles)}, 0 para volver atrás) :")
            materiaElegida = validarEntero(0,len(materiasDisponibles))
            if materiaElegida==0:
                menuPrincipal(usuario)
            else:
                materia= buscarMateriaPorIndice(materiasDisponibles[materiaElegida-1])
                verNotas(usuarioActual, materia)

    #VER PROMEDIO CURSADA
        elif opcionElegida == 7 and tipoUsuarioEncontrado == "User":
            promedioCursada(usuarioActual)

    #VER OPCIONES FLASHCARDS  
        elif opcionElegida == 8 and tipoUsuarioEncontrado == "User":
            menuFlashcards(usuarioActual)
            menuPrincipal(usuario)

    #AJUSTES DE LA CUENTA (CAMBIO DE CONTRASEÑA Y CERRAR SESION)
        elif opcionElegida == 9 and tipoUsuarioEncontrado == "User" or opcionElegida == 5 and tipoUsuarioEncontrado == "Administrator":
            cierraSesion = menuAjustes(usuario)
            if cierraSesion:
                print("Cerrando sesión.\n-----------------------------------------------------")
                break
        else:
            break       
    if cierraSesion == True:
        menuLoginPrincipal()
    else:
        print("Gracias por usar el sistema. ¡Hasta luego!")

def menuLoginPrincipal():
    #inicializarUsuariosFake()
    print("Bienvenido al sistema de gestión académica.\nPor favor, elija una de las siguientes opciones: \n1-Iniciar sesión\n2-Crear usuario\n3-Salir")
    opcionElegida = validarEntero(1,3)
    log("main", "INFO", f"Opción elegida en el menú de login: {opcionElegida}")
    inicioDeSesionExitoso, usuario = menuLogin(opcionElegida)
    if usuario is None or inicioDeSesionExitoso is False:
        print("Inicio de sesión fallido. Saliendo del programa.")
        log("main", "INFO", "Inicio de sesión fallido.")
        return
    print(f"Acceso concedido. Bienvenido {usuario}.")
    log("main", "INFO", f"Usuario {usuario} ha iniciado sesión correctamente.")
    menuInicial(usuario)

def inicioDeSesion(usuario=None, intentosRestantes=3):
    if usuario is None:
        inicioDeSesionExitoso, usuario = login()
    else:
        inicioDeSesionExitoso = False

    if inicioDeSesionExitoso:
        return inicioDeSesionExitoso, usuario
    else:
        if intentosRestantes > 1:
            log("inicioDeSesion", "WARNING", f"Intento fallido de inicio de sesión para el usuario {usuario}. Intentos restantes: {intentosRestantes-1}.")
            print("Acceso denegado. Inténtelo de nuevo.")
            print(f"Le quedan {intentosRestantes-1} intentos.")
            return inicioDeSesion(None, intentosRestantes-1)
        else:
            print("Ha agotado todos los intentos. Saliendo del programa.")
            log("inicioDeSesion", "WARNING", f"Usuario {usuario} ha agotado todos los intentos de inicio de sesión.")
            raise SystemExit("Fin del programa por múltiples intentos fallidos de inicio de sesión.")

def menuLogin(opcionElegida):
    inicioDeSesionExitoso = False
    if opcionElegida == 1:
        inicioDeSesionExitoso, usuario = inicioDeSesion()
    elif opcionElegida == 2:
        usuario = altaUsuario()
        print("¿Desea iniciar sesión ahora? (s/n): ")
        inicioSesion = validarTexto(("s","si","n","no"))
        if inicioSesion == 's' or inicioSesion == 'si':
            inicioDeSesionExitoso = True
        else:
            main()
    else:
        print("Saliendo del programa. ¡Hasta luego!")
        raise SystemExit("Fin del programa por elección del usuario.")
    return inicioDeSesionExitoso, usuario

def main():
    crearArchivoMaterias()
    crearUsuariosCsv()
    crearUsuariosJson()
    try:
        menuLoginPrincipal()
    except (KeyboardInterrupt, SystemExit):
        print("\nProceso finalizado por el usuario.")

if __name__ == "__main__":
    main()