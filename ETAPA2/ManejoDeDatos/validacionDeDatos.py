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

    if len(contrasena) < 6:
        mensaje = "Contraseña demasiado corta, debe contener al menos 6 caracteres."
        contrasenaCorrecta = False
    elif len(contrasena) > 12:
        mensaje = "Contraseña demasiado larga, debe contener como máximo 12 caracteres."
        contrasenaCorrecta = False
    elif repiteCaracteres:
        mensaje = "Contraseña poco segura, no repita caracteres tantas veces."
        contrasenaCorrecta = False
    elif not contieneEspecial:
        mensaje = "La contraseña debe contener caracteres especiales."
        contrasenaCorrecta = False
    elif not contieneNumeros:
        mensaje = "La contraseña debe contener números."
        contrasenaCorrecta = False
    elif not contieneMinuscula:
        mensaje = "La contraseña debe contener minúsculas."
        contrasenaCorrecta = False
    elif not contieneMayuscula:
        mensaje = "La contraseña debe contener mayúsculas."
        contrasenaCorrecta = False
    else:
        mensaje = "Contraseña segura."
        contrasenaCorrecta = True
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