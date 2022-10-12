import socket
from xmlrpc.client import TRANSPORT_ERROR
import db
import json

# "192.168.5.177"  # Standard loopback interface address (localhost)
HOST = "192.168.28.1" #"localhost"
PORT = 5010  # Port to listen on (non-privileged ports are > 1023)

#cosas por mientras reemplazando bbdd
# 0 = TCP | 1 = UDP
ID_PROTOCOL =   0         #  0,1,2,3,4 
TRANSPORT_LAYER =  0       # 0 = TCP | 1 = UDP

#---TCP--CONNECTION ----------------------------------------------------------------------

def iniciar_servidor() -> None:
    """
    Inicializa el servidor con una conexion TCP con el ESP32.

    Cuando se logra la conexion, se realiza una consulta a la base de datos
    preguntando por el protocolo a usar y el tipo de conexion.
    """
    
    print("Hacer conexion TCP")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Listening on {HOST}:{PORT}")
    while True:
        # conn is a new socket object usable to send and receive data on the connection.
        # address is the address bound to the socket on the other end of the connection.
        conn, addr = s.accept()
        try:
            print(f'Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}')

            # Consulta BD (2) 
            # TODO
            data = db.get_protocol()
            # Enviar datos
            try:
                s.sendall(json.dumps(data).encode())
                print(f"Data {data} enviada")
                break
            except:
                print("Error al  enviar paquete del servidor")
        finally:
            # Clean up the connection
            conn.close()
        
#-----------------------------------------------------------------------------------------

"""

#AQUI IRA UNA FUNCION QUE REVISA QUE TIPO DE PROTOCOLO OCUPAR Y SI OCUPAR UDP O TCP
if TRANSPORT_LAYER == 0: #TCP

    Crea una conexion TCP 

    
    print("Hacer conexion TCP")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #TCP
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on {HOST}:{PORT}")
        # conn is a new socket object usable to send and receive data on the connection.
        # address is the address bound to the socket on the other end of the connection.
        conn, addr = s.accept()
        print(f'Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}')

        
        data = conn.recv(1024)
        if data == b'':
            print(f"Termino no data {data}")
        print(f"Recibido {data}")
        
else:           #UDP
    print("Hacer conexion UDP")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"Listening for UDP packets in {HOST}:{PORT}")
        
        data = s.recv(1024)
        if data == b'':
            print(f"No llego na-> {data}")
        print(f"Recibido -> {data}")
        s.close()
        print("Desconectado")  

"""



#INICIAR CONEXION TCP O UDP


#IR GUARDANDO PAQUETES EN BBDD


if __name__ == "__main__":
    """
    Inicializar el servidor
    """
    iniciar_servidor()