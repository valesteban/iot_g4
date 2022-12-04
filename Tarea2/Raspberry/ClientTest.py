import socket


"""
Modulo de testeo
"""

class TCP_Client_Test:

    def __init__(self, HOST_IP, PORT) -> None:
        self.HOST_IP = HOST_IP
        self.PORT = PORT
        

    def run_tcp_client(self):
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
        


if __name__ == '__main__':
    IP_HOST = "192.168.28.1" 
    PORT = 5011
    
    tcp_client = TCP_Client_Test(IP_HOST, PORT)
    tcp_client.run_tcp_client()
    