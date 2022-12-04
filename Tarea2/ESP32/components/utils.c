#include "nvs_flash.h"
#include "esp_netif.h"
#include "protocol_examples_common.h"
#include "esp_event.h"
#include "esp_log.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>


// char * TAG_UTILS = "utils";

/*
Funcion que recibe un status y dependiendo del valor llama 
a una nueva conexion
*/
// void cambiar_protocolo_status(int status){
//     switch (status)    {
//         case 0:
//             ESP_LOGE(TAG_UTILS, "Configuración por Bluetooth")    ;
//         case 20:
//         ESP_LOGE(TAG_UTILS, "Configuración vía TCP en BD")        ;
//         case 21:
//             ESP_LOGE(TAG_UTILS, "Conexión TCP continua ")   ;
//         case 22:
//             ESP_LOGE(TAG_UTILS, "Conexión TCP discontinua ") ;   
//         case 23:
//             ESP_LOGE(TAG_UTILS, " Conexión UDP")    ;
//         case 30:
//             ESP_LOGE(TAG_UTILS, " BLE continua")    ;
//         case 31:
//             ESP_LOGE(TAG_UTILS, " BLE discontinua")  ;
             

// }



