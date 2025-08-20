from baseDeDatos import mostrarMaterias, inicializarDatos, agregarMateriaAlCalendario

def inicioDePrograma():
    print("Bienvenido al programa de gestión de materias.")
    print("Por favor, siga las instrucciones para ingresar los datos de las materias.")
    anio = int(input("Ingrese el año de la carrera en el que está (1-5). 0 para terminar: "))
    if anio != 0:
        while anio < 0 and anio > 5:
            print("El año debe estar entre 1 y 5. Intente nuevamente: ")
            anio = int(input("Ingrese el año en el que se cursa la materia (0 para terminar): "))
        cuatrimestre = int(input("Ingrese el cuatrimestre en el que se cursa la materia (1-2): "))
        while cuatrimestre < 1 or cuatrimestre > 2:
            print("El cuatrimestre debe ser 1 o 2. Intente nuevamente.")
            cuatrimestre = int(input("Ingrese el cuatrimestre en el que se cursa la materia: "))
        materiasAElegir = mostrarMaterias(anio, cuatrimestre)
        
        agregaMateria = input("¿Desea alegir una de estas materias para cursar? (s/n): ").lower().strip()
        while agregaMateria not in ['s', 'n']:
            print("Entrada no válida. Por favor, ingrese 's' para sí o 'n' para no.")
            agregaMateria = input("¿Desea alegir una de estas materias para cursar? (s/n): ").lower().strip()
        if agregaMateria == 's':
            materiaElegida = int(input("Ingrese el numero de la materia que desea agregar: "))
            while materiaElegida < 1 or materiaElegida > len(materiasAElegir):
                print(f"El número de materia debe estar entre 1 y {len(materiasAElegir)}. Intente nuevamente.")
                materiaElegida = int(input("Ingrese el numero de la materia que desea agregar: "))
            diaElegido = int(input("Ingrese el dia de la materia que desea cursar (1-Lun, 2-Mar, 3-Mie, 4-Jue, 5-Vie): "))
            while diaElegido < 1 or diaElegido > 5:
                print("Día no válido. Debe ser un número entre 1 y 5.")
                diaElegido = int(input("Ingrese el dia de la materia que desea cursar (1-Lun, 2-Mar, 3-Mie, 4-Jue, 5-Vie): "))
            agregarMateriaAlCalendario(diaElegido-1,materiasAElegir[materiaElegida - 1])
        deseaContinuar = input("¿Desea ingresar otra materia? (s/n): ").lower().strip()
        while deseaContinuar not in ['s', 'n']:
            print("Entrada no válida. Por favor, ingrese 's' para sí o 'n' para no.")
            deseaContinuar = input("¿Desea ingresar otra materia? (s/n): ").lower().strip()
        if deseaContinuar == 's':
            inicioDePrograma()
        else:
            print("Programa terminado.")
    else:
        print("Programa terminado.")

if __name__ == "__main__":
    inicializarDatos()
    inicioDePrograma()