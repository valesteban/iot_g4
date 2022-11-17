#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "esp_log.h"

#include "sensores.c"

#define HEADER_LEN 12
#define PROTOCOL0_MSG_LEN 6
#define PROTOCOL1_MSG_LEN 16
#define PROTOCOL2_MSG_LEN 20
#define PROTOCOL3_MSG_LEN 44
#define PROTOCOL4_LEN_WITHOUT_ACC 16

#define ACC_ARRAY_LEN 2000
#define PROTOCOL4_MAX_POINT_PRINTS 200

static const char *PKGTAG = "Paquete";

/*
typedef struct {
    unsigned int id;
    unsigned long long mac;
    unsigned char tlayer;
    unsigned char protocol;
    unsigned int lenmsg;
} Header;
*/

typedef struct {
    unsigned int id;
    unsigned char mac[6];
    unsigned char tlayer;
    unsigned char protocol;
    unsigned int lenmsg;
} Header;

/*
unsigned long long encodeIdMac(Header* pHeader)
{
    unsigned long long idMask = pHeader->id;
    unsigned long long encoded = pHeader->mac;
    unsigned long long mask = ~(0xffffULL << 48); // para borrar los últimos 2 bytes
    encoded = (encoded & mask) | (idMask << 48);
    return encoded;unsigned long long
}
*/

int encodeIdMac(Header* pHeader, unsigned char* arr, int pos)
{
    unsigned char* curr = arr+pos;
    for(int i=0; i < 6; i++)
    {
        *(curr+i) = pHeader->mac[i];
    }
    *(curr+6) = pHeader->id;
    *(curr+7) = ((pHeader->id) >> 8);
    return 8;
}

/*
int decodeIdMac(unsigned long long idmac, Header* pEditedHeader)
{
    unsigned int id = (int) (idmac >> 48);
    unsigned long long mask = ~(0xffffULL << 48); // para borrar los últimos 2 bytes
    unsigned long long mac = idmac & mask;

    pEditedHeader->id = id;
    pEditedHeader->mac = mac;

    return 0;
}
*/

int decodeIdMac(unsigned char idmac[8], Header* pEditedHeader)
{
    for(int i=0; i < 6; i++)
    {
        pEditedHeader->mac[i] = idmac[i];
    }

    unsigned int id = (unsigned int) idmac[6];
    id |= ((unsigned int) idmac[7]) << 8;

    pEditedHeader->id = id;

    return 8;
}

unsigned int encodeTPL(Header* pHeader)
{
    unsigned int tlayer = pHeader->tlayer;
    unsigned int protocol = pHeader->protocol;
    unsigned int mask = 0x0000ffffu;
    unsigned int encoded = (pHeader->lenmsg)&mask;
    encoded = encoded | (tlayer << 24) | (protocol << 16);
    return encoded;
}

unsigned int decodeTPL(unsigned int tpl, Header* pEditedHeader)
{
    unsigned char tlayer = tpl >> 24;
    unsigned char protocol = tpl >> 16;
    protocol = protocol & (0x000000ffu);
    unsigned int lenmsg = tpl & 0x0000ffffu;

    pEditedHeader->tlayer = tlayer;
    pEditedHeader->protocol = protocol;
    pEditedHeader->lenmsg = lenmsg;
    return 0;
}

int headerInit(Header* pHeader, 
               unsigned int id,
               unsigned char* mac,
               unsigned char tlayer,
               unsigned char protocol,
               unsigned int lenmsg)
{
    pHeader->id = id;
    for(int i=0; i < 6; i++)
    {
        pHeader->mac[i] = mac[i];
    }
    
    pHeader->tlayer = tlayer;
    pHeader->protocol = protocol;
    pHeader->lenmsg = lenmsg;

    return 0;
}

int printHeader(Header* pHeader)
{
    char mac_str[18];
    for(int i=0; i<5; i++)
    {
        snprintf(&(mac_str[i*3]), 4, "%02x:", pHeader->mac[i]);
    }
    snprintf(&(mac_str[15]), 3,"%02x", pHeader->mac[5]);

    ESP_LOGI(PKGTAG, "{id: %u; mac: %s; t_layer: %u; protocol: %u; len_msg: %u}", pHeader->id, mac_str, pHeader->tlayer, pHeader->protocol, pHeader-> lenmsg);

    return 0;
}



int encodeHeader(Header* pHeader, unsigned char* arr, int pos)
{
    int writtenBytes = 0;
    unsigned char* curr = arr+pos;

    writtenBytes += encodeIdMac(pHeader, curr, 0);
    curr += writtenBytes;

    unsigned int tpl = encodeTPL(pHeader);
    encodeUInt(&tpl, curr, 0);
    writtenBytes += sizeof(unsigned int);

    return writtenBytes;
}

int decodeHeader(Header* pHeader, unsigned char* arr, int pos)
{
    int readBytes = 0;
    unsigned char* curr = arr+pos;

    readBytes += decodeIdMac(curr, pHeader);
    curr += readBytes;

    unsigned int tpl = decodeUInt(curr, 0);
    decodeTPL(tpl, pHeader);
    readBytes += sizeof(unsigned int);

    return readBytes;
}

typedef struct {
    Header header;
    BattSensor battery;
} Protocol0;

int protocol0Init(Protocol0* pro, 
                 unsigned int id,
                 unsigned char* mac,
                 unsigned char tlayer)
{
    Header h;
    headerInit(&h, id, mac, tlayer, 0, PROTOCOL0_MSG_LEN);
    pro->header = h;
    battSInit(&(pro->battery));

    return 0;
}

int printProtocol0(Protocol0* pro)
{
    ESP_LOGI(PKGTAG, "PROTOCOL 0\n    HEADER=");
    printHeader(&(pro->header));
    ESP_LOGI(PKGTAG, "\n    MSG=[");
    printBattS(&(pro->battery));
    ESP_LOGI(PKGTAG, "]\n");
    return 0;
}

int encodeProtocol0(Protocol0* pro, unsigned char* arr, int pos)
{
    int writtenBytes = 0;
    int totalBytes = 0;
    unsigned char* curr = arr + pos;

    writtenBytes = encodeHeader(&(pro->header), curr, 0);
    totalBytes += writtenBytes;
    curr += writtenBytes;

    totalBytes += encodeBattS(&(pro->battery), curr, 0);
    
    return totalBytes;
}

int decodeProtocol0(Protocol0* pro, unsigned char* arr, int pos)
{
    int readBytes = 0;
    int totalBytes = 0;
    unsigned char* curr = arr + pos;

    readBytes = decodeHeader(&(pro->header), curr, 0);
    totalBytes += readBytes;
    curr += readBytes;

    totalBytes += decodeBattS(&(pro->battery), curr, 0);
    return totalBytes;
}

typedef struct {
    Header header;
    BattSensor battery;
    ThpcSensor thpc;
} Protocol1;

int protocol1Init(Protocol1* pro, 
                 unsigned int id,
                 unsigned char* mac,
                 unsigned char tlayer)
{
    Header h;
    headerInit(&h, id, mac, tlayer, 1, PROTOCOL1_MSG_LEN);
    pro->header = h;
    battSInit(&(pro->battery));
    thpcSInit(&(pro->thpc));

    return 0;
}

int printProtocol1(Protocol1* pro)
{
    ESP_LOGI(PKGTAG, "PROTOCOL 1\n    HEADER=");
    printHeader(&(pro->header));
    ESP_LOGI(PKGTAG, "\n    MSG=[");
    printBattS(&(pro->battery));
    ESP_LOGI(PKGTAG, ",\n\t");
    printThpcS(&(pro->thpc));
    ESP_LOGI(PKGTAG, "]\n");
    return 0;
}


int encodeProtocol1(Protocol1* pro, unsigned char* arr, int pos)
{
    int writtenBytes = 0;
    int totalBytes = 0;
    unsigned char* curr = arr + pos;

    writtenBytes = encodeHeader(&(pro->header), curr, 0);
    totalBytes += writtenBytes;
    curr += writtenBytes;

    writtenBytes = encodeBattS(&(pro->battery), curr, 0);
    totalBytes += writtenBytes;
    curr += writtenBytes;

    totalBytes += encodeThpcS(&(pro->thpc), curr, 0);
    return totalBytes;
}

int decodeProtocol1(Protocol1* pro, unsigned char* arr, int pos)
{
    int readBytes = 0;
    int totalBytes = 0;
    unsigned char* curr = arr + pos;

    readBytes = decodeHeader(&(pro->header), curr, 0);
    totalBytes += readBytes;
    curr += readBytes;

    readBytes = decodeBattS(&(pro->battery), curr, 0);
    totalBytes += readBytes;
    curr += readBytes;

    totalBytes += decodeThpcS(&(pro->thpc), curr, 0);
    return totalBytes;
}

typedef struct {
    Header header;
    BattSensor battery;
    ThpcSensor thpc;
    AccelKpi kpi;
} Protocol23;

int protocol23Init(Protocol23* pro, 
                 unsigned int id,
                 unsigned char* mac,
                 unsigned char tlayer,
                 unsigned char protocol,
                 unsigned int lenmsg)
{
    Header h;
    headerInit(&h, id, mac, tlayer, protocol, lenmsg);
    pro->header = h;
    battSInit(&(pro->battery));
    thpcSInit(&(pro->thpc));
    accelKInit(&(pro->kpi));

    return 0;
}

int protocol2Init(Protocol23* pro, 
                 unsigned int id,
                 unsigned char* mac,
                 unsigned char tlayer)
{
    return protocol23Init(pro,
                   id,
                   mac,
                   tlayer,
                   2,
                   PROTOCOL2_MSG_LEN);
}

int protocol3Init(Protocol23* pro, 
                 unsigned int id,
                 unsigned char* mac,
                 unsigned char tlayer)
{
    return protocol23Init(pro,
                   id,
                   mac,
                   tlayer,
                   3,
                   PROTOCOL3_MSG_LEN);
}

int printProtocol23(Protocol23* pro)
{
    ESP_LOGI(PKGTAG, "PROTOCOL %d\n    HEADER=", (pro->header).protocol);
    printHeader(&(pro->header));
    ESP_LOGI(PKGTAG, "\n    MSG=[");
    printBattS(&(pro->battery));
    ESP_LOGI(PKGTAG, ",\n\t");
    printThpcS(&(pro->thpc));
    ESP_LOGI(PKGTAG, ",\n\t");

    if((pro->header).protocol == 2)
    {
        ESP_LOGI(PKGTAG, "{rms: %.4f}", (pro->kpi).rms);
    }
    else
    {
        printAccelK(&(pro->kpi));
    }

    ESP_LOGI(PKGTAG, "]\n");
    return 0;
}

int encodeProtocol2(Protocol23* pro, unsigned char* arr, int pos)
{
    int writtenBytes = 0;
    int totalBytes = 0;
    unsigned char* curr = arr + pos;

    writtenBytes = encodeHeader(&(pro->header), curr, 0);
    totalBytes += writtenBytes;
    curr += writtenBytes;

    writtenBytes = encodeBattS(&(pro->battery), curr, 0);
    totalBytes += writtenBytes;
    curr += writtenBytes;

    writtenBytes = encodeThpcS(&(pro->thpc), curr, 0);
    totalBytes += writtenBytes;
    curr += writtenBytes;

    // just write RMS
    encodeFloat(&(pro->kpi.rms), curr, 0);

    return totalBytes + sizeof(float);
}

int decodeProtocol2(Protocol23* pro, unsigned char* arr, int pos)
{
    int readBytes = 0;
    int totalBytes = 0;
    unsigned char* curr = arr + pos;

    readBytes = decodeHeader(&(pro->header), curr, 0);
    totalBytes += readBytes;
    curr += readBytes;

    readBytes = decodeBattS(&(pro->battery), curr, 0);
    totalBytes += readBytes;
    curr += readBytes;

    readBytes = decodeThpcS(&(pro->thpc), curr, 0);
    totalBytes += readBytes;
    curr += readBytes;

    // just write RMS
    pro->kpi.rms = decodeFloat(curr, 0);

    return totalBytes + sizeof(float);
}

int encodeProtocol3(Protocol23* pro, unsigned char* arr, int pos)
{
    int writtenBytes = 0;
    int totalBytes = 0;
    unsigned char* curr = arr + pos;

    writtenBytes = encodeHeader(&(pro->header), curr, 0);
    totalBytes += writtenBytes;
    curr += writtenBytes;

    writtenBytes = encodeBattS(&(pro->battery), curr, 0);
    totalBytes += writtenBytes;
    curr += writtenBytes;

    writtenBytes = encodeThpcS(&(pro->thpc), curr, 0);
    totalBytes += writtenBytes;
    curr += writtenBytes;

    totalBytes += encodeAccelK(&(pro->kpi), curr, 0);
    return totalBytes;
}

int decodeProtocol3(Protocol23* pro, unsigned char* arr, int pos)
{
    int readBytes = 0;
    int totalBytes = 0;
    unsigned char* curr = arr + pos;

    readBytes = decodeHeader(&(pro->header), curr, 0);
    totalBytes += readBytes;
    curr += readBytes;

    readBytes = decodeBattS(&(pro->battery), curr, 0);
    totalBytes += readBytes;
    curr += readBytes;

    readBytes = decodeThpcS(&(pro->thpc), curr, 0);
    totalBytes += readBytes;
    curr += readBytes;

    totalBytes += decodeAccelK(&(pro->kpi), curr, 0);
    return totalBytes;
}

typedef struct {
    Header header;
    BattSensor battery;
    ThpcSensor thpc;
    AccelSensor acc;
} Protocol4;

int protocol4Init(Protocol4* pro, 
                 unsigned int id,
                 unsigned char* mac,
                 unsigned char tlayer)
{
    Header h;
    headerInit(&h, id, mac, tlayer, 4, PROTOCOL4_LEN_WITHOUT_ACC + ACC_ARRAY_LEN  * sizeof(float) * 3 );
    pro->header = h;
    battSInit(&(pro->battery));
    thpcSInit(&(pro->thpc));
    accelInit(&(pro->acc), ACC_ARRAY_LEN);

    return 0;
}

int protocol4Destroy(Protocol4* pro)
{
    accelDestroy(&(pro->acc));
    return 0;
}

int printProtocol4(Protocol4* pro)
{
    ESP_LOGI(PKGTAG, "PROTOCOL 4\n    HEADER=");
    printHeader(&(pro->header));
    ESP_LOGI(PKGTAG, "\n    MSG=[");
    printBattS(&(pro->battery));
    ESP_LOGI(PKGTAG, ",\n\t");
    printThpcS(&(pro->thpc));
    ESP_LOGI(PKGTAG, ",\n\t");
    printAccelP(&(pro->acc), PROTOCOL4_MAX_POINT_PRINTS);
    ESP_LOGI(PKGTAG, "]\n");
    return 0;
}

int encodeProtocol4(Protocol4* pro, unsigned char* arr, int pos)
{
    int writtenBytes = 0;
    int totalBytes = 0;
    unsigned char* curr = arr + pos;

    writtenBytes = encodeHeader(&(pro->header), curr, 0);
    totalBytes += writtenBytes;
    curr += writtenBytes;

    writtenBytes = encodeBattS(&(pro->battery), curr, 0);
    totalBytes += writtenBytes;
    curr += writtenBytes;

    writtenBytes = encodeThpcS(&(pro->thpc), curr, 0);
    totalBytes += writtenBytes;
    curr += writtenBytes;

    totalBytes += encodeAccelS(&(pro->acc), curr, 0);
    return totalBytes;
}
    
int decodeProtocol4(Protocol4* pro, unsigned char* arr, int pos)
{
    int readBytes = 0;
    int totalBytes = 0;
    unsigned char* curr = arr + pos;

    readBytes = decodeHeader(&(pro->header), curr, 0);
    totalBytes += readBytes;
    curr += readBytes;

    readBytes = decodeBattS(&(pro->battery), curr, 0);
    totalBytes += readBytes;
    curr += readBytes;

    readBytes = decodeThpcS(&(pro->thpc), curr, 0);
    totalBytes += readBytes;
    curr += readBytes;

    totalBytes += decodeAccelS(&(pro->acc), pro->header.lenmsg -PROTOCOL4_LEN_WITHOUT_ACC,curr, 0);
    return totalBytes;
}

int encode_pkg(
    char id_protocol, 
    unsigned char* mac, 
    unsigned int device_id, 
    unsigned char tlayer, 
    unsigned char** dataPtr, 
    int* dataSizePtr)
{
    Protocol0 pro0;
    Protocol1 pro1;
    Protocol23 pro2;
    Protocol23 pro3;
    Protocol4 pro4;

    const char *anotherTag = "empaquetamiento";
    
    switch(id_protocol) {
        case '0' :
            ESP_LOGI(anotherTag, "Enviando paquete de Protocolo 0"); 
            protocol0Init(&pro0, device_id, mac, tlayer);
            *dataSizePtr = (HEADER_LEN + pro0.header.lenmsg)*sizeof(char);
            *dataPtr = malloc(*dataSizePtr);
            printProtocol0(&pro0);
            encodeProtocol0(&pro0, *dataPtr, 0);
            break;
        case '1' :
            ESP_LOGI(anotherTag, "Enviando paquete de Protocolo 1"); 
            protocol1Init(&pro1, device_id, mac, tlayer);
            *dataSizePtr = (HEADER_LEN + pro1.header.lenmsg)*sizeof(char);
            *dataPtr = malloc(*dataSizePtr);
            printProtocol1(&pro1);
            encodeProtocol1(&pro1, *dataPtr, 0);
            break;
        case '2' :
            ESP_LOGI(anotherTag, "Enviando paquete de Protocolo 2"); 
            protocol2Init(&pro2, device_id, mac, tlayer);
            *dataSizePtr= (HEADER_LEN + pro2.header.lenmsg)*sizeof(char);
            *dataPtr = malloc(*dataSizePtr);
            printProtocol23(&pro2);
            encodeProtocol2(&pro2, *dataPtr, 0);
            break;
        case '3' :
            ESP_LOGI(anotherTag, "Enviando paquete de Protocolo 3"); 
            protocol3Init(&pro3, device_id, mac, tlayer);
            *dataSizePtr = (HEADER_LEN + pro3.header.lenmsg)*sizeof(char);
            *dataPtr = malloc(*dataSizePtr);
            printProtocol23(&pro3);
            encodeProtocol3(&pro3, *dataPtr, 0);
            break;
        case '4' :
            ESP_LOGE(anotherTag, "Enviando paquete de Protocolo 4"); 
            protocol4Init(&pro4, device_id, mac, tlayer);
            *dataSizePtr = (HEADER_LEN + pro4.header.lenmsg)*sizeof(char);
            *dataPtr = malloc(*dataSizePtr);
            printProtocol4(&pro4);
            encodeProtocol4(&pro4, *dataPtr, 0);
            protocol4Destroy(&pro4);
            break;
        default:
            ESP_LOGE(anotherTag, "ermanito, eso no es un protocolo....\n");  
            return 1;
    }
    return 0;
}

/*
int main()
{

    time_t t0 = time(0);
    unsigned char test[ACC_ARRAY_LEN*4*sizeof(float)];

    Header h = { .id = 8, .mac = 404, .tlayer = 1, .protocol = 4, .lenmsg = 14 };
    Header h2;
    printHeader(&h);
    printf("\n");
    printHeader(&h2);
    printf("\nholi\n");
    unsigned long idmac = encodeIdMac(&h);
    unsigned int tpl = encodeTPL(&h);

    printf("encoded: %lu\n", idmac);
    printf("encoded: %u\n", tpl);

    decodeIdMac(idmac, &h2);
    printHeader(&h2);
    
    printf("\n");
    decodeTPL(tpl, &h2);
    printHeader(&h2);

    //time_t t1 = time(0);
    printf("\n Time 0: %d, not truncated: %lld \n", (int) t0, t0);


    Protocol0 p0;
    protocol0Init(&p0, 8, 404, 1);
    printProtocol0(&p0);

    Protocol0 p0a;
    int n = encodeProtocol0(&p0, test, 0);
    
    printf("Printing %d bytes as hex\n", n);
    for(int i=0; i<n; i++)
    {
        printf("%x ", test[i]);
    }
    printf("\n");
    

    decodeProtocol0(&p0a, test, 0);
    printProtocol0(&p0a);

    Protocol1 p1;
    protocol1Init(&p1, 8, 404, 1);
    printProtocol1(&p1);

    Protocol1 p1a;
    n = encodeProtocol1(&p1, test, 0);

    printf("Printing %d bytes as hex\n", n);
    for(int i=0; i<n; i++)
    {
        printf("%x ", test[i]);
    }
    printf("\n");

    decodeProtocol1(&p1a, test, 0);
    printProtocol1(&p1a);

    Protocol23 p2;
    protocol2Init(&p2, 8, 404, 1);
    printProtocol23(&p2);

    Protocol23 p2a;
    encodeProtocol2(&p2, test, 0);
    n = decodeProtocol2(&p2a, test, 0);

    printf("Printing %d bytes as hex\n", n);
    for(int i=0; i<n; i++)
    {
        printf("%x ", test[i]);
    }
    printf("\n");

    printProtocol23(&p2a);

    Protocol23 p3;
    protocol3Init(&p3, 8, 404, 1);
    printProtocol23(&p3);

    Protocol23 p3a;
    n = encodeProtocol3(&p3, test, 0);

    printf("Printing %d bytes as hex\n", n);
    for(int i=0; i<n; i++)
    {
        printf("%x ", test[i]);
    }
    printf("\n");

    decodeProtocol3(&p3a, test, 0);
    printProtocol23(&p3a);

    
    encodeAccelK(&(p3.kpi), test, 0);
    printf("Encoded accelK: %s\nTEST DECODE: ", test);

    AccelKpi ktest;
    decodeAccelK(&ktest, test, 0);
    printAccelK(&ktest);


    encodeBattS(&(p3.battery), test, 0);
    printf("\nEncoded battery: %s\nTEST DECODE: ", test);

    BattSensor btest;
    int readB = decodeBattS(&btest, test, 0);
    printf("read Bytes: %d\n", readB);
    printBattS(&btest);

    encodeThpcS(&(p3.thpc), test, 0);
    printf("\nEncoded thpc: %s\nTEST DECODE: ", test);

    ThpcSensor ttest;
    int readT = decodeThpcS(&ttest, test, 0);
    printf("read Bytes: %d\n", readT);
    printThpcS(&ttest);

    Protocol4 p4;
    protocol4Init(&p4, 8, 404, 1);
    printProtocol4(&p4);

    Protocol4 p4a;
    n=encodeProtocol4(&p4, test, 0);

    printf("Printing %d bytes as hex\n", n);
    for(int i=0; i<n; i++)
    {
        printf("%x ", test[i]);
    }
    printf("\n");

    decodeProtocol4(&p4a, test, 0);
    printProtocol4(&p4a);

    printf("seg\n");

    encodeAccelS(&(p4.acc), test, 0);
    printf("\nEncoded thpc: %s\nTEST DECODE: ", test);

    AccelSensor atest;
    int readA = decodeAccelS(&atest, ACC_ARRAY_LEN,test, 0);
    printf("read Bytes: %d\n", readA);
    printAccelP(&atest,0);

    protocol4Destroy(&p4);
    
    Header h3;
    encodeHeader(&h, test, 0);
    printf("\nTest header\n");
    decodeHeader(&h3, test, 0);
    printHeader(&h3);

    return 0;
}
*/
