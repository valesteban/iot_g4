import os
from time import sleep
from db import DB
import ipaddress
import pprint

"""
Globales
"""

def delete_db_all() -> None:
    """
        Elimina los logs y datos de DB
    """
    # host | user | pass | database
    db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")
    # Eliminamos los datos de la tabla datos.
    db.delete_all()


"""
Configuracion
"""

def change_db_config(configuration_dict:dict) -> None:
    """
        Cambia la configuracion de la BBDD
    """
    # host | user | pass | database
    db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")
    db.change_config(configuration_dict)

def return_db_config() -> tuple:
    # host | user | pass | database
    db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")
    return db.get_all_config()

def add_default_config() -> None:
    # host | user | pass | database
    db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")
    db.insert_default_configuration()


"""
Logs
"""

def show_db_logs() -> None:
    """
        Muestra los logs de la DB
    """
    try:
        # host | user | pass | database
        db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")
        # Recibimos los datos de la DB
        db_logs = db.get_logs()

        # Printeamos los resultados
        for log in db_logs:
            print(log)
    except:
        print("Error al mostrar los logs")


"""
Data
"""

def show_db_data() -> None:
    """
        Muestra los datos de la BD
    """
    # host | user | pass | database
    db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")
    # Recibimos los datos de la DB
    db_data = db.get_data()

    # Printeamos los resultados
    for data in db_data:
        print(data)

"""
Data acc sensor
"""
def show_db_data_acc_sensor():
    # host | user | pass | database
    db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")
    # Recibimos los datos de la DB
    db_data = db.get_data_acc_sensor()

    # Printeamos los resultados
    for data in db_data:
        print(data)




if __name__ == "__main__":
    """
    Inicializar script para cambiar la configuracion o ver info de la DB.

    """
    while True: 
        print("\n----- Opciones para la BBDD ----- ")
        print("[1] Configuracion\n[2] Log\n[3] Data\n[4] Data Acc sensor\n[5] Borrar todo\n[exit] Salir\n")
        opcion = input("Elija una opcion: ")

        if opcion == "exit":
            print("Bye :)")
            break

        opcion = int(opcion)
        # Configuracion 
        if opcion == 1:
            print("\n===== OPCIONES DE CONFIGURACION =====")
            print("[1] Cambiar configuracion\n[2] Ver Configuracion\n[3] Insertar valor por defecto\n")
            opcion = input("Elija una opcion: ")

            # Cambiar configuracion
            if opcion == "1":
                print("----- CAMBIAR LA CONFIGURACION DE LA BBDD -----\n")

                configuration_dict = {
                    "id_device": 3,
                    "status_conf": 20,
                    "protocol_conf": 2,
                    "acc_sampling": 400,
                    "acc_sensibility": 16,
                    "gyro_sensibility": 200,
                    "bme688_sampling": 4,
                    "discontinuos_time": 420,
                    "tcp_port": 5010,
                    "udp_port": 5010,
                    "host_ip_addr": int(ipaddress.IPv4Address("192.168.28.1")),
                    "ssid": "ssid",
                    "pass": "pass"
                }

                print(f"Cambiando la configuracion por:")
                pprint.pprint(configuration_dict)
                change_db_config(configuration_dict)

                print("----- NUEVA CONFIGURACION AGREGADA -----")
            # Ver configuracion
            elif opcion == "2":
                print("----- VER LA CONFIGURACION -----\n")
                config = return_db_config()
                print(f"Configuracion actual: {config}")
            elif opcion == "3":
                add_default_config()
                print("----- CONFIGURACION POR DEFECTO AGREGADA -----")
                                               
        # Logs
        elif opcion == 2:
            print("\n===== OPCIONES DE LOG  =====")
            print("[1] Mostrar logs actuales\n")
            opcion = input("Elija una opcion: ")
            if opcion == "1":
                show_db_logs()
        # Datos
        elif opcion == 3:
            print("\n===== OPCIONES DE DATA =====")
            print("[1] Mostrar datos actuales\n[2] Mostrar datos continuamente\n")
            opcion = input("Elija una opcion: ")
            if opcion == "1":
                show_db_data()
            elif opcion == "2":
                while True:
                    show_db_data()
                    sleep(5)
                    os.system('clear')
        elif opcion == 4:
            print("\n===== OPCIONES DE DATA ACC SENSOR=====")
            print("[1] Mostrar datos actuales\n[2] Mostrar datos continuamente\n")
            opcion = input("Elija una opcion: ")
            if opcion == "1":
                show_db_data_acc_sensor()
            elif opcion == "2":
                while True:
                    show_db_data_acc_sensor()
                    sleep(5)
                    os.system('clear')
        elif opcion == 5:
            delete_db_all()
            print("!! Log y Datos removidos !!")
        

        







