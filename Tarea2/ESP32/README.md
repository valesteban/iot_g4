# ESP32 Client

Se incluye el proyecto de ej para ambos tipos de Cliente (TCP y UDP)

Se recomienda tener 4 archivos con el programa, de la siguiente forma

**Cliente**
|  
|---------- Main  
|---------- Conexiones  
|---------- Empaquetamiento  
|---------- Sensores  

### Main:
 Usara a los demás para realizar el flow de envio de datos, siendo el programa main del proyecto.
### Conexiones:
 Definira todas las funciones para lo que tenga que ver con redes, esto se recomienda que sea:  
    - Wifi_connect(Name_SSID, PASS), función para realizar la conexión wifi, esto se realiza dentro del ejemplo.  
    - TCP_connect/UDP_connect(IPV4, PORT), realiza la conexión con un socket TCP/UDP.  
    - TCP_send/UDP_send(data, large), manda los datos de tamaño large.  
    - TCP_close/UDP_close, cierra el socket
### Empaquetamiento:
 Tendra las funciones necesarias para armar el paquete de envio, este puede ser sola una función si prefiere incluirlo en otro de los archivos. Llamara a todo lo necesario desde Sensores. Se recomienda tener:  
    - Header(protocolo), crea el header para cierto protocolo.  
    - Body(protocolo), llama a las funciones de generación de dato y arma el cuerpo del mensaje.  
    - Packet(protocolo), usando las funciones anteriores arma el paquete entero y lo deja preparado para envio.  
### Sensores:
 Genera todos los números necesarios para los datos, simulando ser sensores.
