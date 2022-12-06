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
char * host_ip_udp = "192.168.28.1";

static const char *TAG_UDP = "conexion UDP";

// Conexión UDP 
// - status = 23
// - protocolos -> 1-2-3-4-5
// - Raspeberry detiene conexion (interfaz gráfica)
// void protocolo_udp(char id_protocol ,int32_t Port_UDP, char* Host_IP_Addr ){
void protocolo_udp(Configuracion conf_struct ){
    
//     ESP_LOGI(TAG_UDP, "Configurando wifi...");
//     wifi_iniciate();

    
    // char* host_ip_addr = conf_struct.Host_IP_Addr;
    char * host_ip_addr = host_ip_udp;
    int32_t port_udp = conf_struct.Port_UDP;
    int id_protocol = conf_struct.ID_Protocol;
    int device_id = 1113;
    Configuracion conf = conf_struct;
    // int tcp_layer_id = 0;
    // int udp_layer_id = 1;

    char rx_buffer[128];
    
    // LOOP CREACION SOCKET
    while (1) {


        
        struct sockaddr_in addr;
        inet_pton(AF_INET, host_ip_addr, &addr.sin_addr);
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port_udp);
        addr_family = AF_INET;
        ip_protocol = IPPROTO_IP;

        //CREAMOS EL SOCKET
        int sock = socket(addr_family, SOCK_DGRAM, ip_protocol);
        if (sock < 0) {
            ESP_LOGE(TAG_UDP, "Unable to create socket: errno %d", errno);
            break;
        }
        ESP_LOGI(TAG_UDP, "Se creó el socket");

        // Set timeout
        struct timeval timeout;
        timeout.tv_sec = 10;
        timeout.tv_usec = 0;
        setsockopt (sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof timeout);


        char ddbb_layerProtocol = '1';

        // LOOP ENVIO PAQUETES UDP
        while (1) {
            

            //CREAMOS PAQUETE DEPENDIENDO DEL PROTOCOLO QUE NOS LLEGO
            // char *data = "paquete hardcodeado";

                        
            unsigned char *data = NULL;
            int data_size = 0;
            uint8_t mac[6];
            esp_base_mac_addr_get(mac);
            char id_char_protocol = id_protocol+'0';
            ddbb_layerProtocol =
            encode_pkg(id_char_protocol, mac, device_id, ddbb_layerProtocol, &data, &data_size);

            
            // int err = sendto(s}ock, data, strlen(data) , 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
            // if (err < 0) {
            //     ESP_LOGE(TAG_UDP, "Error occurred during sending: errno %d", errno);
            //     break;
            // }
            // ESP_LOGI(TAG_UDP, "Paquete enviado correctamente ");
            

            struct sockaddr_storage source_addr; // Large enough for both IPv4 or IPv6
            socklen_t socklen = sizeof(source_addr);
            fragmentationUDP(data, data_size, sock, (struct sockaddr *)&addr, sizeof(addr), (struct sockaddr *)&source_addr, &socklen);
            
            //DEVUELTA RECIBIMOS LOS VALORES DE LA BBDD
            int len = recvfrom(sock, rx_buffer, sizeof(rx_buffer) - 1, 0, (struct sockaddr *)&source_addr, &socklen);

            // Error occurred during receiving
            if (len < 0) {
                ESP_LOGE(TAG_UDP, "recvfrom failed: errno %d", errno);
                break;
            }
            // Data received
            else {
                rx_buffer[len] = 0; // Null-terminate whatever we received and treat like a string
                ESP_LOGI(TAG_UDP, "Se recibieron %d bytes ", len);
                ESP_LOGI(TAG_UDP, "Se recibió -> %s", rx_buffer);
                if (strncmp(rx_buffer, "OK: ", 4) == 0) {
                    ESP_LOGI(TAG_UDP, "Received expected message, reconnecting");
                    break;
                }
            }

            int8_t status = atoi(rx_buffer);
            if (status != 21){
                shutdown(sock, 0);
                close(sock);
                // esp_wifi_stop();
                // esp_wifi_disconnect();
                return ;
                break;
            }
            
            
            // 
            if (status == 20){
                shutdown(sock, 0);
                close(sock);
                conf.Status = 20;
                return ;
                
            }
            

            
            
            vTaskDelay(2000 / portTICK_PERIOD_MS);

            
        }
        if (sock != -1) {
            ESP_LOGE(TAG_UDP, "Shutting down socket and restarting...");
            shutdown(sock, 0);
            close(sock);
            return ;
        
        }

    }
}




