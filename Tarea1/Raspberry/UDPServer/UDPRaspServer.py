import socket

UDP_IP = "192.168.5.177"# "localhost" 
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
