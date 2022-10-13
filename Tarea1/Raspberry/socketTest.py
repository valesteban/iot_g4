import socket

HOST = "192.168.28.1" # as both code is running on same pc
PORT = 5010 # socket server PORT number

def echo_client_test():
    """
    Crea una conexion echo entre el cliente y el servidor.
    """

    client_socket = socket.socket()  # instantiate
    client_socket.connect((HOST, PORT))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection

def client_recv_test():
    """
    Crea una conexion que solo recibe respuesta del servidor
    """

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket.connect((HOST, PORT))  # connect to the server

    while True:
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal

        if data:
            break
 
    client_socket.close()  # close the connection

def client_send_recv():
    """
    Crea una conexion echo entre el cliente y el servidor.
    """
    client_socket = socket.socket()  # instantiate
    client_socket.connect((HOST, PORT))  # connect to the server

    message ="owoo"  # take input""
    client_socket.send(message.encode())  # send message
    data = client_socket.recv(1024).decode()  # receive response

    print('Received from server: ' + data)  # show in terminal
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_recv_test()
