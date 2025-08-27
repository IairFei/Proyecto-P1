from vallidacionDeDatos import estaDentroDelRango

def inicioDePrograma():
    print("Bienvenido al programa de gestión de materias.")
    print("Por favor, siga las instrucciones para ingresar los datos de las materias.")
    print("-----------------------------------------------------")
    print("Elija una opción:\n1- Anotarse a materias\n2- Estado 'Pack de 5 materias'\n3- Cargar nota de materia\n4- Dar de baja una materia\n5- Ver calendario\n6- Ver notas\n0- Salir\n")
    opcionElegida = int(input("Usuario: "))
    print("-----------------------------------------------------")
    while estaDentroDelRango(0,6,opcionElegida) == False:
        print("Opción inválida. Por favor, elija una opción válida.")
        print("Elija una opción:\n1- Anotarse a materias\n2- Estado 'Pack de 5 materias'\n3- Cargar nota de materia\n4- Dar de baja una materia\n5- Ver calendario\n6- Ver notas\n0- Salir\n")
        opcionElegida = int(input("Usuario: "))
        print("-----------------------------------------------------")
    if opcionElegida == 1:
        print("Ingrese el año de la materia (1-5): ")
        anioElegido = int(input("Usuario: "))
        while estaDentroDelRango(1,5,anioElegido) == False:
            print("Año inválido. Por favor, ingrese un año válido (1-5).")
            print("Ingrese el año de la materia (1-5): ")
            anioElegido = input("Usuario: ")       
        print("Ingrese el semestre de la materia (1-2): ")
        semestreElegido = int(input("Usuario: "))
        while estaDentroDelRango(1,2,semestreElegido) == False:
            print("Semestre inválido. Por favor, ingrese un semestre válido (1-2).")
            print("Ingrese el semestre de la materia (1-2): ")
            semestreElegido = int(input("Usuario: "))
    if opcionElegida == 2:
        estado = estadoPackDe5Materias()
        print(f"Estado 'Pack de 5 materias': {estado}")  
        
        

if __name__ == "__main__":
    materias = ["1.1.Fundamentos de Informatica", "1.1.Sistemas de Información I", "1.1.Pensamiento Crítico y Comunicación", "1.1.Teoría de Sistemas", "1.1.Elementos de Álgebra y Geometría", "1.2.Programación I", "1.2.Sistemas de Representación", "1.2.Matemática Discreta", "1.2.Fundamentos de Química", "1.2.Arquitectura de Computadores", "1.2.Álgebra", "2.1.Programación II", "2.1.Sistemas de Información II", "2.1.Sistemas Operativos", "2.1.Física I", "2.1.Cálculo I", "2.2.Programación III", "2.2.Paradigma Orientado a Objetos", "2.2.Fundamentos de Telecomunicaciones", "2.2.Ingeniería de Datos I", "2.2.Cálculo II", "3.1.Proceso de Desarrollo de Software", "3.1.Seminario de Integración Profesional", "3.1.Teleinformática y Redes", "3.1.Ingeniería de Datos II", "3.1.Probabilidad y Estadística", "3.1.Examen de Inglés", "3.2.Aplicaciones Interactivas", "3.2.Ingeniería de Software", "3.2.Física II", "3.2.Teoría de la Computación", "3.2.Estadística Avanzada", "4.1.Desarrollo de Aplicaciones I", "4.1.Dirección de Proyectos Informáticos", "4.1.Ciencia de Datos", "4.1.Seguridad e Integridad de la Información", "4.1.Modelado y Simulación", "4.2.Desarrollo de Aplicaciones II", "4.2.Evaluación de Proyectos Informáticos", "4.2.Inteligencia Artificial", "4.2.Tecnología y Medio Ambiente", "4.2.Práctica Profesional Supervisada", "4.2.Optativa 1", "5.1.Arquitectura de Aplicaciones", "5.1.Tendencias Tecnológicas", "5.1.Proyecto Final de Ingeniería en Informática", "5.1.Calidad de Software", "5.1.Optativa 2", "5.2.Negocios Tecnológicos", "5.2.Tecnología e Innovación", "5.2.Derecho Informático", "5.2.Optativa 3"]
    inicioDePrograma()