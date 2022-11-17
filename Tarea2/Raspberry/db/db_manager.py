import os
from time import sleep
from db import DB


def change_db_config(id_protocol:int,transport_layer:int) -> None:
    """
        Cambia la configuracion de la BBDD
    """
    # host | user | pass | database
    db = DB("localhost", "iot4", "12345678", "tarea1")
    db.change_config(id_protocol, transport_layer)

def return_db_config() -> tuple:
    # host | user | pass | database
    db = DB("localhost", "iot4", "12345678", "tarea1")
    return db.return_config()

def show_db_data() -> None:
    """
        Muestra los datos de la BD
    """
    try:
        # host | user | pass | database
        db = DB("localhost", "iot4", "12345678", "tarea1")
        # Recibimos los datos de la DB
        db_data = db.get_data()

        # Printeamos los resultados
        for data in db_data:
            print(data)
    except:
        print("Error al mostrar los datos")

def show_db_logs() -> None:
    """
        Muestra los logs de la DB
    """
    try:
        # host | user | pass | database
        db = DB("localhost", "iot4", "12345678", "tarea1")
        # Recibimos los datos de la DB
        db_logs = db.get_logs()

        # Printeamos los resultados
        for log in db_logs:
            print(log)
    except:
        print("Error al mostrar los logs")

def delete_db_data() -> None:
    """
        Elimina los datos de la tabla data
    """
    # host | user | pass | database
    db = DB("localhost", "iot4", "12345678", "tarea1")
    # Eliminamos los datos de la tabla datos.
    db.delete_all_data()

def delete_db_logs() -> None:
    """
        Elimina los logs que hay en la tabla
    """
    # host | user | pass | database
    db = DB("localhost", "iot4", "12345678", "tarea1")
    # Eliminamos los logs de la base de datos.
    db.delete_all_logs()


if __name__ == "__main__":
    """
    Inicializar script para cambiar la configuracion o ver info de la DB.

    """


    while True: 
        print("\n----- Opciones para la BBDD ----- ")
        print("[1] Configuracion\n[2] Datos\n[3] Logs\n[exit] Salir\n")
        opcion = input("Elija una opcion: ")

        if opcion == "exit":
            print("Bye :)")
            break

        opcion = int(opcion)
        # Configuracion 
        if opcion == 1:
            print("\n===== OPCIONES DE CONFIGURACION =====")
            print("[1] Cambiar configuracion\n[2] Ver Configuracion\n")
            opcion = input("Elija una opcion: ")

            # Cambiar configuracion
            if opcion == "1":
                print("----- CAMBIAR LA CONFIGURACION DE LA BBDD -----\n")

                new_id_protocol = input("Nuevo ID_PROTOCOL: ")
                new_transport_layer = input("Nuevo TRANSPORT_LAYER: ")

                print(f"Cambiando la configuracion por: ({new_id_protocol}, {new_transport_layer})")
                change_db_config(int(new_id_protocol), int(new_transport_layer))

                print("----- NUEVA CONFIGURACION AGREGADA -----")
            # Ver configuracion
            elif opcion == "2":
                print("----- VER LA CONFIGURACION -----\n")
                config = return_db_config()
                print(f"Configuracion actual: {config}")                    
            
        # Datos
        elif opcion == 2:
            print("\n===== OPCIONES DE DATOS =====")
            print("[1] Mostrar datos actuales\n[2] Mostrar datos continuamente\n[3] Eliminar todos los datos (Borrar primero los logs)")
            opcion = input("Elija una opcion: ")
            if opcion == "1":
                show_db_data()
            elif opcion == "2":
                while True:
                    show_db_data()
                    sleep(10)
                    os.system('clear')
            elif opcion == "3":
                delete_db_data()
                print("Datos eliminados")
        # Logs
        elif opcion == 3:
            print("\n===== OPCIONES DE LOGS  =====")
            print("[1] Mostrar logs actuales\n[2] Borrar los logs\n")
            opcion = input("Elija una opcion: ")
            if opcion == "1":
                show_db_logs()
            elif opcion == "2":
                delete_db_logs()
                print("Logs eliminados")







