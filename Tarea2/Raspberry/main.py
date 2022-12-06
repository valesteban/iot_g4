#!/usr/bin/python3
# -- coding: utf-8 --
import ipaddress
import socket
import json

from db import *
# from desempaquetamiento import Protocol
# from desempaquetamiento import decode_pkg, print_hex
from ConnectBLE_test import GUIController
import json
from raspberry import Raspberry


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