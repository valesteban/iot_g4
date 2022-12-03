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

# TAREA 2 -----------------------------------------------------------------------------------------


#  Conexión UDP 
#  - status = 23
#  - protocolos -> 1-2-3-4-5
#  - Raspeberry detiene conexion (interfaz gráfica)
def protocolo_udp(host,port):
    print(f" host : {host} \n puerto : {port}")

    while(True):
        print(f"creo socket")

        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
            s.settimeout(10)
            s.bind((host,port))
            print(f"Escuchando UDP en el host : {host} y puerto : {port}")
            
        
            raw_data = b""

            # while(True):
            #     try:
            #         raw_fragment ,addr = s.recvfrom(1024)
            #         if raw_fragment == b'\0':
            #             print("Llegarón todos los fragmentos")
            #             break
            #         else:
            #             raw_data += raw_fragment
            #             s.sendto(b'\1',addr)
            #     except TimeoutError:
            #         raise
            #     except Exception:
            #         raise
            try:
                data ,addr= s.recvfrom(1024)
                print(f"La data que llego -> {data.decode()}")
            except Exception as e:
                print(e,file=sys.stderr) 
                break

            # ENVIA PAQUETE DE LA 
            #por mientras una tupla
            data_envi = (23,            # STATUS
                        False           # STOP
                        )
            s.sendto(str(data_envi).encode(), addr) 

            #SI DATA ENVIADA PIDE PARAR (por interfaz) 
            #break 

            #SI DATA ENVIADA CAMBIA STATUS 20
            #retornamos 20 para que la funcion main se encarge de llamar
            ##a la funcion tcp_configuracion()


            #SI DATA ENVIADA CAMBIA STATUS A 0
            #retornamos 0 para que la funcion main se encarge de llamar
            ##a la funcion ble_configuracion()


            s.close()
            print("Se desconectó socket")  

