from main_server import Raspberry
from threading import Thread
import time


def cambiarConfiguracion(raspberry:Raspberry):
    time.sleep(4)
    
    # Cambio la configuracion de la Base de datos



def server_test():
    raspberry = Raspberry()
    raspberry.set_HostIp("127.0.0.1")
    raspberry.set_Port(5011)
    raspberry.setStatus(20)
    raspberry.start_status20()

    new_thread = Thread(target=cambiarConfiguracion, args=(raspberry,))
    new_thread.start()

if __name__ == "__main__":
    """
    Inicializar el servidor
    """
    server_test()