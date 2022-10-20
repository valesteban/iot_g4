#!/usr/bin/python3
# -- coding: utf-8 --
import socket
from xmlrpc.client import TRANSPORT_ERROR
from desempaquetamiento import Protocol
from db import DB
import json
from desempaquetamiento import decode_pkg, print_hex

def get_protocol_values(data: Protocol) -> dict:
    """
        Funcion auxiliar que procesa un protocollo y obtiene
        toda la info necesaria para ser guardada en la DB
    """

    header = data.get_header()
    id_device = header.get_device_id()
    mac = header.get_mac()
    transport_layer = header.get_transport_layer()
    id_protocol = header.get_protocol_id()

    battery = data.get_battery()
    timestamp = battery.get_timestamp()

    protocol_data = json.dumps(data.get_protocol_data())

    protocol_values = {
        "id_device" : id_device,
        "timestamp" : timestamp,
        "mac": mac,
        "id_protocol": id_protocol,
        "transport_layer": transport_layer,
        "data" : protocol_data
    }

    return protocol_values


# "192.168.5.177"  # Standard loopback interface address (localhost)
HOST = "192.168.28.1" #"localhost"
PORT = 5010  # Port to listen on (non-privileged ports are > 1023)

# host | user | pass | database
db = DB("localhost", "iot4", "12345678", "tarea1")

#---TCP--CONNECTION ----------------------------------------------------------------------

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
              

    if TRANSPORT_LAYER == 0: #TCP
        
        print("Hacer conexion TCP")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on {HOST}:{PORT}")
        # conn is a new socket object usable to send and receive data on the connection.
        # address is the address bound to the socket on the other end of the connection.
        conn, addr = s.accept()
        print(f'Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}')

        while(True):
            if (ID_PROTOCOL == 4):
                raw_data = b""
                while(True):  #paquetes fragmentados
                    try: 
                        raw_fragment = conn.recv(1024)
                        if raw_fragment == b'\0':
                            break
                        else:
                            raw_data += raw_fragment
                            print("Data recibida como bytes: ")
                            print_hex(raw_fragment.hex())
                    except TimeoutError:
                        raise
                    except Exception:
                        raise
                    # ojito, quizás se recibió un paquete :eyes: 
                data = decode_pkg(raw_data)
                        
            else:
                #otros protocolos
                raw_data = conn.recv(1024)     
                print("Data recibida como bytes: ")
                print_hex(raw_data.hex())
                try:
                    data = raw_data.decode()
                except:
                    # ojito, quizás se recibió un paquete :eyes:
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
            db.save_data(protocol_values)
            db.save_log(protocol_values)


        print("CHAO")
            
    else:           
        print("Hacer conexion UDP")

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((HOST, PORT))
            print(f"Listening for UDP packets in {HOST}:{PORT}")

            while(True):
                # data,addr = s.recvfrom(1024)
                # if data == b'':
                #     print(f"No llego na-> {data } y {addr}")
                #     break
                # print(f"Paquete recibido: {data}")

                raw_data = b""
                while(True):  #paquetes fragmentados
                    try: 
                        raw_fragment,addr = s.recvfrom(1024)
                        if raw_fragment == b'\0':
                            break
                        else:
                            raw_data += raw_fragment
                            print("Data recibida como bytes: ")
                            print_hex(raw_fragment.hex())
                            # enviar confirmación de que llegó el paquete
                            s.sendto(b'\1', addr)
                    except TimeoutError:
                        raise
                    except Exception:
                        raise
                    # ojito, quizás se recibió un paquete :eyes: 
                data = decode_pkg(raw_data)

                #VA A BUSCAR LOS VALORES DE LA BBDD Y ENVIARSELO AL CLIENTE, PORQUE CUANDO CAMBIEN 
                #AHI EL CLIENTE PARARA LA EJECUCION
                # host | user | pass | database
                db = DB("localhost", "iot4", "12345678", "tarea1")
                # ((id_protocol, transport_layer))
                protocol_config = db.get_protocol()
                print(f"PROTOCOL_CONFIG: {protocol_config}")  #q envie de la misma forma porq asi lo parsie ya 
                protocol_config = protocol_config[0] #q envie de la misma forma porq asi lo parsie ya 
                ID_PROTOCOL = protocol_config[0]
                TRANSPORT_LAYER = protocol_config[1]
                protocol_config_data = str(protocol_config).encode()
                
                s.sendto(protocol_config_data, addr)

            s.close()
            print("Desconectado")  
        print("CHAO")    

  
if __name__ == "__main__":
    """
    Inicializar el servidor
    """
    iniciar_servidor()
