/*
 * SPDX-FileCopyrightText: 2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Unlicense OR CC0-1.0
 */
#include "sdkconfig.h"
#include <string.h>
#include <stdio.h>  
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

#include "../payload/empaquetamiento.c"
#include "../payload/fragmentacion.c"
#include "../components/config.c"

#include "../deep_sleep.c"

static const char *TAG2 = "example";

char rx_buffer[128];
// char host_ip[] = HOST_IP_ADDR;
int addr_family = 0;
int ip_protocol = 0;


// Conexión TCP continua 
// - status = 21
// - id_protocols ->1-2-3-4-5
// - Raspeberry detiene conexion (interfaz gráfica) 
void tcp_continuo(Configuracion conf_struct){

    ESP_LOGI(TAG2, "Configurando wifi...");
    // ESP_ERROR_CHECK(example_connect());
    wifi_iniciate();

    char* host_ip_addr = conf_struct.Host_IP_Addr;
    int32_t port_tcp = conf_struct.Port_TCP;
    char id_protocol = conf_struct.ID_Protocol;
    int device_id = 1113;
    int tcp_layer_id = 0;
    int udp_layer_id = 1;

    // LOOP CREA SOCKET
    while (true) {
        struct sockaddr_in addr;
        inet_pton(AF_INET, host_ip_addr, &addr.sin_addr);
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port_tcp);
        addr_family = AF_INET;
        ip_protocol = IPPROTO_IP;
        
        //CREAMOS SOCKET
        int sock =  socket(addr_family, SOCK_STREAM, ip_protocol);
        if (sock < 0) {
            ESP_LOGE(TAG2, "Unable to create socket: errno %d", errno);
            break;
        }else{
            ESP_LOGI(TAG2, "Se creó el Socket correctamente, conectando a %s:%d", host_ip_addr, port_tcp);
        }

        //CONECTAMOS SOCKET CON SERV
        int err = connect(sock, (struct sockaddr *)&addr, sizeof(addr));
        if (err != 0) {
            ESP_LOGE(TAG2, "Socket unable to connect: errno %d", errno);
            break;
        }else{
            ESP_LOGI(TAG2, "Conectado correctamente");
        }
        

        // int status= 21;
        
        while (true) {

            //LLAMAMOS AL PROTOCOLO QUE CREA EL PAQUETE
            // char *data = "Paquete hardcodeao\n";                       

           unsigned char *data = NULL;
           int data_size = 0;
           uint8_t mac[6];
           esp_base_mac_addr_get(mac);

           encode_pkg(id_protocol, mac, device_id , tcp_layer_id , &data, &data_size);

            //ENVIAMOS DATA---------------------------------------------------------------------------
            
            if(id_protocol == '4'){

                //FRAGMENTACIÓN
                int err = fragmentation(data, data_size, sock);
                free(data);
                if (err < 0) {
                    ESP_LOGE(TAG2, "Error occurred during sending: errno %d", errno);
                    break;
                }
                // ESP_LOGI("Envio tcp", "Completado envío TCP de protocolo 4! err: %d", err);
            }else{
                ESP_LOGI(TAG2, "Paquete encodeado:");
                ESP_LOG_BUFFER_HEX("Hexadecimal: ", data, data_size);
                //ENVIAMOS DATA
                int err = send(sock, data, data_size, 0);
                free(data);
                if (err < 0) {
                    ESP_LOGE(TAG2, "Error occurred during sending: errno %d", errno);
                    break;
                }
            }
            
            //RECIVIMOS RESPUESTA
            int len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
            // Error occurred during receiving
            if (len < 0) {
                ESP_LOGE(TAG2, "recv failed: errno %d", errno);
                break;
            }
            else {
                rx_buffer[len] = 0; // Null-terminate whatever we received and treat like a string
                ESP_LOGI(TAG2, "Received %d bytes from %s:", len, host_ip_addr);
                ESP_LOGI(TAG2, "Paquete recibido: %s", rx_buffer);
            }
            
//             // SI DATA RECIBIDA PIDE PARAR (por interfaz) 
//             // BREAK Y RETURN

//             // SI DATA ENVIADA CAMBIA STATUS A 20
//             // retornamos 20 para que la funcion main se encarge de llamar
//             // a la funcion tcp_configuracion()


//             // SI DATA ENVIADA CAMBIA STATUS A 0
//             // retornamos 0 para que la funcion main se encarge de llamar
//             // a la funcion ble_configuracion()
            
//         } //cierre while status = 21

//         //CERRAMOS SOCKET Y CHAO
//         if (sock != -1) {
//             ESP_LOGE(TAG2, "Shutting down socket and restarting...");
//             shutdown(sock, 0);
//             close(sock);
        }
    }
}

// Conexión TCP discontinua 
// - status= 22
// - id_protocols ->1-2-3-4-5
// - según el valor de Discontinuous_Time el ESP32 entrara por ese tiempo en modo Deep_sleep.
// - Raspeberry detiene conexion (interfaz gráfica) 
// - se recomienda que el Discontinuous_Time tenga como unidad minutos y que su valor mínimo sea 1.
void tcp_discontinuo(Configuracion conf_struct ){
    ESP_LOGI(TAG2, "Configurando wifi...");
    // ESP_ERROR_CHECK(example_connect());
    wifi_iniciate();

    char* host_ip_addr = conf_struct.Host_IP_Addr;
    int32_t port_tcp = conf_struct.Port_TCP;
    char id_protocol = conf_struct.ID_Protocol;
    int device_id = 1113;
    int tcp_layer_id = 0;
    int udp_layer_id = 1;




    // LOOP CREA SOCKET
    while (true) {
        struct sockaddr_in addr;
        inet_pton(AF_INET, host_ip_addr, &addr.sin_addr);
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port_tcp);
        addr_family = AF_INET;
        ip_protocol = IPPROTO_IP;
    

        //CREAMOS SOCKET
        int sock =  socket(addr_family, SOCK_STREAM, ip_protocol);
        if (sock < 0) {
            ESP_LOGE(TAG2, "Unable to create socket: errno %d", errno);
            break;
        }
        ESP_LOGI(TAG2, "Socket creado , connecting to %s:%d", host_ip_addr, port_tcp);

        //CONECTAMOS SOCKET CON SERV
        int err = connect(sock, (struct sockaddr *)&addr, sizeof(addr));
        if (err != 0) {
            ESP_LOGE(TAG2, "Socket unable to connect: errno %d", errno);
            break;
        }
        ESP_LOGI(TAG2, "Successfully connected");

        int status= 21;
        
        while (status == 21) {
            //LLAMAMOS AL PROTOCOLO QU ECREA EL PAQUETE
            // char *data = "Paquete hardcodeao\n";                       

           unsigned char *data = NULL;
           int data_size = 0;
           uint8_t mac[6];
           esp_base_mac_addr_get(mac);
           encode_pkg(id_protocol, mac, device_id,tcp_layer_id, &data, &data_size);

            //ENVIAMOS DATA---------------------------------------------------------------------------
            
            if(id_protocol == '4'){
                //FRAGMENTACIÓN
                int err = fragmentation(data, data_size, sock);
                // sleep(10);
                free(data);
                if (err < 0) {
                    ESP_LOGE(TAG2, "Error occurred during sending: errno %d", errno);
                    break;
                }
                ESP_LOGI("Envio tcp", "Completado envío TCP de protocolo 4! err: %d", err);
            
            }else{
                ESP_LOGI(TAG2, "Paquete encodeado: \n");
                ESP_LOG_BUFFER_HEX("Hexadecimal: ", data, data_size);
                int err = send(sock, data, data_size, 0);
                free(data);
                if (err < 0) {
                    ESP_LOGE(TAG2, "Error occurred during sending: errno %d", errno);
                    break;
                }

            }  
            //--------------------------------------------------------------------------------------


            //ENVIAMOS DATA
            // int err = send(sock, data, strlen(data), 0);
            // if (err < 0) {
            //     ESP_LOGE(TAG2, "Error occurred during sending: errno %d", errno);
            //     break;
            // }
            
            //RECIVIMOS RESPUESTA
            int len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
            // Error occurred during receiving
            if (len < 0) {
                ESP_LOGE(TAG2, "recv failed: errno %d", errno);
                break;
            }
            else {
                rx_buffer[len] = 0; // Null-terminate whatever we received and treat like a string
                ESP_LOGI(TAG2, "Received %d bytes from %s:", len, host_ip_addr);
                ESP_LOGI(TAG2, "%s", rx_buffer);
            }

            // SI DATA RECIBIDA PIDE PARAR (por interfaz) 
            // BREAK Y RETURN

            // SI DATA ENVIADA CAMBIA STATUS A 20
            // retornamos 20 para que la funcion main se encarge de llamar
            // a la funcion tcp_configuracion()


            // SI DATA ENVIADA CAMBIA STATUS A 0
            // retornamos 0 para que la funcion main se encarge de llamar
            // a la funcion ble_configuracion()
            
            
            // Data received
            float operation_time =  2 ;
            int32_t time_to_wake_up = 3;

            deep_sleep( operation_time,  time_to_wake_up) ;
            ESP_LOGE(TAG2, "Se terminó de esperar");


            
        } //cierre while status = 21

        //CERRAMOS SOCKET Y CHAO
        if (sock != -1) {
            ESP_LOGE(TAG2, "Shutting down socket and restarting...");
            shutdown(sock, 0);
            close(sock);
        }
    }
}


//Conexion TCP CONFIGURACION 
// - Ssid, Pass y Port_TCP toman de valores configurados por la interfaz
// - En este modo el ESP32 puede actualizar cualquiera valores de la tabla Parámetros de Configuración
// - status = 20
void tcp_configuracion(Configuracion conf_struct  ){
    
    ESP_LOGI(TAG2, "Configurando wifi...");
    // ESP_ERROR_CHECK(example_connect());
    wifi_iniciate();

    char* host_ip_addr = conf_struct.Host_IP_Addr;
    int32_t port_tcp = conf_struct.Port_TCP;
    
    struct sockaddr_in addr;
    inet_pton(AF_INET, host_ip_addr, &addr.sin_addr);
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port_tcp);
    addr_family = AF_INET;
    ip_protocol = IPPROTO_IP;

    // ESP_LOGI(TAG2, "Configuracion WIFI");
    
    

    // ESP_LOGI(TAG2, "TCP configuracion \n Status 20");

    
    // LOOP CREA SOCKET
    while (1) {
        
        // #if defined(CONFIG_EXAMPLE_IPV4)
        //         struct sockaddr_in dest_addr;
        //         inet_pton(AF_INET, HOST_IP_ADDR, &dest_addr.sin_addr);
        //         dest_addr.sin_family = AF_INET;
        //         dest_addr.sin_port = htons(PORT);
        //         addr_family = AF_INET;
        //         ip_protocol = IPPROTO_IP;
        // #elif defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
        //         struct sockaddr_storage dest_addr = { 0 };
        //         ESP_ERROR_CHECK(get_addr_from_stdin(PORT, SOCK_STREAM, &ip_protocol, &addr_family, &dest_addr));
        // #endif
        // ESP_LOGI(TAG2, "...");

        //CREAMOS SOCKET
        int sock =  socket(addr_family, SOCK_STREAM, ip_protocol);
        if (sock < 0) {
            ESP_LOGE(TAG2, "Unable to create socket: errno %d", errno);
        //     break;
        }
        ESP_LOGI(TAG2, "Se creó el socket");

        //CONECTAMOS SOCKET CON SERV
        // int err = connect(sock, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
        int err = connect(sock, (struct sockaddr *)&addr, sizeof(addr));

        if (err != 0) {
            ESP_LOGE(TAG2, "Socket unable to connect: errno %d", errno);
            // break;
        }
        ESP_LOGI(TAG2, "Conectado correctamente");
                     

        //RECIVIMOS RESPUESTA
        int len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
        // Error occurred during receiving
        if (len < 0) {
            ESP_LOGE(TAG2, "recv failed: errno %d", errno);
            break;
        }
        else {
            rx_buffer[len] = 0; // Null-terminate whatever we received and treat like a string
            ESP_LOGI(TAG2, "Received %d bytes from %s:", len,  host_ip_addr);
            ESP_LOGI(TAG2, "%s", rx_buffer);
        }
        
        
        // SI DATA RECIBIDA PIDE PARAR (por interfaz) 
        // BREAK Y RETURN

        // SI DATA ENVIADA CAMBIA STATUS A 20
        // retornamos 20 para que la funcion main se encarge de llamar
        // a la funcion tcp_configuracion()


        // SI DATA ENVIADA CAMBIA STATUS A 0
        // retornamos 0 para que la funcion main se encarge de llamar
        // a la funcion ble_configuracion()
        
        

        //CERRAMOS SOCKET Y CHAO
        if (sock != -1) {
            ESP_LOGE(TAG2, "Shutting down socket and restarting...");
            shutdown(sock, 0);
            close(sock);
        }

        // HACEMOS LA CONEXION DEPENDIENDO DE LA INFO RECIBIDA
        // ESP_LOGI(TAG2, "Cambiamos de conexion");
        // return  1;
    }
    
}

