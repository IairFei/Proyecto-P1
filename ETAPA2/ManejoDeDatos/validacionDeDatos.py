from Logs.logs import log

def validarEntero(min, max):
    while True:
        try:
            entrada = int(input("Usuario: "))
            if entrada>max or entrada<min:
                raise ValueError
            break
        except:
            print("Entrada inválida. Intente nuevamente.")
    return entrada

def validarTexto(opciones):
    while True:
        try:
            entrada = input("Usuario: ").lower().strip()
            if entrada not in opciones:
                raise ValueError
            break
        except ValueError:
            print("Entrada inválida. Intente nuevamente.")
    return entrada

def verificarSeguridadContrasena(contrasena):
    caracteresEspeciales = ["@", "!", "?", "#", "$", "¿", "¡", "&", "%", "(", ")", "=",".",",",";",":","_","-"]
    repiteCaracteres = False
    contieneEspecial = False
    contieneNumeros = False
    contieneMinuscula = False
    contieneMayuscula = False
    contrasenaCorrecta = True 
    caracteres = [str(caracter) for caracter in contrasena]

    for caracter in caracteres:
        if caracteres.count(caracter) > 2:
            repiteCaracteres = True
        if caracter in caracteresEspeciales:
            contieneEspecial = True
        elif caracter.isnumeric():
            contieneNumeros = True
        elif caracter.islower():
            contieneMinuscula = True
        else:
            contieneMayuscula = True
    mensaje="La contraseña debe cumplir con los siguientes requisitos:\n"

    if len(contrasena) < 6:
        mensaje += "- Debe contener al menos 6 caracteres.\n"
        contrasenaCorrecta = False
    if len(contrasena) > 12:
        mensaje += "- Debe contener como máximo 12 caracteres.\n"
        contrasenaCorrecta = False
    if repiteCaracteres:
        mensaje += "- No repetir caracteres tantas veces.\n"
        contrasenaCorrecta = False
    if not contieneEspecial:
        mensaje += "- Debe contener caracteres especiales.\n"
        contrasenaCorrecta = False
    if not contieneNumeros:
        mensaje += "- Debe contener números.\n"
        contrasenaCorrecta = False
    if not contieneMinuscula:
        mensaje += "- Debe contener minúsculas.\n"
        contrasenaCorrecta = False
    if not contieneMayuscula:
        mensaje += "- Debe contener mayúsculas.\n"
        contrasenaCorrecta = False
    if contrasenaCorrecta:
        mensaje = "Contraseña segura."
    return (mensaje, contrasenaCorrecta)

def eleccionDeMateriaAnio(usuario):
    print("Ingrese el año de la materia (1-5): ")
    anioElegido = validarEntero(1,5)
    log("eleccionDeMateriaAnio", "INFO", f"Usuario {usuario} eligió el año {anioElegido} para la materia.")  
    return anioElegido

def eleccionDeMateriaCuatrimestre(usuario):
    print("Ingrese el cuatrimestre de la materia (1-2): ")
    cuatrimestreElegido = validarEntero(1,2)
    log("eleccionDeMateriaCuatrimestre", "INFO", f"Usuario {usuario} eligió el cuatrimestre {cuatrimestreElegido} para la materia.")
    return cuatrimestreElegido