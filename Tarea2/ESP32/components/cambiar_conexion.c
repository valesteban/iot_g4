#include "nvs_flash.h"
#include "esp_netif.h"
#include "protocol_examples_common.h"
#include "esp_event.h"
#include "esp_log.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>


char * TAG_CONEXION = "Seleccion conexion ";


void cambiar_conexion(Configuracion conf_struct){
    switch (conf_struct.Status){
        case 20:
            ESP_LOGI(TAG_CONEXION, "****************TCP-CONFIGURACION***********************************************");
            tcp_configuracion(conf_struct);
            break;
        case 21:
            ESP_LOGI(TAG_CONEXION, "****************TCP-CONTINUO***********************************************");
            tcp_continuo(conf_struct);
            break;
        case 22:
            ESP_LOGI(TAG_CONEXION, "****************TCP-DISCONTINUO***********************************************");
            tcp_discontinuo(conf_struct);
            break;
        case 23:
            ESP_LOGI(TAG_CONEXION, "****************UDP***********************************************");
            // char id_protocol = '1';
            // char* host_ip_addr = "192.168.28.1";
            // int port_udp = 5010;
            // char* ssid = "iot4";
            // char* pass = "12345678" ;
            // protocolo_udp(conf_struct.ID_Protocol );
            // protocolo_udp( conf_struct.ID_Protocol ,conf_struct.Port_UDP, conf_struct.Host_IP_Addr );
            break;
        case 30:
            ESP_LOGE(TAG_CONEXION, "****************NO IMPLEMENTADO BLE CONTINUO ***********************************************");
            break;
        case 31:
            ESP_LOGE(TAG_CONEXION, "****************NO IMPLEMENTADO BLE DISCONTINUO ***********************************************");
            break;
        default:
            break;
    }
}


