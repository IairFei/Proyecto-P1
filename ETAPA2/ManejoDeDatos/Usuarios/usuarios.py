import json


def cambiarRol(nuevoRol, usuario):
    seModficoEnCSV = False
    datos = []
    try:
        with open('ETAPA2/Archivos/usuarios.csv', 'r') as usuarios:
            for linea in usuarios:
                datos.append(linea.strip().split(','))
        for dato in datos:
            if dato[0].strip() == usuario[0].strip():
                dato[2] = nuevoRol
        with open('ETAPA2/Archivos/usuarios.csv', 'w') as usuarios:
            for dato in datos:
                usuarios.write(','.join(dato) + '\n')
        seModficoEnCSV = True
        return seModficoEnCSV
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return None
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

def guardarUsuario(usuarioActual):
    """
    Actualiza un usuario específico en el archivo JSON manteniendo los demás usuarios
    """
    try:
        with open('ETAPA2/Archivos/usuarios.json', 'r') as usuarios:
            datos_sistema = json.load(usuarios)
        
        usuario_encontrado = False
        for i in range(len(datos_sistema['usuarios'])):
            if datos_sistema['usuarios'][i]['usuario'] == usuarioActual['usuario']:
                datos_sistema['usuarios'][i]['id'] = usuarioActual['id']
                datos_sistema['usuarios'][i]['nombre'] = usuarioActual['nombre']
                datos_sistema['usuarios'][i]['apellido'] = usuarioActual['apellido']
                datos_sistema['usuarios'][i]['pack5materias'] = usuarioActual['pack5materias']
                
                datos_sistema['usuarios'][i]['notas'] = {}
                for materia_id, nota_data in usuarioActual['notas'].items():
                    datos_sistema['usuarios'][i]['notas'][materia_id] = {
                        'parcial1': nota_data['parcial1'],
                        'parcial2': nota_data['parcial2'],
                        'final': nota_data['final'],
                        'nota_final': nota_data['nota_final'],
                        'aprobada': nota_data['aprobada'],
                        'recursa': nota_data['recursa']
                    }
                
                datos_sistema['usuarios'][i]['calendario'] = {
                    'Lunes': usuarioActual['calendario']['Lunes'],
                    'Martes': usuarioActual['calendario']['Martes'],
                    'Miercoles': usuarioActual['calendario']['Miercoles'],
                    'Jueves': usuarioActual['calendario']['Jueves'],
                    'Viernes': usuarioActual['calendario']['Viernes']
                }
                
                usuario_encontrado = True
        
        if not usuario_encontrado:
            print(f"Error: Usuario {usuarioActual['usuario']} no encontrado en el archivo")
            return False
        
        with open('ETAPA2/Archivos/usuarios.json', 'w') as usuarios:
            json.dump(datos_sistema, usuarios, indent=4)
        
        return True
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return False

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