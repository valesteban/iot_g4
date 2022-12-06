#!/usr/bin/python3
# -- coding: utf-8 --
import ipaddress
import socket
import json
from threading import Thread

from db import *
# from desempaquetamiento import Protocol
# from desempaquetamiento import decode_pkg, print_hex
from ConnectBLE_test import GUIController
import json
from raspberry import Raspberry

import time
import utils
NUEVA_CONFIGURACION = (3,21,1,400,16,200,4,420,5010,5011,"192.168.28.1","iot4","12345678")
def cambiarConfiguracion(raspberry:Raspberry):
    print("INICIANDO SLEEP THREAD")
    time.sleep(20)

    print("Thread:Agregando nueva configuracion:")
    nueva_configuracion = NUEVA_CONFIGURACION
    # Cambio la configuracion de la Base de datos
    db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")
    db.change_config(utils.parse_config(nueva_configuracion))
    print("Thread: CONFIGURACION CAMBIADA")
    raspberry.actualizarConfiguracion()


def init_server():
    
    print("main: Iniciando Status 0")
    raspberry = Raspberry()

    # == STATUS 0 ==
    # Buscamos dispositivos ESP BLE
    # Y le entregamos la configuracion
    gui_controller = GUIController(raspberry)
    print("main: Buscando dispositivos BLE...")
    gui_controller.actualizarMacs() # Buscamos dispositivos BLE (ESP)
    print("main: Iniciando conexion con la ESP...")
    # Iniciamos conexion con la ESP, enviamos la configuracion 
    # y seteamos la configuracion en la raspberry
    gui_controller.configSetup()

    # Iniciamos el servidor dependiendo del status
    while True:
        status = raspberry.get_current_status()
        print(f"main: Iniciando status {status}")
        if status == 20:

            # Simulacion de Cambio de config UI
            new_thread = Thread(target=cambiarConfiguracion, args=(raspberry,))
            new_thread.start()
            # == Status 20 ==
            raspberry.start_status20()
        elif status == 21:
            # == Status 21 ==
            raspberry.start_status21()
        elif status == 23:
            # == Status 23 ==
            raspberry.start_status23()
        else:
            break
        """
        # TODO Agregar el resto de estadus

        elif status == 22:
            # == Status 22 ==
            raspberry.start_status22()
        elif status == 23:
            # == Status 23 ==
            raspberry.start_status23()
        elif status == 30:
            # == Status 30 ==
            raspberry.start_status30()
        elif status == 31:
            # == Status 31 ==
            raspberry.start_status31()
        """
            
if __name__ == "__main__":
    """
    Inicializar el servidor
    """
    init_server()