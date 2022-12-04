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
#include "../components/conexion/wifi/wifi.c"
#include "../components/conexion/tcp.c"
#include "../components/conexion/udp.c"
#include "../components/conexion/ble/gatts_table_creat_demo.c"
#include "../components/cambiar_conexion.c"


// #include "../components/utils.c"
// #include "../components/config.c"


// VARIABLES GLOBALES
// Configuracion conf_struct ;
Configuracion conf_struct = {
    20 ,
    '1' ,
    10,
    2,
    200 ,
    1 ,
    10 ,
    5000,
    5001,
    "192.168.28.1",
    "iot4",
    "12345678",
};



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
    // ESP_LOGI(TAG, "****************TEST***********************************************");


    /* This helper function configures Wi-Fi or Ethernet, as selected in menuconfig.
     * Read "Establishing Wi-Fi or Ethernet Connection" section in
     * examples/protocols/README.md for more information about this function.
     */
    // ESP_ERROR_CHECK(example_connect());
    // ESP_LOGI(TAG, "****************EXAMPLE***********************************************");


    // char *res = tcp_initial_connection();
    
    // char id_protocol = res[1];
    // char transport_layer = res[4];

    

    // ESP_LOGE(TAG, "loe ee eotocolo %c, %c",id_protocol,transport_layer);
    
    //esto por mientras nomas me da lata parsear aun la *res donde esta n los valores q realmente recibe
    //imaginemos que obtuvo los valores y son 

    // int id_protocol = 0;
    // int transport_layer = 0; //TCP

    // IF STATUS ES 0 
    // ELIMINAMOS WIFI ---> ESP_ERR_WIFI_NOT_INIT:WIFI











    // protocolo_udp(id_protocol);

    // protocolo_udp(host_ip_addr,port_udp,ssid,pass,id_protocol);

    ESP_LOGE(TAG,"*******************BLE CONF*************************************");
    // funcion ble
    // protocolo_ble(); !!

    //espera hasta que se se envie configuracion por ble
    // while (value_config == NULL){   !!
    //     ESP_LOGE(TAG,"aun nada");
    //     sleep(10);
    // }

    // uint8_t *   config_char = (char*) value_config ;  !!
    // char * config_char = "(3, 21, 2, 400, 16, 200, 4, 400, 5010, 5010, 3232242689, 'iot', '12345678')";
    // value_config = NULL;                                            //para reiniciar valor
    // ESP_LOGI(TAG,"valor main -> %s" , config_char);
    
    // //de datos recibidos por ble construimos estructura
    // conf_struct  = construccion_conf(config_char, conf_struct);

    // // 
    ESP_LOGE(TAG,"---> %d",conf_struct.Status);
    //     sleep(10);

    // Empieza conexion segun status de la configuracion
    cambiar_coenxion(conf_struct);
}

