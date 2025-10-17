def validarNombreUsuarioEnSistema(usuario):
    try:
        datosEncontrados = None
        with open('ETAPA2/Archivos/usuarios.csv', 'r') as usuarios:
            usuarios_lineas = usuarios.readlines()
            for linea in usuarios_lineas[1:]:
                datos = linea.strip().split(',')
                if len(datos) >= 2:
                    usuario_archivo = datos[0].strip()
                    if usuario == usuario_archivo:
                        datosEncontrados = datos
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
    try:
        datos = validarNombreUsuarioEnSistema(usuario)
        if datos is not None:
            contrasena_archivo = datos[1].strip()
            if contrasena == contrasena_archivo:
                usuario = datos[0].strip()
        return usuario
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
        return validacion
    except Exception as e:
        print(f"Error: {e}")
        return None 