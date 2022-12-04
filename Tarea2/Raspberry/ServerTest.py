import ipaddress
from main_server import Raspberry
from db import DB
import time
from threading import Thread
import socket


def tcp_socket_server():
    HOST_IP = "127.0.0.1"
    PORT = 5012
    # Iniciamos conexion TCP
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((HOST_IP, PORT))
    s.listen()
    print(f"Iniciando Socket HOST_IP: {HOST_IP}, PORT: {PORT}")
    print("Listening.....")
    conn,addr = s.accept()
    print(f"Conectado con {addr}")


def cambiarConfiguracion(raspberry):
    print("INICIANDO SLEEP THREAD")
    time.sleep(10)

    
    # Cambio la configuracion de la Base de datos
    db = DB("localhost", "iot4", "12345678", "IoT_Tarea2")
    db.insert_default_configuration()
    raspberry.actualizarConfiguracion()
    print("CONFIGURACION CAMBIADA")


def server_test():
    raspberry = Raspberry()
    raspberry.set_HostIp("192.168.28.1")
    raspberry.set_Port(5011)
    configuracion = (3,23,2,400,16,200,4,420,5011,5011,int(ipaddress.IPv4Address("192.168.28.1")),"ssid","pass")
    raspberry.setConfiguracion(configuracion)
    raspberry.set_nueva_configuracion(configuracion)

    new_thread = Thread(target=cambiarConfiguracion, args=(raspberry,))
    new_thread.start()

    
    raspberry.start_status20()


if __name__ == "__main__":
    """
    Inicializar el servidor
    """
    server_test()
