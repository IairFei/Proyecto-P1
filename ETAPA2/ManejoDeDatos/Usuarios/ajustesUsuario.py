from ManejoDeDatos.validacionDeDatos import estaDentroDelRango
from ..validacionDeDatos import verificarSeguridadContraseña
from ManejoDeDatos.Usuarios.usuarios import validarContrasena
from Logs.logs import log

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
            status =  verificarSeguridadContraseña(contrasenaNueva)
            if status[1] == True:
                print(status[0])
                log("ajusteUsuario", "INFO", f"Contraseña para el usuario {usuario} cumple con los requisitos de seguridad.")
                break
            else:
                print(status[0])
                log("ajusteUsuario", "WARNING", f"Contraseña para el usuario {usuario} no cumple con los requisitos de seguridad por el motivo: {status[0]}")
                contrasenaNueva = input("Ingrese su nueva contraseña: ").strip()
                log("ajusteUsuario", "INFO", f"Nuevo intento de contraseña ingresada para el usuario {usuario}.")
                continue
        status = contrasenaActualizada(usuario,exContrasena,contrasenaNueva)
        if status == True:   
            print("Contraseña actualizada.\nVolviendo al Menu")
            log("ajusteUsuario", "INFO", f"Se actualizo la contraseña del usuario: {usuario}.")
            print("-----------------------------------------------------")
        else:
            print("Ocurrio un error mientras se actualizaba la contraseña.")
            log("ajusteUsuario", "WARNING", f"Se actualizo la contraseña del usuario: {usuario}.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def contrasenaActualizada(usuario,exContrasena,contrasenaNueva):
    try:
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
            return True
    except Exception as e:
        print(f"Error: {e}")
    return None

def menuAjustes(usuario):
    while True:
        try:
            print("Ingrese el numero de la opcion a elegir.")
            print("OPCIONES:")
            print("1- Cambiar contraseña\n0- Salir\n")
            opcion=int(input(f"{usuario}: "))
            
            if estaDentroDelRango(0,1,opcion)==False:
                raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
            if opcion==1:
                cambioContrasena(usuario) 
            else:
                break
        except ValueError:
            print("El valor ingresado no es correcto,intente nuevamente")
    return None