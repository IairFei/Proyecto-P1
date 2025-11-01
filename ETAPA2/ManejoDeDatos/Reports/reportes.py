from Logs.logs import log
from ..Usuarios.usuarios import obtenerCantidadUsuarios, obtenerUsuarioPorRol
from Entidades.materias import obtenerCantidadDeMaterias, obtenerCantidadDeInscriptosEnMaterias
from Entidades.flashcards import obtenerCantidadDeFlashcardsEnMaterias, obtenerCantdadDeFlashcards, obtenerCantidadDeFlashcardsPorCreador

def generarReporte(opcion):
    try:
        reporteGenerado = False
        pathGeneral = r'C:\Users\93179\Desktop\Programacion 1\Proyecto-P1\ETAPA2\ManejoDeDatos\Reports'
        cantidadDeMaterias = obtenerCantidadDeMaterias()
        cantidadDeUsuarios = obtenerCantidadUsuarios()
        if opcion == 1:
            usuariosAdministradores = obtenerUsuarioPorRol("Administrator")
            nombresAdministradores = ', '.join(admin for admin in usuariosAdministradores)
            usuariosEstudiantes = obtenerUsuarioPorRol("User")
            nombresEstudiantes = ', '.join(estudiantes for estudiantes in usuariosEstudiantes)
            arch = open(f'{pathGeneral}\\reporte_usuarios.csv', 'w', encoding='utf-8')
            arch.write("Reporte de Usuarios\n\n")
            arch.write("Cantidad de usuarios en el sistema: {}\n".format(cantidadDeUsuarios))
            arch.write("Cantidad de administradores: {}\n".format(len(usuariosAdministradores)))
            arch.write("Usuarios administradores: {}\n".format(nombresAdministradores))
            arch.write("Cantidad de estudiantes: {}\n".format(len(usuariosEstudiantes)))
            arch.write("Usuarios estudiantes: {}\n".format(nombresEstudiantes))
            arch.close()
            reporteGenerado = True
            log("generarReporte", "INFO", "Reporte de usuarios generado exitosamente.")
        elif opcion == 2:
            inscriptosPorMateria = obtenerCantidadDeInscriptosEnMaterias()
            arch = open(f'{pathGeneral}\\reporte_materias.csv', 'w', encoding='utf-8')
            arch.write("Reporte de Materias\n\n")
            arch.write("Cantidad de materias en el sistema: {}\n".format(cantidadDeMaterias))
            arch.write("Inscriptos por materia:\n")
            for materia, inscriptos in inscriptosPorMateria:
                if inscriptos == 0:
                    continue
                arch.write("{}: {}\n".format(materia, inscriptos))
            arch.write("Cantidad de materias en el sistema: {}\n".format(cantidadDeMaterias))
            arch.write("Cantidad de usuarios en el sistema: {}\n".format(cantidadDeUsuarios))
            arch.close()
            reporteGenerado = True
            log("generarReporte", "INFO", "Reporte de materias generado exitosamente.")
        elif opcion == 3:
            cantidadDeFlashcards = obtenerCantdadDeFlashcards()
            flashcardsPorMateria = obtenerCantidadDeFlashcardsEnMaterias()
            flashcardsPorCreador = obtenerCantidadDeFlashcardsPorCreador()
            arch = open(f'{pathGeneral}\\reporte_flashcards.csv', 'w', encoding='utf-8')
            arch.write("Reporte de Flashcards\n\n")
            arch.write("Cantidad total de flashcards en el sistema: {}\n".format(cantidadDeFlashcards))
            arch.write("Cantidad de flashcards por materia:\n")
            for materia, cantidad in flashcardsPorMateria:
                if cantidad == 0:
                    continue
                arch.write("{}: {}\n".format(materia, cantidad))
            #ranking de creadores de flashcards
            arch.write("Cantidad de flashcards por creador:\n")
            for creador, cantidad in flashcardsPorCreador.items():
                arch.write("{}: {}\n".format(creador, cantidad))
            arch.write("Cantidad de materias en el sistema: {}\n".format(cantidadDeMaterias))
            arch.write("Cantidad de usuarios en el sistema: {}\n".format(cantidadDeUsuarios))
            reporteGenerado = True
            log("generarReporte", "INFO", "Reporte de flashcards generado exitosamente.")
        return reporteGenerado
    except IOError as e:
        log("generarReporte", "ERROR", f"Error al generar el reporte: {e}")