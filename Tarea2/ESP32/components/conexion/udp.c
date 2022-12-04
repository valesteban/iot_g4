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
#include "esp_sleep.h"
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

// #include "../../empaquetamiento.c"
// #include "../../fragmentacion.c"





static const char *TAG_UDP = "example";

char rx_buffer_udp[128];
// char host_ip_udp[] = HOST_IP_ADDR;
int addr_family_udp = 0;
int ip_protocol_udp = 0;

// /*
// - Se enviara los datos sin para hasta que el valor de T ransport_Layer
// cambie, este deberá poder ser cambiado manualmente (por ejemplo apretando un botón).*/
// void udp_client(char id_protocol){
//     ESP_LOGI(TAG_UDP, "empieza udp");

    
//     while (1) {

//         #if defined(CONFIG_EXAMPLE_IPV4)
//                 struct sockaddr_in dest_addr;
//                 dest_addr.sin_addr.s_addr = inet_addr(HOST_IP_ADDR);
//                 dest_addr.sin_family = AF_INET;
//                 dest_addr.sin_port = htons(PORT);
//                 addr_family_udp = AF_INET;
//                 ip_protocol_udp = IPPROTO_IP;
//         #elif defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
//                 struct sockaddr_storage dest_addr = { 0 };
//                 ESP_ERROR_CHECK(get_addr_from_stdin(PORT, SOCK_DGRAM, &ip_protocol_udp, &addr_family_udp, &dest_addr));
//         #endif

//         //CREAMOS EL SOCKET
//         int sock = socket(addr_family_udp, SOCK_DGRAM, ip_protocol_udp);
//         if (sock < 0) {
//             ESP_LOGE(TAG_UDP, "Unable to create socket: errno %d", errno);
//             break;
//         }

//         // Set timeout
//         struct timeval timeout;
//         timeout.tv_sec = 10;
//         timeout.tv_usec = 0;
//         setsockopt (sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof timeout);

//         ESP_LOGI(TAG_UDP, "Socket created, sending to %s:%d", HOST_IP_ADDR, PORT);

//         char ddbb_layerProtocol = '1';
//         while (1) {

//             //CREAMOS PAQUETE DEPENDIENDO DEL PROTOCOLO QUE NOS LLEGO
//             unsigned char *data = NULL;
//             int data_size = 0;
//             uint8_t mac[6];
//             esp_base_mac_addr_get(mac);
            
//             encode_pkg(id_protocol, mac, DEVICE_ID, ddbb_layerProtocol, &data, &data_size);

//             /*
//             int err = sendto(sock, data, data_size, 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
//             if (err < 0) {
//                 ESP_LOGE(TAG_UDP, "Error occurred during sending: errno %d", errno);
//                 break;
//             }
//             ESP_LOGI(TAG_UDP, "Message sent");
//             */

//             struct sockaddr_storage source_addr; // Large enough for both IPv4 or IPv6
//             socklen_t socklen = sizeof(source_addr);

//             fragmentationUDP(data, data_size, sock, (struct sockaddr *)&dest_addr, sizeof(dest_addr), (struct sockaddr *)&source_addr, &socklen);
            

//             //DEVUELTA RECIBIMOS SOLO STATUS
//             int len = recvfrom(sock, rx_buffer_udp, sizeof(rx_buffer_udp) - 1, 0, (struct sockaddr *)&source_addr, &socklen);

//             // Error occurred during receiving
//             if (len < 0) {
//                 ESP_LOGE(TAG_UDP, "recvfrom failed: errno %d", errno);
//                 break;
//             }
//             // Data received
//             else {
//                 rx_buffer_udp[len] = 0; // Null-terminate whatever we received and treat like a string
//                 ESP_LOGI(TAG_UDP, "Received %d bytes from %s:", len, host_ip_udp);
//                 ESP_LOGI(TAG_UDP, "%s", rx_buffer_udp);
//                 if (strncmp(rx_buffer_udp, "OK: ", 4) == 0) {
//                     ESP_LOGI(TAG_UDP, "Received expected message, reconnecting");
//                     break;
//                 }
//             }

//             //SI LO RECIBIDO CAMBIO A LO ORIGINAL PARAMOS LOOP
//             ddbb_layerProtocol = rx_buffer_udp[4];
//             ESP_LOGI(TAG_UDP, "protocolo bbdd -> %c ",ddbb_layerProtocol);
            
//             if( ddbb_layerProtocol == '0' ){          
//                 ESP_LOGI(TAG_UDP, "cambiaron valores bbdd estonces termina ");
//                 break;
//             }
        

//             //SINO  CONTINUAMOS

//             vTaskDelay(2000 / portTICK_PERIOD_MS);
//         }
//         if (sock != -1) {
//             ESP_LOGE(TAG_UDP, "Shutting down socket and restarting...");
//             shutdown(sock, 0);
//             close(sock);
//         }
//         if (ddbb_layerProtocol == '0') {
//             ESP_LOGE(TAG_UDP, "shauuu");
//             break;
//         }
//     } 
// }

// Conexión UDP 
// - status = 23
// - protocolos -> 1-2-3-4-5
// - Raspeberry detiene conexion (interfaz gráfica)
// void protocolo_udp(char id_protocol ,int32_t Port_UDP, char* Host_IP_Addr ){
//     ESP_LOGI(TAG_UDP, "Comienzo protocolo UDP");

//     #if defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
//     #include "addr_from_stdin.h"
//     #endif

//     #if defined(CONFIG_EXAMPLE_IPV4)
//     #define HOST_IP_ADDR CONFIG_EXAMPLE_IPV4_ADDR
//     #elif defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
//     #define HOST_IP_ADDR "192.168.28.1"
//     #endif

//     #define PORT Port_UDP
//     #define DEVICE_ID 1113
//     // #define TCP_LAYER_ID 0
//     #define UDP_LAYER_ID 1




//     // LOOP CREACION SOCKET
//     while (1) {
//         // struct sockaddr_in dest_addr;
//         // dest_addr.sin_addr.s_addr = inet_addr(HOST_IP_ADDR);
//         // dest_addr.sin_family = AF_INET;
//         // dest_addr.sin_port = htons(PORT);
//         // addr_family_udp = AF_INET;
//         // ip_protocol_udp = IPPROTO_IP;
//         // ESP_LOGI(TAG_UDP, "Se creó el socket", inet_addr(HOST_IP_ADDR));
//         // ESP_LOGI(TAG_UDP, "Se creó el socket",AF_INET);
//         // ESP_LOGI(TAG_UDP, "Se creó el socket",htons(PORT));
//         // ESP_LOGI(TAG_UDP, "Se creó el socket", htons(PORT));
//         // ESP_LOGI(TAG_UDP, "Se creó el socket", IPPROTO_IP);


//         #if defined(CONFIG_EXAMPLE_IPV4)
//                 struct sockaddr_in dest_addr;
//                 dest_addr.sin_addr.s_addr = inet_addr(HOST_IP_ADDR);
//                 dest_addr.sin_family = AF_INET;
//                 dest_addr.sin_port = htons(PORT);
//                 addr_family_udp = AF_INET;
//                 ip_protocol_udp = IPPROTO_IP;
//         #elif defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
//                 struct sockaddr_storage dest_addr = { 0 };
//                 ESP_ERROR_CHECK(get_addr_from_stdin(PORT, SOCK_DGRAM, &ip_protocol_udp, &addr_family_udp, &dest_addr));
//         #endif

//         //CREAMOS EL SOCKET
//         int sock = socket(addr_family_udp, SOCK_DGRAM, ip_protocol_udp);
//         if (sock < 0) {
//             ESP_LOGE(TAG_UDP, "Unable to create socket: errno %d", errno);
//             break;
//         }
//         ESP_LOGI(TAG_UDP, "Se creó el socket");

//         // Set timeout
//         struct timeval timeout;
//         timeout.tv_sec = 10;
//         timeout.tv_usec = 0;
//         setsockopt (sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof timeout);

//         // ESP_LOGI(TAG_UDP, "Socket created, sending to %s:%d", HOST_IP_ADDR, PORT);

//         char ddbb_layerProtocol = '1';

//         // LOOP ENVIO PAQUETES UDP
//         while (1) {

//             //CREAMOS PAQUETE DEPENDIENDO DEL PROTOCOLO QUE NOS LLEGO
//             // char *data = "paquete hardcodeado";

//             unsigned char *data = NULL;
//             int data_size = 0;
//             uint8_t mac[6];
//             esp_base_mac_addr_get(mac);
//             ddbb_layerProtocol =
//             encode_pkg(id_protocol, mac, DEVICE_ID, ddbb_layerProtocol, &data, &data_size);


            
//             // int err = sendto(sock, data, strlen(data) , 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
//             // if (err < 0) {
//             //     ESP_LOGE(TAG_UDP, "Error occurred during sending: errno %d", errno);
//             //     break;
//             // }
//             // ESP_LOGI(TAG_UDP, "Paquete enviado correctamente ");
            

//             struct sockaddr_storage source_addr; // Large enough for both IPv4 or IPv6
//             socklen_t socklen = sizeof(source_addr);

//             fragmentationUDP(data, data_size, sock, (struct sockaddr *)&dest_addr, sizeof(dest_addr), (struct sockaddr *)&source_addr, &socklen);
            
//             //DEVUELTA RECIBIMOS LOS VALORES DE LA BBDD
//             int len = recvfrom(sock, rx_buffer_udp, sizeof(rx_buffer_udp) - 1, 0, (struct sockaddr *)&source_addr, &socklen);

//             // Error occurred during receiving
//             if (len < 0) {
//                 ESP_LOGE(TAG_UDP, "recvfrom failed: errno %d", errno);
//                 break;
//             }
//             // Data received
//             else {
//                 rx_buffer_udp[len] = 0; // Null-terminate whatever we received and treat like a string
//                 ESP_LOGI(TAG_UDP, "Se recibieron %d bytes ", len);
//                 ESP_LOGI(TAG_UDP, "Se recibió -> %s", rx_buffer_udp);
//                 if (strncmp(rx_buffer_udp, "OK: ", 4) == 0) {
//                     ESP_LOGI(TAG_UDP, "Received expected message, reconnecting");
//                     break;
//                 }
//             }

            // OBTENER VALOR DE STATUS Y DEPENDIENDO DE ESO CAMBIO

            // char status[2];
            // memcpy(status,(char*) rx_buffer[1], 2);
            // strcpy(status, rx_buffer_udp,);
         

            // ESP_LOGI(TAG_UDP, "status -> %s", status);


            //SI LO RECIBIDO CAMBIO A LO ORIGINAL PARAMOS LOOP
            // si cambia status llamamos funicon controla status
            // ddbb_layerProtocol = rx_buffer_udp[4];
            // ESP_LOGI(TAG_UDP, "protocolo bbdd -> %c ",ddbb_layerProtocol);
            
            // if( ddbb_layerProtocol == '0' ){          
//             //     ESP_LOGI(TAG_UDP, "cambiaron valores bbdd estonces termina ");
//             //     break;
//             // }

//             // int status = 100;
//             // if (status = 100){
//             //     return cambiar_protocolo_status(status);
//             // }
        
//             /*
//             SI STATUS ES DIFERENTE DE 23
//             return cambiar_protocolo_status(status)
//             */

//             //SINO  CONTINUAMOS

//             vTaskDelay(2000 / portTICK_PERIOD_MS);
//         }
//         if (sock != -1) {
//             ESP_LOGE(TAG_UDP, "Shutting down socket and restarting...");
//             shutdown(sock, 0);
//             close(sock);
//         }
//         // if (ddbb_layerProtocol == '0') {
//         //     ESP_LOGE(TAG_UDP, "shauuu");
//         //     break;
//         // }

//     }
    
// }


