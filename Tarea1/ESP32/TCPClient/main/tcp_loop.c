/*
Se creará la conexión TCP con el servidor/raspberry y dependiendo del protocolo que se le pasa
va a empezar a enviar los paquetes
 */
#include "sdkconfig.h"
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <errno.h>
#include <netdb.h>            // struct addrinfo
#include <arpa/inet.h>
#include "esp_netif.h"
#include "esp_log.h"
#if defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
#include "addr_from_stdin.h"
#endif

#if defined(CONFIG_EXAMPLE_IPV4)
#define HOST_IP_ADDR CONFIG_EXAMPLE_IPV4_ADDR
#elif defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
#define HOST_IP_ADDR "192.168.28.1"
#endif

#define PORT 5010

static const char *TAG = "test";
static const char *payload = "Hola soy el tonto ESP32";
char rx_buffer[128];
char host_ip[] = HOST_IP_ADDR;
int addr_family = 0;
int ip_protocol = 0;


    
#if defined(CONFIG_EXAMPLE_IPV4)
        struct sockaddr_in dest_addr;
        inet_pton(AF_INET, host_ip, &dest_addr.sin_addr);
        dest_addr.sin_family = AF_INET;
        dest_addr.sin_port = htons(PORT);
        addr_family = AF_INET;
        ip_protocol = IPPROTO_IP;
#elif defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
        struct sockaddr_storage dest_addr = { 0 };
        ESP_ERROR_CHECK(get_addr_from_stdin(PORT, SOCK_STREAM, &ip_protocol, &addr_family, &dest_addr));
#endif
        //SE CREO EL SOCKET TCP 
        int sock =  socket(addr_family, SOCK_STREAM, ip_protocol);
        if (sock < 0) {
            ESP_LOGE(TAG, "No su pudo crear socket: errno %d", errno);
        }
        ESP_LOGI(TAG, "Socket creado, conectando a %s:%d", host_ip, PORT);

        //CONECTA AL SERVIDOR
        int err = connect(sock, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
        if (err != 0) {
            ESP_LOGE(TAG, "Socket no se pudo conectar: errno %d", errno);
            
        }
        ESP_LOGI(TAG, "Conecxion exitosa");

        
    
        //while para seguir enviando cosas 
        int i = 0
        while (i < 10) {  
            //aqui par aobtener el primer paquete y decidir enviarlo
            char* paquete_protolo
            if (i ==9){
                paquete_protolo = "SE SUPONE QUE SOY UNO DE LOS PROTOCOLOS"

            }else{  //para que termine
                paquete_protolo = ""

            }
            car* paquete_protolo = "SE SUPONE QUE SOY UNO DE LOS PROTOCOLOS"

            int err = send(sock, paquete_protolo, strlen(paquete_protolo), 0);
            if (err < 0) {
                ESP_LOGE(TAG, "Error occurred during sending: errno %d", errno);
                break;
            }

            //ENVIO  PAQUETE 

            //AHORA SE PONE EN DEEP SLEEP POR 60 SEGUNDOS
            sleep(60);


            int len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
            
            if (len < 0) {
                ESP_LOGE(TAG, "recv failed: errno %d", errno);
                break;
            }
            // Data received
            else {
                rx_buffer[len] = 0; // Null-terminate whatever we received and treat like a string
                ESP_LOGI(TAG, "Received %d bytes from %s:", len, host_ip);
                ESP_LOGI(TAG, "%s", rx_buffer);
                datida = rx_buffer;
                break;
            }
        
        i++;    
        }

        if (sock != -1) {
            ESP_LOGE(TAG, "Shutting down socket and restarting...");
            shutdown(sock, 0);
            close(sock);
        }
    
    
}