import json

#Alta en archivo JSON
def altaEnSistema(usuario, nombreAlumno, apellidoAlumno):
    try:
        with open('ETAPA2/Archivos/usuarios.json', 'r') as users:
            datos_sistema = json.load(users)
            cantidad_usuarios = len(datos_sistema['usuarios'])
            print(cantidad_usuarios)
            cantidad_usuarios+=1
        cantidad_usuarios = {
            "id": f"{cantidad_usuarios}",
            "usuario": f"{usuario}",
            "nombre": f"{nombreAlumno}",
            "apellido": f"{apellidoAlumno}",
            "pack5materias": True,
            "notas": {},
            "calendario": {
                "Lunes": None,
                "Martes": None,
                "Miercoles": None,
                "Jueves": None,
                "Viernes": None
            }
        }
        datos_sistema['usuarios'].append(cantidad_usuarios)
        with open('ETAPA2/Archivos/usuarios.json', 'w') as users:
            json.dump(datos_sistema, users, indent=4)
        return True
        
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
            dadoDeAlta = altaEnSistema(usuario,nombreAlumno,apellidoAlumno)
            if dadoDeAlta == False or dadoDeAlta is None:
                print("No se pudo dar de alta al usuario en el sistema.")
                archivo.detach
                usuario = None
            return usuario
    except Exception as e:
        print(f"Error: {e}")
        return None