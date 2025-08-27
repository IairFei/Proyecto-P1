def estaDentroDelRango(nMinimo, nLimite, datoAValidar):
    estaEnElRango = True
    if datoAValidar < nMinimo or datoAValidar > nLimite:
        estaEnElRango = False
    return estaEnElRango