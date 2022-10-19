#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "esp_log.h"

#define PACKET_LEN 1000


void fragmentation(char * paq, int size,int sock){
    ESP_LOGI("Info", "Fragmentando!\n");
    // char rx_buffer[128];

    for (int i = 0; i < size; i += PACKET_LEN){

        // Generamos el siguiente trozo
        int actualSize = fmin(PACKET_LEN, size - i);
        //char *pack = malloc(size);
        //memcpy(pack, &(payload[i]), size);

        //Enviamos el trozo
        int err = send(sock, &(paq[i]), actualSize, 0);  //send(sock, data, data_size, 0);
        //free(pack);
        if (err < 0)
        {
            ESP_LOGE(TAG, "Error occurred during sending: errno %d", errno);
        }
    }
    //el último mensaje es solo un \0 para avisarle al server que terminamos
    int err = send(sock, "\0", 1, 0);
}
