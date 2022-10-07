# Raspberry Server

Se incluye servidores Echo de ej para cada tipo de socket (TCP y UDP)

Lo que necesitan para esta parte es programar las funcionalidades de creación de sockets y la recepción del paquete, junto con su desempaquemiento y guardardado en la base de datos.

Se recomienda tener la siguiente estructura de proyecto

**Server**
|  
|-------- ServerMain  
|-------- Desempaquetamiento  

- ServerMain: Contiene la creación de socket, la recepción de paquete. Importara y usara las funciones de Desempaquetamiento para lo demás.
- Desempaquetamiento: Simplemente trae todas las funciones para recibir el paquete, abrirlo y guardarlo en una base de datos. Recuerde que en el enunciado esta descrito como se conforman los paquete