import socket
from Tarea2.Raspberry.desempaquetamiento import decode_pkg, print_hex
from Tarea2.Raspberry.utils import get_protocol_values

from db import *

def run_tcp_server(IP_HOST, PORT):
    print("Inicializar Servidor TCP")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP_HOST, PORT))
    s.listen(1) # configure how many client the server can listen simultaneously
    print(f"Listening on {IP_HOST}:{PORT}")
    # conn is a new socket object usable to send and receive data on the connection.
    # address is the address bound to the socket on the other end of the connection.
    conn, addr = s.accept()
    print(f'Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}')

    return s



def run_tcp_protocol(IP_HOST, PORT, ID_PROTOCOL):
    print("Hacer conexion TCP")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    s.bind((IP_HOST, PORT))
    s.listen()
    print(f"Listening on {IP_HOST}:{PORT}")
    # conn is a new socket object usable to send and receive data on the connection.
    # address is the address bound to the socket on the other end of the connection.
    conn, addr = s.accept()
    print(f'Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}')
    while True:
        if (ID_PROTOCOL == 4):
            raw_data = b""
            size = 0
            while(True):  #paquetes fragmentados
                try: 
                    raw_fragment = conn.recv(1024)
                    size += len(raw_fragment)
                    print_hex(raw_fragment.hex())
                    if raw_fragment == b'\0':
                        print("Paquete completo recibido b00")
                        break
                    else:
                        raw_data += raw_fragment
                except TimeoutError:
                    raise
                except Exception:
                    raise
                # ojito, quizás se recibió un paquete :eyes: 
            data = decode_pkg(raw_data)
                    
        else:
            #otros protocolos
            raw_data = conn.recv(1024)   
            print_hex(raw_data.hex())
            data = decode_pkg(raw_data)
                
        if data == b'':
            print(f"Termino no data {data}")

        # Printeamos la data recibida
        print(f"Paquete recibido: {data} \n")

        # Info del paquete:
        protocol_values = get_protocol_values(data)
        print(f"PROTOCOL_DATA")
        print(protocol_values)

        # Guarda todo lo necesario en la base de datos
        # host | user | pass | database
        db = DB("localhost", "iot4", "12345678", "tarea1")
        db.save_data(protocol_values)
        db.save_log(protocol_values)
