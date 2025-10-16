def tipoUsuario(usuario):
    try:
        tipo_usuario_encontrado = None
        with open("ETAPA2/Archivos/usuarios.csv", mode="r") as archivo:
            lineas = archivo.readlines()
            for linea in lineas[1:]:
                datos = linea.strip().split(',')
                if len(datos) >= 2:
                    usuario_archivo, tipo_usuario = datos[0].strip(), datos[2].strip()
                    if usuario == usuario_archivo:
                        tipo_usuario_encontrado = tipo_usuario
        return tipo_usuario_encontrado
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return None


def validarLogin(usuario, contrasena):
    try:
        with open("ETAPA2/Archivos/usuarios.csv", mode="r") as archivo:
            lineas = archivo.readlines()
            for linea in lineas[1:]:
                datos = linea.strip().split(',')
                if len(datos) >= 2:
                    usuario_archivo, contrasena_archivo = datos[0].strip(), datos[1].strip()
                    if usuario == usuario_archivo and contrasena == contrasena_archivo:
                        usuario = usuario_archivo
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