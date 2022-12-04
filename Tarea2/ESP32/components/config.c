#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "nvs_flash.h"
// #include "esp_netif.h"
// #include "protocol_examples_common.h"
// #include "esp_event.h"
// #include "esp_log.h"

typedef struct {
    int8_t Status;
    char ID_Protocol;
    int32_t BMI270_Sampling;
    int32_t BMI270_Acc_Sensibility;
    int32_t BMI270_Gyro_Sensibility ;
    int32_t BME688_Sampling ;
    int32_t Discontinuos_Time;
    int32_t Port_TCP;
    int32_t Port_UDP;
    char* Host_IP_Addr;
    char* SSID ;
    char* Pass;

} Configuracion;

void remove_all_chars(char* str, char c) {
    char *pr = str, *pw = str;
    while (*pr) {
        *pw = *pr++;
        pw += (*pw != c);
    }
    *pw = '\0';
}

Configuracion construccion_conf(char * paquete, Configuracion conf){
    char * valores =( char *) paquete;

    // IF UUID ES DE LA CONFIG??
    // FIX CREAR FUNCION CON ESTO 
    // char str[] = "(3, 20, 2, 400, 16, 200, 4, 420, 5010, 5010, 3232242689, 'ssid', 'pass')";
    // remove_all_chars(value, '(');
    // remove_all_chars(value, ')');
    // printf("%s", value);
    // // int init_size = strlen(value);

    char *token = strtok(valores, ",");
    // mostrarioa la uu
                
    for (int i=0 ;i<= 12; i++){
        printf("%s\n", token);
        token = strtok(NULL, ",");
        ESP_LOGI("test","--> %s",token);
        
        // switch (i) {
        //     case 0:     
        //         conf.Status = token;

        //         ESP_LOGI("test","--> %s",token);

        //     case 1:
        //         conf.ID_Protocol = token;
        //         ESP_LOGI("test","--> %s",token);
        //     case 2:
        //          conf.BMI270_Sampling = token;
        //         ESP_LOGI("test","--> %s",token);
        //     case 3:
        //          conf.BMI270_Acc_Sensibility = token;
        //         ESP_LOGI("test","--> %s",token);

        //     case 4:
        //          conf.BMI270_Gyro_Sensibility = token;
        //         ESP_LOGI(TAG,"--> %s",token);

        //     case 5:
        //          conf.BME688_Sampling = token;
        //         ESP_LOGI(TAG,"--> %s",token);
        //     case 6:
        //          conf.Discontinuos_Time = token;
        //         ESP_LOGI(TAG,"--> %s",token);

        //     case 7:
        //          conf.Port_TCP = token;
        //         ESP_LOGI(TAG,"--> %s",token);
        //     case 8:
        //          conf.Port_UDP = token;
        //         ESP_LOGI(TAG,"--> %s",token);

        //     case 9:
        //          conf.Host_IP_Addr = token;
        //         ESP_LOGI(TAG,"--> %s",token);

        //     case 10:
        //          conf.SSID = token;
        //         ESP_LOGI(TAG,"--> %s",token);

        //     case 11:
        //          conf.Pass = token;
        //         ESP_LOGI(TAG,"--> %s",token);

         

        //     }
    }
    

    return conf;
}