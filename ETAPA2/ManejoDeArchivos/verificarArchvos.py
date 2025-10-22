from Logs.logs import log
from pathlib import Path

def verificarArchivos():

    logs_dir = Path("ETAPA2/Logs")
    log_file = logs_dir / "log.txt"
    error_file = logs_dir / "errorLogs.txt"
    try:
        if not logs_dir.exists():
            print("Creando carpeta Logs...")
            logs_dir.mkdir(parents=True, exist_ok=True)
            print("SYSTEM: Carpeta 'Logs' creada.")
    except Exception as e:
        verificarArchivos()
    try:
        if not log_file.exists():
            print("SYSTEM: Creando archivo log.txt...")
            log_file.write_text("Registro de log:\n", encoding="utf-8")
            log("verificarArchivos", "INFO", "Creando archivo log.txt...")
            print("SYSTEM: Archivo 'log.txt' creado.")
            log("verificarArchivos", "INFO", "Archivo log.txt creado.")
    except Exception as e:
        if error_file.exists():
            log("verificarArchivos", "ERROR", f"Error al crear el archivo log.txt: {e}")
        verificarArchivos()
    try:
        if not error_file.exists():
            print("SYSTEM: Creando archivo errorLogs.txt...")
            error_file.write_text("Registro de errores:\n", encoding="utf-8")
            log("verificarArchivos", "INFO", "Creando archivo errorLogs.txt...")
            print("SYSTEM: Archivo 'errorLogs.txt' creado.")
            log("verificarArchivos", "INFO", "Archivo errorLogs.txt creado.")
    except Exception as e:
        if error_file.exists():
            log("verificarArchivos", "ERROR", f"Error al crear el archivo errorLogs.txt: {e}")
        verificarArchivos()
    
