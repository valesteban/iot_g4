/*
 * SPDX-FileCopyrightText: 2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Unlicense OR CC0-1.0
 */
#include "nvs_flash.h"
#include "esp_netif.h"
#include "protocol_examples_common.h"
#include "esp_event.h"
#include "esp_log.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>




// #include "../components/conexion/ble.c"
#include "../components/config.c"
#include "../components/conexion/wifi/wifi.c"

#include "../components/conexion/tcp.c"
#include "../components/conexion/udp.c"
#include "../components/conexion/ble/gatts_table_creat_demo.c"
#include "../components/cambiar_conexion.c"



// #include "../components/utils.c"
// #include "../components/config.c"


// VARIABLES GLOBALES
Configuracion conf_struct ;
bool detener = 0;
// Configuracion conf_struct = {
//     20 ,
//     1 ,
//     10,
//     2,
//     200 ,
//     1 ,
//     10 ,
//     5010,
//     5011,
//     "192.168.28.1",
//     "iot4",
//     "12345678",
// };
char* ip_host = "192.168.28.1";
char* ssid = "iot4";
char* pass = "12345678";

static const char *TAG = "";


char *getSubstring(char* dst,const char *src,size_t start,size_t ens){
    return strncpy(dst,src+start,ens);
}




void app_main(void){
    ESP_LOGI(TAG, "****************COMIENZO***********************************************");

    // Test 0.2.0
    // ESP_ERROR_CHECK(nvs_flash_init());
    // ESP_ERROR_CHECK(esp_netif_init());
    // ESP_ERROR_CHECK(esp_event_loop_create_default());

    /* This helper function configures Wi-Fi or Ethernet, as selected in menuconfig.
     * Read "Establishing Wi-Fi or Ethernet Connection" section in
     * examples/protocols/README.md for more information about this function.
     */


   
    // funcion ble
    protocolo_ble(); 

    // espera hasta que se se envie configuracion por ble
    while (value_config == NULL){   
        ESP_LOGE(TAG,"aun nada");

        sleep(10);
    }
    esp_bluedroid_disable();
    ESP_LOGI(TAG,"Se conectó");


    char*   config_char = (char*) value_config ;  
    ESP_LOGI(TAG,"Valores -> %s",config_char);

    value_config = NULL;                                            //para reiniciar valor
    
    //de datos recibidos por ble construimos estructura
    conf_struct  = construccion_conf(config_char, conf_struct);
    conf_struct.Host_IP_Addr = host_ip;
    conf_struct.Pass = pass;
    conf_struct.SSID = ssid;


    // // 
    // // ESP_LOGE(TAG,"---> %d",conf_struct.Status);
    // //     sleep(10);

    // //loop de conexiones termina cuando se poara por la gui
    while ( detener==0){
        Configuracion  conf = cambiar_conexion(conf_struct);
        conf_struct = conf;
    }
    
}



