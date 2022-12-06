import ipaddress
from raspberry import Raspberry
from db import DB
import time
from threading import Thread
import utils


# int(ipaddress.IPv4Address("192.168.28.1"))
CONFIGURACION = (3,20,1,400,16,200,4,420,5010,5011,"192.168.28.1","iot4","12345678")
NUEVA_CONFIGURACION = (3,21,1,400,16,200,4,420,5010,5011,"192.168.28.1","iot4","12345678")


def cambiarConfiguracion(raspberry:Raspberry):
    print("INICIANDO SLEEP THREAD")
    time.sleep(12)

    print("Thread:Agregando nueva configuracion:")
    nueva_configuracion = NUEVA_CONFIGURACION
    # Cambio la configuracion de la Base de datos
    db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")
    db.change_config(utils.parse_config(nueva_configuracion))
    print("Thread: CONFIGURACION CAMBIADA")
    raspberry.actualizarConfiguracion()


def test_status_20(raspberry):

    new_thread = Thread(target=cambiarConfiguracion, args=(raspberry,))
    new_thread.start()
    

    raspberry.start_status20()

    return None


def test_status_21(raspberry):
    raspberry.start_status21()


def test_status_23(raspberry):
    raspberry.start_status23()
    


if __name__ == "__main__":
    """
    Inicializar el servidor
    """
    raspberry = Raspberry()
    configuracion = CONFIGURACION
    raspberry.setConfiguracion(configuracion)
    raspberry.set_nueva_configuracion(configuracion)

    
    while True:
        status = raspberry.get_current_status()
        print(f"main: Iniciando status {status}")
        if status == 20:
            # == Status 20 ==
            test_status_20(raspberry)
        elif status == 21:
            # == Status 21 ==
            test_status_21(raspberry)

        elif status == 23:
            # == Status 23 ==
            test_status_23(raspberry)
        else:
            break