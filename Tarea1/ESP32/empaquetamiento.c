#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "sensores.c"

#define HEADER_LEN 12
#define PROTOCOL0_MSG_LEN 6
#define PROTOCOL1_MSG_LEN 16
#define PROTOCOL2_MSG_LEN 20
#define PROTOCOL3_MSG_LEN 44
#define PROTOCOL4_LEN_WITHOUT_ACC 16

#define ACC_ARRAY_LEN 20

typedef struct {
    unsigned int id;
    unsigned long mac;
    unsigned char tlayer;
    unsigned char protocol;
    unsigned int lenmsg;
} Header;

unsigned long encodeIdMac(Header* pHeader)
{
    unsigned long long idMask = pHeader->id;
    unsigned long encoded = pHeader->mac;
    unsigned long long mask = ~(0xffffULL << 48); // para borrar los últimos 2 bytes
    encoded = (encoded & mask) | (idMask << 48);
    return encoded;
}

int decodeIdMac(unsigned long long idmac, Header* pEditedHeader)
{
    unsigned int id = (int) (idmac >> 48);
    unsigned long long mask = ~(0xffffULL << 48); // para borrar los últimos 2 bytes
    unsigned long mac = idmac & mask;

    pEditedHeader->id = id;
    pEditedHeader->mac = mac;

    return 0;
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
               unsigned long mac,
               unsigned char tlayer,
               unsigned char protocol,
               unsigned int lenmsg)
{
    pHeader->id = id;
    pHeader->mac = mac;
    pHeader->tlayer = tlayer;
    pHeader->protocol = protocol;
    pHeader->lenmsg = lenmsg;

    return 0;
}

int printHeader(Header* pHeader)
{
    printf("{id: %u; mac: %lu; t_layer: %u; protocol: %u; len_msg: %u}", pHeader->id, pHeader->mac, pHeader->tlayer, pHeader->protocol, pHeader-> lenmsg);

    return 0;
}



int encodeHeader(Header* pHeader, unsigned char* arr, int pos)
{
    int writtenBytes = 0;
    unsigned char* curr = arr+pos;

    unsigned long idmac = encodeIdMac(pHeader);
    encodeULong(&idmac, curr, 0);
    writtenBytes += sizeof(unsigned long);
    curr += sizeof(unsigned long);

    unsigned int tpl = encodeTPL(pHeader);
    encodeUInt(&tpl, curr, 0);
    writtenBytes += sizeof(unsigned int);

    return writtenBytes;
}

int decodeHeader(Header* pHeader, unsigned char* arr, int pos)
{
    int readBytes = 0;
    unsigned char* curr = arr+pos;

    unsigned long idmac = decodeULong(curr, 0);
    decodeIdMac(idmac, pHeader);
    readBytes += sizeof(unsigned long);
    curr += sizeof(unsigned long);

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
                 unsigned long mac,
                 unsigned char tlayer)
{
    Header h = {.id = id, .mac = mac, .tlayer = tlayer, .protocol=0, .lenmsg=PROTOCOL0_MSG_LEN };
    pro->header = h;
    battSInit(&(pro->battery));

    return 0;
}

int printProtocol0(Protocol0* pro)
{
    printf("PROTOCOL 0\n    HEADER=");
    printHeader(&(pro->header));
    printf("\n    MSG=[");
    printBattS(&(pro->battery));
    printf("]\n");
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
                 unsigned long mac,
                 unsigned char tlayer)
{
    Header h = {.id = id, .mac = mac, .tlayer = tlayer, .protocol=1, .lenmsg=PROTOCOL1_MSG_LEN };
    pro->header = h;
    battSInit(&(pro->battery));
    thpcSInit(&(pro->thpc));

    return 0;
}

int printProtocol1(Protocol1* pro)
{
    printf("PROTOCOL 1\n    HEADER=");
    printHeader(&(pro->header));
    printf("\n    MSG=[");
    printBattS(&(pro->battery));
    printf(",\n\t");
    printThpcS(&(pro->thpc));
    printf("]\n");
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
                 unsigned long mac,
                 unsigned char tlayer,
                 unsigned char protocol,
                 unsigned int lenmsg)
{
    Header h = {.id = id, .mac = mac, .tlayer = tlayer, .protocol=protocol, .lenmsg=lenmsg };
    pro->header = h;
    battSInit(&(pro->battery));
    thpcSInit(&(pro->thpc));
    accelKInit(&(pro->kpi));

    return 0;
}

int protocol2Init(Protocol23* pro, 
                 unsigned int id,
                 unsigned long mac,
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
                 unsigned long mac,
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
    printf("PROTOCOL %d\n    HEADER=", (pro->header).protocol);
    printHeader(&(pro->header));
    printf("\n    MSG=[");
    printBattS(&(pro->battery));
    printf(",\n\t");
    printThpcS(&(pro->thpc));
    printf(",\n\t");

    if((pro->header).protocol == 2)
    {
        printf("{rms: %.4f}", (pro->kpi).rms);
    }
    else
    {
        printAccelK(&(pro->kpi));
    }

    printf("]\n");
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
                 unsigned long mac,
                 unsigned char tlayer)
{
    Header h = {.id = id, .mac = mac, .tlayer = tlayer, .protocol=4, .lenmsg=PROTOCOL4_LEN_WITHOUT_ACC + ACC_ARRAY_LEN };
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
    printf("PROTOCOL 4\n    HEADER=");
    printHeader(&(pro->header));
    printf("\n    MSG=[");
    printBattS(&(pro->battery));
    printf(",\n\t");
    printThpcS(&(pro->thpc));
    printf(",\n\t");
    printAccelP(&(pro->acc));
    printf("]\n");
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
    /*
    printf("Printing %d bytes as hex\n", n);
    for(int i=0; i<n; i++)
    {
        printf("%x ", test[i]);
    }
    printf("\n");
    */

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
    printAccelP(&atest);

    protocol4Destroy(&p4);
    
    Header h3;
    encodeHeader(&h, test, 0);
    printf("\nTest header\n");
    decodeHeader(&h3, test, 0);
    printHeader(&h3);

    return 0;
}
