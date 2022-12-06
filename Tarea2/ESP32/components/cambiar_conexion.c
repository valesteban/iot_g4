#include "nvs_flash.h"
#include "esp_netif.h"
#include "protocol_examples_common.h"
#include "esp_event.h"
#include "esp_log.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>


char * TAG_CONEXION = "Seleccion conexion ";


Configuracion cambiar_conexion(Configuracion conf_struct){
    ESP_LOGI("cambio conexion","**************Cambiando conexión****************");
    ESP_LOGI("cambio conexion","**************status -> %d ****************",conf_struct.Status);
    Configuracion conf;

    switch (conf_struct.Status){
        case 20:
            ESP_LOGI(TAG_CONEXION, "****************TCP-CONFIGURACION***********************************************");
            conf = tcp_configuracion(conf_struct);
            break;
        case 21:
            ESP_LOGI(TAG_CONEXION, "****************TCP-CONTINUO***********************************************");
            tcp_continuo(conf_struct);
            break;
        // case 22:
        //     ESP_LOGI(TAG_CONEXION, "****************TCP-DISCONTINUO***********************************************");
        //     tcp_discontinuo(conf_struct);
        //     break;
        case 23:
            ESP_LOGI(TAG_CONEXION, "****************UDP***********************************************");
            protocolo_udp(conf_struct );
            break;
        // case 30:
        //     ESP_LOGE(TAG_CONEXION, "****************NO IMPLEMENTADO BLE CONTINUO ***********************************************");
        //     break;
        // case 31:
        //     ESP_LOGE(TAG_CONEXION, "****************NO IMPLEMENTADO BLE DISCONTINUO ***********************************************");
        //     break;
        // default:
        //     break;
    }
    return conf;
}


