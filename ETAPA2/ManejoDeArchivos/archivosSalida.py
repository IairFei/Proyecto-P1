import json
from Entidades.materias import buscarMateriaPorIndice
from Logs.logs import log

def generarReporte(opcion):
    archivos =["","porcentajeXMateria","cantEstudiantePack5","rankingMejoresFlashcards","rankingMateriaFlashcards","cantEstudiantesXmateria"]
    datos = None 
    if opcion == 1:
        datos = porcentajeXMateria()
    elif opcion == 2:
        datos = cantEstudiantePack5()
    elif opcion == 3:
        datos = rankingMejoresFlashcards()
    elif opcion == 4:
        datos = rankingMateriaFlashcards()
    elif opcion == 5:
        datos = cantEstudiantesXmateria()
    elif opcion == 0:
        return "salir"
    else:
        print(f"Error: Opción '{opcion}' no válida.")
        
        return False
    if datos is not None:
        generarArchivosSalida(datos)
        log("GenerarReporte","INFO",f"Se creo el reporte {archivos[opcion]}")
        return True
    else:
        print("No se generaron datos para el reporte.")
        log("GenerarReporte","ERROR",f"Se produjo un error creando el reporte {archivos[opcion]}")
        return False

def generarArchivosSalida(data):
    try:
        print("-----------------------------------------------------\nGenerando archivo de salida...")
        path = "ETAPA2/ArchivosSalida/" + data[0] + ".csv"
        with open(path, 'w', encoding='utf-8') as archivo:
            for datos in data[1]:
                # Convierte la tupla/lista en una línea CSV separada por comas
                linea_csv = ",".join([str(dato) for dato in datos]) + "\n"
                archivo.write(linea_csv)
        print(f"datos extraidos, en: {path}")
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")
        log("generarArchivosSalida","ERROR","Se produjo un error creando el reporte")
    return

def porcentajeXMateria():
    temp = {}
    try:
        with open("ETAPA2/Archivos/materias.json", 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    materia = json.loads(linea)
                    nombreMateria = materia["id"]
                    temp[str(nombreMateria)] = {"total": 0, "Porcentaje": 0}
        with open("ETAPA2/Archivos/usuarios.json", 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip() 
                if linea:
                    usuario = json.loads(linea)
                    for materia in usuario["notas"]:
                        if materia in temp: 
                            temp[materia]["total"] += 1
                            if usuario["notas"][materia]["aprobada"]:
                                temp[materia]["Porcentaje"] += 1
        datosAsubir = []
        datosAsubir.append(("materia", "aprobados", "total"))
        for materiaId in temp.keys():
            materia = buscarMateriaPorIndice(int(materiaId))
            nombreMateria = materia["nombre"]
            datosAsubir.append((nombreMateria, f"{temp[materiaId]['Porcentaje']}", f"{temp[materiaId]['total']}"))
        return ("PorcentajeDeAprobacionXMateria", datosAsubir)
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")

def cantEstudiantePack5():
    conPack = 0
    sinPack = 0
    try:
        with open("ETAPA2/Archivos/usuarios.json", 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                usuario = json.loads(linea)
                if usuario["pack5materias"] == True:
                    conPack += 1
                else:
                    sinPack +=1
        datosAsubir = []
        datosAsubir.append(("Estudiantes que usan Pack 5 materias", f"{conPack}"))
        datosAsubir.append(("Estudiantes que no usan Pack 5 materias", f"{sinPack}"))
        return ("cantEstudiantesUsanPack5Materias",datosAsubir)
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")

#Funcion para calcular los porcentajes de las materias, [DESHABILITADA]
# def calcularPorcentaje(datos):
#     resultados = {}
#     for clave in datos:
#         data = datos[clave]
#         total = data["total"]
#         Porcentaje = data["Porcentaje"]
#         if total > 0:
#             Porcentaje = (Porcentaje / total) * 100  
#         else:
#             Porcentaje = 0.0 
#         resultados[clave] = {
#             "total": total, 
#             "Porcentaje": Porcentaje
#         }
#     return resultados

def rankingMateriaFlashcards():
    datosMaterias = []
    try:
        with open("ETAPA2/Archivos/materias.json", 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    materia = json.loads(linea)
                    nombre = materia["nombre"]
                    cantFlashcards = len(materia["flashcards"])
                    datosMaterias.append((nombre, cantFlashcards))
        return ("rankingMateriasFlashcards", datosMaterias)
    except (IOError, OSError):
        print(f"Error al abrir el archivo.")

def rankingMejoresFlashcards():
    datos = []
    try:
        with open("ETAPA2/Archivos/materias.json", 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    materia = json.loads(linea)
                    
                    for flashcardDic in materia["flashcards"]:
                        for pregunta in flashcardDic.items():
                            flashcardPuntuaciones = pregunta[1][2] 
                            if len(flashcardPuntuaciones) > 0:
                                promedioFlashcard = (sum(flashcardPuntuaciones)) / len(flashcardPuntuaciones)
                            else:
                                promedioFlashcard = 0
                            datos.append((pregunta[0], f"{promedioFlashcard:.2f}"))
        return ("rankingFlashcards",datos)
    except (IOError, OSError):
        print(f"Error procesando el archivo.")

def cantEstudiantesXmateria():
    datos = []
    materias = []
    cant = 0
    try:
        with open("ETAPA2/Archivos/materias.json", 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    materia = json.loads(linea)
                    cantidadAlumnos = materia["inscriptos"]
                    nombreMateria = materia["nombre"]
                    materias.append((nombreMateria,cantidadAlumnos))
        with open("ETAPA2/Archivos/usuarios.json", 'r', encoding='utf-8') as archivo: 
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    cant += 1
            materias.append(("Total Alumnos: ", cant))
        for materia in materias:
            datos.append((f"{materia[0]}",f"{materia[1]}"))
        return ("cantidadInscriptosXMateria",datos)
    except (IOError, OSError):
        print(f"Error procesando el archivo:.")