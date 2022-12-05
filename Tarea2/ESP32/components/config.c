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

void removechar( char str[], char t )
{
  int i,j;
  for(i=0; i<strlen(str); i++)
  {
    if (str[i]==t) 
      for (j=i; j<strlen(str); j++)
      {
        str[j]=str[j+1];   
      } 
  }
}




Configuracion construccion_conf(char * paquete, Configuracion conf){
    
    ESP_LOGI("conf","Creando estructura...");

    char * valores =( char *) paquete;
    // char *valores = paquete+1; // removes first character
    ESP_LOGI("conf","%s",valores);
    ESP_LOGI("conf","%c",valores[strlen(valores)-1]);

    // valores[strlen(valores)-1] = 'e'; // removing the last character i

    ESP_LOGI("conf","%s",valores);
    int cant_valores = 0;
    char* ptr = paquete;
    char* ptr_coma = paquete;
    while (cant_valores  != 13){

        int i = 0;
        ptr = ptr+1;
        ptr_coma = ptr_coma+1;
        // ESP_LOGI("conf"," ptr --> %c",*ptr);

        while (*ptr_coma != ',' && *ptr_coma != ')' ){
            ESP_LOGI("loop"," ptr_c --> %c",*ptr_coma);

            ptr_coma = ptr_coma +1;
            i = i+1;
        }
        // if (cant_valores == 12){
        //     i = i-1;
        // }
        
        // ESP_LOGI("conf"," ptr_c --> %c",*ptr_coma);
        char valor[i];
        memcpy( valor, ptr, i);
        valor[i] = '\0';
        // ESP_LOGI("conf"," --> %d",i);
  
        ptr = ptr_coma +1;
        ptr_coma = ptr;
        // ESP_LOGI("conf"," --> %s",valor);
           
        
        cant_valores = cant_valores+1; 
        // ESP_LOGI("conf","valor --> %s",valor);
        // ESP_LOGI("conf"," ------------ "); 


        if(cant_valores ==1){
            conf.Status = atoi(valor);
            // ESP_LOGI("test","--> %d",conf.Status);

        }else if(cant_valores ==2){
           conf.BMI270_Sampling = atoi(valor);
        //    ESP_LOGI("test","--> %d",conf.BMI270_Sampling);

        }
        else if(cant_valores ==3){
            conf.ID_Protocol = atoi(valor);
            // ESP_LOGI("test","--> %d",conf.ID_Protocol);

        }
        else if(cant_valores ==4){
            conf.BMI270_Acc_Sensibility = atoi(valor);
            // ESP_LOGI("test","--> %d", conf.BMI270_Acc_Sensibility);
        }
        else if(cant_valores ==5){  
            conf.BMI270_Gyro_Sensibility =  atoi(valor);
            // ESP_LOGI("test","--> %d",conf.BMI270_Gyro_Sensibility);
        }
        else if(cant_valores ==6){
            conf.BME688_Sampling = atoi(valor);;
            // ESP_LOGI("test","--> %d",conf.BME688_Sampling);
        }
        else if(cant_valores ==7){
            conf.Discontinuos_Time = atoi(valor);;
            // ESP_LOGI("test","--> %d",conf.Discontinuos_Time);
        }else if(cant_valores ==8){
            conf.Port_TCP = atoi(valor);;
            // ESP_LOGI("test","--> %d",conf.Port_TCP);
          
        }else if(cant_valores ==9){
            conf.Port_UDP = atoi(valor);;
            // ESP_LOGI("test","--> %d",conf.Port_UDP);

        }else if(cant_valores ==10){
            conf.Host_IP_Addr = valor;
            // ESP_LOGI("test","--> %s",conf.Host_IP_Addr);

        }else if(cant_valores ==11){
            conf.SSID = valor;
            // ESP_LOGI("test","--> %s",conf.SSID);

        }else if(cant_valores ==12){
            conf.Pass = valor;
            // ESP_LOGI("test","--> %s",conf.Pass );

        }

          

            


        // }
    }
    return conf;
}
    

    //eliminar primer y ultimo char

    // removechar(valores, ")");
    // ESP_LOGI("conf","%s",valores);
    // ESP_LOGI("conf","%s",valores);
    // // // int init_size = strlen(value);

    // char *token = strtok(valores, ",");
    // mostrarioa la uu
                
    // for (int i=0 ;i<= 12; i++){
    //     printf("%s\n", token);
    //     token = strtok(NULL, ",");
    //     ESP_LOGI("test","--> %s",token);
        
        
    
