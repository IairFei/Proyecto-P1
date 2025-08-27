from vallidacionDeDatos import estaDentroDelRango

def mostrarMateriasDisponibles(anio, semestre):
    print(f"Mostrando materias disponibles para el año {anio}, semestre {semestre}:")
    for materia in materias:    
        codigo= materia.split("-", 1)
        anioMateria= codigo[1].split(".", 1)[0]
        cuatrimestre= codigo[1].split(".", 2)[1]
        if int(anioMateria) == anio and int(cuatrimestre) == semestre:
            print(f"- {materia}")
    
def inicioDePrograma():
    print("Elija una opción:\n1- Anotarse a materias\n2- Estado 'Pack de 5 materias'\n3- Cargar nota de materia\n4- Dar de baja una materia\n5- Ver calendario\n6- Ver notas\n0- Salir\n")
    opcionElegida = int(input("Usuario: "))
    print("-----------------------------------------------------")
    while opcionElegida != 0:
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
                anioElegido = int(input("Usuario: "))  
            print("Ingrese el semestre de la materia (1-2): ")
            semestreElegido = int(input("Usuario: "))
            while estaDentroDelRango(1,2,semestreElegido) == False:
                print("Semestre inválido. Por favor, ingrese un semestre válido (1-2).")
                print("Ingrese el semestre de la materia (1-2): ")
                semestreElegido = int(input("Usuario: "))
            mostrarMateriasDisponibles(anioElegido, semestreElegido)
            inicioDePrograma()
            
            
            
        """if opcionElegida == 2:
            estado = estadoPackDe5Materias()
            print(f"Estado 'Pack de 5 materias': {estado}")  """

        

if __name__ == "__main__":
    materias = ["391-1.1.Fundamentos de Informatica","863-1.1.Sistemas de Información I","385-1.1.Pensamiento Crítico y Comunicación","546-1.1.Teoría de Sistemas","438-1.1.Elementos de Álgebra y Geometría","842-1.2.Programación I","663-1.2.Sistemas de Representación","186-1.2.Matemática Discreta","605-1.2.Fundamentos de Química","920-1.2.Arquitectura de Computadores","665-1.2.Álgebra","365-2.1.Programación II","560-2.1.Sistemas de Información II","378-2.1.Sistemas Operativos","214-2.1.Física I","329-2.1.Cálculo I","247-2.2.Programación III","802-2.2.Paradigma Orientado a Objetos","100-2.2.Fundamentos de Telecomunicaciones","495-2.2.Ingeniería de Datos I","345-2.2.Cálculo II","587-3.1.Proceso de Desarrollo de Software","563-3.1.Seminario de Integración Profesional","817-3.1.Teleinformática y Redes","211-3.1.Ingeniería de Datos II","737-3.1.Probabilidad y Estadística","382-3.1.Examen de Inglés","887-3.2.Aplicaciones Interactivas","977-3.2.Ingeniería de Software","901-3.2.Física II","107-3.2.Teoría de la Computación","748-3.2.Estadística Avanzada","615-4.1.Desarrollo de Aplicaciones I","559-4.1.Dirección de Proyectos Informáticos","178-4.1.Ciencia de Datos","772-4.1.Seguridad e Integridad de la Información","683-4.1.Modelado y Simulación","530-4.2.Desarrollo de Aplicaciones II","437-4.2.Evaluación de Proyectos Informáticos","284-4.2.Inteligencia Artificial","944-4.2.Tecnología y Medio Ambiente","269-4.2.Práctica Profesional Supervisada","766-4.2.Optativa 1","321-5.1.Arquitectura de Aplicaciones","145-5.1.Tendencias Tecnológicas","889-5.1.Proyecto Final de Ingeniería en Informática","770-5.1.Calidad de Software","473-5.1.Optativa 2","966-5.2.Negocios Tecnológicos","308-5.2.Tecnología e Innovación","112-5.2.Derecho Informático","412-5.2.Optativa 3"]
    materiasAprobadas = []
    print("Bienvenido al programa de gestión de materias.")
    print("Por favor, siga las instrucciones para ingresar los datos de las materias.")
    print("-----------------------------------------------------")
    inicioDePrograma()