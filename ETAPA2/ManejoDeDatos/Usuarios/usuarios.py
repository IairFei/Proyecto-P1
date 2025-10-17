import json


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
        return seModficoEnCSV
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return None

def validarNombreUsuarioEnSistema(usuario):
    try:
        datosEncontrados = None
        with open('ETAPA2/Archivos/usuarios.csv', 'r') as usuarios:
            for linea in usuarios:
                datos = linea.strip().split(',')
                if datos[0].strip() == usuario:
                    datosEncontrados = datos
                    break
        return datosEncontrados
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return None

def tipoUsuario(usuario):
    try:
        tipo_usuario_encontrado = None
        datos = validarNombreUsuarioEnSistema(usuario)
        if datos is not None:
            tipo_usuario_encontrado = datos[2].strip()
        return tipo_usuario_encontrado
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return None

def validarLogin(usuario, contrasena):
    concidencia = False
    try:
        datos = validarNombreUsuarioEnSistema(usuario)
        if datos is not None:
            contrasena_archivo = datos[1].strip()
            if contrasena == contrasena_archivo:
                concidencia = True
        return concidencia
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return None
        
        
def login():
    validacion = None
    try:
        print("Ingrese su nombre de usuario:")
        usuario = input("Usuario: ").strip().lower()
        while usuario is None or usuario == "":
            print("El nombre de usuario no puede estar vacío. Por favor, ingréselo nuevamente.")
            usuario = input("Usuario: ").strip().lower()                
        print("Ingrese su contraseña:")
        contrasena = input("Contraseña: ").strip()
        while contrasena is None or contrasena == "":
            print("La contraseña no puede estar vacía. Por favor, ingrésela nuevamente.")
            contrasena = input("Contraseña: ").strip()
        validacion = validarLogin(usuario, contrasena)
        if validacion:
            print("Inicio de sesión exitoso.")
        else:
            print("Nombre de usuario o contraseña incorrectos.")
        return validacion, usuario
    except Exception as e:
        print(f"Error: {e}")
        return None 