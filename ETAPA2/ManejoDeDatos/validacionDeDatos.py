from Logs.logs import log

def estaDentroDelRango(nMinimo, nLimite, datoAValidar):
    try:
        estaEnElRango = True
        datoAValidar = int(datoAValidar)
        if datoAValidar is None or datoAValidar == "":
            raise ValueError("El dato a validar no puede estar vacío.")
        #validar que sea int
        if datoAValidar < nMinimo or datoAValidar > nLimite:
            estaEnElRango = False
    except ValueError as e:
        log("estaDentroDelRango", "ERROR", f"Error al validar el rango: {e}")
        estaEnElRango = False
    return estaEnElRango


def charValido(char):
    try:
        esValido = False
        char = str(char)
        char = char.lower().strip()
        if char == 's' or char == 'n':
            esValido = True
    except ValueError as e:
        log("charValido", "ERROR", f"Error al validar el carácter: {e}")
        esValido = False
    return esValido

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
    anioElegido = int(input(f"{usuario}: "))
    while estaDentroDelRango(1,5,anioElegido) == False:
        print("Año inválido. Por favor, ingrese un año válido (1-5).")
        print("Ingrese el año de la materia (1-5): ")
        anioElegido = int(input(f"{usuario}: "))
    log("eleccionDeMateriaAnio", "INFO", f"Usuario {usuario} eligió el año {anioElegido} para la materia.")  
    return anioElegido

def eleccionDeMateriaCuatrimestre(usuario):
    print("Ingrese el cuatrimestre de la materia (1-2): ")
    cuatrimestreElegido = int(input(f"{usuario}: "))
    while estaDentroDelRango(1,2,cuatrimestreElegido) == False:
        print("Cuatrimestre inválido. Por favor, ingrese un cuatrimestre válido (1-2).")
        print("Ingrese el cuatrimestre de la materia (1-2): ")
        cuatrimestreElegido = int(input(f"{usuario}: "))
    log("eleccionDeMateriaCuatrimestre", "INFO", f"Usuario {usuario} eligió el cuatrimestre {cuatrimestreElegido} para la materia.")
    return cuatrimestreElegido