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