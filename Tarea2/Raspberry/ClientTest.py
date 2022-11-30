import socket


def run_tcp_client(IP_HOST, PORT):
    print("Inicializar Cliente TCP")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_HOST, PORT))


if __name__ == '__main__':
    IP_HOST = "127.0.0.1" #"localhost"
    PORT = 5010
    run_tcp_client(IP_HOST, PORT)