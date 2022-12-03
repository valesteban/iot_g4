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

# TAREA 2 ---------------------------------------------------------------------------------------

# Conexión TCP discontinua 
# - status= 22
# - id_protocols ->1-2-3-4-5
# - según el valor de Discontinuous_Time el ESP32 entrara por ese tiempo en modo Deep_sleep.
# - Raspeberry detiene conexion (interfaz gráfica) 
# - se recomienda que el Discontinuous_Time tenga como unidad minutos y que su valor mínimo sea 1.
def protocolo_tcp_discontinuo(host,port,id_protocol):
    while(True):
        print(f" host : {host} \n puerto : {port}")
        print("Se creo el socket")
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            s.bind((host,port))
            s.listen()

            print(f"Esta escuchando TCP ")
            conn,addr = s.accept()
            print(f"Se conecto {addr[0]} desde el puerto {addr[1]}")

        
            if (id_protocol  == 4):
                raw_data = b""
                size = 0
                # while(True):
                #     try:
                #         raw_fragment = conn.recv(1024)
                #         size += len(raw_fragment)
                #         # print_hex(raw_fragment.hex())
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
            else:
                raw_data = conn.recv(1024)
            
            print(f"Paquete recibido -> {raw_data}")

            data_envi = (23,            # STATUS
                        False           # STOP
                        )
            conn.sendall(str(data_envi).encode())
            print("Se envió")
            
            
            #SI DATA ENVIADA PIDE PARAR (por interfaz) 
            #break 

            #SI DATA ENVIADA CAMBIA STATUS 20
            #retornamos 20 para que la funcion main se encarge de llamar
            ##a la funcion tcp_configuracion()


            #SI DATA ENVIADA CAMBIA STATUS A 0
            #retornamos 0 para que la funcion main se encarge de llamar
            ##a la funcion ble_configuracion()

        conn.close()
        print("Se desconectó socket")  




#  Conexión TCP continua 
#  - status = 21
#  - id_protocols ->1-2-3-4-5
#  - Raspeberry detiene conexion (interfaz gráfica) 
def protocolo_tcp_continuo(host,port,id_protocol):
    print(f" host : {host} \n puerto : {port}")
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((host,port))
        s.listen()

        print(f"Esta escuchando TCP ")
        conn,addr = s.accept()
        print(f"Se conecto {addr[0]} desde el puerto {addr[1]}")

        # Loop enviar y recibir 
        while(True):
            if (id_protocol  == 4):
                raw_data = b""
                size = 0
                # while(True):
                #     try:
                #         raw_fragment = conn.recv(1024)
                #         size += len(raw_fragment)
                #         # print_hex(raw_fragment.hex())
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
            else:
                raw_data = conn.recv(1024)
            
            print(f"Paquete recibido -> {raw_data}")

            data_envi = (23,            # STATUS
                        False           # STOP
                        )
            conn.sendall(str(data_envi).encode())
            print("Se envió")

            #SI DATA ENVIADA PIDE PARAR (por interfaz) 
            #break 

            #SI DATA ENVIADA CAMBIA STATUS 20
            #retornamos 20 para que la funcion main se encarge de llamar
            ##a la funcion tcp_configuracion()


            #SI DATA ENVIADA CAMBIA STATUS A 0
            #retornamos 0 para que la funcion main se encarge de llamar
            ##a la funcion ble_configuracion()


    
    conn.close()
    print("Se desconectó socket")  



def configuracion_tcp(host,puerto,):

    # CREAMOS SOCKET TCP
    print("Creamos socket TCP configuracion")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((host,puerto))
    s.listen()
    print("EScuchando")
    conn,addr = s.accept()
    
    # SE CONECTA CON UN CLIENTE
    print(f"Conectado con {addr}")

    # SACAMOS INFO DE LA INTERFAZ Y LA MANDAMOS

    Status = 21
    ID_Protocol = 1
    BMI270_Sampling  = 10 #(Valores Posibles: 10, 100, 400, 1000)
    BMI270_Acc_Sensibility = 2 #(Valores Posibles: 2,4,8,16)
    BMI270_Gyro_Sensibility = 200 # (Valores posibles: 200, 250, 500)
    BME688_Sampling = 1 #(1,2,3,4)
    Discontinuos_Time = 10
    Port_TCP = 5000
    Port_UDP = 5001
    Host_IP_Addr = "10.13.1.100" 
    SSID_X = "iot4"
    Pass = "12345678"
    data = ( Status,
            ID_Protocol,
            BMI270_Sampling, 
            BMI270_Acc_Sensibility,
            BMI270_Gyro_Sensibility, 
            BME688_Sampling ,
            Discontinuos_Time, 
            Port_TCP ,
            Port_UDP ,
            Host_IP_Addr, 
            SSID_X ,
            Pass
            )
    conn.sendall(str(data).encode())
    conn.close()

    # retornamos valores para que un main llame a la funcion queu creará la nueva funcion
    return data



