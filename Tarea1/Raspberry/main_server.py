import socket

# "192.168.5.177"  # Standard loopback interface address (localhost)
HOST = "192.168.28.1"#"localhost"
PORT = 5010  # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
s.bind((HOST, PORT))
s.listen(5)
print(f"Listening on {HOST}:{PORT}")

conn, addr = s.accept()
print(f'Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}')
data = conn.recv(1024)
if data == b'':
    print(f"termino no data {data}")
print(f"Recibido {data}")
conn.close()
print('Desconectado')

#AQUI IRA UNA FUNCION QUE REVISA QUE TIPO DE PROTOCOLO OCUPAR Y SI OCUPAR UDP O TCP


#INICIAR CONEXION TCP O UDP


#IR GUARDANDO PAQUETES EN BBDD


