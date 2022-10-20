/*
 * SPDX-FileCopyrightText: 2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Unlicense OR CC0-1.0
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
#include "esp_mac.h"
#include <sys/param.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include "esp_netif.h"
#include "protocol_examples_common.h"

#include "lwip/err.h"
#include "lwip/sockets.h"
#include "lwip/sys.h"
#include <lwip/netdb.h>
#include "addr_from_stdin.h"
#include "../../empaquetamiento.c"
#include "../../fragmentacion.c"

#if defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
#include "addr_from_stdin.h"
#endif

#if defined(CONFIG_EXAMPLE_IPV4)
#define HOST_IP_ADDR CONFIG_EXAMPLE_IPV4_ADDR
#elif defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
#define HOST_IP_ADDR "192.168.28.1"
#endif

#define PORT 5010

#define DEVICE_ID 1113
#define TCP_LAYER_ID 0
#define UDP_LAYER_ID 1

static const char *TAG = "example";
static const char *payload = "Message from ESP32 ";

char rx_buffer[128];
char host_ip[] = HOST_IP_ADDR;
int addr_family = 0;
int ip_protocol = 0;



void encodePkg(unsigned char* data, int* dataSize, char protocol)
{
    uint8_t mac[6];
    //mac = 404u;
    esp_base_mac_addr_get(mac);
    Protocol0 pro0;
    Protocol1 pro1;
    Protocol23 pro2;
    Protocol23 pro3;
    Protocol4 pro4;

    const char *anotherTag = "empaquetamiento";
    
    switch(protocol) {
        case '0' :
            ESP_LOGI(anotherTag, "Enviando paquete de Protocolo 0"); 
            protocol0Init(&pro0, DEVICE_ID, mac, TCP_LAYER_ID);
            *dataSize = (HEADER_LEN + pro0.header.lenmsg)*sizeof(char);
            data = malloc(*dataSize);
            printProtocol0(&pro0);
            encodeProtocol0(&pro0, data, 0);
            break;
        break;
        case '1' :
            ESP_LOGI(anotherTag, "Enviando paquete de Protocolo 1"); 
            protocol1Init(&pro1, DEVICE_ID, mac, TCP_LAYER_ID);
            *dataSize = (HEADER_LEN + pro1.header.lenmsg)*sizeof(char);
            data = malloc(*dataSize);
            printProtocol1(&pro1);
            encodeProtocol1(&pro1, data, 0);
            break;
        case '2' :
            ESP_LOGI(anotherTag, "Enviando paquete de Protocolo 2"); 
            protocol2Init(&pro2, DEVICE_ID, mac, TCP_LAYER_ID);
            *dataSize = (HEADER_LEN + pro2.header.lenmsg)*sizeof(char);
            data = malloc(*dataSize);
            printProtocol23(&pro2);
            encodeProtocol2(&pro2, data, 0);
            break;
        case '3' :
            ESP_LOGI(anotherTag, "Enviando paquete de Protocolo 3"); 
            protocol3Init(&pro3, DEVICE_ID, mac, TCP_LAYER_ID);
            *dataSize = (HEADER_LEN + pro3.header.lenmsg)*sizeof(char);
            data = malloc(*dataSize);
            printProtocol23(&pro3);
            encodeProtocol3(&pro3, data, 0);
            break;
        case '4' :
            ESP_LOGE(anotherTag, "Enviando paquete de Protocolo 4"); 
            protocol4Init(&pro4, DEVICE_ID, mac, TCP_LAYER_ID);
            *dataSize = (HEADER_LEN + pro4.header.lenmsg)*sizeof(char);
            data = malloc(*dataSize);
            printProtocol4(&pro4);
            encodeProtocol4(&pro4, data, 0);
            protocol4Destroy(&pro4);
            break;
        default:
            ESP_LOGE(anotherTag, "ermanito, eso no es un protocolo....\n");  
    }
}


char* tcp_initial_connection(void){
            
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

        //CREA SOCKET
        int sock =  socket(addr_family, SOCK_STREAM, ip_protocol);
        if (sock < 0) {
            ESP_LOGE(TAG, "Unable to create socket: errno %d", errno);
            
        }
        ESP_LOGI(TAG, "Socket created, connecting to %s:%d", host_ip, PORT);

        //CONECTA SOCKET CON SERVODIR/RASPBERRY
        int err = connect(sock, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
        if (err != 0) {
            ESP_LOGE(TAG, "Socket unable to connect: errno %d", errno);
           
        }
        ESP_LOGI(TAG, "Successfully connected");

        while (1) {
            //ENVIA UN PAQUETE 
            int err = send(sock, payload, strlen(payload), 0);
            if (err < 0) {
                ESP_LOGE(TAG, "Error occurred during sending: errno %d", errno);
                break;
            }

            //RECIVE PAQUETE CON CONTENIDO id_protocol y layer_protocol
            int len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
            // Error occurred during receiving
            if (len < 0) {
                ESP_LOGE(TAG, "recv failed: errno %d", errno);
                break;
            }
            else {
                rx_buffer[len] = 0; // Null-terminate whatever we received and treat like a string
                ESP_LOGI(TAG, "Received %d bytes from %s:", len, host_ip);
                ESP_LOGI(TAG, "%s", rx_buffer);
                if (strlen(rx_buffer) > 0){
                    break; //salimos del loop si si llego algo
                }
            }

        }
        
        if (sock != -1) {
            ESP_LOGE(TAG, "Shutting down socket and restarting...");
            shutdown(sock, 0);
            close(sock);
        }

    
    ESP_LOGE(TAG, "retornamosss");   
    return rx_buffer;
}



void tcp_client(char id_protocol){

    while (1) {
        
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

        //CREAMOS SOCKET
        int sock =  socket(addr_family, SOCK_STREAM, ip_protocol);
        if (sock < 0) {
            ESP_LOGE(TAG, "Unable to create socket: errno %d", errno);
            break;
        }
        ESP_LOGI(TAG, "Socket created, connecting to %s:%d", host_ip, PORT);

        //CONECTAMOS SOCKET CON SERV
        int err = connect(sock, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
        if (err != 0) {
            ESP_LOGE(TAG, "Socket unable to connect: errno %d", errno);
            break;
        }
        ESP_LOGI(TAG, "Successfully connected");

        int change_bbdd= 0;
        while (change_bbdd == 0) {
            //LLAMAMOS AL PROTOCOLO QU ECREA EL PAQUETE
            //APLIQUE VALE SUS SUPERPODERESSSSSSSSSSSSSSSSSSSSSSS
            //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            //char *data = "Paquete ficticio\n";                        //por mientras dejo este chantita
            unsigned char *data = NULL;
            int data_size = 0;
            
            encodePkg(data, &data_size, id_protocol);

            //ENVIAMOS DATA
            
            if(id_protocol == '4'){
                //FRAGMENTACIÓN
                fragmentation(data, data_size, sock);
            }else{
                ESP_LOGI(TAG, "Paquete encodeado: \n");
                ESP_LOG_BUFFER_HEX("Hexadecimal: ", data, data_size);
                // int err = send(sock, data, strlen(payload), 0);
                int err = send(sock, data, data_size, 0);
                free(data);
                if (err < 0) {
                    ESP_LOGE(TAG, "Error occurred during sending: errno %d", errno);
                    break;
                }

            }

            
            
            

            //DEEPSLEEP 60 SEC
            ESP_LOGE(TAG, "sleeping for 60 sec");
            sleep(10);  //le puse 10 sec por mientras q lo 60 era muy largo
 
            /*
            //RECIVIMOS RESPUESTA
            int len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
            // Error occurred during receiving
            if (len < 0) {
                ESP_LOGE(TAG, "recv failed: errno %d", errno);
                break;
            }
            else {
                rx_buffer[len] = 0; // Null-terminate whatever we received and treat like a string
                ESP_LOGI(TAG, "Received %d bytes from %s:", len, host_ip);
                ESP_LOGI(TAG, "%s", rx_buffer);
            }
            
            */
            // Data received
            
        }

        //CERRAMOS SOCKET Y CHAO
        if (sock != -1) {
            ESP_LOGE(TAG, "Shutting down socket and restarting...");
            shutdown(sock, 0);
            close(sock);
        }
    }
}

void udp_client(char id_protocol){

    
    while (1) {

        #if defined(CONFIG_EXAMPLE_IPV4)
                struct sockaddr_in dest_addr;
                dest_addr.sin_addr.s_addr = inet_addr(HOST_IP_ADDR);
                dest_addr.sin_family = AF_INET;
                dest_addr.sin_port = htons(PORT);
                addr_family = AF_INET;
                ip_protocol = IPPROTO_IP;
        #elif defined(CONFIG_EXAMPLE_IPV6)
                struct sockaddr_in6 dest_addr = { 0 };
                inet6_aton(HOST_IP_ADDR, &dest_addr.sin6_addr);
                dest_addr.sin6_family = AF_INET6;
                dest_addr.sin6_port = htons(PORT);
                dest_addr.sin6_scope_id = esp_netif_get_netif_impl_index(EXAMPLE_INTERFACE);
                addr_family = AF_INET6;
                ip_protocol = IPPROTO_IPV6;
        #elif defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
                struct sockaddr_storage dest_addr = { 0 };
                ESP_ERROR_CHECK(get_addr_from_stdin(PORT, SOCK_DGRAM, &ip_protocol, &addr_family, &dest_addr));
        #endif

        //CREAMOS EL SOCKET
        int sock = socket(addr_family, SOCK_DGRAM, ip_protocol);
        if (sock < 0) {
            ESP_LOGE(TAG, "Unable to create socket: errno %d", errno);
            break;
        }

        // Set timeout
        struct timeval timeout;
        timeout.tv_sec = 10;
        timeout.tv_usec = 0;
        setsockopt (sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof timeout);

        ESP_LOGI(TAG, "Socket created, sending to %s:%d", HOST_IP_ADDR, PORT);

        char ddbb_layerProtocol = '1';
        while (1) {

            //CREAMOS PAQUETE DEPENDIENDO DEL PROTOCOLO QUE NOS LLEGO

            unsigned char *data = NULL;
            int data_size = 0;

            encodePkg(data, &data_size, id_protocol);

            if(id_protocol == '4'){
                //FRAGMENTACIÓN
                fragmentation(data, data_size, sock);
            }else{
                int err = sendto(sock, data, strlen(payload), 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
                if (err < 0) {
                    ESP_LOGE(TAG, "Error occurred during sending: errno %d", errno);
                    break;
                }
            }
            ESP_LOGI(TAG, "Message sent");

            struct sockaddr_storage source_addr; // Large enough for both IPv4 or IPv6
            socklen_t socklen = sizeof(source_addr);

            
            //DEVUELTA RECIBIMOS LOS VALORES DE LA BBDD
            int len = recvfrom(sock, rx_buffer, sizeof(rx_buffer) - 1, 0, (struct sockaddr *)&source_addr, &socklen);

            // Error occurred during receiving
            if (len < 0) {
                ESP_LOGE(TAG, "recvfrom failed: errno %d", errno);
                break;
            }
            // Data received
            else {
                rx_buffer[len] = 0; // Null-terminate whatever we received and treat like a string
                ESP_LOGI(TAG, "Received %d bytes from %s:", len, host_ip);
                ESP_LOGI(TAG, "%s", rx_buffer);
                if (strncmp(rx_buffer, "OK: ", 4) == 0) {
                    ESP_LOGI(TAG, "Received expected message, reconnecting");
                    break;
                }
            }

            //SI LO RECIBIDO CAMBIO A LO ORIGINAL PARAMOS LOOP
            ddbb_layerProtocol = rx_buffer[4];
            ESP_LOGI(TAG, "protocolo bbdd -> %c ",ddbb_layerProtocol);
            
            if( ddbb_layerProtocol == '0' ){          
                ESP_LOGI(TAG, "cambiaron valores bbdd estonces termina ");
                break;
            }
        

            //SINO  CONTINUAMOS

            vTaskDelay(2000 / portTICK_PERIOD_MS);
        }
        if (sock != -1) {
            ESP_LOGE(TAG, "Shutting down socket and restarting...");
            shutdown(sock, 0);
            close(sock);
        }
        if (ddbb_layerProtocol == '0') {
            ESP_LOGE(TAG, "shauuu");
            break;
        }

    }
}




