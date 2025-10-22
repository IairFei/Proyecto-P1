import datetime


def log(funcion, tipoMensaje, mensaje):
    try:
        if tipoMensaje not in ["INFO", "ERROR", "WARNING"]:
            raise ValueError("Tipo de mensaje no válido. Use 'INFO', 'ERROR'.")
        if tipoMensaje == "INFO" or tipoMensaje == "WARNING":
            with open("ETAPA2/Logs/log.txt", "a", encoding="utf-8") as file:
                file.write("\n" + str(datetime.datetime.now()) + f" - {funcion} - {tipoMensaje}: {mensaje}\n")  
        elif tipoMensaje == "ERROR":
            with open("ETAPA2/Logs/errorLogs.txt", "a", encoding="utf-8") as file:
                file.write("\nFecha y hora: " + str(datetime.datetime.hour())+":"+ str(datetime.datetime.min())+":"+str(datetime.datetime.second()) + "\n")
                file.write(f"Función: {funcion}\n")
                file.write(f"Error: {mensaje}\n")
                file.write("-" * 50 + "\n")
    except Exception as e:
        print(f"SYSTEM: Error al escribir en el log {e}")
        with open("ETAPA2/Logs/errorLogs.txt", "a", encoding="utf-8") as file:
            file.write("\nFecha y hora: " + str(datetime.datetime.now()) + "\n")
            file.write(f"Error: {Exception}\n")
            file.write(f"Detalles del error: {e}\n")
            file.write("-" * 50 + "\n")