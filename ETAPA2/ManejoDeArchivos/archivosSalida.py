from ManejoDeDatos.validacionDeDatos import estaDentroDelRango
import json
from Entidades.materias import buscarMateriaPorIndice

def menuExportacion(user):
    cierraSesion = False
    while True:
        try:
            print("Ingrese el numero de la opcion a elegir.")
            print("OPCIONES:")
            print("1- Porcentaje aprobacion por materia\n2- Grafico comparativo entre estudiantes con pack 5 materias y los que no\n3- Ranking flashcards\n4-Ranking de materias con mas flashcards \n0- Salir\n")
            opcion=int(input(f"{user}: "))
    
            if estaDentroDelRango(0,4,opcion)==False:
                raise ValueError("Numero ingresado fuera del rango, intente nuevamente\n")
            if opcion==1:
                datos = porcentajeXMateria()
                break
            if opcion == 2:
                datos = cantEstudiantePack5()
                break
            if opcion == 3:
                print("Falta")
                break
            if opcion == 4:
                datos = rankingMateriaFlashcards()
                break
            else:
                print("hola")
                break
        except ValueError:
            print("El valor ingresado no es correcto,intente nuevamente")
    generarArchivosSalida(datos)
    return cierraSesion



def generarArchivosSalida(data):
    try:
        path = "ETAPA2/ArchivosSalida/" + data[0] + ".csv"
        with open( path, 'w') as archivo:
            for datos in data[1]:
                restructedDatos = str(datos) + "\n"
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
        PorcentajeDeMaterias = calcularPorcentaje(temp)
        datosAsubir = []

        for materiaId in PorcentajeDeMaterias.keys():
            materia = buscarMateriaPorIndice(int(materiaId))
            nombreMateria = materia["nombre"]
            datosAsubir.append(nombreMateria + ": ")
            datosAsubir.append(str(PorcentajeDeMaterias[materiaId]["Porcentaje"]) + "%")
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
        datosAsubir.append("Estudiantes que usan Pack 5 materias: ")
        datosAsubir.append(f"{conPack}")
        datosAsubir.append("Estudiantes que no usan Pack 5 materias: ")
        datosAsubir.append(f"{sinPack}")
        print(datosAsubir)
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
    datos = []
    try:
        with open("ETAPA2/Archivos/materias.json", 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                materia = json.loads(linea)
                nombre = materia["nombre"]
                cantFlashcards = len(materia["flashcards"])
                datos.append((nombre, cantFlashcards))
        datos.sort(key=, reverse=True)
            
        return datos
             
    except Exception as e:
        print(f"Error: {e}")
        return None