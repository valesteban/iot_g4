#!/usr/bin/python3
# -- coding: utf-8 --
import socket
from xmlrpc.client import TRANSPORT_ERROR
import json
import sys

# from desempaquetamiento import Protocol
# from desempaquetamiento import decode_pkg, print_hex




# "192.168.5.177"  # Standard loopback interface address (localhost)
HOST = "192.168.28.1" #"localhost"
PORT = 5010  # Port to listen on (non-privileged ports are > 1023)
ID_PROTOCOL = 1

# host | user | pass | database
# db = DB("localhost", "iot4", "12345678", "tarea1")



if __name__ == "__main__":
    """
    Inicializar el servidor
    """
    configuracion_tcp(HOST, PORT)
