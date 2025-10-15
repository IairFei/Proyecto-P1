
def validarLogin(usuario, contrasena):
    try:
        with open("ETAPA1/Archivos/usuarios.csv", mode="r") as archivo:
            lineas = archivo.readlines()
            for linea in lineas[1:]:
                datos = linea.strip().split(',')
                if len(datos) >= 2:
                    usuario_archivo, contrasena_archivo = datos[0].strip(), datos[1].strip()
                    if usuario == usuario_archivo and contrasena == contrasena_archivo:
                        return usuario
            return None
    except FileNotFoundError as file_error:
        print(f"Error: {file_error}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
        


def login():
    try:
        print("Ingrese su nombre de usuario:")
        usuario = input("Usuario: ")
        while usuario is None or usuario.strip() == "":
            print("El nombre de usuario no puede estar vacío. Por favor, ingréselo nuevamente.")
            usuario = input("Usuario: ")                
        print("Ingrese su contraseña:")
        contrasena = input("Contraseña: ")
        while contrasena is None or contrasena.strip() == "":
            print("La contraseña no puede estar vacía. Por favor, ingrésela nuevamente.")
            contrasena = input("Contraseña: ")
        validacion = validarLogin(usuario, contrasena)
        return validacion
    except Exception as e:
        print(f"Error: {e}")
    