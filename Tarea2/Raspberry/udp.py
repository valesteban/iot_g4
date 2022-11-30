import sys
import socket

import db
from desempaquetamiento import decode_pkg, print_hex
from utils import get_protocol_values


def run_udp_protocol(IP_HOST, PORT):
    print("Hacer conexion UDP")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((IP_HOST, PORT))
        print(f"Listening for UDP packets in {IP_HOST}:{PORT}")

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
                        print("All fragments received!\n")
                        break
                    else:
                        raw_data += raw_fragment
                        # enviar confirmación de que llegó el paquete
                        s.sendto(b'\1', addr)
                except TimeoutError:
                    raise
                except Exception:
                    raise
                # ojito, quizás se recibió un paquete :eyes: 
            try:
                data = decode_pkg(raw_data)
            except Exception as e:
                print(e, file=sys.stderr)
                continue
            # Info del paquete:
            protocol_values = get_protocol_values(data)
            print(f"PROTOCOL_DATA")
            print(protocol_values)

            # Guarda todo lo necesario en la base de datos
            db.save_data(protocol_values)
            db.save_log(protocol_values)

            # VA A BUSCAR LOS VALORES DE LA BBDD Y ENVIARSELO AL CLIENTE, PORQUE CUANDO CAMBIEN 
            # AHI EL CLIENTE PARARA LA EJECUCION

            # host | user | pass | database
            db = db.DB("localhost", "iot4", "12345678", "tarea1")
            # ((id_protocol, transport_layer))
            protocol_config = db.get_protocol()
            print(f"PROTOCOL_CONFIG: {protocol_config}")  #q envie de la misma forma porq asi lo parsie ya 
            protocol_config = protocol_config[0] #q envie de la misma forma porq asi lo parsie ya 
            ID_PROTOCOL = protocol_config[0]
            TRANSPORT_LAYER = protocol_config[1]
            protocol_config_data = str(protocol_config).encode()
            
            s.sendto(protocol_config_data, addr)

        s.close()
        print("SOCKET UDP CERRADO")  
    print("FIN CONEXION UDP")    