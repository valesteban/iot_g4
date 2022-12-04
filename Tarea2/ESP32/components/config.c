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
    int ID_Protocol;
    int32_t BMI270_Sampling;
    int32_t BMI270_Acc_Sensibility;
    int32_t BMI270_Gyro_Sensibility ;
    int32_t BME688_Sampling ;
    int32_t Discontinuos_Time;
    int32_t Port_TCP;
    int32_t Port_UDP;
    int32_t Host_IP_Addr;
    char* SSID ;
    char* Pass;

} Configuracion;

Configuracion construccion_conf(char * paquete){
    char * value =( char *) paquete;
    // IF UUID ES DE LA CONFIG??
    // FIX CREAR FUNCION CON ESTO 
    // char str[] = "(3, 20, 2, 400, 16, 200, 4, 420, 5010, 5010, 3232242689, 'ssid', 'pass')";
    remove_all_chars(value, '(');
    remove_all_chars(value, ')');
    printf("%s", value);
    int init_size = strlen(value);

    char *token = strtok(value, ",");
    // mostrarioa la uu
                
    Configuracion conf ;
    for (int i=0 ;i<= 12; i++){
        printf("%s\n", token);
        token = strtok(NULL, ",");
        
    // 	 	switch (i) {
    // 	 	    case 0:
    // 	 	    case 1:
    // 	 	    case 1:
    // 	 	    case 1:
    // 	 	    case 1:
    // 	 	    case 1:
    // 	 	    case 1:
    // 	 	    case 1:
    // 	 	 	}
        
    }

    restrict conf;




}