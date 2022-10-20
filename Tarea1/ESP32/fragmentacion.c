#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "esp_log.h"

#define PACKET_LEN 1000


void fragmentation(unsigned char * paq, int size,int sock){
    ESP_LOGI("Info", "Fragmentando!\n");
    // char rx_buffer[128];

    for (int i = 0; i < size; i += PACKET_LEN){
        ESP_LOGI("Fragmentacion", "Enviando fragmento en posicion %d:\n", i);
        // Generamos el siguiente trozo
        int actualSize = fmin(PACKET_LEN, size - i);
        //char *pack = malloc(size);
        //memcpy(pack, &(payload[i]), size);
        ESP_LOG_BUFFER_HEX("Hexadecimal: ", paq+i, actualSize);

        //Enviamos el trozo
        int err = send(sock, &(paq[i]), actualSize, 0);  //send(sock, data, data_size, 0);
        //free(pack);
        if (err < 0)
        {
            ESP_LOGE("Envio", "Error occurred during sending: errno %d", errno);
        }
    }
    //el último mensaje es solo un \0 para avisarle al server que terminamos
    int err = send(sock, "\0", 1, 0);
    if (err < 0) {
        ESP_LOGE("Final Fragmentacion", "Error occurred during sending: errno %d", errno);
    }
}
