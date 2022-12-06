import random
import socket
import json

"""
Modulo de testeo
"""

class TCP_Client_Test:

    def __init__(self, HOST_IP, PORT) -> None:
        self.HOST_IP = HOST_IP
        self.PORT = PORT
        

    def test_status20_client(self):
        print("Inicializar Cliente TCP")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST_IP, self.PORT))
        print(f"Conectado a IP: {self.HOST_IP}, PORT: {self.PORT}")


        while True:
            # Haremos un eco hasta que se envie el mensaje del cambio
            server_data = s.recv(1024)
            if not server_data:
                break
            elif server_data.decode() != "Ningun Cambio":
                print("Nueva configuracion recibida")
                # Debo cambiar la configuracion
                s.sendall("Nueva configuracion recibida".encode())
                break
            else:
                print(f"Data recibida del server: {server_data}")
                s.sendall(server_data)

        s.close()
        

    def test_status21_client(self):
        print("Inicializar Cliente TCP Status 21")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST_IP, self.PORT))
        print(f"Conectado a IP: {self.HOST_IP}, PORT: {self.PORT}")

        while True:

            data_test = {
                "id_device": 3,
                "status_report": 21,
                "protocol_report": 0,
                "battery_level": 100,
                "conf_peripheral": 3123311,
                "time_client": 9999,
                "configuration_id_device": 3,
                "data": {
                    "test": "data de testeo"
                }
            }
            # Envio los datos dependiendo del protocol_conf
            s.sendall(json.dumps(data_test).encode())

            s.recv(1024)

            r = random.random()
            if r < 0.2:
                break

        s.close()

class UDP_Client_Test():

    def __init__(self, HOST_IP, UDP_PORT) -> None:
        self.HOST_IP = HOST_IP
        self.PORT = UDP_PORT
    
    def test_status23_client(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        while True:
            s.sendto("test".encode(), (self.HOST_IP, self.PORT))
            s.recvfrom(1024)
            break
        
        s.close()


if __name__ == '__main__':
    IP_HOST = "192.168.28.1" 
    TCP_PORT = 5010
    UDP_PORT = 5011
    
    # tcp_client = TCP_Client_Test(IP_HOST, TCP_PORT)
    # tcp_client.test_status20_client()

    udp_client = UDP_Client_Test(IP_HOST, UDP_PORT)
    udp_client.test_status23_client()