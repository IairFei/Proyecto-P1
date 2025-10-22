import json
from ..validacionDeDatos import verificarSeguridadContraseña
from ManejoDeDatos.Usuarios.usuarios import validarNombreUsuarioEnSistema
from faker import Faker
from Logs.logs import log
#fake = Faker('es_AR')

#Alta en archivo JSON
def nombreUsuarioRepetido(nombreAlumno, apellidoAlumno):
    existeUsuario = "a"
    try:
        contador = 1
        while existeUsuario is not None and len(nombreAlumno) > contador:
            usuario = nombreAlumno[0].lower() + nombreAlumno[contador].lower() + apellidoAlumno.lower()
            contador += 1
            existeUsuario = validarNombreUsuarioEnSistema(usuario)
        if len(nombreAlumno) == contador and existeUsuario is not None:
            sufijo = 1
            while existeUsuario is not None:
                usuario = nombreAlumno.lower() + apellidoAlumno.lower() + str(sufijo)
                sufijo += 1
                existeUsuario = validarNombreUsuarioEnSistema(usuario)
        return usuario
    except Exception as e:
        print(f"Error: {e}")
def altaEnSistema(usuario, nombreAlumno, apellidoAlumno):
    try:
        with open('ETAPA2/Archivos/usuarios.json', 'r') as users:
            datos_sistema = json.load(users)
            cantidad_usuarios = len(datos_sistema['usuarios'])
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
            log("altaUsuario", "INFO", "Iniciando proceso de alta de usuario.")
            nombreAlumno = input("Ingrese el primer nombre del alumno: ").strip()
            log("altaUsuario", "INFO", f"Nombre ingresado para nuevo usuario: {nombreAlumno}.")
            apellidoAlumno = input("Ingrese el apellido del alumno: ").strip()
            log("altaUsuario", "INFO", f"Apellido ingresado para nuevo usuario: {apellidoAlumno}.")
            print("Ingrese los datos del nuevo usuario:")
            usuario = nombreAlumno[0].lower() + apellidoAlumno.lower()
            log("altaUsuario", "INFO", f"Generando nombre de usuario: {usuario}.")
            existeUsuario = validarNombreUsuarioEnSistema(usuario)
            log("altaUsuario", "INFO", f"Verificando existencia de usuario: {usuario}. Resultado: ")
            if existeUsuario is not None:
                log("altaUsuario", "WARNING", f"El usuario {usuario} ya existe. Generando nuevo nombre de usuario.")
                usuario = nombreUsuarioRepetido(nombreAlumno, apellidoAlumno)
                if usuario is None:
                    log("altaUsuario", "INFO", f"Nuevo nombre de usuario generado: {usuario}.")
                    usuario = nombreUsuarioRepetido(nombreAlumno, apellidoAlumno)
            contrasena = input("Ingrese la contraseña: ").strip()
            log("altaUsuario", "INFO", f"Contraseña ingresada para el usuario {usuario}. Verificando seguridad.")
            while True:
                status =  verificarSeguridadContraseña(contrasena)
                if status[1] == True:
                    print(status[0])
                    log("altaUsuario", "INFO", f"Contraseña para el usuario {usuario} cumple con los requisitos de seguridad.")
                    break
                else:
                    print(status[0])
                    log("altaUsuario", "WARNING", f"Contraseña para el usuario {usuario} no cumple con los requisitos de seguridad por el motivo: {status[0]}")
                    contrasena = input("Ingrese la contraseña: ").strip()
                    log("altaUsuario", "INFO", f"Nuevo intento de contraseña ingresada para el usuario {usuario}.")
                    continue
            tipo_usuario = "User"
            log("altaUsuario", "INFO", f"Asignando tipo de usuario '{tipo_usuario}' para el usuario {usuario}.")
            print(f"Usuario: {usuario}, Contraseña: {contrasena}, Tipo de usuario: {tipo_usuario}")
            archivo.writelines(f"{usuario},{contrasena},{tipo_usuario}\n")
            dadoDeAlta = altaEnSistema(usuario,nombreAlumno,apellidoAlumno)
            log("altaUsuario", "INFO", f"Intento de alta en sistema para el usuario {usuario}.")
            if dadoDeAlta == False or dadoDeAlta is None:
                log("altaUsuario", "INFO", f"No se pudo dar de alta al usuario {usuario} en el sistema.")
                print("No se pudo dar de alta al usuario en el sistema.")
                usuario = None
            return usuario
    except Exception as e:
        print(f"Error: {e}")
        return None



def inicializarUsuariosFake():
    fake = Faker()
    for _ in range(10):
        nombreAlumno = fake.first_name()
        apellidoAlumno = fake.last_name()
        usuario = nombreAlumno[0].lower() + apellidoAlumno.lower()
        existeUsuario = validarNombreUsuarioEnSistema(usuario)
        if existeUsuario is not None:
            nombreUsuarioRepetido(nombreAlumno, apellidoAlumno)
        contrasena = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        tipo_usuario = "User"
        try:
            with open('ETAPA2/Archivos/usuarios.csv', 'a') as archivo:
                archivo.writelines(f"{usuario},{contrasena},{tipo_usuario}\n")
            dadoDeAlta = altaEnSistema(usuario,nombreAlumno,apellidoAlumno)
            if dadoDeAlta == False or dadoDeAlta is None:
                print(f"No se pudo dar de alta al usuario {usuario} en el sistema.")
        except Exception as e:
            print(f"Error: {e}")
    