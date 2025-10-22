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

def tieneNotasParciales(p1,p2, indiceMateria):
    tieneNotas = False
    if p1[indiceMateria] !=0 and p2[indiceMateria] != 0:
        tieneNotas = True
    return tieneNotas

def tieneNotaParcial1(p1, indiceMateria):
    tieneNota = False
    if p1[indiceMateria] != 0:
        tieneNota = True
    return tieneNota


def verificarSeguridadContraseña(contraseña):
    caracteresEspeciales = ["@", "!", "?", "#", "$", "¿", "¡", "&", "%", "(", ")", "=",".",",",";",":"]
    contieneNumeros = False
    contieneEspecial = False

    letras = [letra for letra in contraseña]
    
    for caracter in letras:
        if caracter in caracteresEspeciales:
            contieneEspecial = True
            break
    if len(contraseña) < 3:
        error = "minimo 3 caracteres!"
        message = "" + error
        return(message, False)
    if not contieneEspecial:
        error = "no contiene caracteres especiales!"
        message = "Contraseña poco Segura, " + error
        
        return (message, False)

    for caracter in letras:
        try:
            int(caracter)
            contieneNumeros = True
            break
        except ValueError:
            continue

    if not contieneNumeros:
        error = "no contiene numeros"
        message = "Contraseña poco Segura, " + error
        
        return (message, False)

    else:
        message = "Contraseña segura"
        return (message, True)

