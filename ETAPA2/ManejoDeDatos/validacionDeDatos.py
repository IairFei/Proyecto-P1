def estaDentroDelRango(nMinimo, nLimite, datoAValidar):
    estaEnElRango = True
    if datoAValidar < nMinimo or datoAValidar > nLimite:
        estaEnElRango = False
    return estaEnElRango

def charValido(char):
    esValido = False
    char = char.lower().strip()
    if char == 's' or char == 'n':
        esValido = True
    return esValido

def verificarSeguridadContraseña(contraseña):
    caracteresEspeciales = ["@", "!", "?", "#", "$", "¿", "¡", "&", "%", "(", ")", "=",".",",",";",":"]
    contieneNumeros = False
    contieneEspecial = False

    letras = [letra for letra in contraseña]
    
    for caracter in letras:
        if caracter in caracteresEspeciales:
            contieneEspecial = True
            break
    if len(contraseña) < 6:
        error = "debe contener minimo 6 caracteres!"
        message = "Contraseña poco segura, " + error
        return(message, False)
    if not contieneEspecial:
        error = "debe contener al menos 1 caracter especial!"
        message = "Contraseña poco segura, " + error
        
        return (message, False)

    for caracter in letras:
        try:
            int(caracter)
            contieneNumeros = True
            break
        except ValueError:
            continue

    if not contieneNumeros:
        error = "debe contener al menos un numero"
        message = "Contraseña poco Segura, " + error
        
        return (message, False)

    else:
        message = "Contraseña segura"
        return (message, True)