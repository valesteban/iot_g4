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

int fragmentationUDP(
    unsigned char * paq, 
    int size,int sock, 
    struct sockaddr* dest_addr_ptr, 
    size_t dest_addr_size,
    struct sockaddr* source_addr_ptr,
    socklen_t* socklen_ptr)
{
    ESP_LOGI("Info", "Fragmentando!\n");
    char rx_buffer[128];

    for (int i = 0; i < size; i += PACKET_LEN){
        ESP_LOGI("Fragmentacion", "Enviando fragmento en posicion %d:\n", i);
        // Generamos el siguiente trozo
        int actualSize = fmin(PACKET_LEN, size - i);
        //char *pack = malloc(size);
        //memcpy(pack, &(payload[i]), size);
        ESP_LOG_BUFFER_HEX("Hexadecimal: ", paq+i, actualSize);

        //Enviamos el trozo
        int err = sendto(sock, paq+i, actualSize, 0, dest_addr_ptr, dest_addr_size);
        if (err < 0) {
            ESP_LOGE("Envio UDP:", "Error occurred during sending: errno %d", errno);
            break;
        }
        ESP_LOGI("Envio UDP:", "Fragmento enviado");
        ESP_LOGI("ACK UDP:", "Confirmando recibo...");

        int len = recvfrom(sock, rx_buffer, sizeof(rx_buffer) - 1, 0, source_addr_ptr, socklen_ptr);
        if (len < 0) {
            ESP_LOGE("ACK UDP", "recvfrom failed: errno %d", errno);
            break;
        }
        else
        {
            rx_buffer[len] = 0;
            char ack = rx_buffer[0];
            if (!ack)
            {
                ESP_LOGE("ACK UDP", "Server side failure while processing fragment at %d", i);
                return -1;
            }
            else
            {
                ESP_LOGI("ACK UDP", "Server received fragment successfully!");
            }
        }
        
    }
    //el último mensaje es solo un \0 para avisarle al server que terminamos
    int err = send(sock, "\0", 1, 0);
    if (err < 0) {
        ESP_LOGE("Final Fragmentacion", "Error occurred during sending: errno %d", errno);
    }
    return 0;
}