#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MY_PI 3.1415926f

#include <math.h>

// valores para THPC dados en el enunciado
#define MIN_TEMP 5
#define MAX_TEMP 30
#define MIN_HUM 30
#define MAX_HUM 80
#define MIN_PRES 1000
#define MAX_PRES 1200
#define MIN_CO2 30
#define MAX_CO2 200

#define MIN_BATT_LEVEL 1
#define MAX_BATT_LEVEL 100

// valores para ACC KPI del enunciado
#define MIN_AMPX 0.0059f
#define MAX_AMPX 0.12f
#define MIN_AMPY 0.0041f
#define MAX_AMPY 0.11f
#define MIN_AMPZ 0.008f
#define MAX_AMPZ 0.15f
#define MIN_FRECX 29.0f
#define MAX_FRECX 31.0f
#define MIN_FRECY 59.0f
#define MAX_FRECY 61.0f
#define MIN_FRECZ 89.0f
#define MAX_FRECZ 91.0f

/*
Retorna un numero flotante aleatorio en el rango [min, max]
*/
float randFloat(float min, float max)
{
    return min + rand()*(max-min)/RAND_MAX; 
    // hay promoción de rand() desde int a float al multiplicar por (max-min), por lo que no es necesario hacer un cast a float
}

/*
Retorna un numero entero aleatorio en el rango [min, max-1]
*/
int randInt(int min, int max)
{
    return (rand() % (max-min)) + min;
}

int encodeFloat(float* floatPtr, char* arrWrite, int pos)
{
    size_t lenF = sizeof(float);
    char* curr = arrWrite+pos;
    unsigned int* ptr = (unsigned int*) floatPtr;

    for(int j=0; j < lenF; j++)
    {
        unsigned char floatPiece = (unsigned char) (*ptr >> (j*8));
        *(curr+j) = floatPiece;
    }
    return 0;
}

int encodeUInt(unsigned int* uintPtr, char* arrWrite, int pos)
{
    size_t lenI = sizeof(int);
    char* curr = arrWrite+pos;

    for(int j=0; j < lenI; j++)
    {
        unsigned char intPiece = (unsigned char) (*uintPtr >> (j*8));
        *(curr+j) = intPiece;
    }
    return 0;
}

int encodeInt(int* intPtr, char* arrWrite, int pos)
{
    unsigned int* ptr = (unsigned int*) intPtr;
    
    return encodeUInt(ptr, arrWrite, pos);
}

unsigned long encodeULong(unsigned long* uLPtr, char* arrWrite, int pos)
{
    size_t lenUL = sizeof(unsigned long);
    size_t lenI = sizeof(int);
    char* curr = arrWrite+pos;
    unsigned long uLong = *uLPtr;

    for(int j=0; j < lenUL/lenI; j++)
    {
        unsigned int longPiece = uLong >> (j*lenI*8);
        encodeUInt(&longPiece, arrWrite, j*lenI);
    }
    return 0;
}

float decodeFloat(char* arrRead, int pos)
{
    size_t lenF = sizeof(float);
    char* curr = arrRead+pos;
    
    unsigned int ftemp = 0;
    for(int j=0; j < lenF; j++)
    {
        unsigned char charPiece = *(curr+j);
        unsigned int floatPiece = charPiece;
        floatPiece = floatPiece << (j*8);
        ftemp |= floatPiece;
    }

    float* ptr = (float*) &ftemp;
    return *ptr;
}



unsigned int decodeUInt(char* arrRead, int pos)
{
    size_t lenI = sizeof(int);
    char* curr = arrRead+pos;
    
    unsigned int itemp = 0;
    for(int j=0; j < lenI; j++)
    {
        unsigned char charPiece = *(curr+j);
        unsigned int intPiece = charPiece;
        intPiece = intPiece << (j*8);
        itemp |= intPiece;
    }
    return itemp;
}

int decodeInt(char* arrRead, int pos)
{
    unsigned int itemp = decodeUInt(arrRead, pos);
    int* ptr = (int*) &itemp;
    return *ptr;
}

unsigned long decodeULong(char* arrRead, int pos)
{
    size_t lenUL = sizeof(unsigned long);
    size_t lenI = sizeof(unsigned int);
    char* curr = arrRead+pos;

    unsigned long uLong = 0;

    for(int j=0; j < lenUL/lenI; j++)
    {
        unsigned long uLongPiece = decodeUInt(arrRead, j*lenI);
        uLong |= (uLongPiece << (j*lenI*8));
    }
    return uLong;
}

/*
typedef struct {
    float accx;
    float accy;
    float accz;
} Accel;

int accelInit(Accel *pAccel, int n)
{
    pAccel->accx = 2*sinf(2*MY_PI*0.001f*n);
    pAccel->accy = 3*cosf(2*MY_PI*0.001f*n);
    pAccel->accz = 10*sinf(2*MY_PI*0.001f*n);
    return 0;
}

int printAccel(Accel *pAccel)
{
    printf("{Acc_x: %.4f; Acc_y: %.4f; Acc_z: %.4f}\n", pAccel->accx, pAccel->accy, pAccel->accz);
    return 0;
}

typedef struct {
    Accel* data;
} AccelSensor;

int accelSInit(AccelSensor* pAccelS, int size)
{
    int randomN = randInt(0,size * 2);
    pAccelS->data = malloc(size * sizeof(Accel));

    for(int i = 0; i < size; i++ )
    {
        Accel acc ;
        accelInit(&acc, randomN+i);
        printAccel(&acc);
        pAccelS->data[i] = acc;
    }
}
*/

/*
Estructura para representar un arreglo de puntos que representan aceleraciones.
Cada dimensión X,Y,Z están representadas en arreglos de largo size
*/
typedef struct {
    float* datax;
    float* datay;
    float* dataz;
    int size;
} AccelSensor;

int accelDataSet(AccelSensor* pAccelS, int index, float accx, float accy, float accz)
{
    if( index < 0 || index >= pAccelS->size)
    {
        return -1;
    }
    else
    {
        *(pAccelS->datax+index) = accx;
        *(pAccelS->datay+index) = accy;
        *(pAccelS->dataz+index) = accz;
        return 0;
    }
}

int printAccelPoint(AccelSensor* pAccelS, int index)
{
    if( index < 0 || index >= pAccelS->size)
    {
        return -1;
    }
    else
    {
        float* startx = pAccelS->datax;
        float* starty = pAccelS->datay;
        float* startz = pAccelS->dataz;
        printf("{Acc_x: %.4f; Acc_y: %.4f; Acc_z: %.4f}", *(startx+index), *(starty+index), *(startz+index));
        return 0;
    }
}


int accelInit(AccelSensor* pAccelS, int size)
{
    pAccelS->size = size;
    int randomN = randInt(0,size * 2);
    pAccelS->datax = NULL;
    pAccelS->datay = NULL;
    pAccelS->dataz = NULL;

    // falto memoria, fallo malloc, algo malo paso :(
    if( NULL == (pAccelS->datax = malloc(size * sizeof(float))))
    {
        return -1;
    }
    if( NULL == (pAccelS->datay = malloc(size * sizeof(float))))
    {
        return -1;
    }
    if( NULL == (pAccelS->dataz = malloc(size * sizeof(float))))
    {
        return -1;
    }

    for(int i = 0; i < size; i++ )
    {
        int n = randomN+i;
        float accx = 2*sinf(2*MY_PI*0.001f*n);
        float accy = 3*cosf(2*MY_PI*0.001f*n);
        float accz = 10*sinf(2*MY_PI*0.001f*n);
        accelDataSet(pAccelS, i, accx, accy, accz);
    }
    return 0;  
}

int accelDestroy(AccelSensor* pAccelS)
{
    free(pAccelS->datax);
    free(pAccelS->datay);
    free(pAccelS->dataz);
    return 0;
}

int printAccelP(AccelSensor* pAccelS)
{
    printf("[");
    for(int i=0; i < (pAccelS->size-1); i++)
    {

        printAccelPoint(pAccelS, i);
        printf(",\n");
    }
    printAccelPoint(pAccelS, pAccelS->size-1);
    printf("]\n");
}

int encodeAccelS(AccelSensor* pAccelS, unsigned char* arr, int pos)
{
    int writtenBytes = 0;
    float* members[3] = { pAccelS->datax, pAccelS->datay, pAccelS->dataz, };
    
    size_t lenF = sizeof(float);
    char* curr = arr+pos;
    
    for(int j=0; j < 3; j++)
    {
        for(int i=0; i < pAccelS->size; i++)
    {
        encodeFloat(members[j]+i, curr, 0);
        writtenBytes += lenF;
        curr += lenF;
    }
    }
    
    return writtenBytes;
}

int decodeAccelS(AccelSensor* pAccelS, int len, unsigned char* arr, int pos)
{
    int readBytes = 0;
    float** members[3] = { &(pAccelS->datax), &(pAccelS->datay), &(pAccelS->dataz) };

    for(int j=0; j<3; j++)
    {
        // free pointer if it was previously assigned
        // nah, do it yourself, it is much safer as we cannot assume an unitialized variable will be NULL
        /*
        if(*members[j] != NULL)
        {
            free(*(members[j]));
        }
        */
        // create new dynamic pointer
        if( NULL == (*(members[j]) = malloc(len * sizeof(float))))
        {
            return -1;
        }
    }
    pAccelS-> size = len;
    
    size_t lenF = sizeof(float);
    char* curr = arr+pos;
    
    for(int j=0; j < 3; j++)
    {
        for(int i=0; i < pAccelS->size; i++)
        {
            float decoded = decodeFloat(curr, 0);
            *(*(members[j])+i) = decoded;
            readBytes += lenF;
            curr += lenF;
        }
    }
    
    return readBytes;
}

/*
Estructura para almacenar datos de temperatura, humedad, presion y CO2
*/
typedef struct {
    char temp;
    float pres;
    char hum;
    float co2;
} ThpcSensor;

int thpcSInit(ThpcSensor* pThpcS)
{
    pThpcS->temp = (char) randInt(MIN_TEMP, MAX_TEMP+1);
    pThpcS->hum  = (char) randInt(MIN_HUM, MAX_HUM+1);
    pThpcS->pres = randFloat(MIN_PRES, MAX_PRES);
    pThpcS->co2  = randFloat(MIN_CO2, MAX_CO2);
    return 0;

}

int printThpcS(ThpcSensor* pThpcS)
{
    printf("{temp: %d; hum: %d; pres: %.4f; hum: %.4f}", pThpcS->temp, pThpcS->hum, pThpcS->pres, pThpcS->co2);
}

int encodeThpcS(ThpcSensor* pThpcS, unsigned char* arr, int pos)
{
    int writtenBytes = 0;
   
    char* curr = arr+pos;
    
    *curr = (unsigned char) pThpcS->temp;
    curr += sizeof(char);
    writtenBytes += sizeof(char);

    encodeFloat(&(pThpcS->pres), curr, 0);
    curr += sizeof(float);
    writtenBytes += sizeof(float);

    *curr = (unsigned char) pThpcS->hum;
    curr += sizeof(char);
    writtenBytes += sizeof(char);

    encodeFloat(&(pThpcS->co2), curr, 0);
    writtenBytes += sizeof(float);

    return writtenBytes;
}

int decodeThpcS(ThpcSensor* pThpcS, unsigned char* arr, int pos)
{
    int readBytes = 0;
    char* curr = arr+pos;

    pThpcS->temp = (char) *curr;
    curr += sizeof(char);
    readBytes += sizeof(char);

    pThpcS->pres = decodeFloat(curr, 0);
    curr += sizeof(float);
    readBytes += sizeof(float);

    pThpcS->hum = (char) *curr;
    curr += sizeof(char);
    readBytes += sizeof(char);

    pThpcS->co2 = decodeFloat(curr, 0);
    readBytes += sizeof(float);
    
    return readBytes;
}



typedef struct {
    char data1;
    char level;
    int timestamp;
} BattSensor;

int setTimestamp(BattSensor* pBattS)
{
    pBattS->timestamp = time(0);
    return 0;
}


int battSInit(BattSensor* pBattS)
{
    pBattS->level = (char) randInt(MIN_BATT_LEVEL, MAX_BATT_LEVEL+1);
    pBattS->data1 = 1;
    setTimestamp(pBattS);
    return 0;
}

int printBattS(BattSensor* pBattS)
{
    printf("{battery_level: %d; time_stamp: %d; data_1: %d}", 
        pBattS->level, pBattS->timestamp, pBattS->data1);
    return 0;
}

int encodeBattS(BattSensor* pBattS, unsigned char* arr, int pos)
{
    int writtenBytes = 0;
   
    char* curr = arr+pos;

    *curr = (unsigned char) pBattS->data1;
    curr += sizeof(char);
    writtenBytes += sizeof(char);

    *curr = (unsigned char) pBattS->level;
    curr += sizeof(char);
    writtenBytes += sizeof(char);

    encodeInt(&(pBattS->timestamp), curr, 0);
    writtenBytes += sizeof(int);

    return writtenBytes;

}

int decodeBattS(BattSensor* pBattS, unsigned char* arr, int pos)
{
    int readBytes = 0;
    char* curr = arr+pos;

    pBattS->data1 = (char) *curr;
    curr += sizeof(char);
    readBytes += sizeof(char);

    pBattS->level = (char) *curr;
    curr += sizeof(char);
    readBytes += sizeof(char);

    pBattS->timestamp = decodeInt(curr, 0);
    readBytes += sizeof(int);
    
    return readBytes;
}

typedef struct {
    float rms;
    float ampx;
    float frecx;
    float ampy;
    float frecy;
    float ampz;
    float frecz;
} AccelKpi;

int accelKInit(AccelKpi* pAccelK)
{
    float ampx = randFloat(MIN_AMPX, MAX_AMPX);
    float ampy = randFloat(MIN_AMPY, MAX_AMPY);
    float ampz = randFloat(MIN_AMPZ, MAX_AMPZ);

    pAccelK->ampx = ampx;
    pAccelK->frecx = randFloat(MIN_FRECX, MAX_FRECX);
    pAccelK->ampy = ampy;
    pAccelK->frecy = randFloat(MIN_FRECY, MAX_FRECY);
    pAccelK->ampz = ampz;
    pAccelK->frecz = randFloat(MIN_FRECZ, MAX_FRECZ);
    pAccelK->rms = sqrtf(ampx*ampx + ampy*ampy + ampz * ampz);

    return 0;

}

int printAccelK(AccelKpi* pAccelK)
{
    printf("{amp_x: %.4f; frec_x: %.4f; amp_y: %.4f; frec_y: %.4f; amp_z: %.4f; frec_z: %.4f; rms: %.4f}", 
        pAccelK->ampx, pAccelK->frecx, pAccelK->ampy, pAccelK->frecy, pAccelK->ampz, pAccelK->frecz, pAccelK->rms);
    return 0;
}



int encodeAccelK(AccelKpi* pAccelK, unsigned char* arr, int pos)
{
    int writtenBytes = 0;
    size_t lenK = 7;
    float* members[7] = { &(pAccelK->rms), &(pAccelK->ampx), &(pAccelK->frecx), &(pAccelK->ampy), &(pAccelK->frecy), &(pAccelK->ampz), &(pAccelK->frecz) };
    
    size_t lenF = sizeof(float);
    char* curr = arr+pos;
    
    for(int i=0; i < lenK; i++)
    {
        encodeFloat(members[i], curr, lenF*i);
        writtenBytes += lenF;
    }
    return writtenBytes;

}

int decodeAccelK(AccelKpi* pAccelK, unsigned char* arr, int pos)
{
    int readBytes = 0;
    size_t lenK = 7;
    float* members[7] = { &(pAccelK->rms), &(pAccelK->ampx), &(pAccelK->frecx), &(pAccelK->ampy), &(pAccelK->frecy), &(pAccelK->ampz), &(pAccelK->frecz) };
    
    size_t lenF = sizeof(float);
    char* curr = arr+pos;
    
    for(int i=0; i < lenK; i++)
    {
        *(members[i]) = decodeFloat(curr, i*lenF);
        readBytes += lenF;
    }
    return readBytes;
}

// descomentar para probar estructuras
/*
int main()
{

    // pruebita

    AccelSensor a;
    accelInit(&a, 5);
    printAccelP(&a);
    printAccelPoint(&a, 3);

    printf("\n");
    ThpcSensor b;
    thpcSInit(&b);
    printThpcS(&b);

    printf("\n");
    BattSensor c;
    battSInit(&c);
    printBattS(&c);

    printf("\n");
    AccelKpi d;
    accelKInit(&d);
    printAccelK(&d);
    printf("\n");

    return 0;
}
*/
