import socket

'''

import socket

UDP_IP = "192.168.28.1"# "localhost" 
UDP_PORT = 5010

sUDP = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sUDP.bind((UDP_IP, UDP_PORT))


print(f"Listening for UDP packets in {UDP_IP}:{UDP_PORT}")
while True:

    while True:
        payload, client_address = sUDP.recvfrom(1)
        print("Echoing data back to " + str(client_address) + ": " + payload)
        sent = sUDP.sendto(payload, client_address)

'''
HOST = "192.168.28.1"
PORT = 5010

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(3)           #cantidad clientes que puede escichar al mismo tiempo
    print(f"Listening for UDP packets in {HOST}:{PORT}")

    conn, addr = s.accept()  #acepta nuevas conexiones
    with conn:
        print(f"Connected by {addr}")


        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            conn.send(data)

        conn.close()
        print("Desconectado")    

