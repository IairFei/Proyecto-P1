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
        nombre_materia=materias[materia].split(".", 2)[2]
        print(f"{dia:<12} {nombre_materia:<35}")
    
    print("-" * 50)
    print("✨ Fin del calendario ✨")
    print("=" * 50)