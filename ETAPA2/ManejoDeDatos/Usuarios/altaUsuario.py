def altaEnSistema(usuario, nombreAlumno, apellidoAlumno):
    try:
        with open('ETAPA2/Archivos/usuarios.json', 'a') as archivo:
            print(archivo)
            #archivo.write(f"{usuario},{nombreAlumno},{apellidoAlumno}\n")
    except Exception as e: 
        print(f"Error: {e}")
        return None

def altaUsuario():
    try:
        with open('ETAPA2/Archivos/usuarios.csv', 'a') as archivo:
            nombreAlumno = input("Ingrese el nombre del alumno: ").strip()
            apellidoAlumno = input("Ingrese el apellido del alumno: ").strip()
            print("Ingrese los datos del nuevo usuario:")
            usuario = nombreAlumno[0].lower() + apellidoAlumno.lower()
            contrasena = input("Ingrese la contraseña: ").strip()
            tipo_usuario = int(input("Ingrese el tipo de usuario (1- Administrator/2- Standard): "))
            if tipo_usuario == 1:
                tipo_usuario = "Administrator"
            else:
                tipo_usuario = "User"
            print(f"Usuario: {usuario}, Contraseña: {contrasena}, Tipo de usuario: {tipo_usuario}")
            archivo.writelines(f"{usuario},{contrasena},{tipo_usuario}\n")
            #dadoDeAlta = altaEnSistema(usuario,nombreAlumno,apellidoAlumno)
            return usuario
    except Exception as e:
        print(f"Error: {e}")
        return None