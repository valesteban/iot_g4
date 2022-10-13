import socket
from xmlrpc.client import TRANSPORT_ERROR
import db
import json

# "192.168.5.177"  # Standard loopback interface address (localhost)
HOST = "192.168.28.1" #"localhost"
PORT = 5010  # Port to listen on (non-privileged ports are > 1023)


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
        
        data = db.get_protocol()
        ID_PROTOCOL = data[0]
        TRANSPORT_LAYER = data[1]
        
        
        data = str(data).encode()
        if not data:
            break
        try:
            conn.sendall(data)
            print(f"lo qu eva a enviar servidor a cliente {data}")
        
        except:
            print("fallo algo al tratar de enviar paquete por socket")
            break  
        if len(data) >0:
            break
    s.shutdown(socket.SHUT_RDWR)
    conn.close()
    
    
        
            
                               

    if TRANSPORT_LAYER == 0: #TCP
        
        print("Hacer conexion TCP")
        s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        print("????")
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on {HOST}:{PORT}")
        # conn is a new socket object usable to send and receive data on the connection.
        # address is the address bound to the socket on the other end of the connection.
        conn, addr = s.accept()
        print(f'Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}')

        while(True):
            data = conn.recv(1024).decode()
            if data == b'':
                print(f"Termino no data {data}")
            print(f"Recibido {data}")

        print("CHAO")
            
    else:           
        print("Hacer conexion UDP")

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((HOST, PORT))
            print(f"Listening for UDP packets in {HOST}:{PORT}")

            while(True):
                data,addr = s.recvfrom(1024)
                if data == b'':
                    print(f"No llego na-> {data } y {addr}")
                    break
                print(f"Recibido -> {data}")

                #VA A BUSCAR LOS VALORES DE LA BBDD Y ENVIARSELO AL CLIENTE, PORQUE CUANDO CAMBIEN 
                #AHI EL CLIENTE PARARA LA EJECUCION
                #podi tal ves enviar solo el valor de transport layer???? es lo unico q se necesita enviar
                data = db.get_protocol()
                ID_PROTOCOL = data[0]
                TRANSPORT_LAYER = data[1]
                data = str(data).encode()
                
                s.sendto(data,addr)



            s.close()
            print("Desconectado")  
        print("CHAO")    




  
if __name__ == "__main__":
    """
    Inicializar el servidor
    """
    iniciar_servidor()