
import random
from Entidades.materias import tieneCorrelativasAprobadas, darDeBajaNotas
from Logs.logs import log
import json
from ManejoDeDatos.Usuarios.usuarios import guardarUsuario

def verCalendario(usuarioActual):
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

    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    calendario = usuarioActual["calendario"]
    for i in range(5):
        dia = dias[i]
        materia_id = calendario[dia]
        if materia_id is None or materia_id == -1:
            nombre_materia = "Libre"
        else:
            nombre_materia = None
            with open('ETAPA2/Archivos/materias.json', 'r', encoding='utf-8') as archivo_materias:
                for linea in archivo_materias:
                    datos_materia = json.loads(linea)
                    if datos_materia['id'] == materia_id:
                        nombre_materia = datos_materia['nombre']
                        break
            if nombre_materia is None:
                nombre_materia = f"ID {materia_id} (no encontrada)"
        print(f"{dia:<12} {nombre_materia:<35}")

    print("-" * 50)
    print("✨ Fin del calendario ✨")
    print("=" * 50)



def inscribirseAMateria(materiaSeleccionada, usuarioActual):
    try:
        with open('ETAPA2/Archivos/materias.json', 'r', encoding='utf-8') as archivo_materias:
            materia = None
            for linea in archivo_materias:
                datos_materia = json.loads(linea)
                if datos_materia['id'] == materiaSeleccionada:
                    materia = datos_materia
                    break
            if materia is None:
                raise ValueError("Materia no encontrada.")
        dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]  
        calendario = usuarioActual["calendario"]
        diasCalendario = [i for i in range(5) if calendario[dias[i]] is None]
        if not diasCalendario:
            print("No hay días disponibles en el calendario para inscribirse en una nueva materia.")
            return
        diaElegido = random.choice(diasCalendario)
        print(f"Inscribiéndose en la materia {materia['nombre']} el día {dias[diaElegido]}")
        usuarioActual['calendario'][dias[diaElegido]] = materia['id']
        usuarioActual['notas'][materia['id']] = {"parcial1": None, "parcial2": None, "final": None, "nota_final": None, "aprobada": False, "recursa": False}
        log("inscribirseAMateria", "INFO", f"Usuario {usuarioActual['usuario']} se inscribió en la materia {materia['nombre']} el día {dias[diaElegido]}")
        guardarUsuario(usuarioActual)
        verCalendario(usuarioActual)
        return
    except Exception as e:
        print(f"Error al inscribirse en la materia: {e}")

def darDeBajaMateria(usuarioActual, diaIngresado):
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    indiceMateria = usuarioActual["calendario"][dias[diaIngresado-1]]
    usuarioActual["calendario"][dias[diaIngresado-1]] = None
    log("darDeBajaMateria", "INFO", f"Materia dada de baja: {indiceMateria} en el dia {diaIngresado}")
    darDeBajaNotas(indiceMateria, usuarioActual)
    guardarUsuario(usuarioActual)
