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

#include "../components/conexion/ble.c"
#include "../components/conexion/tcp.c"
#include "../components/conexion/udp.c"
// #include "tcp.c"



// extern char* tcp_initial_connection(void);
// extern void tcp_client();
// extern void udp_client();


static const char *TAG = "";

char *getSubstring(char* dst,const char *src,size_t start,size_t ens){
    return strncpy(dst,src+start,ens);
}


void app_main(void)
{
    // Test 0.2.0
    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    /* This helper function configures Wi-Fi or Ethernet, as selected in menuconfig.
     * Read "Establishing Wi-Fi or Ethernet Connection" section in
     * examples/protocols/README.md for more information about this function.
     */
    ESP_ERROR_CHECK(example_connect());

    char *res = tcp_initial_connection();
    
    char id_protocol = res[1];
    char transport_layer = res[4];

    

    // ESP_LOGE(TAG, "loe ee eotocolo %c, %c",id_protocol,transport_layer);
    
    //esto por mientras nomas me da lata parsear aun la *res donde esta n los valores q realmente recibe
    //imaginemos que obtuvo los valores y son 

    // int id_protocol = 0;
    // int transport_layer = 0; //TCP


    ESP_LOGE(TAG, "****************************************************************************");
    if ( transport_layer == '0'){
        ESP_LOGE(TAG, "Conexion TCP");
        tcp_client(id_protocol);
    }
    else{
        ESP_LOGE(TAG, "Conexion UDP");
        udp_client(id_protocol);

    }

}
