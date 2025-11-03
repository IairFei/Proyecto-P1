import json
from Logs.logs import log
from ..validacionDeDatos import verificarSeguridadContrasena, validarEntero
from Logs.logs import log

def cambiarRol(nuevoRol, usuario):
    seModficoEnCSV = False
    datos = []
    try:
        with open('ETAPA2/Archivos/usuarios.csv', 'r') as usuarios:
            for linea in usuarios:
                datos.append(linea.strip().split(','))
        for dato in datos:
            if dato[0].strip() == usuario[0].strip():
                dato[2] = nuevoRol
        with open('ETAPA2/Archivos/usuarios.csv', 'w') as usuarios:
            for dato in datos:
                usuarios.write(','.join(dato) + '\n')
        seModficoEnCSV = True
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")
        log("cambiarRol", "ERROR", f"Se produjo un error al cambiar el rol del usuario {usuario[0]} en el sistema.")
    return seModficoEnCSV

def obtenerCantidadUsuarios():
    try:
        contador = 0
        with open('ETAPA2/Archivos/usuarios.csv', 'r') as usuarios:
            for linea in usuarios:
                contador += 1
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")
        contador = -1
    else:
        return contador

def obtenerUsuarioPorRol(rol):
    try:
        usuarios_encontrados = []
        with open('ETAPA2/Archivos/usuarios.csv', 'r') as usuarios:
            for linea in usuarios:
                datos = linea.strip().split(',')
                if datos[2].strip().lower() == rol.strip().lower():
                    usuarios_encontrados.append(datos[0].strip())
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")
        log("obtenerUsuarioPorRol", "ERROR", f"Se produjo un error al obtener usuarios con el rol {rol}.")
    return usuarios_encontrados
    
def validarNombreUsuarioEnSistema(usuario):
    try:
        datosEncontrados = None
        with open('ETAPA2/Archivos/usuarios.csv', 'r') as usuarios:
            for linea in usuarios:
                datos = linea.strip().split(',')
                if datos[0].strip() == usuario:
                    datosEncontrados = datos
                    break
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")
    return datosEncontrados

def validarContrasena(usuario,contrasena):
    try:
        datosEncontrados = None
        with open('ETAPA2/Archivos/usuarios.csv', 'r') as usuarios:
            for linea in usuarios:
                datos = linea.strip().split(',')
                if datos[0].strip() == usuario and datos[1].strip() == contrasena:
                    datosEncontrados = datos
                    break
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")
        log("validarContrasena", "ERROR", f"Se produjo un error al validar la contraseña para el usuario {usuario}.")
    return datosEncontrados

def tipoUsuario(usuario):
    try:
        tipo_usuario_encontrado = None
        datos = validarNombreUsuarioEnSistema(usuario)
        if datos is not None:
            tipo_usuario_encontrado = datos[2].strip()
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")
    return tipo_usuario_encontrado

def crearDiccionarioUsuarioManual(usuario_original):
    notas_copia = {}
    for materia_id, nota_data in usuario_original['notas'].items():
        notas_copia[materia_id] = {
            'parcial1': nota_data['parcial1'],
            'parcial2': nota_data['parcial2'],
            'final': nota_data['final'],
            'nota_final': nota_data['nota_final'],
            'aprobada': nota_data['aprobada'],
            'recursa': nota_data['recursa']
        }

    calendario_copia = {
        'Lunes': usuario_original['calendario']['Lunes'],
        'Martes': usuario_original['calendario']['Martes'],
        'Miercoles': usuario_original['calendario']['Miercoles'],
        'Jueves': usuario_original['calendario']['Jueves'],
        'Viernes': usuario_original['calendario']['Viernes']
    }
    
    usuario_copia = {
        'id': usuario_original['id'],
        'usuario': usuario_original['usuario'],
        'nombre': usuario_original['nombre'],
        'apellido': usuario_original['apellido'],
        'pack5materias': usuario_original['pack5materias'],
        'notas': notas_copia,
        'calendario': calendario_copia
    }
    
    return usuario_copia

def guardarUsuario(usuarioActual):
    """
    Actualiza un usuario específico en el archivo JSON manteniendo los demás usuarios
    """
    usuarioGuardado = False
    try:
        ruta = 'ETAPA2/Archivos/usuarios.json'
        usuario_encontrado = False
        lineas_modificadas = []
        with open(ruta, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                try:
                    usuario = json.loads(linea)
                except Exception:
                    lineas_modificadas.append(linea)
                    continue
                if usuario.get('usuario') == usuarioActual['usuario']:
                    # Actualizar los datos del usuario
                    usuario['id'] = usuarioActual['id']
                    usuario['nombre'] = usuarioActual['nombre']
                    usuario['apellido'] = usuarioActual['apellido']
                    usuario['pack5materias'] = usuarioActual['pack5materias']
                    usuario['notas'] = {}
                    for materia_id, nota_data in usuarioActual['notas'].items():
                        usuario['notas'][materia_id] = {
                            'parcial1': nota_data['parcial1'],
                            'parcial2': nota_data['parcial2'],
                            'final': nota_data['final'],
                            'nota_final': nota_data['nota_final'],
                            'aprobada': nota_data['aprobada'],
                            'recursa': nota_data['recursa']
                        }
                    usuario['calendario'] = {
                        'Lunes': usuarioActual['calendario']['Lunes'],
                        'Martes': usuarioActual['calendario']['Martes'],
                        'Miercoles': usuarioActual['calendario']['Miercoles'],
                        'Jueves': usuarioActual['calendario']['Jueves'],
                        'Viernes': usuarioActual['calendario']['Viernes']
                    }
                    lineas_modificadas.append(json.dumps(usuario, ensure_ascii=False) + '\n')
                    usuario_encontrado = True
                else:
                    lineas_modificadas.append(linea if linea.endswith('\n') else linea + '\n')
        if usuario_encontrado:
            with open(ruta, 'w', encoding='utf-8') as archivo:
                archivo.writelines(lineas_modificadas)
            log("guardarUsuario","INFO",f"Usuario {usuarioActual['usuario']} guardado correctamente.")
            usuarioGuardado = True
        else:
            print(f"Error: Usuario {usuarioActual['usuario']} no encontrado en el archivo")
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")
        log("guardarUsuario","ERROR","Se produjo un error al guardar el usuario.")
    return usuarioGuardado

def getUsuarioPorNombreUsuario(nombreUsuario):
    try:
        datosEncontrados = None
        with open('ETAPA2/Archivos/usuarios.json', 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                try:
                    usuario = json.loads(linea)
                except Exception:
                    continue
                if usuario.get('usuario') == nombreUsuario:
                    datosEncontrados = crearDiccionarioUsuarioManual(usuario)
                    break
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")
        log("getUsuarioPorNombreUsuario","ERROR",f"Se produjo un error al obtener el usuario {nombreUsuario}.")
    return datosEncontrados

def validarLogin(usuario, contrasena):
    concidencia = False
    try:
        datos = validarNombreUsuarioEnSistema(usuario)
        if datos is not None:
            contrasena_archivo = datos[1].strip()
            if contrasena == contrasena_archivo:
                concidencia = True
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")
        log("validarLogin","ERROR",f"Se produjo un error al validar el login para el usuario {usuario}.")
    return concidencia

def login():
    validacion = None
    try:
        print("Ingrese su nombre de usuario:")
        usuario = input("Usuario: ").strip().lower()
        log("login", "INFO", f"Intento de login para el usuario: {usuario}")
        while usuario is None or usuario == "":
            print("El nombre de usuario no puede estar vacío. Por favor, ingréselo nuevamente.")
            log("login", "WARNING", "Nombre de usuario vacío en intento de login.")
            usuario = input("Usuario: ").strip().lower()
            log("login", "INFO", f"Nuevo intento de login para el usuario: {usuario}")                
        print("Ingrese su contraseña:")
        contrasena = input("Contraseña: ").strip()
        log("login", "INFO", f"Intento de login para el usuario: {usuario} con contraseña proporcionada.")
        while contrasena is None or contrasena == "":
            log("login", "WARNING", f"Contraseña vacía en intento de login para el usuario: {usuario}.")
            print("La contraseña no puede estar vacía. Por favor, ingrésela nuevamente.")
            contrasena = input("Contraseña: ").strip()
            log("login", "INFO", f"Nuevo intento de login para el usuario: {usuario} con contraseña proporcionada.")
        validacion = validarLogin(usuario, contrasena)
        if validacion:
            print("Inicio de sesión exitoso.")
        else:
            print("Nombre de usuario o contraseña incorrectos.")
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")
        log("login","ERROR","Se produjo un error al intentar iniciar sesión.")
    return validacion, usuario

def cambioContrasena(usuario):
    try:
        print("-----------------------------------------------------")
        intentos = 3
        log("ajusteUsuario", "INFO", "Iniciando proceso de cambio contraseña.")
        exContrasena = input("Ingrese su contraseña actual: ").strip()
        while intentos != 0:
            intentos -= 1
            if validarContrasena(usuario,exContrasena) == None:
                log("ajusteUsuario", "WARNING", f"Contraseña antigua incorrecta, quedan {intentos} intento/s.")
                print(f"Contraseña incorrecta, le quedan {intentos} intento/s ")
                exContrasena = input("Ingrese su contraseña actual: ").strip()
            else:
                break
        log("ajusteUsuario", "INFO", "Contraseña antigua correcta.") 
        while True:
            contrasenaNueva = input("Ingrese su nueva contraseña: ")
            status =  verificarSeguridadContrasena(contrasenaNueva)
            print(status[0])
            if status[1] == True:    
                log("ajusteUsuario", "INFO", f"Contraseña para el usuario {usuario} cumple con los requisitos de seguridad.")
                break
        status = contrasenaActualizada(usuario,exContrasena,contrasenaNueva)
        if status == True:   
            print("Contraseña actualizada.\nVolviendo al Menu")
            log("ajusteUsuario", "INFO", f"Se actualizo la contraseña del usuario: {usuario}.")
            print("-----------------------------------------------------")
        else:
            print("Ocurrio un error mientras se actualizaba la contraseña.")
            log("ajusteUsuario", "WARNING", f"Se actualizo la contraseña del usuario: {usuario}.")
        return None
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")

def contrasenaActualizada(usuario,exContrasena,contrasenaNueva):
    try:
        seActualizoLaContrasena = False
        with open('ETAPA2/Archivos/usuarios.csv', 'r') as archivo:
            datos = []
            for lineas in archivo:
                datos.append(lineas)
                linea = lineas.strip().split(",")
                if linea[0] == usuario and linea[1] == exContrasena:
                    newLine = linea[0] + "," + contrasenaNueva + "," + linea[2] +"\n"
                    datos.pop()
                    datos.append(newLine)
        with open('ETAPA2/Archivos/usuarios.csv', 'wt') as archivo:
            for dato in datos:
                archivo.write(dato)
        seActualizoLaContrasena = True
        log("contrasenaActualizada", "INFO", f"Contraseña del usuario {usuario} actualizada correctamente.")
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")
    return seActualizoLaContrasena

def menuAjustes(usuario):
    cierraSesion = False
    print("Ingrese el numero de la opcion a elegir.")
    print("OPCIONES:")
    print("1- Cambiar contraseña\n2- Cerrar Sesión\n0- Salir\n")
    opcion = validarEntero(0,2)
    if opcion==1:
        cambioContrasena(usuario) 
    elif opcion == 2:
        cierraSesion = True
    return cierraSesion

def darDeBajaUsuario(usuario):
    try:
        seDioDeBaja = False
        datos = []
        usuario_encontrado = False
        with open('ETAPA2/Archivos/usuarios.csv', 'r') as archivo:
            for linea in archivo:
                datos.append(linea)
                linea_datos = linea.strip().split(",")
                if linea_datos[0] == usuario:
                    datos.pop()
                    usuario_encontrado = True
        if usuario_encontrado:
            with open('ETAPA2/Archivos/usuarios.csv', 'wt') as archivo:
                for dato in datos:
                    archivo.write(dato)
            with open('ETAPA2/Archivos/usuarios.json', 'r', encoding='utf-8') as archivo:
                lineas_modificadas = []
                for linea in archivo:
                    usuario_json = json.loads(linea)
                    if usuario_json.get('usuario') == usuario:
                        continue
                    lineas_modificadas.append(linea)
            with open('ETAPA2/Archivos/usuarios.json', 'w', encoding='utf-8') as archivo:
                archivo.writelines(lineas_modificadas)
            seDioDeBaja = True
        else:
            print(f"Error: Usuario {usuario} no encontrado en el archivo")
        log("darDeBajaUsuario", "INFO", f"Usuario {usuario} dado de baja correctamente del sistema.")
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")
        log("darDeBajaUsuario", "ERROR", f"Se produjo un error al dar de baja al usuario {usuario} del sistema.")
    return seDioDeBaja
    
def crearUsuariosCsv():
    try:
        with open('ETAPA2/Archivos/usuarios.csv', 'r') as archivo:
            pass
    except (FileNotFoundError, IOError, OSError):
        with open('ETAPA2/Archivos/usuarios.csv', 'w', encoding='utf-8') as archivo:
            archivo.write("Usuario,Contraseña,Role\n")
            archivo.write("admin,admin,Administrator\n")
    
def crearUsuariosJson():
    try:
        with open('ETAPA2/Archivos/usuarios.json', 'r', encoding='utf-8') as archivo:
            pass
    except (FileNotFoundError, IOError, OSError):
        with open('ETAPA2/Archivos/usuarios.json', 'w', encoding='utf-8') as archivo:
            pass
