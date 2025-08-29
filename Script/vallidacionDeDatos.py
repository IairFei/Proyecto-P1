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