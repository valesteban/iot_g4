from ast import While
from typing import Tuple
from db import DB


def change_db_config(id_protocol:int,transport_layer:int) -> None:
    """
        Cambia la configuracion de la BBDD
    """

    # host | user | pass | database
    db = DB("localhost", "iot4", "12345678", "tarea1")
    db.change_config(id_protocol, transport_layer)

def return_db_config() -> Tuple:
    # host | user | pass | database
    db = DB("localhost", "iot4", "12345678", "tarea1")
    return db.return_config()



if __name__ == "__main__":
    """
    Inicializar script para cambiar la configuracion.

    """

    print("----- Opciones para la BBDD ----- ")
    print("[1] Cambiar Configuracion\n[2] Ver Configuracion")
    opcion = int(input("Elija una opcion: "))

    if opcion != 2:
        print("----- CAMBIAR LA CONFIGURACION DE LA BBDD -----")

        new_id_protocol = input("Nuevo ID_PROTOCOL: ")
        new_transport_layer = input("Nuevo TRANSPORT_LAYER: ")

        print(f"Cambiando la configuracion por: ({new_id_protocol}, {new_transport_layer})")
        change_db_config(int(new_id_protocol), int(new_transport_layer))

        print("----- NUEVA CONFIGURACION AGREGADA -----")
    else:
        print("----- VER LA CONFIGURACION -----")
        config = return_db_config()
        print(f"Configuracion actual: {config}")


        


