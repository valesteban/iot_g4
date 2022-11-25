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
            ESP_LOGE("Socket", "Unable to create socket: errno %d", errno);
            
        }
        ESP_LOGI("Socket", "Socket created, connecting to %s:%d", host_ip, PORT);

        //CONECTA SOCKET CON SERVODIR/RASPBERRY
        int err = connect(sock, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
        if (err != 0) {
            ESP_LOGE(TAG, "Socket unable to connect: errno %d", errno);
           
        }
        ESP_LOGI("Socket", "Successfully connected");

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
            if (len <= 0) {
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
    ESP_LOGI("tcp client", "Protocolo en uso: %c", id_protocol);

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
           uint8_t mac[6];
           esp_base_mac_addr_get(mac);

           encode_pkg(id_protocol, mac, DEVICE_ID, TCP_LAYER_ID, &data, &data_size);

            //ENVIAMOS DATA
            
            if(id_protocol == '4'){
                //FRAGMENTACIÓN
                int err = fragmentation(data, data_size, sock);
                free(data);
                if (err < 0) {
                    ESP_LOGE(TAG, "Error occurred during sending: errno %d", errno);
                    break;
                }
                ESP_LOGI("Envio tcp", "Completado envío TCP de protocolo 4! err: %d", err);
            }else{
                ESP_LOGI(TAG, "Paquete encodeado: \n");
                ESP_LOG_BUFFER_HEX("Hexadecimal: ", data, data_size);
                int err = send(sock, data, data_size, 0);
                free(data);
                if (err < 0) {
                    ESP_LOGE(TAG, "Error occurred during sending: errno %d", errno);
                    break;
                }

            }  
            

            sleep(10); //le puse 10 sec por mientras q lo 60 era muy largo
            
            /* matamos el deepsleep porque es re turbio...
            // CERRANDO SOCKET
            ESP_LOGI("Deep Sleep", "closing socket");
            shutdown(sock, 0);
            close(sock);

            //DEEPSLEEP 60 SEC
            ESP_LOGI("Deep Sleep", "sleeping for 60 sec");
            //ESP_LOGI("Deep Sleep", "Powering off Wi-Fi...");

            //esp_wifi_stop();
            esp_sleep_enable_timer_wakeup(10 * 1000000ull);
            esp_deep_sleep_start();
            */
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