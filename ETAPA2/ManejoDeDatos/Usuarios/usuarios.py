import json

def validarNombreUsuarioEnSistema(usuario):
    try:
        datosEncontrados = None
        with open('ETAPA2/Archivos/usuarios.csv', 'r') as usuarios:
            for linea in usuarios:
                datos = linea.strip().split(',')
                if datos[0].strip() == usuario:
                    datosEncontrados = datos
                    break
        return datosEncontrados
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return None

def tipoUsuario(usuario):
    try:
        tipo_usuario_encontrado = None
        datos = validarNombreUsuarioEnSistema(usuario)
        if datos is not None:
            tipo_usuario_encontrado = datos[2].strip()
        return tipo_usuario_encontrado
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return None

def crearDiccionarioUsuarioManual(usuario_original):
    """
    Crea una copia manual del diccionario de usuario según la estructura específica del archivo
    """
    # Crear diccionario de notas manualmente
    notas_copia = {}
    for materia_id, nota_data in usuario_original['notas'].items():
        notas_copia[materia_id] = {
            'parcial1': nota_data['parcial1'],
            'parcial2': nota_data['parcial2'],
            'final': nota_data['final'],
            'nota_final': nota_data['nota_final'],
            'aprobada': nota_data['aprobada'],
            'recursa': nota_data['recursa']
        }
    
    # Crear diccionario de calendario manualmente
    calendario_copia = {
        'Lunes': usuario_original['calendario']['Lunes'],
        'Martes': usuario_original['calendario']['Martes'],
        'Miercoles': usuario_original['calendario']['Miercoles'],
        'Jueves': usuario_original['calendario']['Jueves'],
        'Viernes': usuario_original['calendario']['Viernes']
    }
    
    # Crear diccionario de usuario manualmente
    usuario_copia = {
        'id': usuario_original['id'],
        'usuario': usuario_original['usuario'],
        'nombre': usuario_original['nombre'],
        'apellido': usuario_original['apellido'],
        'pack5materias': usuario_original['pack5materias'],
        'notas': notas_copia,
        'calendario': calendario_copia
    }
    
    return usuario_copia

def getUsuarioPorNombreUsuario(nombreUsuario):
    try:
        datosEncontrados = None
        with open('ETAPA2/Archivos/usuarios.json', 'r') as usuarios:
            datos_sistema = json.load(usuarios)
            for usuario in datos_sistema['usuarios']:
                if usuario['usuario'] == nombreUsuario:
                    datosEncontrados = crearDiccionarioUsuarioManual(usuario)
                    break
        return datosEncontrados
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return None

def validarLogin(usuario, contrasena):
    concidencia = False
    try:
        datos = validarNombreUsuarioEnSistema(usuario)
        if datos is not None:
            contrasena_archivo = datos[1].strip()
            if contrasena == contrasena_archivo:
                concidencia = True
        return concidencia
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return None
        
        
def login():
    validacion = None
    try:
        print("Ingrese su nombre de usuario:")
        usuario = input("Usuario: ").strip().lower()
        while usuario is None or usuario == "":
            print("El nombre de usuario no puede estar vacío. Por favor, ingréselo nuevamente.")
            usuario = input("Usuario: ").strip().lower()                
        print("Ingrese su contraseña:")
        contrasena = input("Contraseña: ").strip()
        while contrasena is None or contrasena == "":
            print("La contraseña no puede estar vacía. Por favor, ingrésela nuevamente.")
            contrasena = input("Contraseña: ").strip()
        validacion = validarLogin(usuario, contrasena)
        if validacion:
            print("Inicio de sesión exitoso.")
        else:
            print("Nombre de usuario o contraseña incorrectos.")
        return validacion, usuario
    except Exception as e:
        print(f"Error: {e}")
        return None 