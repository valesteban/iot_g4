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


/*
Función que implementa deep sleep
*/
// void deep_sleep(float operation_time, int32_t time_to_wake_up) {
//     uint64_t wakeup_time_sec;

//     printf("Time to wake up %d \n", time_to_wake_up);
//     printf("Operation time %f \n", operation_time);

//     if ((time_to_wake_up - operation_time) > 0) {
//         wakeup_time_sec = (uint64_t)(time_to_wake_up - operation_time);
//     }
//     else {
//         wakeup_time_sec = 60;
//         printf("tiempo de ejecucion");
//     }

//     // 
//     printf("Enabling timer wakeup, %lld\n", wakeup_time_sec);
//     esp_sleep_enable_timer_wakeup(wakeup_time_sec * 1000000); // *1.000.000
//     printf("going to sleep for clk...") ;
//     esp_deep_sleep_start();
// }