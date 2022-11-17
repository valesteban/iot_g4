#!/usr/bin/python3
# -- coding: utf-8 --
import socket
from xmlrpc.client import TRANSPORT_ERROR
import json
import sys

from db import DB
from desempaquetamiento import Protocol
from desempaquetamiento import decode_pkg, print_hex
from ServerProtocols.TCP import TCPRaspServer
from ServerProtocols.UDP import UDPRaspServer


# "192.168.5.177"  # Standard loopback interface address (localhost)
HOST = "192.168.28.1" #"localhost"
PORT = 5010  # Port to listen on (non-privileged ports are > 1023)

# host | user | pass | database
db = DB("localhost", "iot4", "12345678", "tarea1")


def iniciar_servidor():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((HOST,PORT))
    s.listen()
    print("esta listening")
    conn,addr = s.accept()
    
    print(f"Conectado con {addr}")
    while True:
        try:
            recibido = conn.recv(1024).decode()
            print(f"lo recibido del cliente -> {recibido}")
        except:
            print("fallo algo al recibir paquete por socket")
            break
        
        # host | user | pass | database
        db = DB("localhost", "iot4", "12345678", "tarea1")
        # ((id_protocol, transport_layer))
        protocol_config = db.get_protocol()
        protocol_config = protocol_config[0] # Obtengo la ultima configuracion
        ID_PROTOCOL = protocol_config[0]
        TRANSPORT_LAYER = protocol_config[1]
        
        
        protocol_config_data = str(protocol_config).encode()
        if not protocol_config_data:
            break
        try:
            print(f"-- Protocolo y Transporte a usar: {protocol_config} --")
            conn.sendall(protocol_config_data)
        except:
            print("fallo algo al tratar de enviar paquete por socket")
            break  
        if len(protocol_config_data) >0:
            break
    s.shutdown(socket.SHUT_RDWR)
    conn.close()
              
    # TCP
    if TRANSPORT_LAYER == 0:
        TCPRaspServer.run_tcp_protocol(HOST, PORT, ID_PROTOCOL)
    # UDP
    else:           
        UDPRaspServer.run_udp_protocol(HOST, PORT)

  
if __name__ == "__main__":
    """
    Inicializar el servidor
    """
    iniciar_servidor()
