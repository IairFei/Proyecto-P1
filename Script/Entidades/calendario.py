
import random
from Entidades.materias import tieneCorrelativasAprobadas, darDeBajaNotas

def verCalendario(calendario, materias):
    """
    Muestra el calendario de materias como matriz formateada
    calendario: matriz donde cada fila es [codigo_materia, parcial1, parcial2, nota_final]
    materias: lista de materias con formato "codigo-nombre"
    """
    print("=" * 50)
    print("📚 CALENDARIO ACADÉMICO 📚")
    print("=" * 50)
    
    print(f"{'DÍA':<12} {'MATERIA':<35}")
    print("-" * 50)
    
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    for i in range(5):
        dia = dias[i]
        materia = calendario[i]
        if materia == -1:
            nombre_materia = "Libre"
        else:
            nombre_materia = materias[materia].split(".", 2)[2]
        print(f"{dia:<12} {nombre_materia:<35}")
    
    print("-" * 50)
    print("✨ Fin del calendario ✨")
    print("=" * 50)

def inscribirseAMateria(indice, materias, diasCalendario, calendario, notaFinal, correlativas):
    sePudoInscribir = False
    materiaAInscribirse = materias[indice].split(".",3)
    print(f"Inscribiendose a la materia: {materiaAInscribirse[2]}")
    if tieneCorrelativasAprobadas(indice, materias, notaFinal, correlativas) and indice not in calendario:
        if len(diasCalendario) > 0:
            diaElegido = random.choice(diasCalendario)
            calendario[diaElegido] = indice
            diasCalendario.remove(diaElegido)
            sePudoInscribir = True
    else:
        print("No se pudieron cumplir las condiciones para inscribirse.")
    return sePudoInscribir

def darDeBajaMateria(diaIngresado,calendario,diasCalendario,p1,p2,notaFinal):
    indiceMateria = calendario[diaIngresado-1]
    calendario[diaIngresado-1] = -1
    diasCalendario.append(diaIngresado-1)
    diasCalendario.sort()
    darDeBajaNotas(indiceMateria,p1,p2,notaFinal)
