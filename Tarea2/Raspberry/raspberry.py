
import ipaddress
import time
from db import DB
import socket
import json

# Atributos
# status: int
class Raspberry:
    """
        Clase que representa la Raspberry
    """

    def __init__(self) -> None:
        self.__configuracion:tuple = None
        self.__nueva_configuracion:tuple = None

    def setConfiguracion(self, configuracion:tuple) -> None:
        self.__configuracion = configuracion
    
    def set_nueva_configuracion(self, nueva_configuracion:tuple) -> None:
        self.__nueva_configuracion = nueva_configuracion

    def get_current_configuracion(self) -> tuple:
        return self.__configuracion

    def get_current_status(self) -> int:
        return self.__configuracion[1]

    def get_HOST_IP(self) -> str:
        return str(ipaddress.IPv4Address(self.__configuracion[10]))

    def get_UDP_PORT(self) -> int:
        return self.__configuracion[9]

    def get_TCP_PORT(self) -> int:
        return self.__configuracion[8]


    def actualizarConfiguracion(self):
        """
            Metodo que se llama cuando hay un cambio en la Configuracion por parte de la UI
        """

        # Hago la consulta la base de datos

        # host | user | pass | database
        db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")
        nueva_configuracion = db.get_all_config()[0]

        self.__nueva_configuracion = nueva_configuracion
        print("Raspberry: Nueva configuracion seteada:")
        print(nueva_configuracion)
         

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
        s.bind((self.get_HOST_IP(), self.get_TCP_PORT()))
        s.listen()
        print(f"Iniciando Socket HOST_IP: {self.get_HOST_IP()}, PORT: {self.get_TCP_PORT}")
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
        s.bind((self.get_HOST_IP(), self.get_TCP_PORT()))
        s.listen()
        print(f"Iniciando Socket HOST_IP: {self.get_HOST_IP()}, PORT: {self.get_TCP_PORT()}")
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
                data = conn.recv(1024)   

                # Si llega un dato entonces debemos guardarlo y generar un log
                if data:
                    print(f"Data y Log a guardar: {data}")
                    data = json.loads(data)
                    # Creo conexion a la base de datos:
                    # host | user | pass | database
                    db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")

                    # Creo diccionario con la info para el Log
                    log_dict = {}
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

                    # Enviar configuracion
                    conn.sendall(str(self.__nueva_configuracion).encode())
                else:
                    print('no data from', addr)
                    break
                    

        return None
