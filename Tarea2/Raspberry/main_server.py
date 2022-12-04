#!/usr/bin/python3
# -- coding: utf-8 --
import socket
from xmlrpc.client import TRANSPORT_ERROR
import json
import sys

from db import *
# from desempaquetamiento import Protocol
# from desempaquetamiento import decode_pkg, print_hex
import ConnectBLE
import json



# Atributos
# status: int
class Raspberry:

    def __init__(self) -> None:
        self.__configuracion:tuple = None
        self.__nueva_configuracion:tuple = None
        self.__HOST_IP = "192.168.28.1"
        self.__PORT = 5010

    def setConfiguracion(self, configuracion:tuple) -> None:
        self.__configuracion = configuracion
    
    def set_nueva_configuracion(self, nueva_configuracion:tuple) -> None:
        self.__nueva_configuracion = nueva_configuracion

    def setStatus(self, status:int) -> None:
        self.__status:tuple = status

    def set_HostIp(self, host_ip):
        self.__HOST_IP = host_ip
        
    def set_Port(self, port):
        self.__PORT = port

    def get_current_status(self):
        return self.__configuracion[1]



    def actualizarConfiguracion(self):
        """
            Metodo que se llama cuando hay un cambio en la Configuracion por parte de la UI
        """

        # Hago la consulta la base de datos

        # host | user | pass | database
        db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")
        nueva_configuracion = db.get_all_config()[0]

        self.__nueva_configuracion = nueva_configuracion
         

    def start_status20(self) -> None:
        """
        El ESP32 tendrá un Cliente TCP y la Raspberry un Servidor TCP (el Ssid, Pass y Port_TCP se
        toman de los valores configurados por la interfaz). En este modo el ESP32 puede actualizar cualquiera
        de los valores de la tabla Parámetros de Configuración a través de una conexión TCP. Los valores
        se adquieren de la tabla config de la DB
        """

        print("== INICIANDO STATUS 20 ==")
        # Iniciamos conexion TCP
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((self.__HOST_IP, self.__PORT))
        s.listen()
        print(f"Iniciando Socket HOST_IP: {self.__HOST_IP}, PORT: {self.__PORT}")
        print("Listening.....")
        conn,addr = s.accept()
        
        print(f"Conectado con {addr}")

        # Mensanje inicial de conexion de la esp32
        # conn.recv(1024)

        # Quedamos esperando hasta que haya un cambio de Configuracion
        while True:
            # Mensaje para mantener conexion

            # Hubo un cambio de configuracion
            if self.__configuracion != self.__nueva_configuracion:
                print("Enviar Cambio de configuracion")
                # Envio la nueva configuracion a la ESP32

                # Obtengo la configuracion y encode()
                data = str(self.__nueva_configuracion).encode()
                conn.sendall(data)
                
                # Cambio la antigua configuracion por la nueva
                self.__configuracion = self.__nueva_configuracion
                self.status = self.__configuracion[1] # Cambio tambien el atributo estado

                conn.recv(1024)
                # Si Hay un cambio de status se debe terminar el ciclo
                if self.get_current_status() != 20:
                    break

            # Si no ha pasado envio un dato vacio
            conn.sendall("Ningun Cambio".encode())
            conn.recv(1024)
        
        print("== FIN STATUS 20 ==")
        s.close()
        return None

                
    def start_status21(self) -> None:
        """
        El ESP32 tendrá un Cliente TCP y la Raspberry un Servidor TCP (Este debe poder iniciarse
        desde la interfaz con la configuración puesta ahí). Según el valor de ID_Protocol es el paquete de
        datos que se transferirá. (protocolos de datos se observan en la Tabla 3). El ESP32 deberá enviar
        este paquete de forma continua hasta que desde la Raspberry se detenga la conexión (desde la interfaz
        gráfica)
        """
        # Iniciamos conexion TCP
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((self.__HOST_IP, self.__PORT))
        s.listen()
        print(f"Iniciando Socket HOST_IP: {self.__HOST_IP}, PORT: {self.__PORT}")
        print("Listening.....")
        conn,addr = s.accept()

        print(f"Conectado con {addr}")

        while True:

                #Protocolos 1 al 4
                # Recibo mensaje de la ESP32 y lo decodifico
                # data = {
                #   "id_device": ,
                #   "status_report": ,
                #   "protocol_report" ,
                #   "batterry_level": ,
                #   "conf_peripheral": ,
                #   "time_client": ,
                #   "configuracion.id_device": ,
                #   "data": {...}  
                # }
                raw_data = conn.recv(1024)   
                data = raw_data.decode()

                # Si llega un dato entonces debemos guardarlo y generar un log
                if data:
                    # Creo conexion a la base de datos:
                    # host | user | pass | database
                    db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")

                    # Creo diccionario con la info para el Log
                    log_dict = {}
                    log_dict["id_device"] = data["id_device"] 
                    log_dict["status_report"] = data["status_report"] 
                    log_dict["protocol_report"] = data["protocol_report"] 
                    log_dict["battery_level"] = data["battery_level"] 
                    log_dict["conf_peripheral"] = data["conf_peripheral"] 
                    log_dict["time_client"] = data["time_client"] 
                    log_dict["configuration_id_device"] = data["id_device"] 

                    db.save_log(log_dict) # Guardo el log


                    # Creo diccionario con la data a guardar
                    data_dict = {}
                    data_dict["id_device"] = data["id_device"]
                    data_dict["data"] = json.dumps(data["data"])
                    data_dict["log_id_device"] = data["id_device"]

                    db.save_data(data_dict) # Guarda la data

                
                else:
                    print('no data from', addr)
                    break
                    

        return None





def init_server():

    raspberry = Raspberry()

    # == STATUS 0 ==
    # Buscamos dispositivos ESP BLE
    # Y le entregamos la configuracion
    gui_controller = ConnectBLE.GUIController(raspberry)
    gui_controller.actualizarMacs() # Buscamos dispositivos BLE (ESP)
    # Iniciamos conexion con la ESP y enviamos la configuracion
    gui_controller.configSetup()


    # Iniciamos el servidor dependiendo del status
    while True:
        status = raspberry.getStatus()
        if status == 20:
            # == Status 20 ==
            raspberry.start_status20()
        elif status == 21:
            # == Status 21 ==
            raspberry.start_status21()
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
            



