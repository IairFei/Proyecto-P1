from ManejoDeDatos.validacionDeDatos import estaDentroDelRango
import json
from Entidades.materias import buscarMateriaPorIndice

def generarReporte(opcion):
    
    datos = None 

    if opcion == 1:
        datos = porcentajeXMateria()

    elif opcion == 2:
        datos = cantEstudiantePack5()
        
    elif opcion == 3:
        datos = rankingMejoresFlashcards()
        
    elif opcion == 4:
        datos = rankingMateriaFlashcards()
        
    else:
        print(f"Error: Opción '{opcion}' no válida.")
        return False 

    if datos is not None:
        generarArchivosSalida(datos)
        return True
    else:
        print("No se generaron datos para el reporte.")
        return False



def generarArchivosSalida(data):
    try:
        print("Generando archivo de salida...")
        path = "ETAPA2/ArchivosSalida/" + data[0] + ".csv"
        with open( path, 'w') as archivo:
            print(data[0],data[1])
            for datos in data[1]:
                for dato in datos:
                    print(dato,datos)
                    restructedDatos = str(dato) + "\n"
                    archivo.write(restructedDatos)
                
        print(f"datos extraidos, en: {path}")
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return None
    return


def porcentajeXMateria():
    temp = {}
    try:
        with open("ETAPA2/Archivos/usuarios.json", 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                usuario = json.loads(linea)
                for materia in usuario["notas"]:
                    if materia not in temp:
                        temp[materia] = {"total": 0, "Porcentaje": 0}
                    temp[materia]["total"] += 1
                    if usuario["notas"][materia]["aprobada"]:
                        temp[materia]["Porcentaje"] += 1
        # PorcentajeDeMaterias = calcularPorcentaje(temp)
        datosAsubir = []

        for materiaId in temp.keys():
            materia = buscarMateriaPorIndice(int(materiaId))
            nombreMateria = materia["nombre"]
            datosAsubir.append((nombreMateria + ": ", "aprobados",f"{temp[materiaId]["Porcentaje"]}","total:",f"{temp[materiaId]["total"]}"))
        return ("PorcentajeDeAprobacionXMateria",datosAsubir)

    except Exception as e:
        print(f"Error: {e}")
        return None
    
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
        datosAsubir.append(("Estudiantes que usan Pack 5 materias: ", f"{conPack}"))
        datosAsubir.append(("Estudiantes que no usan Pack 5 materias: ", f"{sinPack}"))
        return ("cantEstudiantesUsanPack5Materias",datosAsubir)
             
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def calcularPorcentaje(datos):
    resultados = {}
    for clave in datos:
        data = datos[clave]
        total = data["total"]
        Porcentaje = data["Porcentaje"]
        if total > 0:
            Porcentaje = (Porcentaje / total) * 100  
        else:
            Porcentaje = 0.0
            
        resultados[clave] = {
            "total": total, 
            "Porcentaje": Porcentaje
        }
        
    return resultados



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

    except Exception as e:
        print(f"Error: {e}")
        return None
    
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
                            datos.append((pregunta[0], promedioFlashcard))
                            
        return ("rankingFlashcards",datos)

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        return []